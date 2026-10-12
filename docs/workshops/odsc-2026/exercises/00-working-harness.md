# Exercise 1: Compare harnesses

## What Problem Are You Solving?

Hold the model, prompt, starter, and checks fixed. Change the harness and inspect what it reads, edits, checks, and repeats. One successful run does not establish a universal ranking.

1. Predict what changes before running or reading results.
2. Try a harness choice and inspect the trace, or use the saved examples.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare the OpenHands workspace first. The Pi and OpenCode workspaces are optional. If you want to compare efficiency, configure the same resolved model and settings in each harness. For exploration, different models are fine as long as you record what changed.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-openhands
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-pi
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-opencode
```

Run one lane at a time. Each starter contains only the pagination module and its tests.

## Try A Variation

Start with whichever harness you already have running. Inspect its first read, edit, and test command. Then try another harness if you have one configured. A single working harness is enough to start learning.

Try asking for a plan before editing, or change the enabled tools. Watch how the agent gets from the prompt to a checked repair. If you want a fair performance comparison, keep the model and task fixed; if you use different models, record that difference.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-1). An offline learner can inspect those receipts without model access and complete the same decision worksheet. The saved examples show what happened in earlier runs.

## Run It And Explore

Use the prompt printed by `prepare`; it substitutes your absolute interpreter path. The copies below make the task readable on the website. Replace the interpreter placeholder if copying directly. Use only the prepared workspace for editing.

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

Which files did it read before editing? Which checks did it actually execute? Did one terminal request bundle multiple commands? What evidence justified stopping?

## Record What You Notice

| Run | What changed? | What did the agent do differently? | What did I learn? |
|---|---|---|---|
| OpenHands | | | |
| Pi (optional) | | | |
| OpenCode (optional) | | | |

Time, calls, and provider usage are optional. Record unavailable numbers as unknown. Repeated runs are useful if you want to make a performance claim.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [saved evidence](/workshops/odsc-2026/results).
