# Solution Brief: P11 Subagents and Context Isolation

## What This Solution Shows

Let's walk through the results. Subagents are not an automatic upgrade. In several runs they added cost and latency without improving the final answer. In one long-running branch run, they improved wall time while still costing more.

Use the walkthrough in this order:

1. Start with Scenario A. The small repo audit shows the fixed cost of child conversations.
2. Show the rejected code-audit corpus. It looked more parallel on paper, but the live numbers did not support it.
3. Move to the research corpus. It gives the lesson a better task shape, but still needs careful measurement.
4. End with long-running branch mode. That is the cleanest positive case from the live runs: quality tied, cost increased, and wall time improved once each branch had enough real waiting time.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_compare.py` | Runs the single-context config and the subagent config (five subagent sessions + synthesis) and prints the token/cost/wall comparison. |
| `run_task_laminar.py` | Runs Scenario A through native OpenHands `TaskToolSet` and emits Laminar traces when `LMNR_PROJECT_API_KEY` is set. |
| `run_scenario_b.py` | Runs the breadth-first research comparison and scores fact completeness against `corpus/ground_truth.json`. |
| `run_monster_repo.py` | Runs native task-tool investigation on the local VS Code custom-image benchmark tree. |
| `../subagent_bench.py` | The engine: the audit dimensions, the local-SDK `run_conversation` (copies the repo to a temp dir per call so runs stay isolated), and the report. |
| `../sample_repo/` | The audit target, with planted issues across all five dimensions. |
| `../make_corpus.py` | Generates the Scenario B research packets and objective ground truth. |

## Key Design Choices

**Same conversation primitive for both configs.** The single-context run and every subagent child use the identical local-SDK `RemoteConversation` setup from P01 to P08. The only thing that changes between them is the context boundary, so the comparison isolates that one variable.

**Isolated, clean workspaces.** `run_conversation` copies `sample_repo` to a fresh temp dir per call. The bundled repo is never mutated, and each subagent starts from the same clean tree.

**Compact returns, then synthesis.** Each subagent returns a few-sentence finding (extracted from `MessageEvent.llm_message`), and a final synthesis conversation combines those findings from a prompt without touching the repo. That is the shape that *should* favor isolation: small results, independent subtasks.

**Manual child conversations remain the controlled benchmark.** OpenHands has SDK subagent orchestration through `TaskToolSet` and the `task` tool. The main benchmark still uses explicit child conversations because it needs per-child cost, tokens, wall time, compaction counts, clean copied workspaces, and model routing knobs.

**Native task-tool orchestration is the traceability check.** `run_task_laminar.py` gives the parent `Tool(name=TaskToolSet.name)`, registers a P11-specific read-only subagent type, and relies on Laminar to show the parent and child trace shape. This measures the product surface, not the same controlled isolation contract as `run_compare.py`.

**Child model routing is explicit.** Both reference runners honor `P11_CHILD_MODEL` first, then `LLM_MODEL_SMALL`, for child work only. The single-context baseline and synthesis stay on `LLM_MODEL`. Set `P11_CHILD_MODEL=same` to force children to use `LLM_MODEL`, even when `LLM_MODEL_SMALL` is present in `.env`.

**Same-model context stress is the fair next experiment.** To test whether subagents help with a smaller context window, set `LLM_MODEL` to a smaller-context model and set `P11_CHILD_MODEL=same`. That keeps the model constant across single, children, and synthesis, so any difference comes from the context boundary rather than from giving one config a stronger model.

**Parallel children in Scenario B.** The research runner uses `P11_PARALLELISM` to run independent topic researchers concurrently. The subagent cost is still the sum of all child costs plus synthesis, but the wall-clock comparison uses actual elapsed child time plus synthesis time.

## Solution Walkthrough

Start the walkthrough with the simplest claim: a single agent is usually a strong baseline. Scenario A and the rejected code-audit corpus demonstrate that adding subagents can multiply token use, add wall time, and still produce the same quality score. That is the learning moment students should hit before seeing any successful case.

Then walk through the research runner. The ordinary research corpus is closer to public multi-agent research patterns, but at small sizes it still does not justify the orchestration. The same-model Haiku stress run shows a quality win, but it is a final-output collapse case rather than a clean compaction event.

End with long-running branch mode. This is the case worth highlighting as the narrow win: each branch has independent work, each child returns a compact result, and the delay is large enough that overlapping branch work beats the extra child-session overhead. Even there, cost goes up.

## Reference Numbers

Measured on `sample_repo` with `claude-sonnet-4-5` via the local agent server. Demo numbers, so your mileage varies (single-context cost ranged $0.09 to $0.14 across runs).

| Config | Input tokens | Output tokens | Cost | Wall |
|---|---:|---:|---:|---:|
| A single context | 127,767 | 3,787 | **$0.1440** | 89.6s |
| C subagents (5 + synthesis) | 309,340 | 12,471 | **$0.5124** | 278.1s |

**Cost ratio (subagents / single): 3.56x.** Per subagent:

| Subagent | Input tokens | Cost |
|---|---:|---:|
| docs | 27,970 | $0.0649 |
| errors | 59,104 | $0.0990 |
| secrets | 84,531 | $0.1072 |
| deps | 49,505 | $0.0818 |
| tests | 69,259 | $0.0925 |
| synthesize | 18,971 | $0.0671 |

**Why subagents lost here.** The five child audits used 290,369 input tokens before synthesis, which is 2.27x the single context's 127,767 input tokens. Each isolated conversation re-pays the same fixed overhead, the system prompt plus exploring the repo from scratch, and on a tiny repo there is no large intermediate-context savings to reclaim against it. The single context reads the repo once and carries everything in one transcript that prompt caching keeps cheap.

**Cheaper child-model rerun.** Routing Scenario A children to the smaller model reduced the subagent penalty, but did not flip the result:

| Config | Input tokens | Output tokens | Cost | Wall | Compactions |
|---|---:|---:|---:|---:|---:|
| A single context | 98,464 | 3,495 | **$0.1269** | 84.9s | 0 |
| C subagents (5 + synthesis) | 380,783 | 16,079 | **$0.2330** | 196.1s | 0 |

**Cost ratio (subagents / single): 1.84x.** Cheaper children helped, but overlap and fixed child setup still dominated.

**When the result flips.** Isolation is most plausible when each subtask is turn-heavy, each child returns a compact answer, the subtasks barely overlap, and child work can run in parallel. The point of the harness is that you can measure the crossover instead of guessing it.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Did your subagent run return real findings? | The synthesis must combine actual findings, not empty headers. If empty, your final-text extraction is reading the wrong event field. |
| Which side used fewer input tokens? | On `sample_repo`, single wins. Confirm you see the same direction and can explain it from the per-subagent overhead. |
| Did both find all five issues? | Quality, not just cost. A single long transcript can drop a dimension; isolated subagents can miss cross-cutting issues. |
| Did runs mutate the repo? | They should not. Each conversation runs against a temp copy. |

## Valid Variations

Run against broader, lower-overlap subtasks and show where the ratio changes. Parallelize the subagent conversations to win on wall-clock even when tokens are a wash. Use a cheaper model for the children and a stronger one for synthesis. Or swap the manual orchestration for OpenHands `TaskToolSet` once you no longer need per-child measurement. The backend is not the lesson; the measured crossover is.

Cheaper child-model command:

```bash
P11_CHILD_MODEL="$LLM_MODEL_SMALL" uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_compare.py
```

## Native OpenHands Task Tool With Laminar

The native runner answers a different question from the manual benchmark. It asks: what does this look like when the parent agent uses OpenHands `TaskToolSet` and Laminar traces the resulting conversation tree?

Run a cheap two-dimension check:

```bash
P11_NATIVE_MODEL=small P11_ONLY_DIMS=docs,secrets \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_task_laminar.py
```

Run the full Scenario A native task-tool check:

```bash
P11_NATIVE_MODEL=small \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_task_laminar.py
```

Print the final report when you want to verify synthesis quality:

```bash
P11_NATIVE_MODEL=small P11_NATIVE_TASK_ONLY=1 P11_NATIVE_SHOW_FINAL=1 \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_task_laminar.py
```

The runner loads `.env` before importing OpenHands, so `LMNR_PROJECT_API_KEY` enables Laminar automatically. It prints the OpenHands conversation id for each run. Use that id to find the trace in Laminar.

One implementation detail matters. On this macOS run, Laminar's gRPC instrumentation emitted fork warnings that broke tmux-backed terminal startup inside child worker threads. The runner registers a P11-specific `p11-code-explorer` subagent that uses the SDK terminal tool in subprocess mode. That keeps native task-tool orchestration intact while avoiding tmux as the child terminal backend.

Live two-dimension native check with `P11_NATIVE_MODEL=small`:

| Config | Input tokens | Output tokens | Cost | Wall | Quality | Conversation id |
|---|---:|---:|---:|---:|---:|---|
| native single | 28,120 | 1,081 | **$0.0202** | 11.2s | 2/5 | `ac55a9ef-81d4-4f59-8164-021d87fc79e9` |
| native task tool | 102,415 | 3,558 | **$0.0375** | 33.8s | 2/5 | `81f6673b-700d-458e-a32a-9e9603db9eab` |

Full native checks with `P11_NATIVE_MODEL=small`:

| Config | Input tokens | Output tokens | Cost | Wall | Quality | Conversation id |
|---|---:|---:|---:|---:|---:|---|
| native single | 88,152 | 2,521 | **$0.0362** | 28.7s | 5/5 | `9145d275-1195-41db-899b-863ee328b8ad` |
| native task tool, final shown | 317,132 | 8,298 | **$0.0967** | 83.6s | 5/5 | `539e1634-f39e-4aeb-8085-e5a9e5eb0b97` |

The native task-tool run gave useful Laminar visibility and per-child usage rows, but it did not beat the local single-agent baseline on this small repo. It inherited the parent model, used one shared workspace, and paid the fixed child setup cost five times. That is the point of keeping both runners: native task-tool orchestration shows the real OpenHands mechanism, while the manual benchmark isolates the context-boundary economics.

## Scenario C: Monster Repo Investigation

Scenario C uses the local VS Code benchmark checkout and custom image demo as a realistic large-repo investigation. It is read-only by design. The agents may inspect files, but they must not run tests, installs, builds, Docker, package managers, or network commands.

Run a cheap smoke:

```bash
P11_MONSTER_MODEL=small P11_MONSTER_ONLY_AREAS=benchmark_doc,custom_image \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_monster_repo.py
```

Run the full comparison:

```bash
P11_MONSTER_MODEL=small \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_monster_repo.py
```

The runner scores a checklist of benchmark facts instead of asking whether the answer feels good. The checklist includes the benchmark branch and commit, target source and test files, exact grep string, benchmark helper scripts, setup phases, custom image helper commands, and rebuilt image tag.

Live full Scenario C run with `P11_MONSTER_MODEL=small`:

| Config | Input tokens | Output tokens | Cost | Wall | Checklist score | Conversation id |
|---|---:|---:|---:|---:|---:|---|
| monster single | 639,540 | 11,934 | **$0.1538** | 123.7s | 13/15 | `c362b9b8-05f9-4b4c-83f5-8ccbb301badd` |
| monster task tool | 3,531,082 | 45,620 | **$0.8125** | 468.6s | 15/15 | `2ebf2bb4-146b-4df5-bd0e-ca299712963e` |

Per child in the native task-tool run:

| Child | Input tokens | Output tokens | Cost |
|---|---:|---:|---:|
| benchmark_doc | 763,748 | 6,895 | $0.1700 |
| source_bug | 1,010,505 | 12,105 | $0.2160 |
| test_contract | 321,292 | 5,551 | $0.0835 |
| setup_helpers | 602,995 | 9,609 | $0.1390 |
| custom_image | 805,816 | 7,965 | $0.1649 |

This is the first P11 task where native task-tool subagents bought a measurable final-answer quality gain: 15/15 checklist facts versus 13/15 for the single conversation. It was still not cheap. The task-tool run cost 5.28x more and took 3.79x longer on this local run. The result is useful because it separates two claims: large-repo subagent orchestration can improve coverage, but it still needs tighter child budgets, narrower areas, or stronger synthesis policy before it is a default.

The first two-area native smoke also exposed a separate synthesis risk. The children found the facts, but the parent initially compressed away exact labels and scored 7/15. The current runner fixes that with a checklist-table final contract. Treat that as part of the lesson: subagent quality depends on the handoff format, not just on whether child agents read the right files.

## Rejected Scenario B: Code-Audit Corpus

The first Scenario B design generated 24 independent Python files, each about 24 KB, with one planted issue near the tail. The hypothesis was reasonable: independent large files should favor bounded child contexts. The live run showed otherwise.

Measured with 24 files, two files per child shard, and cheaper child model routing:

| Config | Input tokens | Output tokens | Cost | Wall | Compactions | Issues found |
|---|---:|---:|---:|---:|---:|---:|
| A single context | 386,993 | 7,483 | **$0.4500** | 122.5s | 0 | 24/24 |
| C subagent shards + synthesis | 1,996,077 | 70,133 | **$0.9727** | 810.7s | 0 | 24/24 |

Raw child findings were 23/24 before synthesis, and the final synthesis reached 24/24. The cost ratio was 2.16x in favor of the single context. This task is worth keeping as a lesson because it proves that "many independent files" is not enough. The single context could still audit successfully, caching helped, and the subagent version paid the fixed setup cost many times.

## Scenario B: Breadth-First Research

The current Scenario B follows the task shape where public multi-agent research systems tend to show value: broad independent research branches, compact branch findings, and one synthesis pass. It is not designed to guarantee cheaper tokens. It is designed to test whether parallel, isolated research improves elapsed time and preserves fact completeness as topic breadth grows.

Generate the corpus, then run the reference:

```bash
python projects/p11-subagents/make_corpus.py --topics 8 --distractors 8

