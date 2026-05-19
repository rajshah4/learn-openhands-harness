# P01: Canvas + Agent Trace

| | |
|---|---|
| **What You Do** | Run one narrow task through the canvas, then read the agent trace. Count tool calls, inspect observations, and save the trace as your baseline. |
| **Harness Mechanism** | Agent Server typed events + persisted conversation events + Canvas trace viewer |

**Phase: SEE THE LOOP.** Before changing any knobs, learn to read the loop. The differentiator here is not that the agent can call tools. Claude Code, Cursor, and OpenHands can all do that. The differentiator is that the harness trace is visible, queryable, forkable, and reusable as evaluation data.

## Directory guide

| Directory | What's inside |
|---|---|
| `starter/` | `run_baseline.py` runs the prompt and prints raw event count + cost. The minimum viable SDK run. |
| `solution/` | `run_baseline.py`, same script, extended to print a structured trace summary. Plus `trace_checklist.md`, the trace-reading checklist to keep. |

## Agent-assisted path

1. Open this `README.md` and `starter/` only.
2. Ask your coding agent to complete the TODOs without reading `solution/`.
3. Require it to run the smoke check or live command below and report the result.
4. Compare against `solution/` only after your starter works, then note what differed.

## Before you run

Pause and predict:

- Which tools do you expect to see in the trace: `terminal`, `file_editor`, or both?
- What should the first useful retrieval step be for `VITE_BACKEND_HOST`?
- Will the note be written by a file-editor action or by a terminal command/script?
- What would make the final answer ungrounded?

## Setup

- Same repo and same prompt for the rest of the projects.
- Use the default canvas setup from the [quickstart](../../01-quickstart.md).
- Set `WORKSPACE_DIR=/path/to/that/repo` before running the SDK scripts.
- If your Agent Canvas server is Dockerized, either set
  `WORKSPACE_DIR=/projects/agent-canvas` or set
  `AGENT_WORKSPACE_HOST_ROOT=/path/to/your/projects` and
  `AGENT_WORKSPACE_SERVER_ROOT=/projects` so host paths map correctly.
- Good default prompt: `"Find every place VITE_BACKEND_HOST is read or set, and write a short note explaining how the dev script picks the backend."`

## Procedure

1. Start a fresh conversation in the canvas and run the prompt to completion.
2. Open the agent trace. Identify: user message, assistant planning, each tool call, each observation, final answer, and any compaction placeholder.
3. Save the agent trace from the canvas UI if export is available in your build, or from the API:

   ```bash
   mkdir -p .openhands-runs/traces
   export CONVERSATION_ID=<id-from-the-canvas-url-or-sidebar>
   curl -sS \
     -H "X-Session-API-Key: $(cat ~/.openhands/agent-canvas/session-api-key.txt)" \
     "http://127.0.0.1:18000/api/conversations/$CONVERSATION_ID/events/search" \
     > .openhands-runs/traces/p01-baseline-events.json
   ```

   OpenHands stores the trace as typed events; "agent trace" is the teaching term.
4. Record the working directory, repo SHA, model, active tool list, number of tool calls, wall-clock time, cost, and whether the final answer cited real files.
5. Run `starter/run_baseline.py` to repeat the same task via the SDK. Compare your SDK trace to the canvas trace. They should match.

## What to write down

| Trace field | Value |
|---|---|
| Repo + SHA | |
| Prompt | |
| Model | |
| Active tools | |
| Tool calls by type | |
| Files read | |
| Files edited | |
| Compaction fired? | |
| Final answer correct? | |

## What to look for

- The agent trace is the unit of diagnosis. If the final answer is wrong, find the first bad observation or skipped retrieval step.
- A healthy code-reading run has a small number of targeted searches and file reads before answering.
- A harness you cannot inspect cannot be tuned. This baseline trace is what makes the later ablations meaningful.

## What you keep

One baseline agent trace plus a trace-reading checklist (see `solution/trace_checklist.md`). Every later project compares against this trace, not against vibes.

→ Next: [P02: Model Routing](../p02-model-routing/)
