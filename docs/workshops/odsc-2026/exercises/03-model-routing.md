# Exercise 4: Route models

## What Problem Are You Solving?

Choose a model for four different tasks: rename, pagination, an async race, and an authentication review. Compare verified results, spend, and latency before designing a routing rule.

1. Predict what changes before running or reading results.
2. Run one controlled comparison, or inspect the saved receipts.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Pick an economical and a stronger model available to your account. Record exact model identifiers and reasoning settings. A free-model practice run is valid, but does not reproduce the historical cost comparison.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-rename --workspace .workshop-runs/w4-cheap-rename
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-pagination --workspace .workshop-runs/w4-cheap-pagination
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-async --workspace .workshop-runs/w4-cheap-async
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w4-security --workspace .workshop-runs/w4-cheap-security
```

Repeat with new directory names for the stronger model. For the static rule, choose the route before starting. For verify-then-escalate, use another fresh starter, run the economical model, check externally, and return a failed requirement to the stronger model only when needed. Record both attempts' spend. This new verifier-driven practice differs from the historical LLM-judge cascade.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-4). An offline learner can inspect those receipts without model access and complete the same decision worksheet. Receipts provide selected measurements and goal events; full behavioral traces are not yet packaged for every lane.

## Run It And Collect Metrics

Use the prompt printed by `prepare`; it substitutes your absolute interpreter path. The copies below make the task readable on the website. Replace the interpreter placeholder if copying directly. Use only the prepared workspace for editing.

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


## Check The Result

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w4-pagination --workspace .workshop-runs/w4-cheap-pagination
```

Exit 0 means the packaged checks passed; exit 1 prints the unmet requirement. Run the workspace's full tests as well. The checker checks scope and independent behavior. In the security lane it only screens finding coverage; a person must validate every claim and proposed fix.

Which task can fail silently? What rejected requirement earns escalation? Which model route would you choose for new held-out tasks, and how would you evaluate it?

## Record The Results

| Lane | Independent result | Model | Calls | Total provider tokens | Time | Evidence and uncertainty |
|---|---|---|---|---|---|---|
| Baseline | | | | | | |
| Changed harness policy | | | | | | |

Record unknown usage as unknown. Include parent and child calls and judge calls where applicable. Keep processed tokens, cache reads, fresh input, and billed cost separate. Repeat trials before claiming performance gains.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [facilitator notes](/workshops/odsc-2026/facilitator).