P11_PARALLELISM=4 P11_CHILD_MODEL="$LLM_MODEL_SMALL" \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

`run_scenario_b.py` copies only topic packets into the research workspaces, so the agent cannot score itself by reading `ground_truth.json`. It prints input tokens, output tokens, cost, actual wall time, compaction, and facts found / total for both configs. It also scores raw child findings before synthesis so you can see whether the synthesis step preserved or dropped facts.

The key tuning knobs are topic breadth and child parallelism:

| Setting | What it tests |
|---|---|
| `--topics 4` | Cheap smoke with limited breadth. |
| `--topics 8` | Default research breadth. |
| `--topics 12` | More branches and a larger synthesis burden. |
| `P11_PARALLELISM=1` | Serial children, useful for debugging. |
| `P11_PARALLELISM=4` | Default parallel child limit. |
| `P11_CHILD_MODEL="$LLM_MODEL_SMALL"` | Cheaper child researchers, stronger baseline and synthesis. |
| `P11_CHILD_MODEL=same` | Same model for baseline, children, and synthesis. Use this for context-window stress tests. |

Use `P11_LIMIT_TOPICS=3` for a cheap live smoke before running the full corpus. Treat the numbers below as reference runs for this repo state, not universal benchmark claims. Scenario B is still sensitive to topic count, distractor count, child parallelism, model choice, and server load.

