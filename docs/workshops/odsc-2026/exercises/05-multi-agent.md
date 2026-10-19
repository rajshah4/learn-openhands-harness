# Exercise 6: Inspect the second context's contribution

Compare a single owner with an owner that requests one independent adversarial review. Both receive the same reservation contract. Predict what independent discovery would add when the single owner can already solve the task.

Run these commands from the course checkout after [setup](../setup). Keep the course checkout and checkers outside the agent workspace. Preparation refuses an existing directory and makes no model requests. New conversations may produce different results from the saved examples. Path instructions are not filesystem isolation.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w6-reservation-single --workspace ../odsc-runs/w6-reservation-single
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w6-reservation-single --workspace ../odsc-runs/w6-reservation-single
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prepare w6-reservation-team --workspace ../odsc-runs/w6-reservation-team
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py check w6-reservation-team --workspace ../odsc-runs/w6-reservation-team
```

Send the printed prompt to the agent after preparation. Run the check command yourself after it stops.

For the team, enable the native task tool and define an `adversary` subagent using terminal and file editor, inheriting the model, with no nested delegation. Its role is to read README.md and inventory.py independently, run read-only probes and return exact input/expected/observed evidence with contract clauses. It must not edit files or suggest code. Keep both runs bounded: the recorded comparison allowed 30 total iterations (single 30; team owner 18 plus child 12), a 360-second parent stop and a $1 total batch receipt stop. That allocation itself can affect the outcome.

### w6-reservation-single

```text
Work only in this workspace; no parent directories, other conversations, grading artifacts, network, credentials or installs. No commits or memory files. Use PYTHONDONTWRITEBYTECODE=1. README.md is the complete acceptance contract, existing tests are smoke tests. Implement and verify every requirement, add regression tests, then report concrete checks and changed files. Path constraints are instructions, not filesystem isolation. Finish the prepared project against README.md. Complete all review, implementation, testing and integration yourself without delegation. You may use any local standard-library probes and all information in the workspace.
```

### w6-reservation-team

```text
Work only in this workspace; no parent directories, other conversations, grading artifacts, network, credentials or installs. No commits or memory files. Use PYTHONDONTWRITEBYTECODE=1. README.md is the complete acceptance contract, existing tests are smoke tests. Implement and verify every requirement, add regression tests, then report concrete checks and changed files. Path constraints are instructions, not filesystem isolation. Finish the prepared project against README.md. Before reading inventory.py or tests or proposing any defect hypothesis, delegate exactly once to adversary. The delegation prompt must contain only the workspace path and "Read README.md and independently test inventory.py against it. Return concrete input/expected/observed evidence. Do not edit files." Wait for returned evidence. Then inspect the code, repair it, add tests and verify. Do not supply suspected bugs or test examples to the child.
```

## Inspect saved evidence

<a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/06C.html" target="_self">06C</a> and <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/06D.html" target="_self">06D</a> both pass the independent product and scope checks. The untipped reviewer executes real failures, but its reporting errors and temporary probe-file scope violation remain visible. This is independent discovery with no demonstrated correctness gain over the baseline.

Optional: use `classroom.py prepare w6-ledger-single` or `w6-ledger-team` with a fresh `--workspace` and print/check the matching case. Define codec-specialist and reducer-specialist roles with disjoint module ownership as specified by the prompt, parent cap 14 and child caps 8 each. <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/06E.html" target="_self">06E</a> completes; <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/classroom/06F.html" target="_self">06F</a> times out before owner integration. Both pass the original checker, while a separately labeled post-hoc newline probe exposes the team's handoff contract drift. The split budget is a confound. All six new outcomes, including scheduling reserve and workflow failures, remain in the <a href="/learn-openhands-harness/workshop-examples/2026-10-18-v3/reports/workshop6.html" target="_self">complete W6 report</a>. Original counter and cache examples remain reserves.
