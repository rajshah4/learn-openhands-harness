# Solution Brief: P01 Agent Trace

## What This Solution Proves

This solution proves that a harness run is something you can inspect, not just something you trust. The starter can launch the prompt and report raw totals. The solution adds the first reusable diagnostic layer: a structured summary of what happened in the agent trace.

That matters because every later project changes one harness lever. Without a baseline trace, model routing, retrieval, memory, safety, and critic results all collapse into subjective impressions. P01 gives you the comparison object.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_baseline.py` | Repeats the Canvas task through the SDK and prints event, cost, token, tool, file, and compaction fields. |
| `trace_checklist.md` | The artifact to keep. It turns a trace into a repeatable review process. |

Read `trace_checklist.md` first if you want the operator view. Read `run_baseline.py` first if you want to understand how the SDK exposes the same run that Canvas shows visually.

## Key Design Choices

The solution does not try to judge the final answer automatically. That is intentional. P01 is teaching trace reading, not grading. The learner still decides whether the final note is grounded, but the script makes the raw evidence visible enough to defend that judgment.

The script records:

- total events
- wall-clock time
- accumulated cost
- input and output tokens
- tool calls by type
- files read
- files edited
- whether compaction appears to have fired

Those fields are deliberately boring. They are the stable facts you can compare across later runs even when the agent's prose changes.

## How OpenHands Fits In

Agent Canvas and the SDK are two clients over the same Agent Server conversation model. Canvas is the teaching surface because the trace is easy to watch. The SDK is the measurement surface because the same events can be counted, summarized, and saved.

The solution uses `conversation.state.events` as the source of truth. That is the key habit: diagnose the typed trace before arguing about the final answer.

## What To Compare Against Your Attempt

Your solution can differ in formatting, but it should preserve the diagnostic intent:

| Question | What to check |
|---|---|
| Can you explain the run? | You can identify the user message, tool calls, observations, and final answer. |
| Can you count the run? | You print or record event count, tool calls, cost, and token usage. |
| Can you inspect grounding? | You can name which files the agent read before answering. |
| Can you reuse the artifact? | The trace checklist works for P02 and later projects without rewriting it. |

If your script prints a different table but helps you answer those questions, it is on the right track.

## Valid Variations

A valid P01 solution might save JSON instead of printing a console summary, group tool calls differently, or add more event fields such as assistant messages and observations. It might also use the Canvas API export directly instead of the SDK run.

The important boundary is that the solution should make the trace easier to inspect. It should not hide the trace behind a pass/fail label.

## What To Keep

Keep the baseline trace and the checklist. In later projects, compare against this baseline whenever you change a harness lever:

- Did the agent search less or more?
- Did it read better evidence?
- Did it edit files unexpectedly?
- Did cost move because the model changed, or because retrieval discipline changed?
- Did compaction appear, and did the run preserve the right facts?

P01 is successful when you can answer those questions from the trace rather than from memory.
