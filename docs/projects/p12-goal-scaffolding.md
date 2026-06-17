# P12: Goal Scaffolding

## What You Do

Take a basic `/goal` loop — the persistent-objective feature now shipping in agents like Codex — and work out what scaffolding a harness needs before it should trust the goal as done. Run a small SDK-free goal-loop fixture and a set of deterministic probes to find where continuation stops being the same thing as verification. Then design the scaffold — criteria, verifier, evidence, budget, envelope — that makes completion harder to fake, using two slugify repos: a true-missing baseline and a false-premise adversarial case.

## Harness Mechanism

A persistent `GoalState`, a continuation loop that re-arms the agent each turn, and an `update_goal` tool to mark `complete`, `blocked`, or `budget_limited`. The scaffold adds what the bare loop lacks: completion criteria, system-owned verifier evidence, token budgets with hard stops, sensors and actuators, and an access envelope enforced before an action runs rather than in prose. Deterministic probes (no LLM) expose each gap, and the two slugify repos separate "the code was broken" from "the prompt asked for evidence that cannot honestly exist."

## Open First

- [`projects/p12-goal-scaffolding/README.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-scaffolding/README.md)
- [`starter/goal_scaffold.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-scaffolding/starter/goal_scaffold.py)
- [`starter/probe_goal_mvp.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-scaffolding/starter/probe_goal_mvp.py)
- [`solution/`](https://github.com/rajshah4/learn-openhands-harness/tree/main/projects/p12-goal-scaffolding/solution)

## Keep

A defensible goal scaffold: what the goal is, what criteria define done, what verifier proves those criteria, what sensors feed the verifier, what actuators can change its world, what envelope limits those actuators, and which stop states the harness owns regardless of what the agent says.

The reusable artifact is not the goal loop. It is the habit of deciding up front what would prove an objective is done — and refusing to let the model's own narration be the proof.
