# Exercise 1: Compare harnesses

## What Problem Are You Solving?

Start by varying the harness and holding the model, prompt, starter, and checks fixed. See how harnesses vary on how they read, edit, check, and repeat.

1. Predict what changes before running or reading results.
2. Try a harness choice and inspect the trace, or use the saved examples.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. If you ran `lab.py prepare-all` during setup, the workspaces below are already prepared inside your session folder. Use its `WORKSPACES.txt` for the exact workspace paths and check commands. Copy the task prompt from this page.

The individual commands below are an alternative for preparing one run at a time. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare the OpenHands workspace first. The Pi and OpenCode workspaces are optional.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-openhands
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-pi
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-opencode
```



## Try A Variation

Start with whichever harness you already have running. Inspect its first read, edit, and test command. Then try another harness if you have one configured. A single working harness is enough to start learning.

Try asking for a plan before editing, or change the enabled tools. Watch how the agent gets from the prompt to a checked repair. If you want a fair performance comparison, keep the model and task fixed; if you use different models, record that difference.

The slides' batched reads, separate reads, and extra checks describe particular recordings. Your harnesses can choose different sequences. Inspect what happened in your run.

## Run It And Explore

Copy the task prompt below. Replace its Python interpreter placeholder with the path printed by `prepare-all`. The optional local prompt files already include that path. Use only the prepared workspace for editing.

### w1

```text
Fix the off-by-one bug in toyapp/pagination.py. The pagination tests describe the correct behavior.

Do not modify tests. Work only inside the current repository. Before finishing, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q, inspect the final git status and diff, and report files changed, checks run, and remaining uncertainty. Do not install dependencies or make git commits.
```


## Optional Checks

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w1 --workspace ../odsc-runs/w1-openhands
```

Use this check as feedback on your experiment. Exit 0 means the example's behavior checks passed; exit 1 explains what needs inspection. Unexpected file edits appear as notes. Add `--strict-scope` if you want to reproduce the supplied editing scope. The check is optional; inspect the agent's actual test output and final diff either way.

The [archived action excerpts](/workshops/odsc-2026/inspection) show all three recorded read/edit/check sequences without model reasoning.

Look through the conversation details. Which files did it read before editing? Which checks did it actually execute? Did one terminal request bundle multiple commands? What evidence justified stopping?

## Record What You Notice

| Run | What changed? | What did the agent do differently? | What did I learn? |
|---|---|---|---|
| OpenHands | | | |
| Pi (optional) | | | |
| OpenCode (optional) | | | |

Time, calls, and provider usage are optional. Record unavailable numbers as unknown. Repeated runs are useful if you want to make a performance claim.
