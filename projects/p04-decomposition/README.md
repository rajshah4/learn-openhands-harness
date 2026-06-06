# P04: Task Decomposition

| | |
|---|---|
| **What You Do** | Run one large review task as a single prompt, then run the same goal as a harness-managed sequence of smaller prompts. Compare correctness, cost, wall time, and failure modes. |
| **Harness Mechanism** | Task decomposition, aggregation, and "fail smaller" workflow design |

**Phase: BREAK DOWN THE WORK.** Some tasks are hard because the model is weak. Others are hard because the harness hands the model too much work at once. This project tests that distinction directly.

The inspiration is the Harvey LAB / "Trust Your Harness" pattern: hold the model mostly constant, change the wrapper, and measure whether smaller scoped calls produce better work than one long call.

## Directory guide

| Directory | What's inside |
|---|---|
| `starter/` | `run_decomposition.py` runs the monolithic task and leaves TODOs for the decomposed workflow. |
| `solution/` | `run_decomposition.py` runs monolithic and decomposed workflows on copied workspaces. `score_report.py` scores saved reports. `decomposition_plan.md` and `evaluation_rubric.md` are the artifacts to keep. |

## Agent-assisted path

1. Open this `README.md` and `starter/` only.
2. Ask your coding agent to complete the TODOs without reading `solution/`.
3. Require it to run the smoke check or live command below and report the result.
4. Compare against `solution/` only after your starter works, then read `solution/README.md` for the solution brief and note what differed.

## Before you run

Pause and predict:

- Which parts of the release-readiness task are independent enough to split?
- What rubric categories might the monolithic run miss?
- How much extra cost or wall time would decomposition need to justify itself?
- What aggregation failure would make the decomposed run worse?

## Setup

- Same model and retrieval policy from P01-P03.
- Same source repo for both configs.
- Use a scratch clone. The script copies the workspace before each run, but the agent still has filesystem tools.

Default target task:

> Review this repo for release readiness and produce `RELEASE_READINESS.md` covering docs accuracy, setup/test commands, secret handling, safety warnings, project structure, and concrete fixes.

Config A gives that full task to one agent run.

Config B runs scoped checks first, then asks a final summarizer to read those check files and produce the same `RELEASE_READINESS.md`.

## Procedure

From the solution directory:

```bash
WORKSPACE_DIR=/path/to/repo \
uv run --with openhands-sdk --with openhands-tools python run_decomposition.py --dry-run
```

Then run live, with the agent server from the quickstart already running:

```bash
WORKSPACE_DIR=/path/to/repo \
uv run --with openhands-sdk --with openhands-tools python run_decomposition.py
```

The default cap is `P04_MAX_ITERATIONS=60` per agent run. Earlier versions used
24, which can make the monolithic run die before producing a useful comparison
on a non-trivial repo.

If the monolithic run still hits the cap, the script writes
`MONOLITH_TRUNCATED.md` in the copied workspace and continues. Treat that as a
result: "the one-prompt version could not finish under this budget."

If your agent server is Dockerized with an Agent Canvas container image or an
older `dev:docker` workflow, the server sees your `PROJECT_PATH` mount at
`/projects`. Run the script from the same shell where `PROJECT_PATH` is set, or
pass the mapping explicitly:

```bash
AGENT_WORKSPACE_HOST_ROOT=/path/to/your/projects \
AGENT_WORKSPACE_SERVER_ROOT=/projects \
WORKSPACE_DIR=/path/to/your/projects/learn-openhands-harness \
uv run --with openhands-sdk --with openhands-tools python run_decomposition.py
```

To save budget while debugging:

```bash
uv run --with openhands-sdk --with openhands-tools python run_decomposition.py --mode decomposed
```

The script copies workspaces under `.openhands-runs/p04-decomposition/`, which
is ignored by git. If a decomposed run is interrupted after one or more scoped
reports have been written, resume from that copied workspace:

```bash
P04_MAX_ITERATIONS=30 \
uv run --with openhands-sdk --with openhands-tools python run_decomposition.py \
  --mode decomposed \
  --resume-dir .openhands-runs/p04-decomposition/p04_decomposed_xxxxxxxx/repo
```

The solution runner prints a rubric scorecard after live runs. To score saved
reports later without making model calls, run from the repo root:

```bash
uv run python projects/p04-decomposition/solution/score_report.py \
  --score-report monolith=.openhands-runs/p04-decomposition/p04_monolith_xxxxxxxx/repo/RELEASE_READINESS.md \
  --score-report decomposed=.openhands-runs/p04-decomposition/p04_decomposed_xxxxxxxx/repo/RELEASE_READINESS.md
```

## What to look for

- Did the monolithic run complete but miss expected blocker categories?
- Did the decomposed run improve rubric coverage or just produce more files?
- Did any scoped check fail without killing the whole review?
- Did the final aggregator preserve caveats and exact file paths from the scoped checks?
- Did the final report's declared issue counts match the issue tables?
- Was the extra cost worth the gain?

This is not automatically better. Decomposition can lose cross-context information and increase spend. The point is to make the tradeoff measurable.

## What you keep

A decomposition rule of thumb. Example:

> Break a task into scoped runs when it has independent review dimensions, a clear aggregation format, and failures that can be retried independently. Keep it monolithic when the subparts require tight shared context.

Save your version in `solution/decomposition_plan.md`. You will use the same judgment again in P07 when deciding whether to add a critic or subagent.

-> Next: [P05: Memory + Compaction](../p05-memory/)
