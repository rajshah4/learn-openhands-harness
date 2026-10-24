> Archived original exercise material. For the current classroom sequence, return to the [workshop index](/workshops/odsc-2026/). These tasks differ from the revised selections.

# Exercise 5: Define completion and stopping

## What Problem Are You Solving?

A goal states what a completed task must achieve. In native goal mode, a judge checks the result and can request another attempt if work is missing. Compare this with an ordinary repair and watch what evidence supports completion.

1. Predict what changes before running or reading results.
2. Try an ordinary repair and goal mode, or use the saved examples.
3. Compare the traces and decide which harness design you would use.

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. If you ran `lab.py prepare-all` during setup, the workspaces below are already prepared inside your session folder. Use its `WORKSPACES.txt` for the exact workspace paths and check commands. Copy the task prompt from this page.

The individual commands below are an alternative for preparing one run at a time. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare the missing-dot starter:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w5 --workspace ../odsc-runs/w5-repair
```

The five existing tests pass. The independent dot assertion fails. Run an ordinary repair first; the preparation output gives the interpreter path. Its prompt asks for a new regression test before the source fix.

For native goal practice, prepare a second workspace:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w5-goal --workspace ../odsc-runs/w5-goal
```

In Canvas, choose **Open Workspace**, select the printed directory, and start a fresh conversation. Paste the complete printed prompt. It begins with `/goal --max 2` and includes your Python interpreter and `PYTHONPATH=src` test command. Canvas shows a goal banner with the round, status, and missing work. After it stops, use the same `check` command with case `w5-goal` and its workspace.

The two-round cap limits outer judge audits, not all model calls or elapsed time. Goal mode uses a judge model as well as the agent. Inspect its explanation and run the optional behavior check yourself.

If your version does not recognize `/goal`, run the ordinary repair and inspect the saved complete/capped events. See the [Canvas goal instructions](https://github.com/OpenHands/docs/blob/main/openhands/usage/agent-canvas/conversations.mdx#run-a-goal).

## Try A Variation

First run the ordinary repair. On another fresh workspace, use the native goal command below and watch the goal banner. Which evidence does the judge use to decide that the work is complete?

For the stopping example shown in the slides, use the optional `w5-goal-capped` workspace from `prepare-all`. If preparing it separately:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w5-goal-capped --workspace ../odsc-runs/w5-goal-capped
```

Open it in a fresh Canvas conversation and use the blocked-goal prompt below. Edits are prohibited on purpose. Watch whether the judge identifies the missing output, requests another attempt, and stops at the two-audit cap. Stop a goal by sending a normal message if you want to change the experiment.

## Run It And Explore

Copy the task prompt below. Replace its Python interpreter placeholder with the path printed by `prepare-all`. The optional local prompt files already include that path. Use only the prepared workspace for editing.

### w5

```text
Add support for preserving dots in slugify: "api.v1 endpoint" must become "api.v1-endpoint". Inspect implementation and tests first. Add a regression test, run PYTHONPATH=src /absolute/path/to/.workshop-venv/bin/python -m pytest -q and show the failing output and exit status before changing implementation. Then fix only src/slugify.py, rerun the tests, and run a separate exact-output assertion. Preserve existing behavior and tests. Inspect the diff and report the commands, results, and uncertainty. Stop honestly incomplete if checks still fail after two repair attempts. Do not install dependencies or make git commits.

For imports and tests use PYTHONPATH=src /absolute/path/to/.workshop-venv/bin/python -m pytest -q. Use the same interpreter and PYTHONPATH=src for the separate dot assertion. The dependencies are already installed; do not install packages.
```

### w5-goal

```text
/goal --max 2 Preserve dots: slugify("api.v1 endpoint") must return "api.v1-endpoint". Existing tests must pass. Inspect first; edit only src/slugify.py and tests/test_slugify.py if needed. Preserve existing tests. Completion requires actual passing test output and a separate exact-output assertion after the latest edit. Report remaining failures honestly.

For imports and tests use PYTHONPATH=src /absolute/path/to/.workshop-venv/bin/python -m pytest -q. Use the same interpreter and PYTHONPATH=src for the separate dot assertion. The dependencies are already installed; do not install packages.
```

### w5-goal-capped (optional)

```text
/goal --max 2 Preserve dots: slugify("api.v1 endpoint") must return "api.v1-endpoint". Existing tests must pass. Completion requires actual passing test output and a separate exact-output assertion. Report remaining failures honestly.

For this deliberately constrained cap probe, do not edit source or tests, create output files, install packages, or make commits. Only inspect and run checks. The starting implementation drops dots; never manufacture a passing result. Do not request human input. If the goal cannot be satisfied under these constraints, report the failed check.

For imports and tests use PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 /absolute/path/to/.workshop-venv/bin/python -m pytest -q -p no:cacheprovider. Use the same interpreter and environment for the separate dot assertion. The dependencies are already installed.
```

This probe should leave the workspace unchanged. Its five existing tests pass while the dot assertion fails. A failed behavior check is expected here; inspect the goal banner for the separate continuation and cap result.

## Optional Checks

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w5 --workspace ../odsc-runs/w5-repair
```

Use this check as feedback on your experiment. Exit 0 means the example's behavior checks passed; exit 1 explains what needs inspection. Unexpected file edits appear as notes. Add `--strict-scope` if you want to reproduce the supplied editing scope. The check is optional; inspect the agent's actual test output and final diff either way.

Look through the conversation details. When original tests pass but the objective check fails, who should reject completion? What new evidence earns another attempt? What should happen when edits are prohibited?

## Record What You Notice

| Run | What changed? | What did the agent do differently? | What did I learn? |
|---|---|---|---|
| Ordinary repair | | | |
| Native goal | | | |
| Blocked goal (optional) | | | |

Time, calls, and provider usage are optional. Record unavailable numbers as unknown. Repeated runs are useful if you want to make a performance claim.
