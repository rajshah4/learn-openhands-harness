# Exercise 2: Design the tool surface

## What Problem Are You Solving?

Hold the PR explanation task and model fixed. Compare four GitHub operations, twelve operations, and one evidence-bundle tool. More operations do not automatically produce better evidence.

1. Predict what changes before running or reading results.
2. Try a harness choice and inspect the trace, or use the saved examples.
3. Record evidence and a decision in the [worksheet](/workshops/odsc-2026/worksheet).

## Start With These Files

Follow [setup](/workshops/odsc-2026/setup) first. If you ran `lab.py prepare-all` during setup, the workspaces below are already prepared inside your session folder. Use its `WORKSPACES.txt` for the exact workspace paths and check commands. Copy the task prompt from this page. The individual commands below are an alternative for preparing one run at a time. The portable package is `workshops/odsc-2026/labs/` in the course checkout. Its `starters/` hold only student inputs; `prompts/` hold full tasks; `checks/` and `evidence/` stay outside the agent workspace.

Prepare an empty scratch workspace:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w2 --workspace ../odsc-runs/w2-primitive
```

In Canvas, open **Customize → MCP Servers** and add a local stdio server. Use the absolute path to `.workshop-venv/bin/python` as the command and the absolute path to `workshops/odsc-2026/labs/tools/github_mcp_server.py` as its single argument. Set `WORKSHOP_MCP_MODE` in the server environment to `primitive`, `broad`, or `task-shaped`. Start a fresh conversation and workspace after changing lanes. Keep the native baseline tools unchanged and record the actual resolved list.

| Mode | GitHub operations exposed |
|---|---:|
| `primitive` | 4 |
| `broad` | 12 |
| `task-shaped` | 1 |

The packaged server performs read-only public GitHub requests. It works without a token; if shared Wi-Fi exhausts the public quota, optionally set `GITHUB_TOKEN` in the server environment to a token with access only to the public repository. Keep it out of prompts and files. Preflight with the command below before timing. It uses GitHub's unauthenticated quota; HTTP 403/429 is a setup failure, not a tool-quality result. If quota is exhausted, use the saved comparison.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/preflight_github.py
```

Optional terminal lane: remove MCP, keep `gh` installed and authenticated, and use the same prompt. Check `gh api repos/OpenHands/OpenHands/pulls/16860` first. Do not compare a failed authentication lane with working retrieval.

## Try A Variation

Try the four-operation GitHub server first. Switch to the evidence bundle, then the broad server, in fresh conversations. Which interface makes the evidence easier to find? Open a citation and check it yourself.

Change the task to an unfamiliar PR or ask for a small file the bundle missed. Notice when the compact tool helps and when you need a primitive read. Review the answer yourself if you are working alone.

## Start With The Baseline

Write your prediction before opening [saved results](/workshops/odsc-2026/results#exercise-2). An offline learner can inspect those receipts without model access and complete the same decision worksheet. The saved examples show what happened in earlier runs.

## Run It And Explore

Copy the task prompt below. Replace its Python interpreter placeholder with the path printed by `prepare-all`. The optional local prompt files already include that path. Use only the prepared workspace for editing.

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


## Optional Checks

Exercise 2 has no automatic semantic checker. Use this six-part rubric: allow-list behavior, two implementation files explained accurately, test runner identified, new tests identified, citations support claims, and uncertainty/test attribution stated. A score is evidence coverage, not complete correctness. Review the cited code yourself, or compare notes with a partner. Trace one claim back to its source and distinguish reported checks from commands the agent executed.

Open two citations and verify the claims. Did the agent execute tests, or read upstream reports? Which necessary evidence was omitted by the bundle selection?

## Record What You Notice

| Run | What changed? | What did the agent do differently? | What did I learn? |
|---|---|---|---|
| Four GitHub operations | | | |
| Evidence bundle | | | |
| Twelve operations (optional) | | | |

Time, calls, and provider usage are optional. Record unavailable numbers as unknown. Repeated runs are useful if you want to make a performance claim.

## What Students Should Leave With

One policy you can explain with observed evidence, plus the condition that would change your decision. Complete the [worksheet](/workshops/odsc-2026/worksheet) and compare your reasoning with the [saved evidence](/workshops/odsc-2026/results).
