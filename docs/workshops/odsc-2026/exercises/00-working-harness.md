# Exercise 1: Same Model, Different Harnesses

The claim is that harnesses do not matter. You can choose Codex or Claude Code
and focus on the model. This exercise tests how much behavior changes when the
model stays fixed and only the harness changes.

The model is only one part of a coding agent. In this exercise, the same model receives the same task through OpenHands and ACP-backed agents. The repository, prompt, permissions, workspace, stopping policy, and verifier stay fixed. Only the harness changes.

We use Agent Canvas as the shared lab bench. It stores each conversation and gives us one place to inspect model calls, tool actions, observations, edits, tests, and the final answer.

## Use One Fast Task

Run pagination repair by default. It is short enough for the room and shows exploration, testing, and stopping. Keep the CLI feature as a backup when the pagination run has already been prepared or fails for an environmental reason. Do not run both live.

| Task | Task shape | What it can reveal | Observed clean-run range |
|---|---|---|---:|
| Pagination repair | Default, small test-driven bug fix | Exploration, test selection, and stopping behavior | 16 to 30 seconds |
| CLI feature | Backup, small feature with a behavioral contract | How the agent translates a requirement into code and tests | 29 to 56 seconds |

The times come from one clean AWS comparison using GLM-5.2. They are a planning guide, not a promise about a live run.

### A. Pagination repair

```text
Fix the off-by-one bug in toyapp/pagination.py. The pagination tests describe the correct behavior.

Do not modify tests. Work only inside the current repository. Before finishing, inspect the final diff, run the relevant tests, and report the evidence that the task is complete.
```

### B. CLI feature

```text
Add a --verbose flag to the CLI in toyapp/cli.py. When passed, the command should print a line containing verbose before the normal greeting.

Do not modify tests. Work only inside the current repository. Before finishing, inspect the final diff, run the relevant tests, and report the evidence that the task is complete.
```

## Predict Before the Runs Start

Compare your choice with a neighbor. Make one prediction for each row before seeing a trace.

| Question | Prediction | Why? |
|---|---|---|
| Which harness will make the fewest model calls? |  |  |
| Which harness will send the least context per call? |  |  |
| Which harness will finish first? |  |  |
| Which harness will provide the strongest completion evidence? |  |  |

Choose one trace behavior that you expect to explain the measurements:

- [ ] Amount of exploration before editing
- [ ] Size of the system instructions and tool definitions
- [ ] Number of model calls
- [ ] Amount of history carried into later calls
- [ ] Test and verifier behavior
- [ ] Recovery from a failed action

## Run the Comparison

The instructor will launch the task through OpenHands, Pi, and OpenCode. Each harness uses the same model and receives an isolated copy of the same starting repository. Agent Canvas provides the shared surface, and ACP lets the other agents run through that surface.

For the workshop setup, use a free model available through OpenHands Cloud or another model that all three harnesses can access. Configure model access separately for each harness and record the exact resolved model name in every lane. If one ACP agent cannot use that model, do not put it in the controlled table.

If you run the exercise yourself, use a separate workspace for every harness. Two editing agents must never share the same working tree.

While the agents work, do not judge the run from the final answer alone. Read each trace at the same checkpoints:

1. First repository action
2. Files inspected before the first edit
3. Plan or implementation approach
4. Failed or repeated actions
5. Tests and verifier evidence
6. Reason the harness decided to stop

## Record What Happened

Use provider-reported tokens when they are available. Do not estimate tokens from characters or file sizes.

| Harness | Passed verifier | Model calls | Context per call | Wall time | First action | Completion evidence |
|---|---:|---:|---:|---:|---|---|
| OpenHands |  |  |  |  |  |  |
| Pi |  |  |  |  |  |  |
| OpenCode |  |  |  |  |  |  |

Discuss three questions with your neighbor:

1. Did the harness with fewer model calls also use fewer tokens?
2. Did sending more context improve the result?
3. Which evidence came from the agent, and which evidence came from the harness or external verifier?

## Turn the Trace Into Evidence

The trace tells you what happened. It does not automatically give you a fair
token or cost comparison. Start with the small set of measurements below.

