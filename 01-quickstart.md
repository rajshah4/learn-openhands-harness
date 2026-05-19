# 1: Quickstart

The fastest path from zero to "I can see the harness running." We'll start the agent server and the canvas with the explicit no-Docker dev command, send a message, and prove the loop is alive.

This quickstart is intentionally dockerless so you can inspect the local process
and API directly. Use it only for the tutorial, disposable scratch work, and
trusted read-only exploration. For real repositories or any task that may edit
files, install packages, run tests, or browse the web, use Docker; local mode is
too easy to aim at the wrong directory and damage your machine or working tree.

If anything in this section fails, fix it before continuing. The rest of the tutorial assumes you have a working setup.

---

## 1.1 Install prerequisites

```bash
# Node 22.12+
node --version   # → v22.12.x or higher

# uv (used by the canvas to run uvx-spawned backends)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version

# Model credentials. Only LLM_API_KEY is required by the SDK scripts.
cp .env.example .env
# Edit .env and set LLM_API_KEY to a provider key.
set -a
source .env
set +a
```

The examples default to `anthropic/claude-sonnet-4-5-20250929` (Sonnet 4.5).
Override `LLM_MODEL` only if you want a different LiteLLM provider/model string.
Keep real keys in `.env`, not in prompts, docs, or commits.

Docker is not required for this dockerless quickstart, but it is required
starting in P06 when the tutorial moves into sandboxed workspaces.

The canvas dev script will install Python dependencies into uvx-managed envs on first run. You don't manage those envs yourself.

> **Optional: pin SDK versions for reproducible traces.** The project scripts use `uv run --with openhands-sdk --with openhands-tools`, which resolves the latest published versions on each run. Trace event counts and metric shapes can drift between re-runs if the SDK changes. To pin, compile a hash-locked file once:
>
> ```bash
> printf 'openhands-sdk\nopenhands-tools\nopenhands-workspace\n' \
>     | uv pip compile - --generate-hashes -o pinned-requirements.txt
> ```
>
> Then run project scripts with `--with-requirements` in place of the inline `--with` arguments:
>
> ```bash
> uv run --with-requirements pinned-requirements.txt \
>     python projects/p01-agent-trace/starter/run_baseline.py
> ```
>
> The script files are unchanged; only the command you type changes. Note: `uv pip install -r requirements.txt` does **not** help here, because `uv run --with` ignores the active virtualenv and resolves dependencies fresh each call. The pin has to live on the `uv run` command itself. Keep this path only if you want comparable traces across re-runs.

---

## 1.2 Clone and start the canvas

This command is named `dangerously-dockerless` for a reason. Keep the first run
small and reversible. A good target is a scratch clone or the tiny default
workspace created by the canvas. Do not point it at your main work repo until
you have moved to the Docker path in the tour.

```bash
git clone https://github.com/OpenHands/agent-canvas.git
cd agent-canvas
npm install
npm run dev:dangerously-dockerless
```

Do not substitute `npm run dev` unless you know which mode your checkout uses.
Recent Agent Canvas builds may start a Dockerized agent server from `npm run dev`
or `npm run dev:docker`. In that mode, the server usually sees your project
root at `/projects`, not at your host path such as `/Users/you/Code`. The SDK
scripts in this repo can map host paths for you when these are set:

```bash
export AGENT_WORKSPACE_HOST_ROOT=/path/to/your/projects
export AGENT_WORKSPACE_SERVER_ROOT=/projects
```

What this actually does, from `DEVELOPMENT.md`:

- Spawns an agent-server subprocess via `uvx` on `127.0.0.1:18000`.
- Spawns the automation backend via `uvx` on `127.0.0.1:18001`.
- Starts a Vite dev server on `http://localhost:3001`.
- Starts an ingress proxy on `http://localhost:8000`; this is the URL you open.
- Writes isolated state under `~/.openhands/agent-canvas/` (session key, conversation persistence, workspaces, bash event log, tmux sockets). This means it won't fight the default OpenHands desktop/cloud-backed state, but repeated Agent Canvas dev runs will share this local state.

You should see logs from the agent server, automation backend, Vite, and ingress interleaved. Wait until the launcher prints `Ready at http://localhost:18000/server_info` and then `Main UI: http://localhost:8000/`. Then open `http://localhost:8000` in a browser.

> **Filesystem warning, repeated.** This setup runs the agent server directly on your machine. The agent has full bash, file-edit, and (optionally) browser tools against your real filesystem. Dockerless mode is for learning only; use a Docker sandbox before real work.

---

## 1.3 Confirm the harness is alive (without the UI)

Before you trust the canvas, hit the agent server's HTTP API directly. This is the same surface the canvas uses; if it works here, the canvas can't be lying to you.

```bash
# Health check: no auth needed by default
if command -v jq >/dev/null 2>&1; then
  curl -fsS http://127.0.0.1:18000/health | jq .
else
  curl -fsS http://127.0.0.1:18000/health
fi

# Expected response (shape may evolve):
# {
#   "status": "ok"
# }
```

You can also run `scripts/health.sh`, which uses the same fallback when `jq`
is not installed.

If you get a connection refused, the server isn't up yet. Wait, then try again. `/health`, `/ready`, and `/server_info` are public server-detail endpoints. Most `/api/*` routes are authenticated because the dev script generates or reuses a session key. For direct API calls, send `X-Session-API-Key` with the value from `~/.openhands/agent-canvas/session-api-key.txt`, or export `SESSION_API_KEY` / `VITE_SESSION_API_KEY` yourself before starting the stack.

