# Start Here

This course is a guided lab. The goal is to change how you think, not just run through the exercises. Do not use an agent to quickly solve every problem. At most, guide the agent to code your ideas. Even then, look carefully at the results and try different combinations. You want a deep understanding of each of these problems.

## The Four Entry Points

If you are new to harness engineering, start with the concept path. If you already know the framing, go straight to the OpenHands lab.

| Path | Use it when | Start |
|---|---|---|
| Concept | You want the thesis before touching code | [Concepts](/concepts/) |
| Video | You want the narrative walkthrough first | [Videos](/videos) |
| Lab | You want to run Agent Canvas and inspect traces | [Quickstart](/quickstart) |
| Reuse | You want copy-ready harness artifacts | [Library](/library/) |

## The Learning Loop

Every project follows the same loop:

1. Read the problem.
2. Open the starter files.
3. Predict what the trace should show.
4. Run one small experiment.
5. Inspect the trace.
6. Compare against the solution.
7. Keep the policy only if the evidence supports it.

## What You Need

- Node.js 22.12 or newer.
- `uv`.
- An LLM API key.
- Agent Canvas running locally.
- A scratch repo for live agent work.
- Docker by P06, when the course moves into sandboxed workspaces.

The full setup is in the [Quickstart](/quickstart). The runnable source is in the [GitHub repo](https://github.com/rajshah4/learn-openhands-harness).

## What You Will Build

By P07, you will have a runnable `harness.py` that combines model selection, tool policy, retrieval, memory, safety, sandboxing, and critic evaluation. P08, P09, and P10 are advanced extensions for dynamic workflows, measured model routing, and indexing agent history.
