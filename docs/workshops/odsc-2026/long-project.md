# Optional Lab: Compare Harnesses on a Long Project

The workshop shows the results of this project on a slide because a valid run takes much longer than the live session allows. You can run the same benchmark later or adapt its structure to an application you care about.

## Use the Exact Benchmark

The benchmark starts with a working in-memory incident application. The agent must add durable storage, concurrent alert handling, audit history, a background escalation worker, HTTP and CLI workflows, a responsive browser interface, and tests.

The repository provides everything needed to reproduce it:

- [Exact prompt used in the comparison](https://github.com/rajshah4/learn-openhands-harness/blob/main/workshops/odsc-2026/experiments/incident-operations-center/task.md)
- [Starter application](https://github.com/rajshah4/learn-openhands-harness/tree/main/workshops/odsc-2026/experiments/incident-operations-center/starter)
- [External verifier](https://github.com/rajshah4/learn-openhands-harness/blob/main/workshops/odsc-2026/experiments/incident-operations-center/verify_incident_ops.py)
- [Measured OpenHands, Pi, and OpenCode results](https://github.com/rajshah4/learn-openhands-harness/blob/main/workshops/odsc-2026/evidence/harness-suite/20260824-aws-incident-v2.md)

If you cloned the course repository, the prompt is at:

```text
workshops/odsc-2026/experiments/incident-operations-center/task.md
```

Run the unchanged benchmark before modifying it if you want to compare your result with the workshop numbers.

## Run It

1. Configure every harness with the same model, endpoint, and model settings.
2. Copy the starter application into one clean workspace per harness.
3. Start a new conversation with no prior harness memory.
4. Send the complete `task.md` prompt without additional hints.
5. Use the same permissions, network access, timeout, and repair policy for every harness.
6. Budget 90 minutes per run. The measured runs finished in 18 to 27 minutes.
7. Save the complete trace and provider usage.
8. Run the external verifier after the harness stops.

From the course repository root:

```bash
python workshops/odsc-2026/experiments/incident-operations-center/verify_incident_ops.py \
  /absolute/path/to/harness-workspace
```

Record the result before giving the agent any verifier feedback. A repair run answers a different question and should have its own time and token totals.

## Record Enough Evidence to Explain the Result

| Measurement | Question it answers |
|---|---|
| External verifier | Did the required behavior work? |
| Wall-clock time | How long did the user wait? |
| Model calls | How many times did the loop ask the model what to do next? |
| Context per call | How much information did the harness send at each step? |
| Input and output tokens | How much provider work did the run require? |
| Cache reads | How much repeated context did the provider reuse? |
| Tool actions | How did model decisions become environment work? |
| Errors and retries | Which delays came from recovery rather than useful progress? |

Get token and cache numbers from provider responses. Mark unavailable fields as unavailable. Do not estimate them from text length.

## Adapt the Prompt to Your Own Application

The incident domain is replaceable. The useful part is the shape of the work: an existing application, several connected layers, objective contracts, and enough steps for history management to become visible.

Preserve these parts when you adapt it:

1. Start from working code with tests. Every harness must receive the same committed revision.
2. Require changes across at least three layers, such as storage, background work, API, CLI, or interface.
3. Include one reliability problem that cannot be solved by editing a single function. Concurrency, restart recovery, idempotency, or version conflicts work well.
4. Specify observable behavior without prescribing the internal design.
5. Keep the external verifier outside the agent workspace.
6. Require the agent to run tests, inspect its diff, and report remaining uncertainty.
7. Set a shared timeout and decide whether repair feedback is allowed before starting.

Use this outline for a new prompt:

```text
# [Project name]

The existing [application] currently [what works today]. Extend it so that
[end-to-end outcome]. Preserve [public API, tests, or compatibility rule].

## Required behavior

- [Storage or state requirement]
- [API, CLI, or interface requirement]
- [Background or multi-step workflow]
- [Failure, concurrency, or recovery invariant]

## Observable contracts

- [Exact command, route, method, or marker]
- [Expected success behavior]
- [Expected error behavior]

## Constraints

- Work only inside the current workspace.
- Do not modify the supplied tests.
- [Dependency, network, security, or compatibility limit]

## Completion expectations

Run the relevant tests and an end-to-end check. Inspect the final diff.
Report the files changed, checks run, and remaining uncertainty.
```

## Change the Difficulty Without Breaking the Experiment

For a shorter project, remove one complete layer and its verifier checks. For example, keep storage, API, and background work but remove the browser interface and import/export workflow.

For a longer project, add one independent operational requirement such as interruption recovery or a migration from existing data. Do not add vague requests for polish. Add behavior that an external verifier can observe.

When you change the prompt, starter code, or verifier, give the experiment a new version. Run every harness against that same version before comparing the results.

## Use It to Improve One Harness

You can also hold the model and harness constant while changing one harness component. Good OpenHands experiments include:

- Current system prompt versus a shorter prompt
- Full skill catalog versus the recommended subset
- Full tool surface versus task-specific tools
- Current history policy versus earlier compaction or smaller tool results
- Current loop versus a call budget or stronger planning guidance

Change one component at a time. Compare accuracy first, then calls, context, time, and cost. A cheaper run that fails the required behavior is not an improvement.
