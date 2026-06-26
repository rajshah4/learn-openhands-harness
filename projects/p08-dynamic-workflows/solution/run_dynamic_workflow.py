"""P08 solution - dynamic deep-research workflow.

Run with:
    uv run --with 'openhands-sdk>=1.29.2' --with 'openhands-tools>=1.29.2' \
      python run_dynamic_workflow.py

Cheap verification:
    uv run python run_dynamic_workflow.py --dry-run

Required env vars for live mode: LLM_API_KEY
Optional: LLM_MODEL (default anthropic/claude-sonnet-4-5-20250929)
          AGENT_SERVER (default http://127.0.0.1:18000)
          WORKSPACE_DIR (default current directory)
          P08_MAX_ITERATIONS (default 40 per agent run)

Dynamic mode requires openhands-tools>=1.29.2, which exposes
openhands.tools.workflow.WorkflowToolSet.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import textwrap
import time
from pathlib import Path

PROJECTS_DIR = Path(__file__).resolve().parents[2]
if str(PROJECTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECTS_DIR))

from _runtime import (
    resolve_api_key,
    resolve_host_working_dir,
    server_visible_path,
    token_counts,
)


DEFAULT_MODEL = "anthropic/claude-sonnet-4-5-20250929"
DEFAULT_SERVER = "http://127.0.0.1:18000"
DEFAULT_MAX_ITERATIONS = 40
DEFAULT_QUESTION = "What is changing about AI coding assistants for software teams?"

IGNORE_PATTERNS = shutil.ignore_patterns(
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
    ".openhands-runs",
    ".env",
    ".DS_Store",
)

ARTIFACT_DIR = ".harness_workflow/dynamic"
REPORT_PATH = f"{ARTIFACT_DIR}/DEEP_RESEARCH_REPORT.md"
SUMMARY_PATH = f"{ARTIFACT_DIR}/WORKFLOW_SUMMARY.md"
SKILL_PATH = Path(__file__).with_name("workflow_orchestrator_skill.md")

DYNAMIC_PROMPT = """\
Run a dynamic deep-research workflow for this question:

{question}

Use the deep-research workflow skill. Choose the research angles, fan out to
registered sub-agents, verify unstable claims, and synthesize the result.

