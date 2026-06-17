# P01: Canvas + Agent Trace

## What Problem Are You Solving?

Every coding agent runs the same loop: the model plans, calls a tool, reads the observation, and decides what to do next. You cannot tune a harness you cannot see, so before touching any lever, you learn to read that loop from its trace.

The differentiator is not that the agent calls tools. Claude Code, Cursor, and OpenHands all do that. It is that the OpenHands harness trace is visible, queryable, forkable, and reusable as evaluation data. In this lesson you:

1. Run one narrow task through Agent Canvas and watch the loop happen.
2. Open the agent trace and account for every event: the user message, the planning, each tool call, each observation, the final answer.
3. Save that trace as the baseline every later project compares against.

This is the reference point for the whole course. Skip it and every later ablation compares against vibes instead of evidence.

## Start With These Files

Open this README and `starter/` only. Ask your coding agent to complete the TODOs without reading `solution/`, run the command below, then compare against `solution/` and read `solution/README.md` for the brief.

| Purpose | Starter | Solution |
|---|---|---|
| Run the task via the SDK | `starter/run_baseline.py` (event count + cost) | `solution/run_baseline.py` (adds a structured trace summary) |
| The artifact to keep | | `solution/trace_checklist.md` |

This is P01, so nothing feeds into it. Its output, one saved baseline trace and a reading checklist, is the foundation the rest of the course builds on.

## The Task

Use the default canvas setup from the [quickstart](../../01-quickstart.md), with the same repo and prompt you will reuse for the rest of the projects.

> Find every place VITE_BACKEND_HOST and VITE_BACKEND_BASE_URL are read or set, and write a short note explaining how the dev script picks the backend.

Before you run it, predict the trace. Which tools do you expect, `terminal`, `file_editor`, or both? What is the first useful retrieval step for `VITE_BACKEND_HOST`? Will the note be written by a file-editor action or a terminal command? What would make the final answer ungrounded? Writing these down first turns the trace from a wall of events into a set of confirmed or broken predictions.

## Run It And Read The Trace

Set the workspace:

```bash
export WORKSPACE_DIR=/path/to/that/repo
```

If your Agent Canvas server is Dockerized, either set `WORKSPACE_DIR=/projects/agent-canvas`, or set `AGENT_WORKSPACE_HOST_ROOT=/path/to/your/projects` and `AGENT_WORKSPACE_SERVER_ROOT=/projects` so host paths map correctly.

1. Start a fresh conversation in the canvas and run the prompt to completion.
2. Open the agent trace. Identify the user message, assistant planning, each tool call, each observation, the final answer, and any compaction placeholder.
3. Save the trace, from the canvas UI if export exists in your build, or from the API:

   ```bash
   mkdir -p .openhands-runs/traces
   export CONVERSATION_ID=<id-from-the-canvas-url-or-sidebar>
   curl -sS \
     -H "X-Session-API-Key: $(cat ~/.openhands/agent-canvas/api-key.txt)" \
     "http://127.0.0.1:18000/api/conversations/$CONVERSATION_ID/events/search" \
     > .openhands-runs/traces/p01-baseline-events.json
   ```

   OpenHands stores the trace as typed events. "Agent trace" is the teaching term.
4. Run the same task through the SDK and confirm the two traces match:

   ```bash
   uv run --with openhands-sdk --with openhands-tools python starter/run_baseline.py
   ```

## Record The Results

Fill this in from your run. It is the baseline every later project compares against.

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

## Why The Trace Is The Unit Of Work

- The trace is the unit of diagnosis. If the final answer is wrong, find the first bad observation or the retrieval step that was skipped.
- A healthy code-reading run has a small number of targeted searches and file reads before it answers. A long wandering trace is a signal, not noise.
- A harness you cannot inspect cannot be tuned. This baseline trace is what makes every later ablation measurable instead of anecdotal.

## What Students Should Leave With

One saved baseline agent trace plus a trace-reading checklist (`solution/trace_checklist.md`). Every later project compares against this trace, not against vibes.

Next: [P02: Model Routing](../p02-model-routing/)
