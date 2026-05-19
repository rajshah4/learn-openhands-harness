# P05: Memory + Compaction

| | |
|---|---|
| **What You Do** | Compare no durable memory vs. a minimal `AGENTS.md`, then inspect whether compaction appears in the agent trace and what it preserved. |
| **Harness Mechanism** | `AGENTS.md` injection + [Condenser](https://docs.openhands.dev/sdk/arch/condenser) policy |

**Phase: REDUCE RE-DISCOVERY.** Memory done well saves turns. Memory done badly adds tokens to every prompt for no benefit.

## Directory guide

| Directory | What's inside |
|---|---|
| `starter/` | `run_memory.py` runs against a repo with no `AGENTS.md` and no condenser config. TODOs for adding memory. |
| `solution/` | `run_memory.py` runs both configs and saves trace JSON. `compare_traces.py` compares saved traces. `AGENTS.md` is a sample for agent-canvas, and `condenser_notes.md` is the policy note to keep. |

## Agent-assisted path

1. Open this `README.md` and `starter/` only.
2. Ask your coding agent to complete the TODOs without reading `solution/`.
3. Require it to run the smoke check or live command below and report the result.
4. Compare against `solution/` only after your starter works, then note what differed.

## Before you run

Pause and predict:

- What repo facts should a minimal `AGENTS.md` contain?
- Which discovery steps should disappear when that memory is present?
- What token or event reduction would make the memory worth keeping?
- What would indicate the memory is generic noise instead of useful context?

## Setup

- Same model + tools + retrieval policy from P01-P04.
- Default target: your local `agent-canvas` checkout. The prompt and sample
  `AGENTS.md` are tuned for that repo:

  ```bash
  export WORKSPACE_DIR=/path/to/your/projects/agent-canvas
  ```

  You can use a different repo, but then replace the prompt and write an
  `AGENTS.md` that matches that repo. The script copies `WORKSPACE_DIR` before
  each run and removes root `AGENTS.md` only from the no-memory copy.
- Two configurations (and one optional):
  - **A: no `AGENTS.md`:** the scripts copy `WORKSPACE_DIR` to a temp directory and remove `AGENTS.md` there, so your original repo is not touched.
  - **B: minimal `AGENTS.md`:** three to five lines, hand-written, describing the directory layout and any non-obvious conventions. Don't auto-generate it.
  - **C (optional): auto-generated `AGENTS.md`:** let the agent write it itself in a previous conversation. Feed that one in.

## Procedure

1. Run the prompt against A. Record turns, tokens, correctness, and *what the agent re-discovered*: directory layout, where to look first, etc.
2. Add `AGENTS.md`, fresh conversation, same prompt. Compare.
3. (Optional) Run C. If the [ETH Zurich result](https://arxiv.org/abs/2510.02669) holds, C will be measurably worse than B.

From the solution directory:

```bash
WORKSPACE_DIR=/path/to/your/projects/agent-canvas \
uv run --with openhands-sdk --with openhands-tools python run_memory.py
```

The runner prints two trace paths, one for `no-memory` and one for
`with-memory`. Compare them without making new model calls:

```bash
uv run python compare_traces.py \
  no-memory=/path/to/no-memory-events.json \
  with-memory=/path/to/with-memory-events.json
```

## What to look for

- Useful `AGENTS.md` reduces re-discovery turns. Useless `AGENTS.md` (verbose, generic) just adds tokens to every prompt.
- This mirrors the [talk + slides](https://github.com/rajshah4/harness-engineering#presentation-materials) theme that useful repo memory reduces re-discovery work. Worth replicating on your own repo once.
- `compare_traces.py` reports event deltas, token deltas, and a likely
  re-discovery proxy. Treat the proxy as a starting point, then inspect the raw
  trace before claiming why the run improved.
- If compaction fires, inspect the synthetic summary event. A closed harness asks you to trust its memory compression; an open harness lets you audit what was kept and what was thrown away.

## Further Reading: Skills

Skills are the same experiment shape, but they are not part of the main P05
path. Once `AGENTS.md` is dialed in, you can evaluate one skill with the same
A/B rule: run without the skill, enable only that skill, rerun the same prompt,
and keep it only if the trace shows a measurable improvement. The pattern is
similar to [`rajshah4/evaluating-skills-tutorial`](https://github.com/rajshah4/evaluating-skills-tutorial);
SkillsBench reports that some skills reduce performance, so don't trust them by
default.

## What you keep

Your hand-written `AGENTS.md` (5-20 lines), the `compare_traces.py` result,
and a note on whether compaction fired and what it preserved. If you also run a
skill experiment later, keep only a skill that demonstrably moved the needle.
See `solution/` for examples.

-> Next: [P06: Org Safety Profile](../p06-safety/)