Live research runs from this repo state:

| Corpus | Config | Input tokens | Output tokens | Cost | Wall | Compactions | Facts found |
|---|---|---:|---:|---:|---:|---:|---:|
| 3 topics, `P11_PARALLELISM=2` | single context | 33,337 | 2,531 | **$0.1009** | 38.5s | 0 | 12/12 |
| 3 topics, `P11_PARALLELISM=2` | subagents + synthesis | 136,920 | 7,153 | **$0.1351** | 79.0s | 0 | 12/12 |
| 8 topics, `P11_PARALLELISM=4` | single context | 61,889 | 5,182 | **$0.1840** | 72.1s | 0 | 32/32 |
| 8 topics, `P11_PARALLELISM=4` | subagents + synthesis | 291,253 | 15,750 | **$0.2697** | 128.9s | 0 | 32/32 |

The 8-topic child researchers completed all 32 facts before synthesis, and the synthesis preserved all 32. The subagent run still lost on cost and wall time at this scale. That is the lesson: the benchmark now has the right breadth-first shape, but you still need enough breadth, lean enough children, or structured aggregation before subagents pay off locally.

For the smaller-context experiment:

```bash
# Replace this with a model available in your environment that has a smaller window.
export LLM_MODEL="provider/model-with-smaller-context"

python projects/p11-subagents/make_corpus.py --topics 12 --distractors 24
P11_CHILD_MODEL=same P11_PARALLELISM=4 \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

This is the cleanest way to see whether a single context starts missing facts while each child still fits its own packet.

Same-model Haiku stress run:

```bash
python projects/p11-subagents/make_corpus.py --topics 12 --distractors 24

