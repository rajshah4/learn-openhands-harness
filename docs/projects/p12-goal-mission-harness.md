# P12: Goal And Mission Harness

## What You Do

Take a working `/goal` loop — the persistent-objective feature now shipping in agents like Codex — and turn it into a mission harness that can prove completion instead of trusting it. Run a small in-repo goal MVP, probe it for the gaps where the agent's own story gets to decide "done," then compare two ways to close them: a caller-side goal loop and an SDK-native `GoalCritic`. Finally, convert a one-line goal into a structured mission contract: objective, criteria, verifier, sensors, actuators, budget, and envelope.

## Harness Mechanism

A persistent `GoalState` stored in conversation state, a continuation loop that re-arms the agent each turn, and an `update_goal` tool to mark `complete`, `blocked`, or `budget_limited`. The mission layer adds what the bare loop lacks: completion criteria, system-owned verifier evidence, token budgets with hard stops, sensors and actuators, and an access envelope enforced before an action runs rather than in prose. Deterministic probes (no LLM) expose each gap, and two tiny slugify repos supply a true-missing baseline plus a false-premise adversarial case.

## Open First

- [`projects/p12-goal-mission-harness/README.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-mission-harness/README.md)
- [`starter/goal_contract.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-mission-harness/starter/goal_contract.py)
- [`starter/probe_goal_mvp.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-mission-harness/starter/probe_goal_mvp.py)
- [`solution/`](https://github.com/rajshah4/learn-openhands-harness/tree/main/projects/p12-goal-mission-harness/solution)

## Keep

A three-layer view of the goal feature you can defend: a goal loop persists the objective and keeps the agent running; a goal critic audits finish attempts and continues the run; a mission layer owns criteria, verifier evidence, budgets, and envelope policy.

The reusable artifact is not the goal loop. It is the habit of deciding up front what would prove an objective is done — and refusing to let the model's own narration be the proof.
