# Exercise 4: Check before escalating

Use the existing counter pair as a baseline, then compare models on a controlled service repair. Choose an economical model and a stronger model available to your account. Record exact model identifiers, settings and total spend across any escalation.

Run these commands from the course checkout after [setup](../setup). Keep the course checkout and checkers outside the agent workspace. Preparation refuses an existing directory and makes no model requests. New conversations may produce different results from the saved examples. Path instructions are not filesystem isolation.

For the counter, use `lab.py prepare w4-async --workspace ../odsc-runs/w4-counter-flash` and repeat with a new folder for the second model. Print its unchanged task with `lab.py prompt w4-async`; check with `lab.py check w4-async --workspace ../odsc-runs/w4-counter-flash`. Prefix these commands with `.workshop-venv/bin/python workshops/odsc-2026/labs/`.

For controlled security repair, prepare separate copies for each model:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w4-controlled-security --workspace ../odsc-runs/w4-security-flash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w4-controlled-security --workspace ../odsc-runs/w4-security-flash
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

Repeat preparation with `../odsc-runs/w4-security-pro`. Inspect both behavior and file scope. A passing behavioral score is insufficient if the attempt also violates the edit contract. Choose an escalation trigger based on a failed requirement, then measure the combined cost if you continue a failed attempt with another model.

### w4-controlled-security

```text
Review and repair this local teaching service under CONTRACT.md. Inspect the code and reproduce each supported vulnerability locally before fixing it. Do not access network services or files outside this workspace. Modify service.py only for implementation; add repro.py and findings.json. Do not change CONTRACT.md.
findings.json must be an array of objects with function, issue, and reproduction (a concise explanation referencing repro.py). List only demonstrated in-scope vulnerabilities; unsupported findings count against the result. repro.py must run on the original service and demonstrate each issue using assertions, local temporary files, and the in-memory database. It should exit nonzero on the repaired service because the demonstrated attacks stop working. You may use a copy of the original source within this workspace while developing it. Include normal behavior checks in your own verification. No third-party dependencies. Finish with commands and observed results. Use at most 30 tool calls.

```

## Inspect saved evidence

<a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/04C.html" target="_self">04C</a> and <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/04G.html" target="_self">04G</a> are the counter pair. <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/04I.html" target="_self">04I</a> is Flash security attempt 2: 10/10 behavioral checks with a scope caveat. <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/04J.html" target="_self">04J</a> is Pro attempt 2: 9/10. Do not attribute Pro attempt 1's distinct failures to attempt 2. No controlled security attempt fully meets acceptance. The <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/reports/workshop4.html" target="_self">complete matrix</a> retains every attempt and the provider timeout. These selected observations do not rank models generally. Original rename, pagination and open-ended authentication review cases remain available through `lab.py` as reserves.
