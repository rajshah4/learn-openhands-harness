"""
Send the canonical 'three facts' task through the agent server that
agent-canvas spun up via `npm run dev`.
Mirrors 01-quickstart.md §1.5.

Run with:

    uv run --with openhands-sdk --with openhands-tools \
        python quickstart.py

Required environment variables:
    LLM_API_KEY  Your provider key (Anthropic, OpenAI, etc.)

Optional:
    LLM_MODEL            LiteLLM-style provider/model string
                         (default anthropic/claude-sonnet-4-5-20250929)
    AGENT_SERVER          Default http://127.0.0.1:18000
    AGENT_SERVER_API_KEY  API key for authenticated dev servers
                         (defaults to ~/.openhands/agent-canvas/api-key.txt)
    WORKSPACE_DIR         Repo/workspace to give the agent (default: cwd)
"""

import os
import sys
from pathlib import Path

PROJECTS_DIR = Path(__file__).resolve().parents[1] / "projects"
if str(PROJECTS_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECTS_DIR))

from _runtime import resolve_server_working_dir

DEFAULT_MODEL = "anthropic/claude-sonnet-4-5-20250929"


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value

    print(
        f"Missing required environment variable: {name}\n\n"
        "Before running this script, set your model provider key, for example:\n"
        "  export LLM_API_KEY='sk-...'\n"
        f"\nOptional model override:\n"
        f"  export LLM_MODEL='{DEFAULT_MODEL}'\n",
        file=sys.stderr,
    )
    raise SystemExit(2)


def resolve_working_dir() -> str:
    return resolve_server_working_dir()


def resolve_agent_server_api_key() -> str | None:
    configured = os.environ.get("AGENT_SERVER_API_KEY")
    if configured:
        return configured

    key_dir = Path.home() / ".openhands" / "agent-canvas"
    for key_path in (
        key_dir / "api-key.txt",
        key_dir / "session-api-key.txt",  # Older Agent Canvas dev builds.
    ):
        if key_path.exists():
            return key_path.read_text().strip()

    return None


def main() -> None:
    api_key = require_env("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL", DEFAULT_MODEL)
    server = os.environ.get("AGENT_SERVER", "http://127.0.0.1:18000")
    agent_server_api_key = resolve_agent_server_api_key()

    from pydantic import SecretStr
    from openhands.sdk import LLM, Conversation, RemoteConversation, Workspace
    from openhands.tools.preset.default import get_default_agent

    llm = LLM(usage_id="agent", model=model, api_key=SecretStr(api_key))
    agent = get_default_agent(llm=llm, cli_mode=True)

    workspace = Workspace(
        host=server,
        api_key=agent_server_api_key,
        working_dir=resolve_working_dir(),
    )

    conversation = Conversation(agent=agent, workspace=workspace)
    assert isinstance(conversation, RemoteConversation)

    try:
        conversation.send_message(
            "Read the current repo and write 3 facts about it into FACTS.txt."
        )
        conversation.run()

        events = len(conversation.state.events)
        cost = conversation.conversation_stats.get_combined_metrics().accumulated_cost
        print(f"events: {events}")
        print(f"cost  : {cost}")
    finally:
        conversation.close()


if __name__ == "__main__":
    main()
