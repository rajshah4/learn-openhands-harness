# Solution Brief: P12 Goal Scaffolding

## What This Solution Shows

The official OpenHands SDK now proves that `/goal` is not mysterious. `run_goal` sends an objective, runs the agent, asks a separate judge LLM whether the transcript proves completion, and either sends a follow-up or returns `GoalOutcome(status="complete" | "capped")`.

The repo-local caller-side MVP remains useful because it exposes the simpler pre-landing loop in deterministic tests: store a goal in conversation state, inject a continuation prompt, and keep calling `conversation.run()` until the goal is complete, blocked, or budget-limited.

The live runs and deterministic probes show the sharper lesson: judged continuation is still not the same thing as system-owned verification. A model can satisfy vague completion criteria with a polished story, and even with an honest model the harness may not know whether the final evidence is authoritative.

The reference solution therefore treats the goal feature as three layers:

1. **Official goal loop.** Use `run_goal` / `GoalController` to continue until a judge confirms completion or the cap is reached.
2. **Verifier and evidence layer.** Record command output, exit code, file diffs, and event ids as system-owned evidence.
3. **Goal scaffolding layer.** Own criteria, budgets, stop states, sensors, actuators, and envelope policy.

## Start With These Files

| File | Why it matters |
|---|---|
| `../probe_official_goal.py` | Shows the landed SDK controller continuing, completing, and capping without a real model call. |
| `goal_scaffold.py` | Shows the state a goal scaffold needs beyond an objective string. |
| `probe_goal_mvp.py` | Runs deterministic probes against the repo-local goal MVP fixture. |
| `../../p12-goal-scaffolding/README.md` | Main lesson and live run procedure. |

Start with the official SDK controller probe:

```bash
cd projects/p12-goal-scaffolding
uv run --with openhands-sdk --with openhands-tools python probe_official_goal.py
```

Then use the repo-local fixture as the implementation under test:

```bash
cd projects/p12-goal-scaffolding
python test_goal_mvp.py
```

Then run the solution probes from the course repo:

```bash
cd projects/p12-goal-scaffolding
python solution/probe_goal_mvp.py
```

## Key Design Choices

**Make the official SDK loop the baseline.** The landed OpenHands feature owns the outer completion loop: objective, judge, follow-up, complete, and capped.

**Keep the MVP as the gap fixture.** The MVP is useful because it isolates the smallest loop: `GoalState`, `run_until_goal`, continuation prompt, and `update_goal`. It makes missing scaffold responsibilities easy to test without an LLM.

**Use deterministic probes before live runs.** Live model behavior is informative, but the basic product semantics should be testable without an LLM. The probe script uses fake conversations to test budget, blocker, terminal-status, and schema behavior.

**Separate criteria from evidence.** A criterion is the requirement. Evidence is the sensor output that proves it. The agent can propose evidence, but the harness should record the command, exit code, output, file diff, event id, and timestamp.

**Treat the verifier as system-owned.** The verifier command should run from the harness after relevant edits. A final answer that says "tests pass" is not the same as a recorded verifier event.

**Keep envelope enforcement outside prompt text.** If only two paths are allowed, the edit tool or workspace policy should reject other paths. If package installation is disallowed, command policy should reject it before it runs.

**Do not turn the judge into the whole verifier.** `judge_goal` reads rendered transcript text. It is useful for deciding whether to continue, but it is not a substitute for executable checks, budget transitions, and tool policy.

## Reference Probe Findings

The expected probe pattern against the current MVP is:

| Probe | Expected result | Why |
|---|---|---|
| `baseline_continuation` | pass | Active goals continue and stop on `complete`. |
| `budget_active_cutoff` | pass | Active unfinished goals become `budget_limited` after exceeding budget. |
| `token_formula_cached_discount` | pass | The budget metric discounts cached prompt tokens. |
| `budget_complete_override_gap` | gap | A run can mark complete after crossing the budget. |
| `completion_without_evidence_gap` | gap | `update_goal complete` accepts no verifier evidence. |
| `scaffold_schema_gap` | gap | `GoalState` has no criteria, verifier, sensors, actuators, envelope, or evidence. |
| `blocked_first_turn_gap` | gap | The tool can mark blocked on turn 1. |
| `max_turns_leaves_active_gap` | gap | A max-turn cap stops the driver but leaves status `active`. |
| `status_terminal_semantics_gap` | gap | `paused` and `blocked` do not continue, but are not terminal by the helper. |

Those gaps are not an indictment of the MVP. They are the point of the lab. The MVP teaches that the continuation loop is easy enough to prototype. The system-owned goal scaffolding semantics are the hard part.

## Official Goal Loop And The Missing Scaffold

The official OpenHands direction is now `run_goal` and `GoalController`, not a custom `GoalCritic`:

```python
from openhands.sdk.conversation.goal import run_goal

outcome = run_goal(conversation, objective, judge_llm, max_iterations=3)
```

That loop composes with a critic, but it operates one layer outside the critic. The critic governs each inner `conversation.run()`. The goal loop decides whether another run is needed at all.

A production `/goal` still needs a thin system layer around the official loop:

| Need | Why `run_goal` alone is not enough |
|---|---|
| Hard token budget | `max_iterations` caps audits, not goal-level tokens or cost. |
| Completion evidence | The judge sees transcript text unless verifier events are structured and required. |
| Criteria | The objective is a string; criterion-by-criterion state still belongs in the harness. |
| Envelope | Disallowed actions must be denied before they happen, not judged after the fact. |
| Fresh verifier run | The harness must know whether tests ran after the latest relevant edit. |
| False-premise handling | A transcript judge can notice missing evidence, but the scaffold must define what honest evidence is possible. |

The practical shape is:

```text
GoalScaffold
  -> official run_goal / GoalController
  -> Verifier runner
  -> Evidence ledger
  -> Budget/status controller
  -> Envelope policy
```

## What To Compare Against Your Attempt

Your solution is on the right track if it can answer these questions without relying on the final assistant message:

- What criteria were required?
- Which verifier ran, with what exit code?
- Did the verifier run after the latest relevant edit?
- Which files changed?
- Which commands ran?
- Did any command or edit violate the envelope?
- Why did the goal stop: complete, blocked, budget-limited, capped, or verifier-failed?
- Could the same goal resume after process restart with the same scaffold?

## Valid Variations

Use the official `run_goal` loop as the default continuation mechanism. Keep the caller-side MVP only as a teaching fixture or for environments pinned before SDK v1.29.2. If you add a critic, use it for inner-run quality control, not as the only source of truth for completion.

The design to avoid is prompt-only trust. A prompt can tell the model to audit itself. A harness has to decide what counts as proof.
