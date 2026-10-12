# Exercise 1: Compare harnesses

## What Problem Are You Solving?

Hold the model, prompt, starter, and checks fixed. Change the harness and inspect what it reads, edits, checks, and repeats. One successful run does not establish a universal ranking.

1. Predict what changes before running or reading results.
2. Run one controlled comparison, or inspect the saved receipts.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare three separate workspaces. Configure OpenHands, Pi, and OpenCode with the same resolved model, endpoint, permissions, and stopping limits. If a harness cannot access that model, leave it out of the controlled comparison.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace .workshop-runs/w1-openhands
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace .workshop-runs/w1-pi
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace .workshop-runs/w1-opencode
```

Run one lane at a time. Each starter contains only the pagination module and its tests.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-1). An offline learner can inspect those receipts without model access and complete the same decision worksheet. Receipts provide selected measurements and goal events; full behavioral traces are not yet packaged for every lane.

## Run It And Collect Metrics

Use the prompt printed by `prepare`; it substitutes your absolute interpreter path. The copies below make the task readable on the website. Replace the interpreter placeholder if copying directly. Use only the prepared workspace for editing.

### w1

```text
Fix the off-by-one bug in toyapp/pagination.py. The pagination tests describe the correct behavior.

Do not modify tests. Work only inside the current repository. Before finishing, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q, inspect the final git status and diff, and report files changed, checks run, and remaining uncertainty. Do not install dependencies or make git commits.
```


## Check The Result

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w1 --workspace .workshop-runs/w1-openhands
```

Exit 0 means the packaged checks passed; exit 1 prints the unmet requirement. Run the workspace's full tests as well. The checker checks scope and independent behavior. In the security lane it only screens finding coverage; a person must validate every claim and proposed fix.

The [archived action excerpts](/workshops/odsc-2026/inspection) show all three recorded read/edit/check sequences without model reasoning.

Which files did it read before editing? Which checks did it actually execute? Did one terminal request bundle multiple commands? What evidence justified stopping?

## Record The Results

| Lane | Independent result | Model | Calls | Total provider tokens | Time | Evidence and uncertainty |
|---|---|---|---|---|---|---|
| Baseline | | | | | | |
| Changed harness policy | | | | | | |

Record unknown usage as unknown. Include parent and child calls and judge calls where applicable. Keep processed tokens, cache reads, fresh input, and billed cost separate. Repeat trials before claiming performance gains.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [facilitator notes](/workshops/odsc-2026/facilitator).
