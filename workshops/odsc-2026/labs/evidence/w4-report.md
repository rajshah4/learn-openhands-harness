# Workshop 4 preliminary result: route risk, then verify the work

## Slide-ready result

Workshop 4 is the model-routing workshop. Its decision is not simply which
model is best. It asks where to spend stronger-model capacity, when escalation
helps, and what evidence must sit outside the model.

Across three fresh trials, risk-aware static routing passed all 12 task runs
while cutting the median four-task bill from $0.883 to $0.517, a 41.5% savings
versus using the strongest model everywhere.

| Median across 3 fresh trials | Strongest everywhere | Economical everywhere | Risk-aware static | Adaptive cascade |
|---|---:|---:|---:|---:|
| External verifier passes, all 12 runs | **12/12** | 9/12 | **12/12** | 11/12 |
| Median tasks passed per trial | **4/4** | 3/4 | **4/4** | **4/4** |
| Median billed provider cost per trial | $0.883 | **$0.247** | $0.517 | $0.628 |
| Savings versus strongest | baseline | 72.0% | **41.5%** | 28.9% |
| Median wall time per trial | **116.2s** | 251.9s | 205.7s | 210.9s |
| Escalations across all trials | 0 | 0 | 0 | 4 |

The strongest model won on speed because it usually finished in fewer calls.
The cheap-only policy won on cost, but failed the security-review rubric in all
three trials. Risk-aware static routing was the best operating point for this
task set: full verified reliability at substantially lower cost. That result
does not make risk-aware static routing the default answer for every system.

The adaptive cascade was not the winner. It spent more than risk-aware static,
escalated the async task in all three trials, escalated an already simple
pagination fix once, and still missed one security-review requirement. Its
11/12 result is a warning about escalation signals, not evidence that cascades
are inherently worse.

## Task-level result

| Policy and model path | Rename | Pagination bug | Async race | Security review |
|---|---:|---:|---:|---:|
| Strongest, frontier on all tasks | 3/3 | 3/3 | 3/3 | 3/3 |
| Economical, cheap on all tasks | 3/3 | 3/3 | 3/3 | **0/3** |
| Risk-aware static, cheap/cheap/cheap/frontier | 3/3 | 3/3 | 3/3 | 3/3 |
| Adaptive cascade | 3/3 | 3/3 | 3/3 | 2/3 |

Median billed cost by task shows why the static route worked:

| Task | Strongest | Economical | Risk-aware static | Adaptive cascade |
|---|---:|---:|---:|---:|
| Rename | $0.177 | $0.038 | $0.035 | $0.040 |
| Pagination bug | $0.134 | $0.045 | $0.045 | $0.040 |
| Async race | $0.245 | $0.078 | $0.076 | $0.169 |
| Security review | $0.339 | $0.094, failed | $0.359 | $0.354 |

The cheap model solved the hard-labeled async race 3/3 when it received a fair
attempt budget. The task's label did not justify escalation by itself. The
security review did justify stronger pre-routing because its output had to
cover six independent security requirements, and the cheap model omitted the
timing-safe comparison requirement in every trial.