LLM_MODEL=anthropic/claude-haiku-4-5-20251001 \
P11_CHILD_MODEL=same \
P11_PARALLELISM=4 \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

| Corpus | Config | Input tokens | Output tokens | Cost | Wall | Compactions | Facts found |
|---|---|---:|---:|---:|---:|---:|---:|
| 12 topics, 24 distractors, Haiku same-model | single context | 125,830 | 4,290 | **$0.0714** | 39.6s | 0 | 6/48 |
| 12 topics, 24 distractors, Haiku same-model | subagents + synthesis | 515,562 | 25,077 | **$0.3667** | 246.4s | 0 | 48/48 |

The children and synthesis preserved every fact, but the cost ratio was 5.14x and the wall ratio was 6.22x in favor of the single context. The single run did read the evidence and had many facts in intermediate notes, then its final response collapsed to a short summary. Score the final answer because that is the artifact a harness user receives, but describe this as final-output loss rather than a clean compaction event.

## Scenario B: Long-Running Branch Mode

The research benchmark can also add real elapsed-time pressure. Pass `--work-delay` to the corpus generator and it creates `work_probe.py`. Each topic then has one extra required fact, a verification code returned by `python work_probe.py <topic_id>` after the configured delay.

The single-context prompt asks the agent to process topics in order, one probe at a time. The subagent runner launches independent topic researchers concurrently through `P11_PARALLELISM`. This is the task shape where manual orchestration can be valuable even if it costs more tokens: the parent overlaps independent waits and synthesizes compact child results.

