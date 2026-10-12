# Exercise 5: Define completion and stopping

## What Problem Are You Solving?

Repair a slug function whose existing tests pass while the requested dot behavior fails. Define completion independently, then inspect how a native goal controller continues and stops.

1. Predict what changes before running or reading results.
2. Run one controlled comparison, or inspect the saved receipts.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare the missing-dot starter:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w5 --workspace .workshop-runs/w5-repair
```

The five existing tests pass. The independent dot assertion fails. Run an ordinary repair first; the preparation output gives the interpreter path. Its prompt asks for a new regression test before the source fix.

For native goal practice, use a second fresh starter and an idle conversation on an Agent Server that supports `POST /api/conversations/{id}/goal`. Confirm the endpoint in your server's `/openapi.json`. The archived probe used Agent Server 1.49.6. Post `objective` from `prompts/w5-goal.txt` with `max_iterations: 2` through your authenticated server client. A detailed ordinary chat prompt does not activate the native loop. Keep the inner agent step limit separate. Inspect goal state events after termination and run the external checker.

If that endpoint is unavailable, complete the ordinary repair and audit the packaged native receipts. The [official SDK guide](https://docs.openhands.dev/sdk/guides/convo-goal) also documents `run_goal` for a standalone conversation. Do not infer native activation from the wording of a prompt.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-5). An offline learner can inspect those receipts without model access and complete the same decision worksheet. Receipts provide selected measurements and goal events.

## Run It And Collect Metrics

Use the prompt printed by `prepare`; it substitutes your absolute interpreter path. The copies below make the task readable on the website. Replace the interpreter placeholder if copying directly. Use only the prepared workspace for editing.

### w5

```text
Add support for preserving dots in slugify: "api.v1 endpoint" must become "api.v1-endpoint". Inspect implementation and tests first. Add a regression test, run /absolute/path/to/.workshop-venv/bin/python -m pytest -q and show the failing output and exit status before changing implementation. Then fix only src/slugify.py, rerun the tests, and run a separate exact-output assertion. Preserve existing behavior and tests. Inspect the diff and report the commands, results, and uncertainty. Stop honestly incomplete if checks still fail after two repair attempts. Do not install dependencies or make git commits.
```


## Check The Result

After the agent stops, run this command yourself from the course checkout. For other lanes replace both the case and workspace. Preserve the checker outside the editing workspace.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w5 --workspace .workshop-runs/w5-repair
```

Exit 0 means the packaged checks passed; exit 1 prints the unmet requirement. Run the workspace's full tests as well. The checker checks scope and independent behavior. In the security lane it only screens finding coverage; a person must validate every claim and proposed fix.

When original tests pass but the objective check fails, who should reject completion? What new evidence earns another attempt? What should happen when edits are prohibited?

## Record The Results

| Lane | Independent result | Model | Calls | Total provider tokens | Time | Evidence and uncertainty |
|---|---|---|---|---|---|---|
| Baseline | | | | | | |
| Changed harness policy | | | | | | |

Record unknown usage as unknown. Include parent and child calls and judge calls where applicable. Keep processed tokens, cache reads, fresh input, and billed cost separate. Repeat trials before claiming performance gains.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [saved evidence](/workshops/odsc-2026/results).
