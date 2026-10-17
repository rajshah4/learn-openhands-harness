# Exercise 6: Compare one agent with a validator

## What Problem Are You Solving?

Start by comparing one repair agent against multiple agents. Both approaches must fix a counter so 50 concurrent jobs produce 50 while keeping the work concurrent. See what the validator adds after the repair.

1. Predict what changes before running or reading results.
2. Try a single agent and a fresh validator, or use the saved examples.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. If you ran `lab.py prepare-all` during setup, the workspaces below are already prepared inside your session folder. Use its `WORKSPACES.txt` for the exact workspace paths and check commands. Copy the task prompt from this page.

The individual commands below are an alternative for preparing one run at a time. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Before the validator run, open a fresh conversation with your OpenHands profile and ask:

```text
List the tool names available to you without calling them or changing files. Is there a native task or delegation tool that can return a child result?
```

Inspect the response and your profile's tool configuration. Start another fresh conversation for the exercise. Confirm that the run contains an actual child tool call and returned result before describing it as native delegation.

If your profile has no delegation tool, use two conversations: let the first repair the task, then open the same workspace in a fresh conversation and ask for read-only validation. Give it the file, required behavior, test command, and a brief return format. Bring its findings back to the repair owner. This lets you explore fresh context; label it manual validation rather than native delegation.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w6-single --workspace ../odsc-runs/w6-single
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w6-validator --workspace ../odsc-runs/w6-validator
```

Use the same model if you want to focus on the effect of adding a context. If you record usage, include the owner and validator.

## Try A Variation

Try the single-agent repair first. Then add a fresh validator, using native delegation or the two-conversation fallback below. Compare what the second context notices and what the owner has to explain again.

Change the validator's brief: ask it to check concurrency, then ask it to critique the evidence. Notice how the handoff changes. You are exploring the cost and usefulness of another context, so a full orchestration system is optional.

## Run It And Explore

Copy the task prompt below. Replace its Python interpreter placeholder with the path printed by `prepare-all`. The optional local prompt files already include that path. Use only the prepared workspace for editing.

### w6-single

```text
Debug the async race in toyapp/async_jobs.py. Fifty concurrent jobs must reliably produce 50. Simulated async work must remain concurrent rather than being serialized behind one long lock.

Do not modify tests. Work only inside the current repository. Before finishing, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q, inspect the final git status and diff, and report files changed, checks run, and remaining uncertainty. Do not install dependencies or make git commits.

Use one agent. Do not delegate or call a subagent tool. Complete the objective and verify the result.
```

### w6-validator

```text
Debug the async race in toyapp/async_jobs.py. Fifty concurrent jobs must reliably produce 50. Simulated async work must remain concurrent rather than being serialized behind one long lock.

Do not modify tests. Work only inside the current repository. Before finishing, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q, inspect the final git status and diff, and report files changed, checks run, and remaining uncertainty. Do not install dependencies or make git commits.

First repair and check the task yourself. Then invoke your harness's native task/delegation tool exactly once for a fresh independent validator of the current result. Do not delegate implementation. If no native delegation tool is available, report that limitation and stop this comparison lane.
The validator must inspect and test only. Pass these requirements explicitly to it: do not edit source or tests, create output files, revert source, or redirect shell output. Run Python with PYTHONDONTWRITEBYTECODE=1 and pytest -p no:cacheprovider. Use subprocess.run with capture_output=True for repeated checks and print results. Return at most 250 words containing commands/results, uncertainty, and PASS/REJECT. Count words before returning.
Do not modify files while the validator runs. After its return, address rejected requirements and report initial and final verdicts. The parent owns the final synthesis.
```

## Optional Checks

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w6-single --workspace ../odsc-runs/w6-single
```

Use this check as feedback on your experiment. Exit 0 means the example's behavior checks passed; exit 1 explains what needs inspection. Unexpected file edits appear as notes. Add `--strict-scope` if you want to reproduce the supplied editing scope. The check is optional; inspect the agent's actual test output and final diff either way.

Look through the conversation details. What did the fresh context add? Did the child return usable commands and results? Who owns synthesis? What could be checked more cheaply with deterministic code?

## Record What You Notice

| Run | What changed? | What did the agent do differently? | What did I learn? |
|---|---|---|---|
| One agent | | | |
| Owner plus validator | | | |

Time, calls, and provider usage are optional. Record unavailable numbers as unknown. Repeated runs are useful if you want to make a performance claim.
