> Archived original exercise material. For the current classroom sequence, return to the [workshop index](/workshops/odsc-2026/). These tasks differ from the revised selections.

# Exercise 4: Route models

## What Problem Are You Solving?

Start by varying the model across four tasks: a rename, a pagination bug, an async race, and an authentication review. See which tasks each model completes and what evidence you would require before trying a stronger model.

1. Predict what changes before running or reading results.
2. Try a model and inspect the trace, or use the saved examples.
3. Compare the traces and decide which harness design you would use.

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. If you ran `lab.py prepare-all` during setup, the workspaces below are already prepared inside your session folder. Use its `WORKSPACES.txt` for the exact workspace paths and check commands. Copy the task prompt from this page.

The individual commands below are an alternative for preparing one run at a time. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Pick an economical and a stronger model available to your account. Record exact model identifiers and reasoning settings.

Flash and Pro are one option with the workshop gateway. The slides' Haiku/Opus results are a separate recorded experiment; you do not need those models to do this exercise.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-rename --workspace ../odsc-runs/w4-cheap-rename
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-pagination --workspace ../odsc-runs/w4-cheap-pagination
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-async --workspace ../odsc-runs/w4-cheap-async
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-security --workspace ../odsc-runs/w4-cheap-security
```

Repeat with new directory names for the stronger model. For the static rule, choose the route before starting. For verify-then-escalate, use another fresh starter, run the economical model, check externally, and return a failed requirement to the stronger model only when needed. Record both attempts' spend.

## Try A Variation

Choose two models available to you. Try the rename or pagination task on both before tackling the async repair or security explanation. Record what you noticed about the answer and the work required.

Write a simple rule for when you would start with each model. Try it on another task. You can also return a failed check to a stronger model and inspect what it changes. Usage and timing are optional observations; no router needs to be implemented for this exercise.

Both models may pass. Compare the supporting evidence and work required, then name a concrete failure that would trigger escalation. A harder task label alone is not a failure signal.

## Run It And Explore

Copy the task prompt below. Replace its Python interpreter placeholder with the path printed by `prepare-all`. The optional local prompt files already include that path. Use only the prepared workspace for editing.

Use a separate workspace and new conversation for each task and model. `prepare-all` creates four `w4-cheap-*` folders and four `w4-stronger-*` folders. For example, run the rename task in `w4-cheap-rename`, then repeat it with the stronger model in `w4-stronger-rename`.

For an escalation experiment, the stronger model can continue the economical model's failed attempt in the same workspace. Record that as one combined attempt.

### w4-rename

```text
Rename raw_items to source_items in toyapp/pagination.py. Keep behavior unchanged. Edit only that source file.

Do not modify tests. Work only inside the current repository. Before finishing, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q, inspect the final git status and diff, and report files changed, checks run, and remaining uncertainty. Do not install dependencies or make git commits.
```

### w4-pagination

```text
Fix the off-by-one bug in toyapp/pagination.py. The pagination tests describe the correct behavior.

Do not modify tests. Work only inside the current repository. Before finishing, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q, inspect the final git status and diff, and report files changed, checks run, and remaining uncertainty. Do not install dependencies or make git commits.
```

### w4-async

```text
Debug the async race in toyapp/async_jobs.py. Fifty concurrent jobs must reliably produce 50. Simulated async work must remain concurrent rather than being serialized behind one long lock.

Do not modify tests. Work only inside the current repository. Before finishing, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q, inspect the final git status and diff, and report files changed, checks run, and remaining uncertainty. Do not install dependencies or make git commits.
```

### w4-security

```text
Review toyapp/auth.py for security issues. Write SECURITY_REVIEW.md with specific findings, affected code, consequences, and concrete fixes. Do not edit source files or tests. Inspect the final diff and report evidence and uncertainty. Do not make git commits.
```

## Optional Checks

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w4-pagination --workspace ../odsc-runs/w4-cheap-pagination
```

Use this check as feedback on your experiment. Exit 0 means the example's behavior checks passed; exit 1 explains what needs inspection. Unexpected file edits appear as notes. Add `--strict-scope` if you want to reproduce the supplied editing scope. The check is optional; inspect the agent's actual test output and final diff either way.

Look through the conversation details. Which task can fail silently? What rejected requirement earns escalation? Which model route would you choose for new held-out tasks, and how would you evaluate it?

The security-review check lists example topics mentioned in the report. It does not judge whether a finding is correct. Read the explanation and proposed fix against the middleware; different wording and different conclusions are part of the discussion.

The historical rubric included timing-safe comparison. Here authentication uses dictionary membership, which does not demonstrate an exploitable timing attack. Distinguish confirmed bugs from hardening suggestions and claims that depend on a router or deployment you have not inspected.

## Record What You Notice

| Run | What changed? | What did the agent do differently? | What did I learn? |
|---|---|---|---|
| Economical model | | | |
| Stronger model | | | |
| My routing rule | | | |

Time, calls, and provider usage are optional. Record unavailable numbers as unknown. Repeated runs are useful if you want to make a performance claim.
