# Solution Brief: P12 Goal Scaffolding

## What This Solution Shows

The repo-local caller-side MVP proves that `/goal` is not mysterious. You can store a goal in conversation state, inject a continuation prompt, and keep calling `conversation.run()` until the goal is complete, blocked, or budget-limited.

The live runs and deterministic probes show the sharper lesson: continuation is not verification. A model can satisfy vague completion criteria with a polished story, and even with an honest model the harness may not know whether the final evidence is authoritative.

The reference solution therefore treats the goal feature as three layers:

1. **Goal loop.** Persist the objective and continue while active.
2. **Goal critic.** Audit stop attempts and feed back missing work through iterative refinement.
3. **Goal scaffolding layer.** Own criteria, verifier results, budgets, evidence, and envelope policy.

## Start With These Files

| File | Why it matters |
|---|---|
| `goal_scaffold.py` | Shows the state a goal scaffold needs beyond an objective string. |
| `probe_goal_mvp.py` | Runs deterministic probes against the repo-local goal MVP fixture. |
| `../../p12-goal-scaffolding/README.md` | Main lesson and live run procedure. |

Use the repo-local fixture as the implementation under test:

```bash
cd projects/p12-goal-scaffolding
python test_goal_mvp.py
```

Then run the solution probes from the course repo:

```bash
cd projects/p12-goal-scaffolding
python solution/probe_goal_mvp.py
```

If you have access to an external modified SDK checkout, compare it explicitly:

```bash
GOAL_MVP_REPO=/path/to/goal-mvp-checkout \
  python projects/p12-goal-scaffolding/solution/probe_goal_mvp.py
```

## Key Design Choices

**Keep the MVP as the baseline.** The MVP is useful because it isolates the smallest loop: `GoalState`, `run_until_goal`, continuation prompt, and `update_goal`.

**Use deterministic probes before live runs.** Live model behavior is informative, but the basic product semantics should be testable without an LLM. The probe script uses fake conversations to test budget, blocker, terminal-status, and schema behavior.

**Separate criteria from evidence.** A criterion is the requirement. Evidence is the sensor output that proves it. The agent can propose evidence, but the harness should record the command, exit code, output, file diff, event id, and timestamp.

**Treat the verifier as system-owned.** The verifier command should run from the harness after relevant edits. A final answer that says "tests pass" is not the same as a recorded verifier event.

**Keep envelope enforcement outside prompt text.** If only two paths are allowed, the edit tool or workspace policy should reject other paths. If package installation is disallowed, command policy should reject it before it runs.

**Use GoalCritic for the SDK integration point, not for all truth.** A critic is the right place to intercept finish attempts and continue the run. It is not a substitute for executable checks, budget transitions, and tool policy.

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

## GoalCritic Composite

The GoalCritic proposal from the issue comment is the best OpenHands-native direction:

```python
class GoalCritic(CriticBase):
    def evaluate(self, events, git_patch=None):
        ...

    def get_followup_prompt(self, result):
        ...
```

Attached to an agent, the critic would judge the attempted finish. If incomplete, iterative refinement feeds the missing criteria back into the same `conversation.run()` call.

That gets the continuation mechanism closer to the SDK core, but a production `/goal` still needs a thin system layer around it:

| Need | Why GoalCritic alone is not enough |
|---|---|
| Hard token budget | SDK budget is cost-oriented; token budget needs goal-level accounting. |
| Completion evidence | The judge sees transcript text unless verifier events are structured and required. |
| Envelope | Critic runs after actions; disallowed actions must be denied before they happen. |
| Fresh goal reset | Iterative-refinement counters must reset when a new goal starts. |
| Capped status | `max_iterations` needs a distinct state instead of silent finish. |
| Finish path coverage | Content-only stops and alternate finish paths must still pass through the gate. |

The practical shape is:

```text
GoalScaffold
  -> GoalState
  -> GoalCritic finish gate
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

You can keep the caller-side loop for a Phase 1 demo if the goal service owns verifier checks and terminal-state transitions. You can move continuation into `GoalCritic` if you want the SDK to own finish interception. You can use both: caller-side or server-side goal state to store the goal scaffold, and `GoalCritic` to turn incomplete finish attempts into continuation.

The design to avoid is prompt-only trust. A prompt can tell the model to audit itself. A harness has to decide what counts as proof.
