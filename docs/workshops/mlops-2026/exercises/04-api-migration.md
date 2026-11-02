# Exercise 5: Verify an API migration

## What Problem Are You Solving?

A service can pass its own model tests and still change the JSON that clients receive. Migrate a small quote API from Pydantic 1 to native Pydantic 2 while preserving its accepted HTTP contract.

1. Freeze accepted requests and responses before the migration.
2. Let an agent update the service and run its own checks.
3. Compare actual HTTP responses with the frozen expectations and inspect how the agent uses the failures.

Check the boundary the client uses.

## Start With These Files

| File | Purpose |
|---|---|
| workshops/mlops-2026/exercise5/starter/app.py | Original FastAPI and Pydantic 1 service. |
| starter/CONTRACT.md | Intended compatibility requirements. |
| starter/smoke.py | Development test of Python model behavior. |
| controller/contract.json | Fifteen frozen requests and accepted outcomes. |
| controller/verify.py | Runs a temporary local HTTP service and compares responses. |
| PROMPT.txt | Exact recorded coding prompt, with session path guidance below. |

Run the [preparation command](../setup#prepare-exercise-5) first. WORKSPACES.txt contains the actual commands for your new session. There is no supplied finished solution: the recorded agent artifact has known gaps outside this finite suite.

## Freeze the client contract

The service accepts customer IDs, integer or string references, units, prices and an optional memo. Responses use aliases and a numeric total. Keep successful and rejected requests in the acceptance corpus. Decide compatibility before implementation, rather than accepting whatever schema the new service generates.

Which check would distinguish a Python Decimal in memory from a JSON string on the wire? Discuss that before running the agent.

## Start With The Baseline, Then Migrate

Verify the original service with the old environment first. Keep controller files outside the service directory the agent edits. Separate ownership is a convention in this local exercise, not an enforced filesystem boundary.

Create a fresh Canvas conversation in the prepared service directory. Use the new interpreter printed in WORKSPACES.txt. The target is FastAPI 0.115.12 and Pydantic 2.11.7, with Uvicorn 0.34.3. Use native v2 APIs, not pydantic.v1.

### Task prompt

```text
Migrate the quote API in this workspace from Pydantic 1 to native Pydantic 2.
Read CONTRACT.md and preserve the documented accepted HTTP behavior.
Update requirements, configuration, validators and serialization as needed.
Use the new environment interpreter from WORKSPACES.txt for your checks.
Do not change the sibling controller files. You may add your own tests.
Run the controller's frozen HTTP replay and use any expected/actual failures
to revise the implementation. Report the checks you actually ran.
Do not commit, publish or contact anyone.
```

This fresh-run prompt makes verifier invocation explicit. The recorded pilot prompt instead disclosed an automatic completion hook; the agent voluntarily invoked the checker before finishing. Do not call a rerun a matched reproduction of that exact prompt. The exact original is retained in PROMPT.txt. Only use it with an actually configured hook and correct session paths.

## Run It And Collect Metrics

WORKSPACES.txt supplies baseline and candidate verification commands. Run with REQUIRE_V2=1 for the candidate to include pinned-version and deprecated-API checks. Preserve every attempt and any cap or loader failure. A first-try pass is a valid result; do not repeat the exercise to manufacture a failure.

Record the model, versions, limits, actual verifier caller and returned output. The recorded teaching example is an agent-invoked external verifier. It does not show a blocked completion or native automatic restart.

## Record The Results

| Check | Before migration | After first edit | After feedback |
|---|---|---|---|
| Development smoke | | | |
| Frozen HTTP replay | | | |
| Native v2 version and API checks | | | |
| Actual stop reason | | | |

## What Students Should Leave With

A compatibility contract owned outside the migration, a replay against the real HTTP boundary, and failure output precise enough to guide an edit. A passing suite establishes the cases it executed.

<details><summary>References</summary>

[Pydantic migration guide](https://docs.pydantic.dev/2.11/migration/). Mechanical conversion tools help update code; separate behavior checks establish compatibility.

</details>