| Question | Record | Best source |
|---|---|---|
| Did the task work? | External verifier result | Instructor-owned verifier |
| How long did it take? | Start, finish, retries, and long waits | Agent Canvas history plus wall clock |
| How much work did the loop do? | Model calls and tool actions | Agent Canvas trace |
| What did the harness keep sending? | System instructions, enabled skills, tools, and growing history | First and later model requests, or a trace export |
| What did the provider bill? | Input, output, cache reads, and cost | Provider response or recording gateway |

With a neighbor, pick one surprising row from the live comparison and classify
it. Is it an outcome, a speed measurement, an explanation of the harness, or
something we still do not know? Write the missing evidence beside it.

OpenTelemetry tools such as Laminar help when you need to search long traces,
line up model and tool latency, or compare repeated runs. They are useful for
the instructor and for a team running its own evaluation program. They are not
the token authority by default. In our runs, provider usage and OTel did not
always agree across harnesses. When they disagree, keep the trace for behavior
and use the provider response for tokens, cache, and cost.

For a real system, you can get quite far with one saved trace, a provider
ledger, an external verifier, and a simple result table. Add OTel when the
trace is too large to inspect manually or when you need to query many runs.

## The Instructor Will Reveal a Long Project

Short tasks reveal fixed overhead, but they usually end before history and loop behavior become dominant. We also ran a prepared full-stack benchmark. The agents started from a working incident application and had to add durable SQLite storage, concurrency control, a background escalation worker, HTTP and CLI workflows, a responsive interface, and tests.

All three harnesses used GLM-5.2 on the same clean AWS instance. Provider responses supplied token and cost measurements. Laminar supplied traces. An instructor-owned verifier checked the result.

| Harness | Model calls | Context per call | Input tokens | Wall time | Provider cost | Verifier |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | 76 | 36,139 | 2.75M | 17m 40s | $0.77 | 8/8 |
| Pi | 69 | 45,858 | 3.16M | 20m 21s | $1.05 | 7/8 |
| OpenHands | 95 | 71,157 | 6.76M | 26m 42s | $2.61 | 8/8 |

One provider error and several slow responses affected the OpenHands time. They do not explain the token difference.

OpenCode made more model calls than Pi but used fewer tokens because each call was smaller. OpenHands made more calls and sent more context on every call. Its first request contained 18,506 tokens, compared with 2,749 for OpenCode and 4,197 for Pi. By the final request, OpenHands sent 97,514 tokens.

This result gives us two separate harness questions:

1. How often should the harness call the model?
2. How much context should it send with each call?

## Run or Adapt the Long Project Later

The incident project takes roughly 20 to 30 minutes per harness in the measured environment. Budget up to 90 minutes for an unfamiliar machine or provider.

Use this procedure:

1. Configure every harness to use the same model, endpoint, and model settings.
2. Copy the committed `starter/` directory into one clean workspace per harness.
3. Start a new conversation with empty harness memory and send the exact `task.md` prompt.
4. Use the same permissions, network policy, timeout, and repair policy for every run.
5. Save the complete conversation history and provider usage for each model call.
6. Run `verify_incident_ops.py` outside the agent workspace after the harness stops.
7. Record wall time, model calls, input and output tokens, cache reads, cost, tool actions, and verifier results.
8. Change one harness behavior at a time if you run a follow-up experiment.

The [optional long-project lab](/workshops/odsc-2026/long-project) includes the exact prompt, the starter application, the verifier, and guidance for adapting the benchmark to your own application. The repository also contains the [measurement protocol](https://github.com/rajshah4/learn-openhands-harness/blob/main/workshops/odsc-2026/experiments/harness-suite/MEASUREMENT-PROTOCOL.md) and the [complete measured report](https://github.com/rajshah4/learn-openhands-harness/blob/main/workshops/odsc-2026/evidence/harness-suite/20260824-aws-incident-v2.md).

## Add the First Decision to Your Harness

Complete the opening section of the [decision worksheet](/workshops/odsc-2026/worksheet):

```text
I trust a coding-agent result when the trace shows:

The harness, rather than the model alone, supplied:

The first efficiency measurement I would add is:
```
