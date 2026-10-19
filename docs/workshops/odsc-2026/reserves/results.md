> Archived original exercise material. For the current classroom sequence, return to the [workshop index](/workshops/odsc-2026/). These tasks differ from the revised selections.

# Saved results

Make your prediction before reading the reveal. These are selected receipts,
not new runs of the portable package. Historical environments, prompts, models,
and fixture sizes differ. Missing usage is unknown. Sources are preserved in
`workshops/odsc-2026/labs/evidence/` and `SOURCE-MANIFEST.json`.

## Exercise 1

<details>
<summary>Open the recorded example after trying the exercise</summary>

October 3, 2026, one classroom pagination run per harness. The OpenHands usage
receipt resolves to DeepSeek V4.1 Flash; the ACP usage receipts do not establish
a complete resolved-model record in this package. Legacy GLM labels in the
archived paths are case names, not evidence of the model used. All three
passed. OpenHands recorded 3 tool requests, Pi 9, and OpenCode 5. A request can
bundle commands. Only OpenHands has complete cumulative usage; Pi has none and
OpenCode's reported usage scope is unestablished. Do not compare their token
totals or infer a general speed ranking. Inspect `evidence/w1.json` and the [action excerpts](/workshops/odsc-2026/inspection).

</details>

## Exercise 2

<details>
<summary>Open the recorded example after trying the exercise</summary>

The source excerpt is `evidence/w2-report.md`.

September comparison, Sonnet 4.6, three trials per configuration:

| GitHub interface | Evidence coverage, out of 6 | Median tool calls | Median fresh input |
|---|---:|---:|---:|
| Terminal/API | 4 | 6 | 32,006 |
| Four operations | 6 | 11 | 42,800 |
| Twelve operations | 6 | 12 | 48,741 |
| Evidence bundle | 6 | 1 | 18,706 |

The eight extra GitHub operations were unused. The bundle was designed by the
experimenter for this workflow and rubric. It selects three largest production
changes and two largest test changes from the first page of files; it can omit
important smaller files or later pages. Retain a fallback to primitive reads.
The classroom attribution task is a separate October prompt, not a matched
September trial. `tools/github_mcp_server.py` preserves the real collection code.

</details>

## Exercise 3

<details>
<summary>Open the recorded example after trying the exercise</summary>

The full per-trial report is `evidence/w3-report.md`.

October 9 fresh AWS matrix, DeepSeek V4.1 Flash, three trials per condition.
All nine passed public API and compatibility checks. Older-note agents followed
newer accepted records rather than blindly copying obsolete design.

| Condition | Independent pass | Median total processed tokens | Median elapsed seconds | Time range |
|---|---:|---:|---:|---|
| No notes | 3/3 | 334,603 | 100.6 | 80.5 to 215.6 |
| Older notes | 3/3 | 176,004 | 135.6 | 80.4 to 175.5 |
| Current notes | 3/3 | 205,048 | 85.4 | 80.4 to 95.4 |

Current notes used 39% fewer median processed tokens than no notes. Most input
was cached, so this is not a 39% cost saving. Time ranges overlap. No correctness
advantage was observed. The package imports the current starter (trailing blank lines normalized), supplied
notes, task, and independent checker; it does not measure native memory loading.

</details>

## Exercise 4

<details>
<summary>Open the recorded example after trying the exercise</summary>

The source excerpt is `evidence/w4-report.md`.

September 7, three trials per policy on four tasks. Economical: Haiku 4.5;
stronger: Opus 4.8. These are historical model labels, not setup requirements.

| Policy | Original check passes | Median four-task provider bill | Median wall seconds |
|---|---:|---:|---:|
| Strongest everywhere | 12/12 | $0.883 | 116.2 |
| Economical everywhere | 9/12 | $0.247 | 251.9 |
| Risk-aware static | 12/12 | $0.517 | 205.7 |
| Adaptive cascade | 11/12 | $0.628 | 210.9 |

The historical rubric required a timing-safe comparison discussion, which
cheap-only omitted in these security reviews. Treat that as a rubric criterion:
when exploring the source yourself, discuss whether the proposed fix applies
to this middleware rather than judging quality by keyword presence.
The source uses dictionary membership, which does not establish an exploitable
timing attack. Missing that rubric topic is not proof of missing a demonstrated bug.
The static route was selected on this task set; transfer is untested. The
cascade used an LLM judge and different attempt budgets. The portable
verify-then-escalate practice is a new design to evaluate, not a proven result.

</details>

## Exercise 5

<details>
<summary>Open the recorded example after trying the exercise</summary>

October 9 native probes used Flash and an outer cap of two audits. Repair
allowed: complete at audit one; original tests and independent dot assertion
passed. Constructed no-edit probe: missing after audit one, continued, then
capped at audit two. Five original tests passed while the dot assertion failed.
The no-edit constraint makes completion deliberately impossible.

Inspect `w5-complete-events.json`, `w5-capped-events.json`, and their verifier
text files. Historical interpreter paths are provenance, not commands for your
laptop. Judge verdicts and independently executed assertions are separate.
Neither probe demonstrates improvement over ordinary repair, enforceable file
boundaries, or restart persistence.

</details>

## Exercise 6

<details>
<summary>Open the recorded example after trying the exercise</summary>

October 2 matched-ceiling pair, Flash, one observation per condition. Both
had byte-identical historical starters and a combined 30-model-call ceiling.

| Architecture | Result | Calls | Total provider tokens | Agent wall seconds |
|---|---|---:|---:|---:|
| One generalist | PASS | 8 | 91,255 | 34.52 |
| Repair owner plus validator | PASS | 15 | 181,347 | 62.65 |

External verification took about 3.18 seconds separately. Tokens include all
parent and child input, cached input, and output. The validator ran after the
repair and returned 142 words. No parallel implementation or correctness gain
was observed. `evidence/w6.json` preserves measurements and starter hashes,
including a separate parallel-specialist observation; keep it outside this pair.
The portable focused async fixture differs from the larger historical starter.
Its validator brief uses a 250-word return limit; the historical pair used 350.

</details>
