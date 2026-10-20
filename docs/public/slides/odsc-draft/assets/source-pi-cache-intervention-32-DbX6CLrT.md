# Sonnet harness comparison and Pi cache-control experiment

## Question

The first Pi + Sonnet trial reported zero cached input while OpenHands and
OpenCode received substantial Sonnet cache reads. Was that a measurement
failure, a provider incident, or a difference in how the harness called the
model?

The provider-boundary ledger showed that the zero was real. Every successful
Pi response included an explicit cache field with `cached_tokens: 0`. The Pi
requests contained no `cache_control` markers. OpenCode's requests did contain
those markers, and the provider returned cache reads.

We therefore added Pi's documented
`cacheControlFormat: "anthropic"` compatibility option, passed the three-turn
cache calibration, and reran the full Incident Operations Center project.

## Sonnet results across harnesses

All cells used Claude Sonnet 4.5 through the same OpenHands provider on the
same clean AWS host. They used fresh workspaces, zero repair rounds, the same
task, and the same external verifier. These are harness-default comparisons;
some harness-specific request parameters can still differ.

| Harness | Quality | Time | Calls | Tool actions | Input | Fresh input | Cache rate | Output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenHands | 7/8 | 12m 24s | 66 | 65 | 4.26M | 98K | 97.7% | 42.5K |
| Pi, default | 7/8 | 14m 44s | 89 | 88 | 3.35M | 3.35M | 0.0% | 49.5K |
| OpenCode | 6/8 | 15m 52s | 75 | 82 | 4.15M | 87K | 97.9% | 82.6K |
| Pi, cache enabled | 6/8 | 16m 49s | 89 | 88 | 3.84M | 213K | 94.5% | 58.3K |

The provider did not report comparable Sonnet cost fields, so cost is
unavailable rather than zero.

## Plain-language conclusion

On this long benchmark, OpenHands worked much better with Sonnet than with
GLM-5.2. Sonnet completed the OpenHands run in 66 model calls and 12 minutes,
while the two GLM trials required 95 to 129 calls and 17 to 27 minutes. Sonnet
also used 4.26 million input tokens, compared with 6.76 to 10.20 million for
GLM.

Pi and OpenCode did not receive the same broad efficiency improvement from
switching models. This suggests Sonnet is a better match for the way OpenHands
structures its instructions, tools, and agent loop. The shorter path still had
a quality tradeoff: it passed seven of eight checks but stopped without finding
a frontend defect.

## What changed when Pi enabled cache control

| Metric | Pi default | Pi cache enabled |
| --- | ---: | ---: |
| External checks | 7/8 | 6/8 |
| Elapsed time | 883.6s | 1009.5s |
| Model calls | 89 | 89 |
| Tool actions | 88 | 88 |
| Provider input | 3,351,630 | 3,841,953 |
| Cache reads | 0 | 3,628,953 |
| Cache writes | 0 | 76,279 |
| Fresh input | 3,351,630 | 213,000 |
| Output | 49,514 | 58,324 |
| Provider errors | 0 | 0 |

The configuration change fixed caching. The calibration produced positive
cache reads on turns two and three, and the long run read 94.5 percent of its
input from cache. Fresh input fell by about 94 percent relative to the default
Pi trial.

Caching did not change Pi's loop length. Both independent trials made exactly
89 model calls and 88 tool actions. The cache-enabled trial was slower because
this particular trajectory generated more context and output and spent about
85 additional seconds waiting for provider responses. This is ordinary run
variation, not evidence that caching made the agent slower.

Caching also did not improve correctness. Both runs missed the concurrent
deduplication requirement. The cache-enabled run additionally left the
browser-feedback element empty, producing a 6/8 result. The original automated
record initially said the browser dependency was unavailable; we installed
the verifier dependency and repeated that check, confirming the frontend
failure. The quality difference should be treated as independent model-run
variation, not as an effect of caching.

## Interpretation

This is a model-by-harness interaction.

Pi + GLM-5.2 received a 97.5 percent cache-read rate in the original incident
benchmark. Pi + Sonnet received zero until the Sonnet request path explicitly
added Anthropic-style cache markers. OpenCode and OpenHands already produced
cacheable Sonnet requests in this setup.

The lesson is not simply that one harness caches and another does not. A
harness can work efficiently with one model/provider contract and miss an
important optimization with another. Cache behavior must be calibrated for
each harness and model combination before comparing cost.

The experiment also separates two different harness concerns:

- Cache controls affect how much repeated context is billed as fresh input.
- The agent loop determines how many calls it makes, what it puts in context,
  which checks it runs, and whether the result is correct.

Fixing the first did not change the second.

## Evidence

- `raw/reruns/20260824-aws-sonnet-pi-cache-enabled-c0.json`
- `raw/reruns/20260824-aws-incident-sonnet-v1-pi.json`
- `raw/reruns/20260824-aws-incident-sonnet-v2-pi-cache-enabled.json`
- `raw/reruns/20260824-aws-incident-sonnet-v2-pi-cache-enabled-verification-audit.txt`
- `provider-ledgers/20260824-aws-incident-sonnet-pi-cache-comparison-ledger.jsonl`
- OpenHands repeat: `incident-repeat-trials.md`
