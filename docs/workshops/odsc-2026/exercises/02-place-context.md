# Exercise 3: Can memory save work?

## What Problem Are You Solving?

Add next-page browsing to a catalog while preserving direct page-number browsing and report exports. Hold the starter and task fixed; supply no notes, older notes, or current notes. The repository history is simulated and clearly labeled.

1. Predict what changes before running or reading results.
2. Try a harness choice and inspect the trace, or use the saved examples.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare identical starters for three lanes:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w3-none --workspace ../odsc-runs/w3-none
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w3-older --workspace ../odsc-runs/w3-older
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w3-current --workspace ../odsc-runs/w3-current
```

Each command prints the task preceded by that lane's notes, if any. Paste the complete printed text. All lanes can inspect current accepted records. Older notes say to follow newer decisions. Disable automatic memory and unrelated skills if your harness permits; otherwise record them and call this an exploratory comparison. This supplies notes explicitly and does not test a product's memory loading.

## Try A Variation

Run the same task with no notes, older notes, and current notes. You can start with one condition and try the others later. Look for a decision the agent rediscovered or a note it checked against newer records.

Then edit the supplied notes for another fresh run: remove a useful fact, add a distracting fact, or save a verified decision from your own project. Watch what changes in the trace. These explicit notes are a simple way to explore memory without depending on one product's memory store.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-3). An offline learner can inspect those receipts without model access and complete the same decision worksheet. The saved examples show what happened in earlier runs.

## Run It And Explore

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

Use /absolute/path/to/.workshop-venv/bin/python for Python commands. Run /absolute/path/to/.workshop-venv/bin/python -m pytest -q after the focused checks. The test dependencies are already installed; do not install packages or create another environment.
```


## Optional Checks

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w3-current --workspace ../odsc-runs/w3-current
```

Use this check as feedback on your experiment. Exit 0 means the example's behavior checks passed; exit 1 explains what needs inspection. Unexpected file edits appear as notes. Add `--strict-scope` if you want to reproduce the supplied editing scope. The check is optional; inspect the agent's actual test output and final diff either way.

Which record supersedes the older note? Did the agent preserve both existing callers and reuse the shared token protocol? Did the notes reduce rediscovery without changing correctness?

## Record What You Notice

| Run | What changed? | What did the agent do differently? | What did I learn? |
|---|---|---|---|
| No notes | | | |
| Older notes | | | |
| Current notes | | | |

Time, calls, and provider usage are optional. Record unavailable numbers as unknown. Repeated runs are useful if you want to make a performance claim.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [saved evidence](/workshops/odsc-2026/results).
