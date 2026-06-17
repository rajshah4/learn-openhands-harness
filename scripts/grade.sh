#!/usr/bin/env bash
# Run a tutorial project end-to-end against the agent-canvas Docker server.
#
# Usage:
#   scripts/grade.sh ping                            quick PONG verify
#   scripts/grade.sh p01                             baseline trace
#   scripts/grade.sh p02                             flagship + small + routed
#   scripts/grade.sh p03                             lexical-exact + synonym
#   scripts/grade.sh p04 monolith|decomposed|both    repo-review comparison
#   scripts/grade.sh p05                             no-memory vs AGENTS.md
#   scripts/grade.sh p06 read|edit|network|delete    safety prompts
#   scripts/grade.sh p07 "your task"                 capstone (needs Docker)
#   scripts/grade.sh p08 manual|dynamic|both ["question"] dynamic workflow comparison
#
# Variant flag: append --starter to run the starter instead of the solution.
#   scripts/grade.sh p02 --starter
#
# Required env (from .env, see .env.example):
#   LLM_API_KEY                  provider key (Anthropic / OpenAI / ...)
# Optional:
#   LLM_MODEL                    default anthropic/claude-sonnet-4-5-20250929
#   LLM_MODEL_SMALL              default anthropic/claude-haiku-4-5-20251001
#   AGENT_WORKSPACE_HOST_ROOT    host path the canvas server bind-mounts
#   AGENT_WORKSPACE_SERVER_ROOT  container path it's mounted at (default /projects)
#   AGENT_CANVAS_DIR             host path to your agent-canvas clone
#                                (default /Users/$USER/Code/agent-canvas)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Load .env without overriding values already in the environment.
if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

: "${AGENT_WORKSPACE_HOST_ROOT:=/Users/${USER}/Code}"
: "${AGENT_WORKSPACE_SERVER_ROOT:=/projects}"
: "${AGENT_CANVAS_DIR:=/Users/${USER}/Code/agent-canvas}"

# Container-visible equivalents for the agent-canvas Docker server.
canvas_server_path="${AGENT_WORKSPACE_SERVER_ROOT}/$(basename "$AGENT_CANVAS_DIR")"

export AGENT_WORKSPACE_HOST_ROOT AGENT_WORKSPACE_SERVER_ROOT

if [[ -z "${LLM_API_KEY:-}" && "${1:-}" != "help" ]]; then
  echo "LLM_API_KEY is not set. Add it to .env or export it." >&2
  exit 2
fi

UV=(uv run --with openhands-sdk --with openhands-tools)

# Some projects (P06 --docker, P07) also need openhands-workspace.
UV_WITH_WORKSPACE=(uv run --with openhands-sdk --with openhands-tools --with openhands-workspace)

usage() { sed -n '2,20p' "${BASH_SOURCE[0]}"; }

# Resolve starter|solution.
variant="solution"
new_args=()
for arg in "$@"; do
  case "$arg" in
    --starter) variant="starter" ;;
    --solution) variant="solution" ;;
    *) new_args+=("$arg") ;;
  esac
done
set -- "${new_args[@]:-}"

project="${1:-help}"
shift || true

case "$project" in
  help|"")
    usage; exit 0 ;;

  ping)
    "${UV[@]}" python - <<'PY'
import os
from pathlib import Path
from pydantic import SecretStr
from openhands.sdk import LLM, Conversation, RemoteConversation, Workspace
from openhands.tools.preset.default import get_default_agent

_canvas_dir = Path.home() / ".openhands" / "agent-canvas"
api_key = os.environ.get("AGENT_SERVER_API_KEY")
for _name in ("api-key.txt", "session-api-key.txt"):  # newer build, then older
    if api_key:
        break
    _key_path = _canvas_dir / _name
    if _key_path.exists():
        api_key = _key_path.read_text().strip()
