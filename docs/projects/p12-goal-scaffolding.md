# P12: Goal Scaffolding

## What You Do

Take the official OpenHands `/goal` loop and work out what scaffolding a harness still needs before it should trust the goal as done. Run the SDK controller probe, then use a small SDK-free pre-landing fixture and deterministic probes to find where continuation stops being the same thing as verification. Then design the scaffold, including criteria, verifier, evidence, budget, and envelope, that makes completion harder to fake, using two slugify repos: a true-missing baseline and a false-premise adversarial case.

## Harness Mechanism

The landed SDK feature gives you `run_goal`, `GoalController`, `judge_goal`, `GoalContinue`, and `GoalOutcome(status="complete" | "capped")`. The scaffold adds what the judge-driven loop does not own by itself: completion criteria, system-owned verifier evidence, token budgets with hard stops, sensors and actuators, and an access envelope enforced before an action runs rather than in prose. Deterministic probes expose each gap, and the two slugify repos separate "the code was broken" from "the prompt asked for evidence that cannot honestly exist."

If you verify through Agent Canvas, check `/server_info` and `/openapi.json` first. On June 24, 2026, Agent Canvas `main` still pinned Agent Server 1.28.1, so the SDK goal loop could be available in `openhands-sdk==1.29.2` before it was exposed by the local Canvas API.

## Open First

- [`projects/p12-goal-scaffolding/README.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-scaffolding/README.md)
- [`probe_official_goal.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-scaffolding/probe_official_goal.py)
- [`starter/goal_scaffold.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-scaffolding/starter/goal_scaffold.py)
- [`starter/probe_goal_mvp.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p12-goal-scaffolding/starter/probe_goal_mvp.py)
- [`solution/`](https://github.com/rajshah4/learn-openhands-harness/tree/main/projects/p12-goal-scaffolding/solution)

## Keep

A defensible goal scaffold: what the goal is, what criteria define done, what verifier proves those criteria, what sensors feed the verifier, what actuators can change its world, what envelope limits those actuators, and which stop states the harness owns regardless of what the agent says.

The reusable artifact is not the goal loop. It is the habit of deciding up front what would prove an objective is done, and refusing to let the model's own narration be the proof.
