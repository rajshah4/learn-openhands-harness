"""P11 solution: Scenario C, native task-tool subagents on a monster repo.

This runner compares one read-only investigation against native OpenHands
task-tool subagents on the local VS Code custom-image benchmark tree.

Run a cheap smoke:
    P11_MONSTER_MODEL=small P11_MONSTER_ONLY_AREAS=benchmark_doc,custom_image \
      uv run --with openhands-sdk --with openhands-tools \
      python projects/p11-subagents/solution/run_monster_repo.py

Run the full scenario:
    P11_MONSTER_MODEL=small \
      uv run --with openhands-sdk --with openhands-tools \
      python projects/p11-subagents/solution/run_monster_repo.py

Env:
    LMNR_PROJECT_API_KEY        optional, read from nearest .env
    LLM_API_KEY                 required, read from nearest .env
    LLM_MODEL                   default parent and child model
    LLM_MODEL_SMALL             used when P11_MONSTER_MODEL=small
    P11_MONSTER_MODEL           optional model override, or "small"
    P11_MONSTER_ROOT            default ~/p11-monster (clone the two benchmark repos there)
    P11_MONSTER_ONLY_AREAS      optional CSV subset
    P11_MONSTER_SINGLE_ONLY=1   run only the single-agent config
    P11_MONSTER_TASK_ONLY=1     run only the task-tool config
    P11_MONSTER_SHOW_FINAL=1    print final reports
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT.parent))  # projects/ for _runtime

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


DEFAULT_ROOT = "~/p11-monster"
MONSTER_AGENT_TYPE = "p11-monster-explorer"

AREAS = [
    (
        "benchmark_doc",
        "Find the VS Code benchmark task, pinned branch and commit, target files, "
        "and the narrow verification command.",
    ),
    (
        "source_bug",
        "Inspect the configuration model implementation around skipRestricted "
        "and excludedConfigurationProperties. Explain the likely regression.",
    ),
    (
        "test_contract",
        "Inspect the excluded restricted properties test. Explain what behavior "
        "the test is asserting.",
    ),
    (
        "setup_helpers",
        "Inspect the OpenHands benchmark helper scripts. Explain bootstrap, "
        "status, verification, phase logs, and why VSCODE_SKIP_PRELAUNCH appears.",
    ),
    (
        "custom_image",
        "Inspect the custom image demo. Explain what the VS Code benchmark image "
        "prebakes, which helper commands it exposes, and which image tag is the "
        "latest rebuilt benchmark image.",
    ),
]

CHECKLIST = [
    ("branch", ["openhands-benchmark-01"]),
    ("commit", ["9d16a199035b6640b955a21f1dddd1604ab3fe29"]),
    ("source_file", ["configurationmodels.ts"]),
    ("test_file", ["configurationmodels.test.ts"]),
    ("grep", ["excluded restricted properties"]),
    ("verify_script", ["openhands-benchmark-verify.sh"]),
    ("bootstrap_script", ["openhands-stock-bootstrap.sh"]),
    ("status_script", ["openhands-benchmark-status.sh"]),
    ("skip_prelaunch", ["vscode_skip_prelaunch"]),
    ("npm_install", ["npm install"]),
    ("transpile", ["transpile-client-esbuild"]),
    ("electron", ["npm run electron"]),
    ("prepare_custom", ["prepare-vscode-benchmark"]),
    ("verify_custom", ["vscode-benchmark-verify"]),
    ("custom_tag", ["vscode-benchmark-2026-05-23-v3"]),
]


def _register_monster_agent_type() -> str:
    get_default_tools(enable_browser=False)

    def create_monster_explorer(llm: LLM) -> Agent:
        skill = Skill(
            name="p11_monster_explorer",
            content=(
                "You are a read-only large-repo investigation agent. Use only "
                "read-only terminal commands such as pwd, ls, find, rg, git, sed, "
                "cat, head, tail, wc, and stat. Do not edit files. Do not run "
                "install, build, test, docker, network, or long-running commands. "
                "Return compact facts with file paths and line evidence."
            ),
            trigger=None,
        )
        return Agent(
            llm=llm,
            tools=[Tool(name="terminal", params={"terminal_type": "subprocess"})],
            agent_context=AgentContext(skills=[skill]),
        )

    register_agent_if_absent(
        name=MONSTER_AGENT_TYPE,
        factory_func=create_monster_explorer,
        description=(
            "Read-only P11 large-repo investigation subagent using subprocess "
            "terminal commands."
        ),
    )
    return MONSTER_AGENT_TYPE


def _root() -> Path:
    root = Path(os.environ.get("P11_MONSTER_ROOT", DEFAULT_ROOT)).expanduser()
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"P11_MONSTER_ROOT is not a directory: {root}")
    return root


def _selected_areas() -> list[tuple[str, str]]:
    only = os.environ.get("P11_MONSTER_ONLY_AREAS")
    if not only:
        return AREAS
    wanted = {value.strip() for value in only.split(",") if value.strip()}
    return [(key, desc) for key, desc in AREAS if key in wanted]


def _resolve_model() -> str:
    raw = os.environ.get("P11_MONSTER_MODEL")
    if raw:
        value = raw.strip()
        if value.lower() == "small":
            small = os.environ.get("LLM_MODEL_SMALL")
            if not small:
                raise SystemExit("P11_MONSTER_MODEL=small requires LLM_MODEL_SMALL")
            return small
        return value
    return os.environ.get("LLM_MODEL", "anthropic/claude-sonnet-4-5-20250929")


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


def _readonly_tools() -> list[Tool]:
    get_default_tools(enable_browser=False)
    return [Tool(name="terminal", params={"terminal_type": "subprocess"})]


def _skill() -> Skill:
    return Skill(
        name="p11_monster_contract",
        content=(
            "This is a read-only benchmark investigation. Use file paths and "
            "line evidence. Do not modify files. Do not run install, build, test, "
            "docker, network, package manager, or long-running commands."
        ),
        trigger=None,
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


def _score(text: str) -> tuple[int, int, list[str]]:
    blob = text.lower()
    found = []
    for label, needles in CHECKLIST:
        if all(needle in blob for needle in needles):
            found.append(label)
    return len(found), len(CHECKLIST), found


def _metric_dict(label: str, conversation, wall: float, final: str) -> dict:
    metrics = conversation.conversation_stats.get_combined_metrics()
    pin, pout = token_counts(metrics)
    score, total, found = _score(final)
    return {
        "label": label,
        "conversation_id": str(conversation.state.id),
        "in": pin,
        "out": pout,
        "cost": float(getattr(metrics, "accumulated_cost", 0.0) or 0.0),
        "wall": wall,
        "events": len(conversation.state.events),
        "compactions": _count_compactions(conversation),
        "score": score,
        "score_total": total,
        "found": found,
        "final": final,
        "usage": _usage_breakdown(conversation),
    }


def _run_conversation(label: str, prompt: str, root: Path, tools: list[Tool]) -> dict:
    agent = Agent(
        llm=_build_llm(),
        tools=tools,
        agent_context=AgentContext(skills=[_skill()]),
        tool_concurrency_limit=5,
    )
    conversation = Conversation(
        agent=agent,
        workspace=root,
        visualizer=None,
        tags={
            "project": "p11-subagents",
            "runner": "monster-repo-native-task",
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


def _area_list(areas: list[tuple[str, str]]) -> str:
    return "\n".join(f"- {key}: {desc}" for key, desc in areas)


def _expected_fact_list() -> str:
    return "\n".join(f"- {label}" for label, _ in CHECKLIST)


def _final_contract() -> str:
    return (
        "Final answer contract: return a concise report plus a checklist table. "
        "The checklist table must use the exact fact label strings below in the "
        "first column. If a fact is found, include the exact value and evidence. "
        "Do not collapse exact script names, commits, commands, tags, or file "
        "paths into general prose.\n"
        f"{_expected_fact_list()}"
    )


def _single_prompt(root: Path, areas: list[tuple[str, str]]) -> str:
    return (
        "Investigate this large local benchmark tree from one conversation.\n\n"
        f"Workspace root: {root}\n"
        "Important paths:\n"
        "- vscode-benchmark-repo/\n"
        "- openhands-custom-image/\n\n"
        "Investigate these areas:\n"
        f"{_area_list(areas)}\n\n"
        "Do not run tests, builds, installs, docker, package managers, or network "
        "commands. Use read-only commands only.\n\n"
        f"{_final_contract()}"
    )


def _task_prompt(root: Path, areas: list[tuple[str, str]], agent_type: str) -> str:
    def task_line(key: str, desc: str) -> str:
        prompt = (
            f"{desc} Work under {root}. Important paths are "
            "vscode-benchmark-repo/ and openhands-custom-image/. Use read-only "
            "commands only. Return compact facts with file and line evidence. "
            "Preserve exact values for any expected checklist labels you find: "
            f"{', '.join(label for label, _ in CHECKLIST)}."
        )
        return (
            f"- description={key!r}, subagent_type={agent_type!r}, "
            f"prompt={prompt!r}"
        )

    tasks = "\n".join(
        task_line(key, desc) for key, desc in areas
    )
    return (
        "Use the task tool for this large-repo investigation. The parent "
        "conversation should not inspect files directly.\n\n"
        "Launch one task for each investigation area. Use these exact task "
        "arguments:\n"
        f"{tasks}\n\n"
        "After all task results return, synthesize one concise report. Preserve "
        "exact values from the child results.\n\n"
        f"{_final_contract()}"
    )


def run_single(root: Path, areas: list[tuple[str, str]]) -> dict:
    return _run_conversation(
        "monster-single",
        _single_prompt(root, areas),
        root,
        _readonly_tools(),
    )


def run_task(root: Path, areas: list[tuple[str, str]]) -> dict:
    agent_type = _register_monster_agent_type()
    return _run_conversation(
        "monster-task",
        _task_prompt(root, areas, agent_type),
        root,
        [Tool(name=TaskToolSet.name)],
    )


def _fmt_row(row: dict) -> str:
    return (
        f"  {row['label']:<17} in={row['in']:>8,} out={row['out']:>6,} "
        f"cost=${row['cost']:>7.4f} wall={row['wall']:>5.1f}s "
        f"events={row['events']:>3} comp={row['compactions']:>2} "
        f"score={row['score']}/{row['score_total']}"
    )


def _print_report(rows: list[dict]) -> None:
    print("\n" + "=" * 76)
    print("P11 Scenario C: monster repo native task-tool subagents")
    print("=" * 76)
    print(f"Laminar: {'enabled' if os.environ.get('LMNR_PROJECT_API_KEY') else 'disabled'}")
    print(f"Model: {_resolve_model()}")
    for row in rows:
        print("\n" + _fmt_row(row))
        print(f"  conversation_id={row['conversation_id']}")
        print(f"  found={', '.join(row['found'])}")
        task_rows = [r for r in row["usage"] if str(r["label"]).startswith("task:")]
        if task_rows:
            print("  task usage:")
            for usage in task_rows:
                print(
                    f"    {usage['label']:<24} in={usage['in']:>8,} "
                    f"out={usage['out']:>6,} cost=${usage['cost']:>7.4f}"
                )
        if os.environ.get("P11_MONSTER_SHOW_FINAL") == "1":
            print("\n" + row["final"])
    print("=" * 76)


def main() -> None:
    root = _root()
    areas = _selected_areas()
    if not areas:
        raise SystemExit("No areas selected")
    print(f"Workspace root: {root}")
    print(f"Areas: {[key for key, _ in areas]}")

    rows = []
    if os.environ.get("P11_MONSTER_TASK_ONLY") != "1":
        print("[monster] single investigation ...")
        rows.append(run_single(root, areas))
    if os.environ.get("P11_MONSTER_SINGLE_ONLY") != "1":
        print("[monster] native task-tool investigation ...")
        rows.append(run_task(root, areas))
    _print_report(rows)


if __name__ == "__main__":
    main()
