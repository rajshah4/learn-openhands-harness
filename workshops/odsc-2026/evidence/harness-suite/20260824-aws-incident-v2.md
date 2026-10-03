# AWS full-stack incident project comparison

Date: 2026-08-24 UTC

## Bottom line

The genuine long project changed the ranking seen on the two medium projects. Pi still made the fewest model calls, but OpenCode sent less context on each call and finished with the lowest token use and provider cost. OpenHands made the most calls, sent the most context per call, and cost more than twice as much as Pi.

The project also exposed two things a short benchmark would have missed:

- an unbounded self-test can strand an otherwise productive agent run
- a hidden verifier can be wrong even after a successful calibration

## Corrected results

Provider-returned usage is the token and cost source of truth.

| Harness | Contract-adjusted quality | Time | Model calls | Context sent per call | Input tokens | Output tokens | Cache reads | Fresh input | Cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenCode | 8/8 | 17m 40s | 76 | 36,139 | 2,746,582 | 39,881 | 2,545,803 | 200,779 | $0.768 |
| Pi | 7/8 | 20m 21s | 69 | 45,858 | 3,164,231 | 58,377 | 3,084,032 | 80,199 | $1.054 |
| OpenHands | specified behavior passed | 26m 42s | 95 | 71,157 | 6,759,904 | 49,952 | 4,888,395 | 1,871,509 | $2.614 |

OpenHands had one provider HTTP 502 that its loop recovered from. OpenCode and Pi had no provider errors. The elapsed times are real end-to-end times, but OpenHands' timing includes the failed request and multiple unusually slow provider responses.

## Why OpenCode used fewer tokens than Pi

Pi made seven fewer model calls, but each Pi call carried about 27 percent more context than an OpenCode call. The larger calls outweighed the smaller call count:

- Pi sent 15 percent more input tokens than OpenCode.
- Pi cost 37 percent more than OpenCode.
- Pi had the highest cache-read rate, about 97 percent, so most of that context was discounted cached input.

This is the key long-project lesson: call count is not enough. The amount of context sent on each call can reverse the result.

## Why OpenHands cost more

Compared with OpenCode, OpenHands made 25 percent more successful model calls and sent almost twice as much context per call. Those effects compounded:

- 2.46 times the input tokens
- 3.40 times the provider cost
- 1.51 times the elapsed time

OpenHands did receive substantial provider cache reads. The provider reported 4.89 million cached input tokens, so the earlier `cache_read=0` result is not a real no-cache condition. Its cache-read rate was still lower than the ACP harnesses, at about 72 percent versus 93 percent for OpenCode and 97 percent for Pi.

## Quality and verifier correction

The raw result files report 7/8 for OpenCode, 6/8 for Pi, and 7/8 for OpenHands. Those raw scores are preserved, but two hidden-verifier assumptions were not fair:

1. The escalation check left an old claimed incident in the database before testing `run_once`. OpenCode and Pi correctly selected that older overdue incident instead of the newly created one the verifier expected. Isolating the worker scenario in a fresh database made both pass.
2. The original task required `EscalationWorker.run_once` but did not specify its return type. OpenHands returned `true` after successfully escalating and persisting the incident. The verifier assumed an `Incident` object and crashed. A separate behavioral audit confirmed the correct incident reached escalation level 1.

The task now explicitly requires:

```python
run_once(now=None) -> Incident | None
run_until_idle(max_incidents=None, now=None) -> list[Incident]
```

The remaining Pi failure is real. Its page included two elements with `data-testid="incident-detail"`, violating the stable browser-marker contract and causing strict selection to fail.

## The invalid first attempt

The first official attempt is excluded from every comparison number. Pi and OpenHands independently wrote HTTP tests that constructed a server but never started its request loop. Their test commands then blocked forever. Pi was rescued once, repeated the same unbounded command, and was stopped. OpenHands reproduced the same trap.

The starter code already required callers to invoke `serve_forever`, but that contract was not stated clearly enough in the task. The corrected task says that `create_server` returns an unstarted server, HTTP tests must start it in a background thread, and potentially blocking checks need explicit time limits. Under that corrected task, all three harnesses completed without operator intervention.

This invalid attempt should remain in the workshop as a long-running-agent case study. Participants can choose among:

- let the command run indefinitely
- impose a tool timeout and return control to the agent
- use a supervisor that detects no-progress periods and pauses for approval

The reveal is that timeouts are not merely infrastructure. They change whether the agent can observe a failure, revise its approach, and finish.

## What Laminar added

Laminar produced a complete trace for every corrected cell. It is valuable for viewing the sequence of model and tool actions, but it is not a consistent token authority across these harnesses.

| Harness | Provider input | Laminar input | Provider output | Laminar output | Provider cache reads | Laminar cache reads |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenCode | 2,746,582 | 2,746,582 | 39,881 | 39,881 | 2,545,803 | 2,545,803 |
| Pi | 3,164,231 | 3,087,205 | 58,377 | 58,377 | 3,084,032 | 3,084,032 |
| OpenHands | 6,759,904 | 6,349,180 | 49,952 | 59,116 | 4,888,395 | 0 |

OpenCode's Laminar token fields reconciled exactly, although its Laminar cost used a different pricing calculation. Pi's Laminar trace missed 77,026 input tokens. OpenHands disagreed on input and output and again showed zero cache reads despite the provider reporting 4.89 million.

The operating rule remains:

- use Laminar to understand what the agent did
- use provider-returned usage to compare tokens and cost

## Workshop exercise

This project is too long to run from scratch during a two-hour workshop. Use a prepared three-lane Agent Canvas history and let pairs make decisions at three checkpoints:

1. Before the run: predict whether fewer calls or smaller calls will matter more.
2. At the blocked-test trace: choose a timeout, supervisor, or wait policy.
3. Before the reveal: decide whether to trust the agent's tests, the hidden verifier, or both.

Then reveal the provider table, the Pi browser defect, and the verifier corrections. The worksheet takeaway is that a production harness needs loop controls, bounded tools, external verification, and evaluator audits in addition to a capable model.

## Reproducibility

- Environment: temporary clean AWS EC2 instance, Agent Canvas 1.15.0, Agent Server 1.42.1
- Model: GLM-5.2 for all harnesses
- Harnesses: Pi ACP, native OpenHands, OpenCode ACP
- Repair feedback: disabled
- Corrected run IDs: `20260824-aws-incident-v2-{harness}`
- Raw result JSON: `runs/20260824-aws-incident-v2-*.json`
- Raw provider ledger: `ledgers/20260824-aws-long-projects-ledger.jsonl`
- Scrubbed Agent Canvas histories: `canvas-state/20260824-aws/`
- Legacy-return audit: `experiments/incident-operations-center/audit_legacy_worker_return.py`

The three result files and provider ledger were copied locally and checksum-verified against the AWS originals. Raw verifier outputs remain unchanged; the corrections are documented rather than written back into the evidence files.
