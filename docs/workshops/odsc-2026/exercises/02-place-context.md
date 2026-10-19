# Exercise 3: Recover a prior agreement

Compare a missing note, an older draft and an accepted customer note. Predict whether the agent should implement or ask for clarification.

Run these commands from the course checkout after [setup](../setup). Keep the course checkout and checkers outside the agent workspace. Preparation refuses an existing directory and makes no model requests. New conversations may produce different results from the saved examples. Path instructions are not filesystem isolation.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w3-agreement-none --workspace ../odsc-runs/w3-agreement-none
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w3-agreement-none --workspace ../odsc-runs/w3-agreement-none
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w3-agreement-draft --workspace ../odsc-runs/w3-agreement-draft
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w3-agreement-draft --workspace ../odsc-runs/w3-agreement-draft
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w3-agreement-accepted --workspace ../odsc-runs/w3-agreement-accepted
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w3-agreement-accepted --workspace ../odsc-runs/w3-agreement-accepted
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

Use the same model, tools and iteration allowance. Vary only the supplied note. The accepted contract checker is expected to reject an untouched starter. A clarification is the correct outcome when the agreement is unavailable; that is different from completing the implementation.

### w3-agreement-none

```text
Work only inside the supplied workspace. Do not access other workspaces, parent directories, network, or user files. Do not install dependencies, commit, or write memory files. Only edit exporter.py and test_exporter.py. Use python3 with PYTHONDONTWRITEBYTECODE=1 for checks. Report changed files, evidence, and any uncertainty. If a necessary prior agreement is missing, ask a specific clarification and stop before guessing it.

Task:
Add a missing-region policy to the CSV exporter for customer Northstar. We agreed the exact missing-value representation and ID compatibility rules in an earlier customer session. That agreement matters for this change. Implement it and add regression tests if you have the agreement; otherwise identify precisely what you need confirmed. The repository does not record the customer-session agreement. Non-missing region values must remain unchanged.

Supplied notes:
No saved session notes are supplied.
```

### w3-agreement-draft

```text
Work only inside the supplied workspace. Do not access other workspaces, parent directories, network, or user files. Do not install dependencies, commit, or write memory files. Only edit exporter.py and test_exporter.py. Use python3 with PYTHONDONTWRITEBYTECODE=1 for checks. Report changed files, evidence, and any uncertainty. If a necessary prior agreement is missing, ask a specific clarification and stop before guessing it.

Task:
Add a missing-region policy to the CSV exporter for customer Northstar. We agreed the exact missing-value representation and ID compatibility rules in an earlier customer session. That agreement matters for this change. Implement it and add regression tests if you have the agreement; otherwise identify precisely what you need confirmed. The repository does not record the customer-session agreement. Non-missing region values must remain unchanged.

Supplied notes:
Saved customer-session note, 2026-09-20, Northstar draft: Missing region (absent key or None) should be an empty field. Preserve customer_id as supplied, including leading zeros. This was a draft pending the October customer export review; the final missing-value representation was not settled here. Confirm the final agreement before shipping. This note is supplied context, not automatically retrieved memory.
```

### w3-agreement-accepted

```text
Work only inside the supplied workspace. Do not access other workspaces, parent directories, network, or user files. Do not install dependencies, commit, or write memory files. Only edit exporter.py and test_exporter.py. Use python3 with PYTHONDONTWRITEBYTECODE=1 for checks. Report changed files, evidence, and any uncertainty. If a necessary prior agreement is missing, ask a specific clarification and stop before guessing it.

Task:
Add a missing-region policy to the CSV exporter for customer Northstar. We agreed the exact missing-value representation and ID compatibility rules in an earlier customer session. That agreement matters for this change. Implement it and add regression tests if you have the agreement; otherwise identify precisely what you need confirmed. The repository does not record the customer-session agreement. Non-missing region values must remain unchanged.

Supplied notes:
Saved customer-session note, 2026-10-17, Northstar export review: Missing region (absent key or None) must be the literal string NA. Keep an existing empty string empty. Preserve customer_id as supplied, including leading zeros: Northstar joins it as a string, not a number. The NA sentinel avoids a legacy importer's blank-field default to US. Customer-session rationale is not yet in repository docs. This note is supplied context, not automatically retrieved memory.
```

## Inspect saved evidence

<a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/03D.html" target="_self">03D</a> and <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/03E.html" target="_self">03E</a> ask for clarification; <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/03F.html" target="_self">03F</a> implements the accepted rule and passes the check. The prompt explicitly requests clarification and marks the older draft provisional. This compares supplied task notes, not automatic retrieval. Canvas also injected shared ambient memory and skills, so these are not memory-disabled runs. The <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/reports/workshop3.html" target="_self">full W3 matrix</a> retains all attempts, including a contaminated investigation pilot. Original catalog-browsing examples remain reserves.
