# Workshops 5 and 6: evidence and design decisions

October 9, 2026. Canonical deck remains 299 pages. Workshop 5 pages 120–126 and Workshop 6 pages 145–152 retain their stable slide IDs. This revision edits only W5–6. Concurrent user-authorized slides 46–48 and Workshop 3 memory edits in the main talk-track chat were preserved. All other lecture slide blocks remain unchanged from the initial snapshot.

## Workshop 5 uses the actual native feature

The selected October case `flash-classroom-goal-dot_missing-Sonnet46` was launched with an ordinary initial message, `run: true`, and an inner 40-step cap. Its settings and provider ledger resolve to DeepSeek V4.1 Flash despite Sonnet46 in the case name. No native goal activation or goal state events occur in that saved run. The October classroom recording’s red/green evidence remains valid: 1 failed + 5 passed, exit 1 before implementation repair; 6 passed, exit 0 afterward; external check passed. Its process is not evidence of a native goal mechanism. The selected API take separately added two tests (2 failed/5 passed → 7 passed); those counts are not substituted into the recording.

Native mechanism verified against the [official goal guide](https://docs.openhands.dev/sdk/guides/convo-goal), AWS `/server_info`, and `/openapi.json`. AWS Agent Server and SDK are 1.49.6. The native API starts the outer judge-driven loop inside an existing conversation; it does not fork. The agent works inside an inner run. After that run stops, a separate judge evaluates the transcript, returns complete/missing, and either sends the missing requirement back or records complete/capped. The judge is an LLM, not an enforced executable verifier.

### New experiments, not saved October 2 results

Two fresh workspaces were reconstructed from the selected saved baseline archive. Neither reused a completed workspace. Both used Flash, the dot objective, a 30-step inner limit, and native `POST /api/conversations/{id}/goal` with `max_iterations: 2`. The cap counts goal audits, not code repairs, model calls, tokens, or time. Existing gateway credentials were retrieved in memory through the retained driver; secrets are redacted in saved settings and events. The new sanitized provider ledger contains 17 forwarded requests, all resolving to deepseek-v4.1-flash.

- **Repair allowed:** conversation `eed0b720-ef10-48c5-abcc-1a31aa3a4132`. Goal running event `f1fee41d-1bf7-4616-a450-52cfe5f66303`; complete at audit 1 event `b806335e-9822-45c0-8d41-d76b71a200c6`. Five original tests pass; independent dot assertion returns `api.v1-endpoint`, exit 0. Only source regex changed. This probe did not add a regression test; the recorded older repair supplies the red/green example.
- **Constructed cap:** conversation `2ae1e3c7-0b77-4913-8130-21a35ad3e9fd`. Source/test edits explicitly prohibited on the missing-dot fixture. First missing verdict event `98c75c0e-21d7-4613-8384-ad14b6eea4e3`. Automatic user follow-up `dc337067-00bc-4bbc-9291-1429522b5ee9` returns the missing dot evidence to another run. Final capped event `6c7ed31a-b7ce-4316-8e1a-179d7b432600` at audit 2. Five original tests still pass; the independent dot assertion returns `apiv1-endpoint`, exit 1. Source diff remains empty. This is deliberately unsatisfiable under its no-edit constraint, not a naturally failed repair or performance comparison.

Read [repair goal events](w56-evidence/native-goal/complete/goal-events.json), [repair verifier](w56-evidence/native-goal/complete/verifier.txt), [capped goal events](w56-evidence/native-goal/capped/goal-events.json), [capped verifier](w56-evidence/native-goal/capped/verifier.txt), and the [driver](w56-evidence/native_goal_probe.py). Exact objectives, sanitized settings, events, and diffs are beside those records. Goal state values are explicitly retained; the older generic scrubber incorrectly redacted all state-update values except an allowlist, so the probe collector preserves the safe `goal` value as well.

The practical decision is to define objective, independently executed verifier, current evidence/workspace version, useful progress, continuation, and terminal states. The native probes measure continuation, completion, and an audit cap. Progress-sensitive replanning/escalation, token/time enforcement, file-access enforcement, and restart persistence remain policy designs or untested properties. A judge score is not a percentage of verified criteria. The constrained second audit repeats an unchanged failure; that illustrates why a separate progress policy can prevent waste. No goal-versus-no-goal improvement is claimed, so a performance comparison is not required.

## Workshop 6 restores one agent versus two

Use saved October 2 `native-task-matched-30-calls-async-repair-generalist` versus `native-task-matched-30-calls-async-repair-worker-validator`. All archived starter file hashes match, including source, tests and metadata. Git commit IDs differ because separate repositories were committed independently; content is identical. Common task text, protected tests, verifier and resolved Flash model match. The architecture instruction changes; settings expose the native task tool in both lanes, but the generalist is instructed not to use it. No dependency installation occurs inside timing. The gateway enforces a shared total 30-call ceiling, including children.

| Recorded condition | External result | Model wall time | External verification | Calls | Provider tokens |
| --- | --- | ---: | ---: | ---: | ---: |
| One agent | PASS | 34.5193 s | 3.1794 s | 8 | 91,255 |
| Worker + validator | PASS | 62.6457 s | 3.1585 s | 15 | 181,347 |
| Parallel specialists (reserve) | PASS | 52.5556 s | 3.2790 s | 21 | 277,861 |

The comparison matches the ceiling, not actual compute. Provider tokens sum each ledger response’s `total_tokens` across parent and child calls: prompt plus completion, including cached/repeated input. Reasoning is included in completion and not added twice. The ledger has no unattributed requests in the pair, and counts agree with shared-budget audits. The child receives a fresh context, makes four attributed provider calls, checks the candidate, and returns a 142-word verdict. Its recorded span is about 18.82 seconds; this is sequential validation after repair, not parallel implementation. We report full run wall time rather than treat the child span as the entire coordination overhead.

The independent `p09-task-08` checker repeats the two async tests five times. These check count correctness and a concurrency threshold. Separate scope audits pass with only `toyapp/async_jobs.py` changed and protected tests unchanged. The parent/child traces contain additional repeated checks and timing probes. Three unrelated planted full-suite failures remain. The matched child uses output redirection in checks (its received prompt suggests it); the later no-redirection rule cannot be retroactively imposed. No end-to-end enforced read-only boundary is established by editor-mutation counts or a clean final diff. Do not claim that all possible side effects were absent.

See [derived metrics and every starter hash](w56-evidence/w6-matched-results.json), [single prompt](w56-evidence/w6-single-prompt.txt), and [worker-validator prompt](w56-evidence/w6-worker-validator-prompt.txt). Their source directories in the JSON link to original launch, settings, event, child-event, scope, native, verifier and provider records.

One agent already passes, so this pair has no observed correctness gain for adding the validator. One run per condition cannot estimate average speed/quality, and differing consumed tokens prevent an equal-token causal claim. Use this coupled repair to inspect extra orientation/checking/handoff/synthesis work, then write a delegation policy with separate work, edit ownership, evidence return, synthesis and a total budget. More difficult independent branches remain a proposed future evaluation.

### Keep the rule-violation audit as supporting evidence

The October 3 refined classroom recording remains under `capture-w6-*`, the inspection evidence, and the supporting core slide `w6-boundary`. Its behavior passes (15 parent and 20 child repeated checks; concurrent timing about 0.006 s versus 0.150 s serialized bound), but child cache creation and diagnostic redirection violate its actual received rules. The parent paraphrases required wording and uses 2>&1. These counts/timings are not mixed with the matched comparison. The redirects do not establish that a failed test was hidden. Isolated read-only checking, controlled cache-free runners and forbidden-write probes remain proposed enforcement, not measured benefits.

## Wider results remain separate

The earlier benchmark’s freight runs use Sonnet 4.6 and different trajectories/budgets: OpenHands single and completion remain 6/9; Pi changes 4/9 to 6/9 with substantially more time/tokens. The incident completion run remains 8/8 with added checking cost. These reserve stories are preserved and labeled separately; neither is a native-goal comparison on slugify or a matched-budget architecture result. See the existing benchmark notes and `workshop-5-ceiling` / `workshop-5-repair-cost` reserve slides.

## Review and verification

[Opus planning review](opus-w56-plan.md) is based on supplied findings; its session had no filesystem access. Codex therefore supplies complete final slide text, narration, receipts and limitations in the final review request instead of assuming the reviewer can read paths. The [first final review](opus-w56-final-first.md) requested prediction-before-reveal, explicit judge-versus-executable-check wording, observed progress limits, and tighter claims. These corrections were applied. Final approval and pixel QA are recorded alongside this report.


Final [Opus review](opus-w56-final.md): W5 and W6 approved for content and teaching structure. Its remaining scene-3 attribution check was verified against agent observation `23564a1a-44fb-43dc-9a23-111fda061b5b`: the agent's own command prints `'api.v1-endpoint'`, `ASSERTION_OK`, and `ASSERT_EXIT=0`. The agent initially hit an import-path error, corrected PYTHONPATH, then obtained this passing result. The external assertion after termination is a separate record.


[Final pixel and build verification](w56-evidence/pixel-qa/qa.md): all 15 target pages inspected in the live browser; zero page errors. The 299-page deck generator, production build and both explainer checks passed. Rendered videos are 1920 × 1080, 30 fps, W5 36 seconds and W6 30 seconds.
