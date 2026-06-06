# Solution Brief: P05 Memory And Compaction

## What This Solution Proves

This solution proves that memory is valuable only when it reduces rediscovery. A durable `AGENTS.md` should help the agent start in the right part of the repo faster. If it merely adds generic instructions to every prompt, it is harness bloat.

The reference solution compares the same task with and without a short, hand-written `AGENTS.md`, saves trace JSON for both runs, and provides a comparison script so the learner can inspect event, token, discovery, and compaction differences.

## Start With These Files

| File | Why it matters |
|---|---|
| `AGENTS.md` | The sample durable memory artifact for `agent-canvas`. |
| `run_memory.py` | Copies the workspace, runs no-memory and with-memory configs, and saves trace JSON. |
| `compare_traces.py` | Compares saved traces without making new model calls. |
| `condenser_notes.md` | The policy note to fill in after inspecting memory and compaction behavior. |

Read `AGENTS.md` first. It is intentionally short. The solution is teaching what to remember, not how to write a long instruction file.

## Key Design Choices

The solution uses a hand-written `AGENTS.md` with repo-specific facts:

- what the repo is
- where source and scripts live
- which docs are canonical
- which environment variables and ports matter
- where local state lives

It does not ask the agent to generate its own memory as the default. Auto-generated memory can encode stale, vague, or overconfident context. The course treats it as an optional comparison, not the baseline.

The runner copies the workspace before each run. The no-memory copy removes root `AGENTS.md`; the with-memory copy receives the sample file. That keeps the original repo untouched and makes the comparison easier to reason about.

## How OpenHands Fits In

OpenHands reads repo memory from `AGENTS.md` when it is present in the workspace. The harness does not need a custom memory database for this first experiment. It needs a durable file that the agent sees at the right time.

Compaction is the second part of the lesson. If compaction fires, the trace should show what summary was kept. The open harness lets the learner audit that compression instead of trusting it blindly.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Did memory reduce rediscovery? | Compare discovery events such as `ls`, `find`, README reads, and directory probing. |
| Did memory reduce cost? | Compare input tokens, events, and wall-clock time. |
| Did correctness stay stable? | A faster wrong answer is not an improvement. |
| Did compaction preserve the right facts? | Inspect compaction or condenser events if they appear. |

The comparison script gives a proxy. The raw trace is still the final evidence.

## Valid Variations

A valid `AGENTS.md` for another repo will look different. It might mention build commands, generated folders, testing conventions, or package-manager rules. It should remain short enough that every line earns its token cost.

A valid solution might also conclude that no durable memory is needed for a tiny repo or a one-off task. P05 is not "always add memory." It is "keep memory only when trace evidence shows it helps."

## What To Keep

Keep:

- a hand-written `AGENTS.md` for the repo
- the no-memory vs. with-memory trace comparison
- notes on whether compaction fired and what it preserved
- a decision about whether any skill or extra memory artifact earned its place

The capstone should inherit memory as a stable repo convention, not as ad hoc chat history.
