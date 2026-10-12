# Exercise 2: Design the tool surface

## What Problem Are You Solving?

Hold the PR explanation task and model fixed. Compare four GitHub operations, twelve operations, and one evidence-bundle tool. More operations do not automatically produce better evidence.

1. Predict what changes before running or reading results.
2. Run one controlled comparison, or inspect the saved receipts.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare an empty scratch workspace:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w2 --workspace .workshop-runs/w2-primitive
```

In Canvas's MCP settings, add a local stdio server. Use the absolute path to `.workshop-venv/bin/python` as the command and the absolute path to `workshops/odsc-2026/labs/tools/github_mcp_server.py` as its single argument. Set `WORKSHOP_MCP_MODE` in the server environment to `primitive`, `broad`, or `task-shaped`. Start a fresh conversation and workspace after changing lanes. Keep the native baseline tools unchanged and record the actual resolved list.

| Mode | GitHub operations exposed |
|---|---:|
| `primitive` | 4 |
| `broad` | 12 |
| `task-shaped` | 1 |

The packaged server performs public GitHub GET requests without a token. Preflight with the command below before timing. It uses GitHub's unauthenticated quota; HTTP 403/429 is a setup failure, not a tool-quality result. If quota is exhausted, use the saved comparison.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/preflight_github.py
```

Optional terminal lane: remove MCP, keep `gh` installed and authenticated, and use the same prompt. Check `gh api repos/OpenHands/OpenHands/pulls/16860` first. Do not compare a failed authentication lane with working retrieval.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-2). An offline learner can inspect those receipts without model access and complete the same decision worksheet. Receipts provide selected measurements and goal events; full behavioral traces are not yet packaged for every lane.

## Run It And Collect Metrics

Use the prompt printed by `prepare`; it substitutes your absolute interpreter path. The copies below make the task readable on the website. Replace the interpreter placeholder if copying directly. Use only the prepared workspace for editing.

### w2

```text
Inspect OpenHands/OpenHands pull request #16860 using public GitHub evidence.
Write five short bullets, targeting 200 words and never exceeding 280 words.
Include the allow-list change; two important implementation files selected from
src/utils/skill-enablement.ts, src/hooks/use-skill-enablement.ts,
src/hooks/use-migrate-enabled-skills.ts, src/api/agent-server-adapter.ts;
the test runner; the new test files; and remaining uncertainty.
Provide the PR link and at least two direct file or commit links attached to
supported claims. Do not modify any files. Count words before finishing.
Explicitly attribute Vitest, lint, and translation results to the upstream PR
report. State whether you personally ran any tests. Your final answer must
contain the complete explanation, not a reference to hidden analysis.
```


## Check The Result

Exercise 2 has no automatic semantic checker. Use this six-part rubric: allow-list behavior, two implementation files explained accurately, test runner identified, new tests identified, citations support claims, and uncertainty/test attribution stated. A score is evidence coverage, not complete correctness. Have a partner review the cited code and reject misleading claims.

Open two citations and verify the claims. Did the agent execute tests, or read upstream reports? Which necessary evidence was omitted by the bundle selection?

## Record The Results

| Lane | Independent result | Model | Calls | Total provider tokens | Time | Evidence and uncertainty |
|---|---|---|---|---|---|---|
| Baseline | | | | | | |
| Changed harness policy | | | | | | |

Record unknown usage as unknown. Include parent and child calls and judge calls where applicable. Keep processed tokens, cache reads, fresh input, and billed cost separate. Repeat trials before claiming performance gains.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [facilitator notes](/workshops/odsc-2026/facilitator).
