# Exercise 5: Separate stopping from acceptance

Start both runs from the same deliberately incomplete daily-report checkpoint. This is staged teaching input, not a naturally observed prior agent failure. Predict what evidence should make the verifier reject the first inspection milestone.

Run these commands from the course checkout after [setup](../setup). Keep the course checkout and checkers outside the agent workspace. Preparation refuses an existing directory and makes no model requests. New conversations may produce different results from the saved examples. Path instructions are not filesystem isolation.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w5-checkpoint-ordinary --workspace ../odsc-runs/w5-checkpoint-ordinary
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w5-checkpoint-ordinary --workspace ../odsc-runs/w5-checkpoint-ordinary
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w5-checkpoint-goal --workspace ../odsc-runs/w5-checkpoint-goal
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w5-checkpoint-goal --workspace ../odsc-runs/w5-checkpoint-goal
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

Use the same model and tools. The native prompt enables `/goal --max 2`; configure a judge supported by your Canvas installation. The first run must inspect and report missing evidence without repairing it. The overall objective still requires both JSON artifacts. After the ordinary run stops, run the external check, show the missing reconciliation feedback, and ask it to continue. Let the native goal verifier request its own continuation within its two-audit cap. Never change this into an approval gate: the prompt already authorizes the repair stage.

### w5-checkpoint-ordinary

```text
Work only in this workspace. Do not read parent directories, external files, other conversations, network, credentials, or grading artifacts. Do not install dependencies, commit, or create memory files. Use PYTHONDONTWRITEBYTECODE=1. All requirements are stated in README.md. Verify the actual behavior and report the evidence and changed files. Complete the daily-report acceptance contract in README.md, including BOTH report.json and reconciliation.json. This is a deliberately prepared incomplete checkpoint, not an observed prior agent failure. Read CHECKPOINT.md and VERIFICATION.json for provenance and executable-check feedback. Only report.py, test_report.py, report.json, reconciliation.json may change.

This exercise intentionally has two stages. On the FIRST run of this conversation, inspect the checkpoint, run the existing tests and CLI, and report concrete missing acceptance evidence. Do not edit any files during that first run (CLI-generated report.json is allowed). End the run after the checkpoint report, explicitly identifying it as incomplete. That inspection milestone does NOT satisfy the overall objective. On a subsequent continuation message, the first-run restriction is lifted: repair the missing implementation, add regression tests, generate both artifacts and verify the complete contract, including empty input and pending retransmission IDs. No human approval is required for the continuation stage. Do not delegate. The objective is complete only when both artifacts and all README requirements are verified.
```

### w5-checkpoint-goal

```text
/goal --max 2 Work only in this workspace. Do not read parent directories, external files, other conversations, network, credentials, or grading artifacts. Do not install dependencies, commit, or create memory files. Use PYTHONDONTWRITEBYTECODE=1. All requirements are stated in README.md. Verify the actual behavior and report the evidence and changed files. Complete the daily-report acceptance contract in README.md, including BOTH report.json and reconciliation.json. This is a deliberately prepared incomplete checkpoint, not an observed prior agent failure. Read CHECKPOINT.md and VERIFICATION.json for provenance and executable-check feedback. Only report.py, test_report.py, report.json, reconciliation.json may change.

This exercise intentionally has two stages. On the FIRST run of this conversation, inspect the checkpoint, run the existing tests and CLI, and report concrete missing acceptance evidence. Do not edit any files during that first run (CLI-generated report.json is allowed). End the run after the checkpoint report, explicitly identifying it as incomplete. That inspection milestone does NOT satisfy the overall objective. On a subsequent continuation message, the first-run restriction is lifted: repair the missing implementation, add regression tests, generate both artifacts and verify the complete contract, including empty input and pending retransmission IDs. No human approval is required for the continuation stage. Do not delegate. The objective is complete only when both artifacts and all README requirements are verified.
```

## Inspect saved evidence

<a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/05D.html" target="_self">05D</a> resumes after ordinary verifier feedback. <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/05E.html" target="_self">05E</a> contains a saved rejection, continuation and acceptance, with exact goal verdict payloads in the full history. Both move from 4/8 to 8/8 external checks. The native judge reviews the transcript; it does not independently execute those checks. Stock Canvas chat can hide internal goal updates; use the linked full history for rejection evidence. Ordinary unsafe cleanup and native rejected out-of-workspace attempts remain explicit in the <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/reports/workshop5.html" target="_self">full W5 report</a>. The original slugify and capped goal examples remain reserves.
