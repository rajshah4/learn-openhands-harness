# Exercise 4: Use the Strongest Model for Everything?

The safest model policy appears to be simple: use the strongest model with high
reasoning for every task. This exercise tests whether a router can preserve the
verified result while spending less time and money.

Routing only works when the harness can recognize failure. A cheap model that
returns a plausible wrong answer is not a saving.

## Route Four Tasks

Choose an initial model tier, reasoning level, verifier, and escalation signal
for each task.

| Task | Initial model | Reasoning | Verifier | Escalate when |
|---|---|---|---|---|
| Rename one symbol in one file | | | | |
| Repair a pagination boundary | | | | |
| Debug an async race | | | | |
| Review authentication middleware | | | | |

Discuss one disagreement with a neighbor. A task can deserve a stronger model
because it is difficult, because mistakes are costly, or because correctness
is hard to verify. Those are different reasons.

## Compare Three Policies

The instructor will reveal results for:

1. Strongest model and high reasoning for every task
2. One economical model for every task
3. Economical first, followed by verification and evidence-based escalation

Predict which policy has the lowest cost per verified result. Also predict the
task where cheap-first is most likely to fail silently.

| Policy | Verified tasks | Escalations | Missed failures | Wall time | Provider cost |
|---|---:|---:|---:|---:|---:|
| Strongest for all | | | | | |
| Economical for all | | | | | |
| Verify and route | | | | | |

## Inspect the Routing Decision

For one escalated task, find:

1. The evidence available before escalation
2. The reason the first attempt was rejected
3. What changed in the second attempt
4. Whether the stronger model fixed the problem
5. Whether a different harness change would have been cheaper

## Write a Routing Policy

```text
Start with an economical model when:

Start with the strongest model when:

Increase reasoning when:

Switch models when:

Stop rather than escalate when:

No result ships unless:
```
