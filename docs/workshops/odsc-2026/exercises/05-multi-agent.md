# Exercise 6: Compare one agent with a validator

## What Problem Are You Solving?

Repair a shared counter so 50 concurrent jobs produce 50 without serializing simulated work. Compare one generalist with a repair owner followed by one fresh validator. This is sequential validation.

1. Predict what changes before running or reading results.
2. Run one controlled comparison, or inspect the saved receipts.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Use OpenHands with its native task/delegation tool enabled for the validator lane. A second browser chat without a recorded child return is a different workflow. If delegation is unavailable, run the single-agent lane and inspect the saved comparison.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w6-single --workspace .workshop-runs/w6-single
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w6-validator --workspace .workshop-runs/w6-validator
```

Use the same model and fresh conversation for both. Choose a shared total budget before running. A prompt is not budget enforcement: only call the comparison matched-budget if your gateway/controller actually limits the combined parent and child requests. Otherwise record actual expenditure and mark the cap unenforced.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-6). An offline learner can inspect those receipts without model access and complete the same decision worksheet. Receipts provide selected measurements and goal events.

## Run It And Collect Metrics

Use the prompt printed by `prepare`; it substitutes your absolute interpreter path. The copies below make the task readable on the website. Replace the interpreter placeholder if copying directly. Use only the prepared workspace for editing.

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


## Check The Result

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w6-single --workspace .workshop-runs/w6-single
```

Exit 0 means the packaged checks passed; exit 1 prints the unmet requirement. Run the workspace's full tests as well. The checker checks scope and independent behavior. In the security lane it only screens finding coverage; a person must validate every claim and proposed fix.

What did the fresh context add? Did the child return usable commands and results? Who owns synthesis? What could be checked more cheaply with deterministic code?

## Record The Results

| Lane | Independent result | Model | Calls | Total provider tokens | Time | Evidence and uncertainty |
|---|---|---|---|---|---|---|
| Baseline | | | | | | |
| Changed harness policy | | | | | | |

Record unknown usage as unknown. Include parent and child calls and judge calls where applicable. Keep processed tokens, cache reads, fresh input, and billed cost separate. Repeat trials before claiming performance gains.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [saved evidence](/workshops/odsc-2026/results).
