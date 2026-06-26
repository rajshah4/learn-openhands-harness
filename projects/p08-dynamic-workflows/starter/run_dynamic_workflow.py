"""P08 starter - manual deep-research orchestration.

Run with:
    uv run --with 'openhands-sdk>=1.29.2' --with 'openhands-tools>=1.29.2' \
      python run_dynamic_workflow.py

Cheap verification:
    uv run python run_dynamic_workflow.py --dry-run

Optional env vars:
    P08_MAX_ITERATIONS (default 40 per agent run)

This starter is intentionally the old way: Python owns the research angles,
the sequencing, the intermediate files, and the final synthesis step. The
solution moves that orchestration into a workflow-capable harness.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import textwrap
import time
from dataclasses import dataclass
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


@dataclass(frozen=True)
class ResearchAngle:
    label: str
    title: str
    output: str
    fact_output: str
    focus: str


RESEARCH_ANGLES = [
    ResearchAngle(
        label="market",
        title="Market landscape and adoption",
        output=".harness_workflow/manual/research_market.md",
        fact_output=".harness_workflow/manual/fact_market.md",
        focus="major products, buyer segments, adoption patterns, and where budgets are moving",
    ),
    ResearchAngle(
        label="technical",
        title="Technical capabilities",
        output=".harness_workflow/manual/research_technical.md",
        fact_output=".harness_workflow/manual/fact_technical.md",
        focus="agent capabilities, tool use, context management, evaluation, and workflow automation",
    ),
    ResearchAngle(
        label="developer-workflow",
        title="Developer workflow impact",
        output=".harness_workflow/manual/research_workflow.md",
        fact_output=".harness_workflow/manual/fact_workflow.md",
        focus="how teams plan, code, review, test, and ship with coding agents",
    ),
    ResearchAngle(
        label="risk",
        title="Risks and open questions",
        output=".harness_workflow/manual/research_risk.md",
        fact_output=".harness_workflow/manual/fact_risk.md",
        focus="security, correctness, cost, governance, evaluation gaps, and failure modes",
    ),
]


RESEARCH_PROMPT = """\
Deep-research question:
{question}

Research angle:
{title}

Focus:
{focus}

Write a scoped research memo to:
{output}

Rules:
- Use available tools to look for current, concrete evidence. If web browsing
  or search is unavailable, say that clearly in the memo.
- Prefer primary sources, product docs, release notes, technical reports, and
  cited customer or benchmark claims.
- Separate evidence from interpretation.
- Include a "Claims to verify" section with the claims most likely to be stale,
  overbroad, or marketing-driven.
- Do not read .env or print secret values.
"""

FACT_CHECK_PROMPT = """\
Read {research_output}.

Fact-check the scoped memo against the original question:
{question}

Write a verification memo to:
{fact_output}

Rules:
- Mark major claims as Verified, Needs source, Stale risk, or Unsupported.
- Preserve source URLs or exact citations from the research memo.
- Flag any claim that depends on current pricing, market size, model capability,
  release status, or customer adoption.
- Do not invent new facts to make the memo look stronger.
"""


def aggregate_prompt(question: str) -> str:
    research_files = "\n".join(f"- {angle.output}" for angle in RESEARCH_ANGLES)
    fact_files = "\n".join(f"- {angle.fact_output}" for angle in RESEARCH_ANGLES)
    return f"""\
Synthesize a deep-research report for:
{question}

Read the scoped research memos:
{research_files}

Read the verification memos:
{fact_files}

Write the final report to:
.harness_workflow/manual/DEEP_RESEARCH_REPORT.md

The final report must include:
1. Executive summary.
2. Key findings by theme.
3. Evidence table with source or verification status.
4. Areas of uncertainty and stale-risk claims.
5. Implications for harness engineering and dynamic workflows.
6. Open questions worth researching next.

Rules:
- Do not invent sources.
- Preserve uncertainty from the verification memos.
- If a claim was not verified, label it clearly.
- Include a short note explaining that this result came from fixed manual
  orchestration: Python chose the angles, ran the loops, and aggregated files.
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
    destination = Path(tempfile.mkdtemp(prefix="p08_manual_research_", dir=run_root)) / "repo"
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


