# Solution Brief: P07 Verification And Capstone

## What This Solution Proves

This solution proves that "looks fine" is not a sufficient completion standard. P07 has two linked parts: first, measure whether a critic improves repeated runs on a checkable task; second, assemble the stable artifacts from P01-P07 into one runnable `harness.py`.

The reference solution does not require the critic to win by assumption. It runs no-critic and critic configurations repeatedly, scores the generated workspace deterministically, and reports pass rate and cost per pass.

## Start With These Files

| File | Why it matters |
|---|---|
| `evaluate.py` | Runs repeated no-critic vs. critic trials on a checkable `wordstats` task. |
| `harness.py` | The capstone harness that wires routing, tools, retrieval policy, memory, safety, Docker, and optional critic. |

Read `evaluate.py` first for the experiment. Read `harness.py` second for the final assembled harness.

## Key Design Choices

The evaluator uses a small `wordstats` task because it has clear requirements and a deterministic scorer. The scorer checks files, imports, empty files, word rules, missing-file behavior, and CLI behavior. That makes the result more useful than asking whether the final answer sounded convincing.

The critic path uses `APIBasedCritic` with `IterativeRefinementConfig`. The critic has a success threshold and an iteration cap, but the course score still comes from the deterministic rubric. Those are different signals:

- the critic decides whether to ask for refinement during the run
- the scorer decides whether the final workspace actually passed

The capstone `harness.py` keeps only stable defaults. Task prompt, repo path, and one-off exceptions stay outside the harness.

## How OpenHands Fits In

The evaluator runs each trial inside `DockerWorkspace` so generated files are isolated and easy to score. The capstone harness also uses Docker, mounts the security policy read-only, sets the security analyzer and confirmation policy, and relies on root `AGENTS.md` for repo memory.

The model router in `harness.py` is the P02 remote-safe pattern. The retrieval and decomposition decisions are comments because they are policy decisions until the learner chooses to wire extra tools or orchestration.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Did the critic improve pass rate? | Compare repeated trials, not one lucky run. |
| Did cost per pass improve or stay acceptable? | A higher raw cost can still be worth it if pass rate rises enough. |
| Did the rubric catch real failures? | Inspect `p07_score.json` for each workspace. |
| Did `harness.py` separate constants from variables? | Stable policies live in the harness; task-specific knobs do not. |

The capstone is not successful because it runs once. It is successful when the same harness produces behavior you would trust across multiple tasks and repos.

## Valid Variations

A valid solution may disable the critic if the repeated-run table does not justify it. It may also use a different checkable task, a local critic endpoint, a stricter rubric, or a different routing policy from P02.

Do not turn the capstone into a pile of every feature the course mentioned. P07 is about composing the decisions that earned their place.

## What To Keep

Keep:

- the critic/rubric block only if it improves repeated-run evidence
- the pass-rate and cost-per-pass table
- the final `harness.py`
- the list of decisions that stayed constants versus per-task variables

P07 is the point where the course stops being a sequence of labs and becomes one harness you can iterate on.
