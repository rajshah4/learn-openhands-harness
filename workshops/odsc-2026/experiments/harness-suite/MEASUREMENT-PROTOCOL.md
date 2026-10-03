# Harness Benchmark Measurement Protocol

## Status

This protocol replaces the earlier practice of choosing different native files
or a tracing summary as the cross-harness token source. The runs collected on
August 22 are exploratory. They must not be used for quantitative harness
claims until this protocol passes calibration.

## What We Are Measuring

Agent Server's native `LLM.metrics` record is a useful transport record, but
not by itself a standardized token source. Native OpenHands populates it from
LiteLLM responses. ACP harnesses populate it from `PromptResponse.usage`
returned by their ACP servers. The installed Agent Server SDK records input,
output, cache-read, cache-write, and reasoning tokens from those inputs.

The reported fields can still have different origins and meanings. In the
August 23 investigation, native OpenHands used LiteLLM-normalized proxy HTTP
usage, Pi used Pi session-RPC statistics, and OpenCode used harness-local
SQLite statistics. In particular, their input and cache fields did not share
one schema. A field that is absent for a completed request is `unknown`, never
zero cache use.

For each run, report these fields separately:

- `fresh_input_tokens`: input tokens that were not read from cache
- `cache_read_input_tokens`: cached input tokens, when the provider reports them
- `cache_write_input_tokens`: cache creation tokens, when reported
- `output_tokens`: all generated output tokens
- `reasoning_tokens`: the reasoning subset, when reported
- `provider_total_tokens`: the provider's total, without recomputing its billing semantics
- `elapsed_seconds`: wall-clock time from accepted task submission to terminal state
- `measured_turn_count`: native token-usage records

Only derive a cross-harness model-work metric when every harness has the same
provider-boundary ledger and the same documented field semantics:

```text
processed_tokens = fresh_input_tokens + cache_read_input_tokens + output_tokens
```

Only derive it when the provider clearly identifies cached input as a subset or
alternative category. Never add cache tokens to a provider total unless the
provider's schema explicitly says they are excluded.

Cost is a separate metric. Cached and uncached tokens can have different prices,
so a token total is not a substitute for a bill.

## Native Measurement Boundary

Agent Canvas and Agent Server remain the execution boundary. Save the complete
native `usage_to_metrics` object for every `(run_id, task_id, harness, attempt)`
tuple as diagnostic evidence. For cross-harness token comparison, also save one
provider-boundary ledger with a common raw response-usage schema. Do not infer
comparability merely because the values arrived in the same Agent Server field.

The saved record must contain:

- benchmark identity and harness
- the complete native accumulated token usage
- the complete native per-turn `token_usages` list
- native cost and response-latency records
- model and ACP profile identity
- start time, terminal time, and runner-measured wall time
- prompt, starter-tree, configuration, and version hashes

Pi session files, OpenCode's database, Codex ACP usage, and Laminar traces are
reconciliation sources. They are not allowed to overwrite the native record.
Use a transparent provider proxy as the common ledger when adapter-native
metrics have different schemas or cache semantics.

## Controlled Comparison

A harness-only comparison requires:

1. The same model identifier and provider endpoint.
2. The same model parameters, including reasoning level and maximum output.
3. The same committed starter tree and exact task prompt.
4. Empty harness memory and a new conversation.
5. The same tool permissions, network policy, timeout, and repair policy.
6. No title-generation, evaluator, or repair calls inside the primary total.
7. A separate ledger for setup, primary attempt, and each repair attempt.

If the model differs, label the result a full-system comparison. Token counts
from different tokenizers are descriptive, not a clean measure of harness
efficiency. Report time, success, cost, and model identity alongside them.

## Calibration Ladder

Do not run the task suite until all four levels pass.

### C0: Native OpenHands control

Run a fixed two-turn cache-eligibility request through native OpenHands. The
second turn must reuse a long stable prefix. Save the raw provider usage,
LiteLLM-normalized usage, and Agent Server per-call and accumulated metrics.
Confirm that their sums agree exactly and that a missing cache field is marked
`unknown`. If the provider reports cache usage but a downstream field is zero,
fail calibration.

### C1: ACP one-turn control

Run one fixed turn through each ACP harness. Confirm that Agent Server receives
nonzero `PromptResponse.usage`, saves one token-usage record, and exposes the
same values in Agent Canvas. Missing ACP usage is a hard failure.

### C2: Scripted multi-call control

Run exactly three user turns through each harness. Confirm:

- three native per-turn usage records
- exact agreement between accumulated metrics and the sum of those records
- a repair turn is separated rather than silently folded into the first attempt

### C3: One microtask per harness

Run the smallest code-edit task once through OpenHands, Pi, and OpenCode using
the same model. For each harness:

- every completed prompt has a native usage record
- every token comparison field comes from the shared provider-boundary ledger
- adapter-native and trace counters are retained only as reconciliation evidence
- the task passes the verifier

The acceptance tolerance for token integers is zero. A counter may be excluded
only when its semantics differ and the difference is documented.

### C4: Repeatability

Repeat the microtask at least three times per harness. Publish the raw trials,
median, range, and first-pass success. Do not claim a stable harness ranking
from one stochastic run.

## Publishability Gate

A run is publishable only when all of these are true:

- provider-boundary usage coverage is 100 percent for completed prompts
- all published usage fields have the same documented schema across harnesses
- model, endpoint, parameters, prompt hash, starter-tree hash, and versions are saved
- setup, primary attempt, and repair totals are separated
- elapsed-time boundaries are recorded by the runner, not inferred from UI events
- the raw ledger and a content-free summary are retained

If any condition fails, report tokens as `unavailable`. Never report zero for
missing telemetry.

## Codex Policy

ChatGPT-authenticated Codex ACP does not pass token usage through the Laminar
parent trace in this setup. It does return ACP usage to Agent Server, which is
why Agent Canvas reported 18,785 tokens in the calibration run. That native ACP
record can enter the measurement protocol after C1 and C2 validate its behavior.

Because Codex uses a different model from the GLM lanes, include it only in a
separately labeled full-system comparison. Its token count is descriptive, not
evidence of harness-only efficiency.

## Why The Previous Totals Failed

The August 22 long-task run produced incompatible accounting for the same
sessions. For the spread-plate task:

| Harness | Native input | Native cache read | Native output | Native accounted total | Laminar input | Laminar output | Laminar total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Pi | 42,005 | 271,955 | 15,086 | 329,046 | 274,584 | 15,086 | 289,670 |
| OpenCode | 103,909 | 709,056 | 18,817 | 831,782 | 814,748 | 24,219 | 838,967 |

The Pi records disagree on fresh input. The OpenCode records disagree on input,
output, and the cache breakdown. This proves that selecting Laminar's aggregate
does not by itself create a standardized measurement.

## Next Experiment

Modify the runner to preserve complete Agent Server metrics without replacing
ACP values. Then run C0 through C2 in native Agent Canvas and run only
`p09-task-01`. Do not run either long benchmark until C0 through C4 pass. Build
a transparent provider proxy only if the native metrics fail these gates.

## References

- [OpenHands SDK metrics tracking](https://docs.openhands.dev/sdk/guides/metrics.md)
- [OpenHands SDK observability and tracing](https://docs.openhands.dev/sdk/guides/observability.md)
- [OpenAI Codex advanced configuration](https://developers.openai.com/codex/config-advanced)
- [OpenAI Codex CLI reference](https://developers.openai.com/codex/cli/reference)
