# Six workshop labs

The participant guide lives in [the workshop docs](../../../docs/workshops/odsc-2026/index.md).
This directory is the portable execution package: prompts, focused starters,
optional behavior checks, a read-only GitHub MCP server, and selected saved receipts.

Run commands from the course repository root. Python 3.11 or newer and Git are required.

```bash
python3 -m venv .workshop-venv
.workshop-venv/bin/python -m pip install -r workshops/odsc-2026/labs/requirements.txt
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py list
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-openhands
```

Preparation prints the exact prompt with your interpreter path. Open only the
printed workspace in Canvas, paste the prompt, and inspect the trace. After
the agent stops, run the checker yourself from this course checkout:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w1 --workspace ../odsc-runs/w1-openhands
```

Exit 0 means the example behavior checks passed. Exit 1 explains a behavior
that needs inspection. Unexpected file edits are notes; `--strict-scope` makes
them blocking when you want the original editing scope. The untouched starters intentionally fail completion
checks, except rename, which passes behavior checks but has not renamed yet.
Exercise 2 uses a human citation rubric; security review has a term-coverage
screen followed by human review. The checkers provide learning feedback, not sandbox
boundaries. Do not expose this full checkout or its evidence to the editing agent.

Run `lab.py prompt CASE` to recover a prompt, or `prepare` with a new directory
for another lane. Preparation never deletes or resets an existing workspace.
The script does not contact a provider, install an agent, or enforce an agent's
call budget. Live calls are made by your chosen agent and can incur charges.

These focused fixtures are portable adaptations. Recorded result receipts used
the historical settings and sometimes larger fixtures. They do not predict
new run times, token totals, or model quality. See SOURCE-MANIFEST.json for provenance and limitations.
