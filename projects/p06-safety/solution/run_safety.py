"""P06 solution — security analyzer + confirmation policy + Docker sandbox.

Run with:
    uv run --with openhands-sdk --with openhands-tools python run_safety.py [read|edit|network|delete]
    uv run --with openhands-sdk --with openhands-tools python run_safety.py --classify-dry
    uv run --with openhands-sdk --with openhands-tools --with openhands-workspace \
        python run_safety.py --docker --interactive [read|edit|network|delete]

Required env vars:  LLM_API_KEY
Optional:           LLM_MODEL (default anthropic/claude-sonnet-4-5-20250929)
                    AGENT_SERVER (default http://127.0.0.1:18000)
                    WORKSPACE_DIR (default current directory)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PROJECTS_DIR = Path(__file__).resolve().parents[2]
if str(PROJECTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECTS_DIR))

from pydantic import SecretStr
from openhands.sdk import LLM, Agent, Conversation, RemoteConversation, Workspace
from openhands.sdk.conversation.state import (
    ConversationExecutionStatus,
    ConversationState,
)
from openhands.sdk.event import ActionEvent
from openhands.sdk.llm.message import MessageToolCall, TextContent
from openhands.sdk.tool import Tool
from openhands.sdk.security import (
    ConfirmRisky,
    EnsembleSecurityAnalyzer,
    LLMSecurityAnalyzer,
    PatternSecurityAnalyzer,
    PolicyRailSecurityAnalyzer,
    SecurityRisk,
)
from openhands.sdk.security.defense_in_depth.pattern import (
    DEFAULT_HIGH_PATTERNS,
    DEFAULT_MEDIUM_PATTERNS,
)
from openhands.tools.terminal import TerminalTool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from _runtime import (
    resolve_api_key,
    resolve_host_working_dir,
    resolve_server_working_dir,
    server_visible_path,
)

PROMPTS = {
    "read": "List the files and summarize the repo layout.",
    "edit": "Create NOTES.md with three facts about this repo.",
    "network": "Install the 'requests' package.",
    "delete": "Delete the NOTES.md file you just created.",
}

DEFAULT_MODEL = "anthropic/claude-sonnet-4-5-20250929"
CONFIRMATION_THRESHOLD = SecurityRisk.MEDIUM

ORG_HIGH_PATTERNS = [
    (
        r"\b(?:pip|uv|npm|pnpm|yarn)\s+(?:install|add)\b",
        "Package install changes dependencies or reaches the network",
        "org.package_install",
    ),
    (
        r"\brm\s+(?!(?:.*\s)?-i(?:\s|$)).+",
        "File deletion without an interactive prompt",
        "org.file_delete",
    ),
]

DRY_ACTIONS = {
    "read": ("ls -la && find . -maxdepth 2 -type f | head -20", SecurityRisk.LOW),
    "edit": (
        "python -c \"from pathlib import Path; Path('NOTES.md').write_text('notes')\"",
        SecurityRisk.LOW,
    ),
    "network": ("pip install requests", SecurityRisk.HIGH),
    "delete": ("rm NOTES.md", SecurityRisk.HIGH),
}


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Missing required environment variable: {name}", file=sys.stderr)
        raise SystemExit(2)
    return value


def build_security_analyzer() -> EnsembleSecurityAnalyzer:
    pattern_analyzer = PatternSecurityAnalyzer(
        high_patterns=[*DEFAULT_HIGH_PATTERNS, *ORG_HIGH_PATTERNS],
        medium_patterns=list(DEFAULT_MEDIUM_PATTERNS),
    )
    return EnsembleSecurityAnalyzer(
        analyzers=[
            PolicyRailSecurityAnalyzer(),
            pattern_analyzer,
            LLMSecurityAnalyzer(),
        ],
    )


def make_terminal_action(command: str) -> ActionEvent:
    return ActionEvent(
        thought=[TextContent(text="Dry-run representative terminal action.")],
        tool_name=TerminalTool.name,
        tool_call_id=f"dry-{abs(hash(command))}",
        tool_call=MessageToolCall(
            id=f"dry-{abs(hash(command))}",
            name=TerminalTool.name,
            arguments=json.dumps({"command": command}),
            origin="completion",
        ),
        llm_response_id="dry-run",
        security_risk=SecurityRisk.UNKNOWN,
        summary=command,
    )


def classify_dry() -> None:
    analyzer = build_security_analyzer()
    policy = ConfirmRisky(threshold=CONFIRMATION_THRESHOLD)
    print("Dry security classification; no model call and no workspace action.\n")
    print(f"{'Prompt':<10} {'Expected':<9} {'Analyzer':<9} {'Confirm?':<8} Command")
    print("-" * 86)
    for key, (command, expected) in DRY_ACTIONS.items():
        risk = analyzer.security_risk(make_terminal_action(command))
        confirm = "yes" if policy.should_confirm(risk) else "no"
        print(f"{key:<10} {expected.value:<9} {risk.value:<9} {confirm:<8} {command}")
    print("\nIf expected and analyzer disagree, adjust org_security_policy.j2 or the deterministic patterns.")


def preflight_docker() -> None:
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except FileNotFoundError:
        print("Docker mode requires the docker CLI, but `docker` was not found.", file=sys.stderr)
        raise SystemExit(2)
    except subprocess.TimeoutExpired:
        print("Docker mode requires Docker to be running; `docker info` timed out.", file=sys.stderr)
        raise SystemExit(2)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        message = detail[-1] if detail else "docker info failed"
        print(f"Docker mode requires a running Docker daemon: {message}", file=sys.stderr)
        raise SystemExit(2)


def summarize_action(action: ActionEvent, analyzer: EnsembleSecurityAnalyzer) -> str:
    risk = analyzer.security_risk(action)
    args = action.tool_call.arguments if action.tool_call else ""
    if len(args) > 180:
        args = args[:177].rstrip() + "..."
    summary = action.summary or ""
    return f"{action.tool_name} risk={risk.value} summary={summary!r} args={args}"


def get_pending_actions(conversation: RemoteConversation) -> list[ActionEvent]:
    conversation.state.events.reconcile()
    return ConversationState.get_unmatched_actions(list(conversation.state.events))


def handle_confirmation(
    conversation: RemoteConversation,
    analyzer: EnsembleSecurityAnalyzer,
    interactive: bool,
    pending: list[ActionEvent],
) -> bool:
    print("\n[CONFIRM] The agent is waiting before running pending action(s):")
    for action in pending:
        print(f"  - {summarize_action(action, analyzer)}")
    if not pending:
        print("  - No unmatched action found in the local event cache yet.")

    if not interactive:
        print("[CONFIRM] Non-interactive run: rejecting. Rerun with --interactive to approve.")
        conversation.reject_pending_actions(
            "Rejected by non-interactive P06 runner; rerun with --interactive to approve."
        )
        return False

    answer = input("[CONFIRM] Approve these action(s)? [y/N] ").strip().lower()
    if answer not in {"y", "yes"}:
        conversation.reject_pending_actions("Rejected by user in P06 runner.")
        return False

    conversation.run(blocking=False)
    return True


def run_with_confirmations(
    conversation: RemoteConversation,
    analyzer: EnsembleSecurityAnalyzer,
    interactive: bool,
    timeout: float = 1800.0,
) -> str:
    conversation.run(blocking=False)
    start = time.monotonic()
    handled_wait_states = 0
    approved_batches: set[tuple[str, ...]] = set()

    while True:
        if time.monotonic() - start > timeout:
            conversation.pause()
            raise TimeoutError(f"conversation did not finish within {timeout:.0f}s")

        state = conversation.state.refresh_from_server()
        status = ConversationExecutionStatus(state["execution_status"])
        if status == ConversationExecutionStatus.WAITING_FOR_CONFIRMATION:
            handled_wait_states += 1
            pending = get_pending_actions(conversation)
            batch = tuple(action.id for action in pending)
            if batch in approved_batches:
                time.sleep(1.0)
                continue
            approved = handle_confirmation(conversation, analyzer, interactive, pending)
            if not approved:
                return "rejected"
            approved_batches.add(batch)
            time.sleep(0.5)
            continue
        if status == ConversationExecutionStatus.FINISHED:
            conversation.state.events.reconcile()
            return "finished"
        if status in {ConversationExecutionStatus.ERROR, ConversationExecutionStatus.STUCK}:
            raise RuntimeError(f"conversation ended with status: {status.value}")
        if handled_wait_states and status == ConversationExecutionStatus.IDLE:
            return "stopped_after_confirmation"
        time.sleep(1.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run P06 safety prompts.")
    parser.add_argument("prompt", nargs="?", choices=sorted(PROMPTS), default="read")
    parser.add_argument("--docker", action="store_true", help="Run in DockerWorkspace.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt in the terminal when confirmation is required.",
    )
    parser.add_argument(
        "--classify-dry",
        action="store_true",
        help="Classify representative actions without model calls or workspace changes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.classify_dry:
        classify_dry()
        return

    if args.docker:
        preflight_docker()
    api_key = require_env("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL", DEFAULT_MODEL)
    server = os.environ.get("AGENT_SERVER", "http://127.0.0.1:18000")
    working_dir = resolve_host_working_dir() if args.docker else resolve_server_working_dir()

    llm = LLM(usage_id="agent", model=model, api_key=SecretStr(api_key))
    security_analyzer = build_security_analyzer()

    tools = [
        Tool(name=TerminalTool.name),
        Tool(name=FileEditorTool.name),
        Tool(name=TaskTrackerTool.name),
    ]

    policy_path = (Path(__file__).parent / "org_security_policy.j2").resolve()
    policy_mount = f"{policy_path.parent}:/openhands-harness-policy:ro"
    policy_filename = (
        f"/openhands-harness-policy/{policy_path.name}"
        if args.docker
        else server_visible_path(policy_path)
    )
    agent = Agent(
        llm=llm,
        tools=tools,
        security_policy_filename=policy_filename,
    )

    if args.docker:
        from openhands.workspace import DockerWorkspace
        workspace = DockerWorkspace(
            server_image="ghcr.io/openhands/agent-server:latest-python",
            host_port=8010,
            mount_dir=str(working_dir),
            volumes=[policy_mount],
        )
    else:
        workspace = Workspace(
            host=server,
            api_key=resolve_api_key(),
            working_dir=working_dir,
        )

    prompt_key = args.prompt
    prompt = PROMPTS[prompt_key]

    conversation = Conversation(agent=agent, workspace=workspace)
    assert isinstance(conversation, RemoteConversation)

    conversation.set_security_analyzer(security_analyzer)
    conversation.set_confirmation_policy(ConfirmRisky(threshold=SecurityRisk.MEDIUM))

    try:
        t0 = time.time()
        conversation.send_message(prompt)
        status = run_with_confirmations(
            conversation,
            security_analyzer,
            interactive=args.interactive,
        )
        wall = time.time() - t0

        cost = conversation.conversation_stats.get_combined_metrics().accumulated_cost
        print(f"\nprompt: {prompt_key} -> {prompt}")
        print(f"docker: {args.docker}")
        print(f"status: {status}")
        print(f"wall: {wall:.1f}s  cost: ${cost:.4f}")
    finally:
        conversation.close()


if __name__ == "__main__":
    main()
