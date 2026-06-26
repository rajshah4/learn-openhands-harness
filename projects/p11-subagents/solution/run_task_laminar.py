"""P11 solution: native OpenHands task-tool subagents with Laminar tracing.

This runner complements run_compare.py. It keeps Scenario A, but switches
the subagent run from manual child conversations to the SDK's native task tool.

Run:
    P11_NATIVE_MODEL=small uv run --with openhands-sdk --with openhands-tools \
      python projects/p11-subagents/solution/run_task_laminar.py

Env:
    LMNR_PROJECT_API_KEY  optional, read from nearest .env, enables Laminar
    LLM_API_KEY           required, read from nearest .env
    LLM_MODEL             default parent and child model
    LLM_MODEL_SMALL       used when P11_NATIVE_MODEL=small
    P11_NATIVE_MODEL      optional model override, or "small"
    P11_ONLY_DIMS         optional CSV subset, for example "docs,secrets"
    P11_NATIVE_SINGLE_ONLY=1    run only the local single-agent baseline
    P11_NATIVE_TASK_ONLY=1      run only the native task-tool config
    P11_NATIVE_SHOW_FINAL=1     print final reports
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import time
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT.parent))  # projects/ for _runtime
sys.path.insert(0, str(PROJECT))         # for subagent_bench

from _runtime import load_dotenv, token_counts  # noqa: E402

load_dotenv(PROJECT)
os.environ.setdefault("OPENHANDS_SUPPRESS_BANNER", "1")

from pydantic import SecretStr  # noqa: E402

from openhands.sdk import Agent, AgentContext, Conversation, LLM, Tool  # noqa: E402
from openhands.sdk.context import Skill  # noqa: E402
from openhands.sdk.conversation.response_utils import (  # noqa: E402
    get_agent_final_response,
)
from openhands.sdk.subagent import register_agent_if_absent  # noqa: E402
from openhands.tools.preset.default import get_default_tools  # noqa: E402
from openhands.tools.task import TaskToolSet  # noqa: E402

import subagent_bench as bench  # noqa: E402


_IGNORE = shutil.ignore_patterns(".git", "__pycache__", ".DS_Store")
P11_AGENT_TYPE = "p11-code-explorer"


def _register_p11_agent_type() -> str:
    get_default_tools(enable_browser=False)

    def create_p11_code_explorer(llm: LLM) -> Agent:
        skill = Skill(
            name="p11_code_explorer",
            content=(
                "You are a read-only code audit agent. Use terminal commands to "
                "inspect files. Do not create, edit, delete, move, install, or "
                "write files. Return concrete findings with file and line "
                "evidence."
            ),
            trigger=None,
        )
        return Agent(
            llm=llm,
            tools=[Tool(name="terminal", params={"terminal_type": "subprocess"})],
            agent_context=AgentContext(skills=[skill]),
        )

    register_agent_if_absent(
        name=P11_AGENT_TYPE,
        factory_func=create_p11_code_explorer,
        description=(
            "Read-only P11 code audit subagent using the subprocess terminal "
            "backend. It avoids tmux startup inside task worker threads."
        ),
    )
    return P11_AGENT_TYPE


def _copy_repo(src: Path) -> Path:
    dst = Path(tempfile.mkdtemp(prefix="p11_native_task_")) / "repo"
    shutil.copytree(src, dst, ignore=_IGNORE)
    return dst


def _selected_dimensions() -> list[tuple[str, str]]:
    dims = bench.DIMENSIONS
    only = os.environ.get("P11_ONLY_DIMS")
    if not only:
        return dims
    wanted = {value.strip() for value in only.split(",") if value.strip()}
    return [(key, desc) for key, desc in dims if key in wanted]


def _resolve_model() -> str:
    raw = os.environ.get("P11_NATIVE_MODEL")
    if raw:
        if raw.strip().lower() == "small":
            small = os.environ.get("LLM_MODEL_SMALL")
            if not small:
                raise SystemExit("P11_NATIVE_MODEL=small requires LLM_MODEL_SMALL")
            return small
        return raw.strip()
    return os.environ.get("LLM_MODEL", bench.DEFAULT_MODEL)


def _build_llm() -> LLM:
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        raise SystemExit("Missing LLM_API_KEY")
    return LLM(
        usage_id="agent",
        model=_resolve_model(),
        api_key=SecretStr(api_key),
        base_url=os.environ.get("LLM_BASE_URL"),
    )


def _final_text(conversation) -> str:
    return get_agent_final_response(conversation.state.events).strip()


def _count_compactions(conversation) -> int:
    total = 0
    for event in conversation.state.events:
        event_type = (getattr(event, "type", None) or type(event).__name__).lower()
        if "compact" in event_type or "condens" in event_type:
            total += 1
    return total


def _metric_dict(label: str, conversation, wall: float, final: str) -> dict:
    metrics = conversation.conversation_stats.get_combined_metrics()
    pin, pout = token_counts(metrics)
    return {
        "label": label,
        "conversation_id": str(conversation.state.id),
        "in": pin,
        "out": pout,
        "cost": float(getattr(metrics, "accumulated_cost", 0.0) or 0.0),
        "wall": wall,
        "events": len(conversation.state.events),
        "compactions": _count_compactions(conversation),
        "quality": score_audit_text(final),
        "final": final,
        "usage": _usage_breakdown(conversation),
    }


def _usage_breakdown(conversation) -> list[dict]:
    rows = []
    usage_to_metrics = getattr(conversation.conversation_stats, "usage_to_metrics", {})
    for usage_id, metrics in usage_to_metrics.items():
        pin, pout = token_counts(metrics)
        rows.append(
            {
                "label": usage_id,
                "in": pin,
                "out": pout,
                "cost": float(getattr(metrics, "accumulated_cost", 0.0) or 0.0),
            }
        )
    return rows


def score_audit_text(text: str) -> str:
    blob = text.lower()
    checks = {
        "docs": "stats" in blob and any(
            term in blob
            for term in ["missing", "not exist", "non-existent", "not implemented"]
        ),
        "errors": (
            "bare except" in blob
            or "except:" in blob
            or "catches all" in blob
            or "swallowed" in blob
            or ("exception" in blob and "return none" in blob)
        ),
        "secrets": "api_key" in blob or "hardcoded" in blob or "credential" in blob,
        "deps": "requests" in blob and any(
            term in blob for term in ["unused", "declared", "dependency"]
        ),
        "tests": "pytest" in blob and any(
            term in blob for term in ["missing", "no test", "not exist"]
        ),
    }
    found = [key for key, ok in checks.items() if ok]
    return f"{len(found)}/5 ({', '.join(found)})"


def _single_agent_prompt(dims: list[tuple[str, str]]) -> str:
    lines = "\n".join(f"  {i + 1}. {desc}" for i, (_, desc) in enumerate(dims))
    return (
        "Audit the repository in your workspace across these dimensions:\n"
        f"{lines}\n\n"
        f"{bench.FINDING_CONTRACT} Produce one findings report covering every "
        "dimension. Do not modify files."
    )


def _task_prompt(dims: list[tuple[str, str]], agent_type: str) -> str:
    tasks = "\n".join(
        (
            f"- description={key!r}, subagent_type={agent_type!r}, "
            f"prompt={bench._dimension_prompt(key, desc)!r}"
        )
        for key, desc in dims
    )
    return (
        "Use the task tool for this audit. Do not inspect the repository in "
        "the parent conversation.\n\n"
        "Launch one task for each audit dimension. Use these exact task "
        "arguments:\n"
        f"{tasks}\n"
        "After all task results return, synthesize a final report grouped by "
        "dimension. Do not invent findings beyond the task results."
    )


def _run_conversation(label: str, prompt: str, repo_src: Path, tools: list[Tool]) -> dict:
    working_dir = _copy_repo(repo_src)
    llm = _build_llm()
    skill = Skill(
        name="p11_audit_contract",
        content="Audit only. Report file and line evidence. Do not modify files.",
        trigger=None,
    )
    agent = Agent(
        llm=llm,
        tools=tools,
        agent_context=AgentContext(skills=[skill]),
        tool_concurrency_limit=5,
    )
    conversation = Conversation(
        agent=agent,
        workspace=working_dir,
        visualizer=None,
        tags={
            "project": "p11-subagents",
            "runner": "native-task-laminar",
            "label": label,
        },
    )
    try:
        t0 = time.time()
        conversation.send_message(prompt)
        conversation.run()
        wall = time.time() - t0
        final = _final_text(conversation)
        return _metric_dict(label, conversation, wall, final)
    finally:
        close = getattr(conversation, "close", None)
        if callable(close):
            close()


def _default_subprocess_tools() -> list[Tool]:
    get_default_tools(enable_browser=False)
    return [
        Tool(name="terminal", params={"terminal_type": "subprocess"}),
        Tool(name="file_editor"),
        Tool(name="task_tracker"),
    ]


def run_single(repo_src: Path, dims: list[tuple[str, str]]) -> dict:
    return _run_conversation(
        "native-single",
        _single_agent_prompt(dims),
        repo_src,
        _default_subprocess_tools(),
    )


def run_task(repo_src: Path, dims: list[tuple[str, str]]) -> dict:
    agent_type = _register_p11_agent_type()
    return _run_conversation(
        "native-task",
        _task_prompt(dims, agent_type),
        repo_src,
        [Tool(name=TaskToolSet.name)],
    )


def _fmt_row(row: dict) -> str:
    return (
        f"  {row['label']:<16} in={row['in']:>8,} out={row['out']:>6,} "
        f"cost=${row['cost']:>7.4f} wall={row['wall']:>5.1f}s "
        f"events={row['events']:>3} comp={row['compactions']:>2} "
        f"quality={row['quality']}"
    )


def _print_report(rows: list[dict]) -> None:
    print("\n" + "=" * 72)
    print("P11 native OpenHands task-tool subagents with Laminar tracing")
    print("=" * 72)
    print(f"Laminar: {'enabled' if os.environ.get('LMNR_PROJECT_API_KEY') else 'disabled'}")
    print(f"Model: {_resolve_model()}")
    for row in rows:
        print("\n" + _fmt_row(row))
        print(f"  conversation_id={row['conversation_id']}")
        task_rows = [r for r in row["usage"] if str(r["label"]).startswith("task:")]
        if task_rows:
            print("  task usage:")
            for usage in task_rows:
                print(
                    f"    {usage['label']:<18} in={usage['in']:>8,} "
                    f"out={usage['out']:>6,} cost=${usage['cost']:>7.4f}"
                )
        if os.environ.get("P11_NATIVE_SHOW_FINAL") == "1":
            print("\n" + row["final"])
    print("=" * 72)


def main() -> None:
    dims = _selected_dimensions()
    if not dims:
        raise SystemExit("No dimensions selected")
    repo_src = PROJECT / "sample_repo"
    print(f"Auditing: {repo_src}")
    print(f"Dimensions: {[key for key, _ in dims]}")

    rows = []
    if os.environ.get("P11_NATIVE_TASK_ONLY") != "1":
        print("[native] single context ...")
        rows.append(run_single(repo_src, dims))
    if os.environ.get("P11_NATIVE_SINGLE_ONLY") != "1":
        print("[native] task tool ...")
        rows.append(run_task(repo_src, dims))
    _print_report(rows)


if __name__ == "__main__":
    main()