The interesting endpoints, all documented in the [agent-server architecture page](https://docs.openhands.dev/sdk/arch/agent-server):

```text
POST   /api/conversations                         Create a conversation
POST   /api/conversations/{id}/events             Send a user message
POST   /api/conversations/{id}/run                Run or resume the loop
GET    /api/conversations/{id}/events/search      Read persisted events
GET    /sockets/events/{id}                       WebSocket for live events
GET    /server_info                               Server version, uptime, and usable tools
```

This is your harness. It's a REST/WS API and a workspace abstraction. The model has not entered the picture yet.

One subtle but important distinction: `/server_info` lists every tool the server knows how to run. A conversation stores the smaller tool list its agent is actually allowed to use. We'll inspect that distinction in the harness tour.

---

## 1.4 Send your first message through the canvas

In the browser:

1. Open `http://localhost:8000`.
2. Create a new conversation. If this is your first run, set the provider API key and model in the canvas LLM settings first: open **Settings → LLM** in the sidebar, or go directly to `http://localhost:8000/settings`.
3. Type something narrow and verifiable. A good first prompt is:

   > Read the current repo and write three facts about it into `FACTS.txt`.

4. Watch the agent trace as it runs.

You'll see the canvas render a sequence of typed events: tool calls such as `terminal`, `file_editor`, and `task_tracker`, tool returns, model deltas, and a final message. In this tutorial, we'll call that sequence the **agent trace**. Each row is one event from the [`Event`](https://docs.openhands.dev/sdk/arch/events) framework. Save this trace; we'll come back to it in the harness tour.

If `FACTS.txt` shows up in the workspace directory the canvas chose, usually under `~/.openhands/agent-canvas/workspaces/`, you have a working harness end-to-end.

---

## 1.5 Send the same message via SDK (optional but recommended)

The canvas is one client. The Python SDK is another. Running the same task through both, against the same server, makes it obvious that the *harness* is the server, not either client.

Use the checked-in helper at [`scripts/quickstart.py`](./scripts/quickstart.py).
That file is the source of truth for the SDK version of this quickstart; inspect
it if you want to see the `LLM`, `Workspace`, `Conversation`, and
`get_default_agent()` wiring.

```bash
uv run --with openhands-sdk --with openhands-tools python scripts/quickstart.py
```

Set `WORKSPACE_DIR=/path/to/repo` if you want the SDK run to inspect a repo other
than the current directory. If your agent server is Dockerized, use the
host/server path mapping from §1.2.

If this exits with `Missing required environment variable: LLM_API_KEY`, the server is fine; the SDK client just doesn't have model credentials in your shell. Source `.env`, export `LLM_API_KEY`, or use the canvas LLM settings path from §1.4.

You should now have *two* conversations on the same agent server: one started from the canvas, one from Python. They share workspace state (subject to `working_dir`) and event persistence. Open the canvas; you can see the SDK-created conversation in the sidebar. That's not a coincidence. Both clients write through the same `/api/conversations` endpoint.

---

## 1.6 Sanity checklist

Before moving on, confirm all of these are true:

- [ ] `curl http://127.0.0.1:18000/health` returns `"status": "ok"`.
- [ ] The canvas at `http://localhost:8000` shows your test conversation.
- [ ] `FACTS.txt` exists in the working directory the canvas chose.
- [ ] You've eyeballed the agent trace and recognize at least: a user message, a `terminal` or `file_editor` tool call, the matching observation, and an agent message.
- [ ] You ran the SDK script *and* the canvas conversation against the same server, and both show up.

If any of the above is false, fix it now. Common failures and fixes:

| Symptom | Likely cause | Fix |
|---|---|---|
| `node: command not found` | Wrong Node version | `nvm install 22.12 && nvm use 22.12` |
| `uvx: command not found` | `uv` not on `PATH` | Re-source your shell, or `~/.local/bin/uvx --version` |
| Server exits immediately, no health endpoint | `uvx` install/start failure or a busy port | Re-read the launcher error; rerun after freeing the port or fixing `uvx` |
| `500 Internal Server Error` when creating a conversation, with a host path like `/Users/...` or `/private/var/...` in the stack trace | Dockerized agent server cannot see the host path passed as `working_dir` | Set `AGENT_WORKSPACE_HOST_ROOT` + `AGENT_WORKSPACE_SERVER_ROOT`, or set `WORKSPACE_DIR` to the server path such as `/projects/agent-canvas` |
| `500 Internal Server Error` with `tmux` / `File name too long` | macOS temp path made the tmux socket path too long | Restart the server with a short tmux temp dir: `mkdir -p /private/tmp/oh-tmux && TMUX_TMPDIR=/private/tmp/oh-tmux npm run dev:dangerously-dockerless` |
| `401 Unauthorized` from `/api/*` | Dev server generated a session API key | Send `X-Session-API-Key: $(cat ~/.openhands/agent-canvas/session-api-key.txt)` or pin `SESSION_API_KEY` / `VITE_SESSION_API_KEY` before restart |
| Canvas blank, console errors about CORS | Frontend pointing at wrong backend | In the full dockerless stack, `VITE_BACKEND_HOST` should point at the ingress port (`127.0.0.1:8000` by default). In frontend-only mode, point it at your existing backend. |
| Canvas can't connect, port 8000 in use | Some other dev server | Set `PORT=8123 npm run dev:dangerously-dockerless` |

Once the checklist passes, move on to [`02-harness-tour.md`](./02-harness-tour.md).