llm = LLM(usage_id="agent", model=os.environ["LLM_MODEL"], api_key=SecretStr(os.environ["LLM_API_KEY"]))
agent = get_default_agent(llm=llm, cli_mode=True)
ws = Workspace(host="http://127.0.0.1:18000", api_key=api_key,
               working_dir=f"{os.environ['AGENT_WORKSPACE_SERVER_ROOT']}/agent-canvas")
c = Conversation(agent=agent, workspace=ws)
assert isinstance(c, RemoteConversation)
try:
    c.send_message("Reply with exactly: PONG. Do not call any tools.")
    c.run()
    print(f"events: {len(c.state.events)}  cost: {c.conversation_stats.get_combined_metrics().accumulated_cost}")
finally:
    c.close()
PY
    ;;

  p01)
    WORKSPACE_DIR="$canvas_server_path" "${UV[@]}" \
      python "projects/p01-agent-trace/${variant}/run_baseline.py"
    ;;

  p02)
    WORKSPACE_DIR="$canvas_server_path" "${UV[@]}" \
      python "projects/p02-model-routing/${variant}/run_routing.py"
    ;;

  p03)
    WORKSPACE_DIR="$canvas_server_path" "${UV[@]}" \
      python "projects/p03-retrieval/${variant}/run_retrieval.py" "$@"
    ;;

  p04)
    mode="${1:-both}"
    : "${P04_MAX_ITERATIONS:=60}"
    export P04_MAX_ITERATIONS
    WORKSPACE_DIR="$REPO_ROOT" "${UV[@]}" \
      python "projects/p04-decomposition/${variant}/run_decomposition.py" --mode "$mode"
    ;;

  p05)
    WORKSPACE_DIR="$AGENT_CANVAS_DIR" "${UV[@]}" \
      python "projects/p05-memory/${variant}/run_memory.py"
    ;;

  p06)
    prompt="${1:-read}"
    docker_flag=""
    if [[ "${2:-}" == "--docker" ]]; then
      docker_flag="--docker"
      WORKSPACE_DIR="$AGENT_CANVAS_DIR" "${UV_WITH_WORKSPACE[@]}" \
        python "projects/p06-safety/${variant}/run_safety.py" $docker_flag "$prompt"
    else
      WORKSPACE_DIR="$AGENT_CANVAS_DIR" "${UV[@]}" \
        python "projects/p06-safety/${variant}/run_safety.py" "$prompt"
    fi
    ;;

  p07)
    task="${1:-What does this repo do?}"
    WORKSPACE_DIR="${WORKSPACE_DIR:-$AGENT_CANVAS_DIR}" "${UV_WITH_WORKSPACE[@]}" \
      python "projects/p07-capstone/${variant}/harness.py" "$task"
    ;;

  p08)
    mode="${1:-manual}"
    if [[ "$mode" == "manual" || "$mode" == "dynamic" || "$mode" == "both" ]]; then
      question="${2:-What is changing about AI coding assistants for software teams?}"
    else
      question="$mode"
      mode="manual"
    fi
    if [[ "$variant" == "starter" || "$mode" == "manual" ]]; then
      WORKSPACE_DIR="$REPO_ROOT" "${UV[@]}" \
        python "projects/p08-dynamic-workflows/starter/run_dynamic_workflow.py" \
          "$question"
    elif [[ "$mode" == "both" ]]; then
      WORKSPACE_DIR="$REPO_ROOT" "${UV[@]}" \
        python "projects/p08-dynamic-workflows/starter/run_dynamic_workflow.py" \
          "$question"
      WORKSPACE_DIR="$REPO_ROOT" "${UV[@]}" \
        python "projects/p08-dynamic-workflows/solution/run_dynamic_workflow.py" \
          "$question"
    else
      WORKSPACE_DIR="$REPO_ROOT" "${UV[@]}" \
        python "projects/p08-dynamic-workflows/solution/run_dynamic_workflow.py" \
          "$question"
    fi
    ;;

  *)
    echo "Unknown project: $project" >&2
    usage
    exit 2 ;;
esac