def run_prompt(label: str, llm, server: str, working_dir: Path, prompt: str) -> dict:
    from openhands.sdk import Conversation, RemoteConversation, Workspace
    from openhands.tools.preset.default import get_default_agent

    agent = get_default_agent(llm=llm, cli_mode=True)
    workspace = Workspace(
        host=server,
        api_key=resolve_api_key(),
        working_dir=server_visible_path(working_dir),
    )
    conversation = Conversation(
        agent=agent,
        workspace=workspace,
        max_iteration_per_run=resolve_max_iterations(),
    )
    assert isinstance(conversation, RemoteConversation)

    try:
        t0 = time.time()
        conversation.send_message(prompt)
        conversation.run()
        wall = time.time() - t0
        metrics = conversation.conversation_stats.get_combined_metrics()
        prompt_tokens, completion_tokens = token_counts(metrics)
        return {
            "label": label,
            "events": len(conversation.state.events),
            "wall": wall,
            "cost": float(getattr(metrics, "accumulated_cost", 0.0) or 0.0),
            "tokens_in": prompt_tokens,
            "tokens_out": completion_tokens,
        }
    finally:
        conversation.close()


def manual_research_prompts(question: str) -> list[tuple[str, str]]:
    prompts = []
    for angle in RESEARCH_ANGLES:
        prompts.append(
            (
                f"research:{angle.label}",
                RESEARCH_PROMPT.format(
                    question=question,
                    title=angle.title,
                    focus=angle.focus,
                    output=angle.output,
                ),
            )
        )
    for angle in RESEARCH_ANGLES:
        prompts.append(
            (
                f"fact-check:{angle.label}",
                FACT_CHECK_PROMPT.format(
                    question=question,
                    research_output=angle.output,
                    fact_output=angle.fact_output,
                ),
            )
        )
    prompts.append(("synthesize", aggregate_prompt(question)))
    return prompts


def run_manual(workspace: Path, question: str) -> None:
    from pydantic import SecretStr
    from openhands.sdk import LLM

    api_key, model, server = require_live_env()
    llm = LLM(usage_id="agent", model=model, api_key=SecretStr(api_key))
    copied_workspace = copy_workspace(workspace)
    print(f"Manual deep-research workspace: {copied_workspace}")
    print(f"Agent-server working_dir: {server_visible_path(copied_workspace)}")

    results = [
        run_prompt(label, llm, server, copied_workspace, prompt)
        for label, prompt in manual_research_prompts(question)
    ]

    print_results(results)
    print(
        "Manual report: "
        f"{copied_workspace / '.harness_workflow' / 'manual' / 'DEEP_RESEARCH_REPORT.md'}"
    )


def print_results(results: list[dict]) -> None:
    print("\n" + "=" * 96)
    print(
        f"{'Step':<24} {'Events':>7} {'Wall':>8} "
        f"{'Cost':>10} {'Tokens in':>12} {'Tokens out':>12}"
    )
    print("-" * 96)
    for row in results:
        print(
            f"{row['label']:<24} {row['events']:>7} {row['wall']:>7.1f}s "
            f"${row['cost']:>9.4f} {row['tokens_in']:>12} {row['tokens_out']:>12}"
        )
    print("=" * 96)


def print_dry_run(workspace: Path, question: str) -> None:
    print(f"Workspace: {workspace}")
    print(f"Question: {question}")
    print("\nNo model calls will be made.")
    print("\n--- fixed manual deep-research workflow ---")
    for label, prompt in manual_research_prompts(question):
        print(f"\n[{label}]")
        print(textwrap.indent(prompt.strip(), "  "))
    print("\nManual orchestration code owns every step above.")
    print("Read the P08 README, then build the dynamic workflow in the solution.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P08 manual deep-research starter.")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    parser.add_argument("--workspace", default=None, help="Workspace for artifacts. Defaults to WORKSPACE_DIR or cwd.")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without model calls.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = resolve_workspace(args.workspace)
    if args.dry_run:
        print_dry_run(workspace, args.question)
        return
    run_manual(workspace, args.question)


if __name__ == "__main__":
    main()
