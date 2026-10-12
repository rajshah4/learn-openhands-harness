# Workshop 3 v2 fresh AWS results

Model: `openhands/deepseek-v4.1-flash`. Agent Server/SDK: `1.49.6`. History: **simulated**.

All conditions received the same task, starter source, accepted design records and prior implementation. The changed variable was explicitly supplied project notes. Product memory and skills were disabled and verified in resolved launch settings.

| Condition | Independent contract | External full suite | Agent focused then full | Median time (range) |
|---|---:|---:|---:|---:|
| no-guidance | 3/3 | 3/3 | 3/3 | 100.6s (80.5 to 215.6) |
| outdated | 3/3 | 3/3 | 3/3 | 135.6s (80.4 to 175.5) |
| current | 3/3 | 3/3 | 3/3 | 85.4s (80.4 to 95.4) |

## All trials

| Block | Condition | Status | Independent | Seconds | Tools | Provider calls | Input | Cached input | Output |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | no-guidance | finished | pass | 215.6 | 20 | 24 | 412471 | 389760 | 10504 |
| 1 | outdated | finished | pass | 175.5 | 11 | 12 | 170822 | 150016 | 5182 |
| 1 | current | finished | pass | 95.4 | 11 | 14 | 198876 | 177280 | 6172 |
| 2 | outdated | finished | pass | 135.6 | 13 | 17 | 269470 | 236032 | 6382 |
| 2 | current | finished | pass | 85.4 | 14 | 15 | 225780 | 207872 | 5898 |
| 2 | no-guidance | finished | pass | 100.6 | 19 | 20 | 326554 | 298496 | 8049 |
| 3 | current | finished | pass | 80.4 | 14 | 10 | 156095 | 134528 | 5966 |
| 3 | no-guidance | finished | pass | 80.5 | 14 | 15 | 220038 | 196736 | 6358 |
| 3 | outdated | finished | pass | 80.4 | 13 | 9 | 127198 | 110336 | 5441 |

## Interpretation

Report API alignment, cursor behavior, compatibility and testing separately. Passing agent-authored tests does not substitute for the independent checks. Source review and exact commands are retained in review-audit.json.

Time and tokens are descriptive observations from three trials per condition. There is no reliable speed claim. Cached input is part of total input, not an extra token total. Response-reported cost is retained as metadata and is not an invoice.

The failed local credential attempts and AWS setup attempts are archived separately and excluded from this comparison. Their unchanged starters failing the new-feature gate are not coding failures. Historical September results are also separate.

Every condition passed 3/3. This task did not demonstrate a correctness advantage from supplied project notes or a stale-guidance failure. The current decisions and sibling implementation were readily discoverable. That null finding should be presented plainly.

## Observed implementation decisions

All nine defined the new public API in toyapp.pagination, added the thin catalog
caller, reused the existing token logic, and left the existing pagination
definitions unchanged. No new cursor module appeared and no package metadata
changed. All current records were preserved. The frozen result contract passed
in every trial; this is a concrete convention check, not a general style score.

All three older-note final reports explicitly identified the superseded separate
module/decimal-token guidance and followed decisions 002/003. Their complete
reports, exact source diffs and traces are retained beside verification.json.
The source-review heuristics were checked against the code; the testing sequence
was reviewed from actual commands, rather than the legacy full-suite counter.

Guidance sizes were 0, 133 and 132 words. This contrast concerns saved decisions,
not a long-prompt versus short-prompt intervention. Neither current nor older
notes denied an agent access to later accepted evidence.

Median tool actions were 19 without notes, 13 with older notes and 14 with current
notes. Median processed input-plus-output tokens were 334,603, 176,004 and 205,048.
These are sample observations. In particular, older notes used fewer median
provider calls than current notes (12 versus 14), while their elapsed median was
longer. Provider latency, model behavior, caching and the small sample limit a
speed conclusion. Setup warm-up requests were retained separately, not controlled
as a cold-cache performance experiment.

## Workshop conclusion

Make accepted decisions discoverable, and link saved notes to their reasons and
current source. In this tested small repo, every condition found and followed
the accepted design. There was no correctness or testing-workflow advantage
from always supplying the refreshed summary. The old notes were successfully
reconciled. General memory-maintenance advice should be stated separately from
these measured findings.

## Workshop efficiency takeaway

Saved project memory helped the agent reach the same correct result with fewer
tokens and less time in this experiment. Current notes versus no notes reduced
median input-plus-output tokens by 39% (334,603 to 205,048) and median elapsed
time by 15% (100.6s to 85.4s). Uncached input decreased 7% and output decreased
26%; most input was cached, so the 39% is not a token-cost reduction. Older
notes had a still lower median total token count (176,004). These are medians
from three trials per condition, with overlapping time ranges.
