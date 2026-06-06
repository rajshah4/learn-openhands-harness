# Solution Brief: P04 Task Decomposition

## What This Solution Proves

This solution proves that task shape can be a harness problem. A large request may fail because the model is weak, but it may also fail because the harness handed it too many independent concerns at once.

The reference solution compares one monolithic release-readiness review with a decomposed workflow: scoped checks first, then a final aggregation pass. The result is not assumed to be better. It is scored against a rubric so the learner can decide whether decomposition earned the extra cost.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_decomposition.py` | Runs monolithic and decomposed workflows on copied workspaces. |
| `decomposition_plan.md` | The artifact to keep. It states when to split work and when not to. |
| `evaluation_rubric.md` | Defines the expected release-readiness signals and integrity checks. |
| `score_report.py` | Scores saved reports without making new model calls. |

Start with `decomposition_plan.md` to understand the design, then read the runner to see how the workflow enforces that plan.

## Key Design Choices

The decomposed solution splits the review into independent surfaces:

- documentation accuracy
- setup and test commands
- secrets and safety warnings
- project structure
- final aggregation

Each scoped run writes a file under `.harness_review/`. The final aggregator reads those scoped reports and writes `RELEASE_READINESS.md`.

That shape is intentional. The scoped reports make partial failure visible, and the final aggregation step has a narrower job: preserve evidence, prioritize findings, and avoid inventing unsupported issues.

The solution also copies the workspace before each run. That keeps the monolithic and decomposed comparisons fair and avoids contamination from files written by a previous run.

## How OpenHands Fits In

OpenHands is doing the work in multiple conversations, but the harness owns the sequence. The model does not decide the phases. The runner decides which scoped prompts exist, where each report goes, and what the aggregator is allowed to read.

That is the distinction from P08. P04 is harness-managed decomposition. P08 later asks when the model should author the short-lived workflow itself.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Did decomposition improve coverage? | Score monolithic and decomposed reports against `evaluation_rubric.md`. |
| Did aggregation preserve evidence? | Check that final findings cite paths from scoped reports. |
| Did issue counts stay consistent? | Compare declared P0 counts with the P0 table. |
| Was the extra cost justified? | Compare cost, wall-clock time, and missed blocker categories. |

The most interesting result is often not "monolithic crashed." It is "monolithic produced a confident report but missed categories the scoped checks found."

## Valid Variations

A valid solution might use fewer scoped checks, add a dependency/security check, or use a different report rubric. It might also keep the task monolithic if the subparts duplicate too much context.

The boundary is evidence. If decomposition adds more files but not better coverage, it did not earn its place.

## What To Keep

Keep a decomposition rule of thumb:

- split work when dimensions are independent and can be scored separately
- require scoped artifacts before aggregation
- retry failed dimensions rather than rerunning the whole task
- keep tasks monolithic when the answer depends on one shared chain of reasoning

P04 is successful when you can defend why the harness should split this kind of task, or why it should not.