Write:
- {report_path}
- {summary_path}
"""


def load_dotenv() -> None:
    for root in [Path.cwd(), *Path.cwd().parents]:
        env_path = root / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
            return


def resolve_workspace(value: str | None) -> Path:
    return resolve_host_working_dir(value)


def copy_workspace(source: Path) -> Path:
    run_root = Path(
        os.environ.get("P08_RUN_ROOT", source / ".openhands-runs" / "p08-dynamic-workflows")
    ).expanduser()
    run_root.mkdir(parents=True, exist_ok=True)
    destination = Path(tempfile.mkdtemp(prefix="p08_dynamic_research_", dir=run_root)) / "repo"
    shutil.copytree(source, destination, ignore=IGNORE_PATTERNS)
    return destination


def require_live_env() -> tuple[str, str, str]:
    load_dotenv()
    api_key = os.environ.get("LLM_API_KEY")
    if not api_key:
        print("Missing required environment variable: LLM_API_KEY", file=sys.stderr)
        raise SystemExit(2)
    model = os.environ.get("LLM_MODEL", DEFAULT_MODEL)
    server = os.environ.get("AGENT_SERVER", DEFAULT_SERVER)
    return api_key, model, server


def resolve_max_iterations() -> int:
    raw = os.environ.get("P08_MAX_ITERATIONS", str(DEFAULT_MAX_ITERATIONS))
    try:
        value = int(raw)
    except ValueError:
        print(f"P08_MAX_ITERATIONS must be an integer, got: {raw}", file=sys.stderr)
        raise SystemExit(2)
    if value < 1:
        print("P08_MAX_ITERATIONS must be at least 1", file=sys.stderr)
        raise SystemExit(2)
    return value


def require_workflow_imports():
    try:
        from openhands.sdk import Agent, Conversation, RemoteConversation, Workspace
        try:
            from openhands.sdk import AgentContext
        except ImportError:
            from openhands.sdk.context import AgentContext
        try:
            from openhands.sdk import Tool
        except ImportError:
            try:
                from openhands.sdk.tool import Tool
            except ImportError:
                from openhands.sdk.tool.spec import Tool
        from openhands.sdk.subagent import register_agent_if_absent
        from openhands.tools.file_editor import FileEditorTool
        from openhands.tools.terminal import TerminalTool
        from openhands.tools.workflow import WorkflowToolSet
    except Exception as exc:
        print(
            "\n".join(
                [
                    "Dynamic workflow mode requires OpenHands packages with WorkflowToolSet.",
                    "The starter manual baseline and solution dry run still work.",
                    "Install openhands-sdk>=1.29.2 and openhands-tools>=1.29.2, then rerun this solution live.",
                    f"Import error: {type(exc).__name__}: {exc}",
                ]
            ),
            file=sys.stderr,
        )
        raise SystemExit(2)

    return {
        "Agent": Agent,
        "AgentContext": AgentContext,
        "Conversation": Conversation,
        "RemoteConversation": RemoteConversation,
        "Workspace": Workspace,
        "Tool": Tool,
        "register_agent_if_absent": register_agent_if_absent,
        "FileEditorTool": FileEditorTool,
        "TerminalTool": TerminalTool,
        "WorkflowToolSet": WorkflowToolSet,
    }


def build_skill(name: str, content: str):
    try:
        from openhands.sdk.context import Skill

        return Skill(name=name, content=content, trigger=None)
    except Exception:
        return {"name": name, "content": content}


def build_agent_context(agent_context_cls, skills: list, suffix: str):
    try:
        return agent_context_cls(skills=skills, system_message_suffix=suffix)
    except TypeError:
        try:
            return agent_context_cls(skills=skills, system_message=suffix)
        except TypeError:
            return agent_context_cls(skills=skills)


def read_workflow_skill() -> str:
    if not SKILL_PATH.exists():
        print(f"Missing workflow skill: {SKILL_PATH}", file=sys.stderr)
        raise SystemExit(2)
    return SKILL_PATH.read_text(encoding="utf-8")


def register_research_agents(imports: dict, llm) -> None:
    Agent = imports["Agent"]
    AgentContext = imports["AgentContext"]
    Tool = imports["Tool"]
    FileEditorTool = imports["FileEditorTool"]
    TerminalTool = imports["TerminalTool"]
    register_agent_if_absent = imports["register_agent_if_absent"]

    reader_tools = [Tool(name=TerminalTool.name), Tool(name=FileEditorTool.name)]

    def role_agent(child_llm, role_skill: str, suffix: str):
        return Agent(
            llm=child_llm,
            tools=reader_tools,
            agent_context=build_agent_context(
                AgentContext,
                [build_skill("role", role_skill)],
                suffix,
            ),
        )

    register_agent_if_absent(
        "web_searcher",
        lambda child_llm: role_agent(
            child_llm,
            "Research one angle deeply. Prefer primary sources. State tool limits.",
            "You are a web researcher. Separate evidence from interpretation.",
        ),
        "Researches one angle with sources",
    )
    register_agent_if_absent(
        "fact_checker",
        lambda child_llm: role_agent(
            child_llm,
            "Verify source quality, flag stale-risk claims, and preserve uncertainty.",
            "You are a skeptical fact-checker. Do not invent sources.",
        ),
        "Verifies claims and source quality",
    )
    register_agent_if_absent(
        "synthesizer",
        lambda child_llm: role_agent(
            child_llm,
            "Synthesize verified research into the required artifacts.",
            "You synthesize deep research. Preserve uncertainty.",
        ),
        "Synthesizes verified research",
    )


def build_workflow_agent(imports: dict, llm, skill_content: str):
    Agent = imports["Agent"]
    AgentContext = imports["AgentContext"]
    Tool = imports["Tool"]
    WorkflowToolSet = imports["WorkflowToolSet"]

    return Agent(
        llm=llm,
        tools=[Tool(name=WorkflowToolSet.name)],
        agent_context=build_agent_context(
            AgentContext,
            [build_skill("deep_research_orchestrator", skill_content)],
            "Use the workflow skill for broad research. Keep the generated workflow bounded and inspectable.",
        ),
    )


def run_dynamic(workspace: Path, question: str) -> None:
    from pydantic import SecretStr
    from openhands.sdk import LLM

    imports = require_workflow_imports()
    Conversation = imports["Conversation"]
    RemoteConversation = imports["RemoteConversation"]
    Workspace = imports["Workspace"]

    api_key, model, server = require_live_env()
    llm = LLM(usage_id="agent", model=model, api_key=SecretStr(api_key))
    register_research_agents(imports, llm)

    copied_workspace = copy_workspace(workspace)
    print(f"Dynamic deep-research workspace: {copied_workspace}")
    print(f"Agent-server working_dir: {server_visible_path(copied_workspace)}")

    agent = build_workflow_agent(imports, llm, read_workflow_skill())
    remote_workspace = Workspace(
        host=server,
        api_key=resolve_api_key(),
        working_dir=server_visible_path(copied_workspace),
    )
    conversation = Conversation(
        agent=agent,
        workspace=remote_workspace,
        max_iteration_per_run=resolve_max_iterations(),
    )
    assert isinstance(conversation, RemoteConversation)

    prompt = DYNAMIC_PROMPT.format(
        question=question,
        report_path=REPORT_PATH,
        summary_path=SUMMARY_PATH,
    )

    try:
        t0 = time.time()
        conversation.send_message(prompt)
        conversation.run()
        wall = time.time() - t0
        metrics = conversation.conversation_stats.get_combined_metrics()
        prompt_tokens, completion_tokens = token_counts(metrics)
        print(
            f"dynamic:deep-research events={len(conversation.state.events)} "
            f"wall={wall:.1f}s cost=${float(getattr(metrics, 'accumulated_cost', 0.0) or 0.0):.4f} "
            f"tokens_in={prompt_tokens} tokens_out={completion_tokens}"
        )
        print(f"Report:  {copied_workspace / REPORT_PATH}")
        print(f"Summary: {copied_workspace / SUMMARY_PATH}")
    finally:
        conversation.close()


def print_dry_run(workspace: Path, question: str) -> None:
    prompt = DYNAMIC_PROMPT.format(
        question=question,
        report_path=REPORT_PATH,
        summary_path=SUMMARY_PATH,
    )
    print(f"Workspace: {workspace}")
    print(f"Question: {question}")
    print("\nNo model calls will be made.")
    print("\n--- registered roles ---")
    print("- web_searcher")
    print("- fact_checker")
    print("- synthesizer")
    print("\n--- workflow skill file ---")
    print(f"  {SKILL_PATH}")
    print("\n--- parent prompt ---")
    print(textwrap.indent(prompt.strip(), "  "))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the P08 dynamic deep-research workflow solution.")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--workspace", default=None, help="Workspace for artifacts. Defaults to WORKSPACE_DIR or cwd.")
    parser.add_argument("--dry-run", action="store_true", help="Print workflow setup without model calls.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = resolve_workspace(args.workspace)
    if args.dry_run:
        print_dry_run(workspace, args.question)
    else:
        run_dynamic(workspace, args.question)


if __name__ == "__main__":
    main()