Run it:

```bash
python projects/p11-subagents/make_corpus.py --topics 6 --distractors 4 --work-delay 20

P11_CHILD_MODEL=same P11_PARALLELISM=3 \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

This is not a claim that subagents are the only way to parallelize waiting. A single agent with a good parallel shell strategy, or a custom script, could also overlap the probes. The lesson is to compare manual subagent orchestration against the simplest one-conversation baseline, then decide whether the added orchestration is worth keeping.

Live long-running runs from this repo state:

| Corpus | Config | Input tokens | Output tokens | Cost | Wall | Compactions | Facts found |
|---|---|---:|---:|---:|---:|---:|---:|
| 6 topics, 20s probe, Haiku same-model | single context | 319,141 | 5,645 | **$0.0860** | 177.5s | 0 | 30/30 |
| 6 topics, 20s probe, Haiku same-model | subagents + synthesis | 293,299 | 30,956 | **$0.2763** | 292.3s | 0 | 30/30 |
| 6 topics, 60s probe, Haiku same-model | single context | 316,374 | 6,355 | **$0.0890** | 434.7s | 0 | 30/30 |
| 6 topics, 60s probe, Haiku same-model | subagents + synthesis | 311,642 | 22,205 | **$0.2349** | 260.2s | 0 | 30/30 |

At 20 seconds per probe, subagents still lost because local Agent Server child-session overhead and WebSocket fallback delays dominated the saved wait time. At 60 seconds per probe, the same manual orchestration won on wall time: 260.2s vs 434.7s, while cost was 2.64x higher. That is the clean P11 story: subagents are not a cheaper default, but they can be worth wiring up when independent branches spend enough real time waiting or working.

## General Guidance

Start with one agent. It has shared context, simpler traces, fewer moving parts, and usually lower cost. If the single agent is accurate and fast enough, stop there.

Reach for subagents only when the shape of the work is narrow and defensible:

- The subtasks are independent enough that each child can work without shared state.
- Each child returns a compact result, not another large transcript.
- The parent only needs synthesis, not continuous coordination.
- The combined work creates real context pressure, final-output loss, or enough elapsed-time waiting to justify parallel branches.
- The measured gain beats alternatives such as a stronger single model, model routing, a purpose-built script, or one agent launching parallel shell jobs.

Treat subagents as an orchestration tool, not an intelligence upgrade. The decision is local to the task, the model, the server, and the cost budget.

## What To Keep

A "when to use subagents" decision rule grounded in your numbers:

> Start with one agent. Add subagents only when the work splits into independent branches, each branch has a compact result, and measurement shows that context isolation or parallel elapsed time beats the child-session overhead. Keep one agent when the task is small, tightly coupled, easy to cache in one transcript, or better handled by a script.

The reusable artifact is the habit of treating the context boundary as a measured harness decision, not the audit script.
