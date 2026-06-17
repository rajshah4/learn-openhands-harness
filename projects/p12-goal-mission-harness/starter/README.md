# Starter: P12 Goal And Mission Harness

## What You Are Building

You are starting from a working `/goal` MVP. Your job is not to make the agent try harder. Your job is to make completion more trustworthy.

The repo-local MVP fixture already has:

- a persistent objective,
- a continuation loop,
- an `update_goal` tool,
- token usage accounting,
- a completion prompt.

The missing part is the mission contract: criteria, verifier, sensors, actuators, envelope, and hard stop policy.

## Your Tasks

1. Read `goal_mvp/state.py`, `goal_mvp/controller.py`, `goal_mvp/tools.py`, and `goal_mvp/prompts.py`.
2. Run `python test_goal_mvp.py` from the project directory.
3. Fill in `goal_contract.py` so a one-line goal becomes a structured contract.
4. Fill in `probe_goal_mvp.py` with at least three probes:
   - complete after budget exceeded,
   - complete without verifier evidence,
   - goal state missing criteria/verifier/envelope fields.
5. Run your probes and compare them to `solution/probe_goal_mvp.py`.
6. Run one live slugify goal against `toy_repos/dot_missing` and one against `toy_repos/dot_present`.
7. Write the result table in the main README.

## Constraints

Keep the exercise small. Do not redesign the whole SDK before you can explain what the current MVP does. Make the smallest change that would move one responsibility from agent narration into harness-owned state or policy.

For the live slugify run, work on a scratch copy of the target repo and use only:

- `src/slugify.py`
- `tests/test_slugify.py`
- the pytest verifier command named in the goal prompt

If the agent needs anything else, record that as envelope pressure.

## Questions To Answer

- What did the agent claim as evidence?
- Which evidence was independently checkable?
- Did the budget limit stop work or just appear in the final report?
- Did the goal status represent why the run stopped?
- Could the same behavior be built as a skill, or did it require harness state?
- Where should the verifier run: inside the critic, outside the critic, or both?

Read `solution/README.md` only after you have your first result table.
