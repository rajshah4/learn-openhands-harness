# Exercise 3: Can memory save work?

## What Problem Are You Solving?

Add next-page browsing to a catalog while preserving direct page-number browsing and report exports. Hold the starter and task fixed; supply no notes, older notes, or current notes. The repository history is simulated and clearly labeled.

1. Predict what changes before running or reading results.
2. Run one controlled comparison, or inspect the saved receipts.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare identical starters for three lanes:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w3-none --workspace .workshop-runs/w3-none
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w3-older --workspace .workshop-runs/w3-older
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w3-current --workspace .workshop-runs/w3-current
```

Each command prints the task preceded by that lane's notes, if any. Paste the complete printed text. All lanes can inspect current accepted records. Older notes say to follow newer decisions. Disable automatic memory and unrelated skills if your harness permits; otherwise record them and call this an exploratory comparison. This supplies notes explicitly and does not test a product's memory loading.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-3). An offline learner can inspect those receipts without model access and complete the same decision worksheet. Receipts provide selected measurements and goal events; full behavioral traces are not yet packaged for every lane.

## Run It And Collect Metrics

Use the prompt printed by `prepare`; it substitutes your absolute interpreter path. The copies below make the task readable on the website. Replace the interpreter placeholder if copying directly. Use only the prepared workspace for editing.

### w3

```text
This package is a small catalog: browse() supports direct page-number access,
and report exports already resume across multiple windows.

Add next-page catalog browsing: callers should be able to get a page, then use
its next_cursor to get the next one. Keep direct page-number browsing and report
exports working. Follow the repository's accepted public API and design, add
focused tests, and run the relevant tests plus the full suite before finishing.

Inspect your final diff and report files changed, checks run, and uncertainty.
Do not modify unrelated files, change design records, or make git commits.
```


## Check The Result

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w3-current --workspace .workshop-runs/w3-current
```

Exit 0 means the packaged checks passed; exit 1 prints the unmet requirement. Run the workspace's full tests as well. The checker checks scope and independent behavior. In the security lane it only screens finding coverage; a person must validate every claim and proposed fix.

Which record supersedes the older note? Did the agent preserve both existing callers and reuse the shared token protocol? Did the notes reduce rediscovery without changing correctness?

## Record The Results

| Lane | Independent result | Model | Calls | Total provider tokens | Time | Evidence and uncertainty |
|---|---|---|---|---|---|---|
| Baseline | | | | | | |
| Changed harness policy | | | | | | |

Record unknown usage as unknown. Include parent and child calls and judge calls where applicable. Keep processed tokens, cache reads, fresh input, and billed cost separate. Repeat trials before claiming performance gains.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [facilitator notes](/workshops/odsc-2026/facilitator).
