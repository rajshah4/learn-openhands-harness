# P11: Subagents and Context Isolation

## What Problem Are You Solving?

Subagents are seductively appealing. Using a child conversation feels like it should make a task cleaner: give one branch of work its own context, ask it for a compact result, and keep the parent from carrying the whole branch transcript.

The catch is that a child conversation is still a full conversation. It has its own setup prompt, tool calls, file reads, latency, and model bill. The synthesis step is another conversation too.

The problem in this lesson is to test that boundary empirically. You are not trying to prove that subagents are good or bad. You are trying to find out what has to be true before a new context is worth paying for.

You will:

1. Run a single-context baseline.
2. Build the same task with isolated child conversations.
3. Measure quality, tokens, cost, wall time, and compaction.
4. Write a decision rule for when a harness should use subagents.

The reusable question is: **did this branch earn its own context?**

## Start With These Files

This project has two scenarios. Start with the starter files, then read the solution brief after you have numbers of your own.

| Purpose | Starter | Solution |
|---|---|---|
| Scenario A: small repo audit | `starter/run_compare.py` | `solution/run_compare.py` |
| Scenario A: native task-tool trace |  | `solution/run_task_laminar.py` |
| Scenario B: research corpus | `starter/run_scenario_b.py` | `solution/run_scenario_b.py` |
| Scenario C: monster repo investigation |  | `solution/run_monster_repo.py` |
| Shared conversation runner and reporting | `subagent_bench.py` | same |
| Scenario A target repo | `sample_repo/` | same |
| Scenario B corpus generator | `make_corpus.py` | same |

This lesson sits underneath [P04](../p04-decomposition/) and [P08](../p08-dynamic-workflows/). P04 decomposes work inside your own code; P08 lets the model write the orchestration. P11 isolates one narrower question beneath both: what changes when a branch gets its own context window, and is that change worth paying for? It shares its measure-don't-assume style with [P09](../p09-model-routing-benchmark/) and [P10](../p10-history-index/), which treat a harness choice as something you benchmark rather than something you guess.

## The Tasks In The Benchmark

I wasn't able to come up with a single problem that captured both the promise and the perils of subagents. The worse compromise you see here was doing all three. It isn't the most elegant setup, but it's the best I could do — and I promise that if you complete all three, you will come away with a stronger understanding of subagents.

### Scenario A: Small Repo Audit

`sample_repo/` is a small URL shortener with planted issues across five audit dimensions: docs, errors, secrets, deps, and tests.

You will audit it two ways:

- **Single context.** One conversation audits all five dimensions in one transcript.
- **Subagents.** Five child conversations audit one dimension each. A synthesis conversation combines their findings without reading the repo.

Before you run it, make a prediction. Which audit dimensions will look at the same files? Which approach will be easier to trace? Which approach is more likely to miss a cross-cutting issue?

### Scenario B: Research Corpus

`make_corpus.py` creates a local research corpus. Each topic folder has a `packet.md` with evidence, old notes, and distractors. Each topic also has a `questions.md` file. The hidden scoring file, `ground_truth.json`, records the facts the final report should recover.

You will compare the same two shapes:

- **Single context.** One conversation researches every topic and returns one table.
- **Subagents.** One child conversation researches each topic. A synthesis conversation combines the child notes.

This scenario offers flexibility to make the task more challenging; topic count, distractor count, child model, child parallelism, and optional probe delay. Those knobs let you test more than one theory about why a context boundary might help.

### Scenario C: Monster Repo Investigation

Scenarios A and B are toy-sized on purpose. Scenario C is the realistic large-repo check: a read-only investigation of a big benchmark checkout where orientation itself is most of the work. The agents may inspect files, but they must not run tests, installs, builds, Docker, package managers, or network commands.

You compare:

- **Single context.** One conversation investigates the whole tree and fills in a checklist of benchmark facts.
- **Task-tool subagents.** A parent launches one native OpenHands `task` per investigation area through `TaskToolSet`, then synthesizes the checklist.



## Start With The Baseline, Then Build Isolation

The single-context run is the control group. It answers: what happens if the harness does nothing special?

The subagent run is the design under test. It answers: what changes when the harness pays for separate conversations, then asks a parent to synthesize them?

Keep these questions visible while you build:

- Does each child avoid enough context to justify its setup cost?
- Do the child tasks share evidence, or are they genuinely separate?
- Does the synthesis preserve the child findings?
- Does child parallelism reduce wall time, or do child sessions add more delay than they save?
- Would a script, a better tool call, a stronger single model, or model routing be simpler?

## Run Scenario A And Collect Metrics

Run the single-context smoke first:

```bash
P11_SINGLE_ONLY=1 uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/starter/run_compare.py
```

Complete the TODO in `starter/run_compare.py`, then run your version:

```bash
uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/starter/run_compare.py
```

After that, run the reference:

```bash
uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_compare.py
```

The reference above is the controlled benchmark. It uses explicit child
conversations so you can measure each child directly. To see the native
OpenHands task-tool surface and send traces to Laminar, run:

```bash
P11_NATIVE_MODEL=small P11_ONLY_DIMS=docs,secrets \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_task_laminar.py
```

Then run the full native check:

```bash
P11_NATIVE_MODEL=small \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_task_laminar.py
```

If `LMNR_PROJECT_API_KEY` is set in your `.env`, the runner loads it before
OpenHands imports and Laminar receives the traces automatically. The printed
conversation ids are the handles to look up in Laminar.

You can route only the child audits to a cheaper model:

```bash
P11_CHILD_MODEL="$LLM_MODEL_SMALL" uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_compare.py
```

## Generate Scenario B Corpus

Generate the default research corpus:

```bash
python projects/p11-subagents/make_corpus.py --topics 8 --distractors 8
```

Use a smaller corpus for a quick smoke:

```bash
python projects/p11-subagents/make_corpus.py --topics 4 --distractors 4
```

Add probe delay when you want elapsed time to matter:

```bash
python projects/p11-subagents/make_corpus.py --topics 6 --distractors 4 --work-delay 20
```

With `--work-delay`, the generator creates `work_probe.py`. Each topic then has one extra required fact: a verification code returned by `python work_probe.py <topic_id>`. The single-context prompt processes probes in topic order. The subagent runner can run topic researchers concurrently through `P11_PARALLELISM`.

## Run Scenario B And Collect Metrics

Use `P11_LIMIT_TOPICS` for a cheap live smoke:

```bash
P11_LIMIT_TOPICS=3 P11_PARALLELISM=2 P11_CHILD_MODEL="$LLM_MODEL_SMALL" \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

Complete `starter/run_scenario_b.py`, then run your version:

```bash
uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/starter/run_scenario_b.py
```

Run the reference after your attempt:

```bash
P11_PARALLELISM=4 P11_CHILD_MODEL="$LLM_MODEL_SMALL" \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

Try more than one corpus shape. Do not stop at the first result:

```bash
python projects/p11-subagents/make_corpus.py --topics 4 --distractors 4
P11_PARALLELISM=2 uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py

python projects/p11-subagents/make_corpus.py --topics 8 --distractors 8
P11_PARALLELISM=4 uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py

python projects/p11-subagents/make_corpus.py --topics 12 --distractors 12
P11_PARALLELISM=6 uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

For a same-model context-window test, set `LLM_MODEL` to the model you want to study and force the children to use it too:

```bash
# Replace this with a model available in your environment.
export LLM_MODEL="provider/model-with-smaller-context"

P11_CHILD_MODEL=same P11_PARALLELISM=4 uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

If you are testing context pressure, increase breadth and distractors:

```bash
python projects/p11-subagents/make_corpus.py --topics 12 --distractors 24
P11_CHILD_MODEL=same P11_PARALLELISM=4 uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

If you are testing elapsed-time pressure, use long-running mode:

```bash
python projects/p11-subagents/make_corpus.py --topics 6 --distractors 4 --work-delay 20

P11_CHILD_MODEL=same P11_PARALLELISM=3 uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_scenario_b.py
```

## Run Scenario C On A Large Repo

Scenario C is read-only: the agents may read files but must not run tests, installs, builds, Docker, package managers, or network commands. The runner scores a fixed checklist of facts rather than asking whether the answer feels right, so the single and task-tool configs are graded on the same coverage bar.

Set it up by cloning the two benchmark repos into one directory and pointing `P11_MONSTER_ROOT` at it:

```bash
mkdir -p ~/p11-monster && cd ~/p11-monster
git clone https://github.com/rajshah4/openhands-custom-image.git
git clone -b openhands-benchmark-01 https://github.com/rajshah4/vscode-benchmark-repo.git

export P11_MONSTER_ROOT=~/p11-monster
```

`openhands-custom-image/` carries the benchmark directions, helper scripts (`prepare-vscode-benchmark`, `vscode-benchmark-verify`), and image tags the checklist looks for — see its `README.md` and `vscode-benchmark/`. `vscode-benchmark-repo/` is the pinned VS Code checkout (branch `openhands-benchmark-01`) that the benchmark fixes. Scenario C only *reads* these trees; it never builds the image or runs the benchmark, so cloning the two repos is the entire setup.

Run a cheap two-area smoke:

```bash
P11_MONSTER_MODEL=small P11_MONSTER_ONLY_AREAS=benchmark_doc,custom_image \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_monster_repo.py
```

Run the full Scenario C comparison:

```bash
P11_MONSTER_MODEL=small \
  uv run --with openhands-sdk --with openhands-tools \
  python projects/p11-subagents/solution/run_monster_repo.py
```

## Record The Results

Fill these from your own runs. Reference numbers live in `solution/README.md`.

| Scenario | Config | Input tokens | Cost | Wall time | Quality score | Compaction fired? |
|---|---|---:|---:|---:|---:|:--:|
| A small repo audit | single | | | | | |
| A small repo audit | subagents | | | | | |
| A native task-tool trace | single | | | | | |
| A native task-tool trace | task tool | | | | | |
| B research | single | | | | | |
| B research | subagents | | | | | |
| B long-running | single | | | | | |
| B long-running | subagents | | | | | |
| C monster repo | single | | | | | |
| C monster repo | task tool | | | | | |

For Scenario B, also record whether synthesis preserved the raw child findings:

| Corpus shape | Raw child facts | Final synthesized facts | Notes |
|---|---:|---:|---|
| | | | |

## Read The Results As A Design Tradeoff

Do not reduce the table to "subagents good" or "subagents bad." The point is to identify the task shape.

Use the numbers to answer:

- What did the context boundary buy?
- What did the context boundary cost?
- Did the subagent run improve quality, wall time, or neither?
- Did the final synthesis lose anything the children found?
- Which alternative would you try before adding subagents to a real harness?

If the answer changes as you adjust topics, distractors, model choice, or delay, write down the condition that changed it.

## How OpenHands Fits In

This lesson uses explicit `RemoteConversation` children for the controlled benchmark. That is intentional. Manual children make each child run visible: workspace, model, cost, tokens, wall time, compaction, and final text.

OpenHands also supports native subagent work through `TaskToolSet`, exposed to the parent agent as the `task` tool. The task tool can launch registered agent types, including file-based agents from `.agents/agents/*.md` or `.openhands/agents/*.md`. `solution/run_task_laminar.py` is the companion native run: it registers a P11 read-only subagent type, gives the parent `Tool(name=TaskToolSet.name)`, and relies on Laminar for the parent and child trace shape.

P11 keeps both approaches because they answer different questions. The manual benchmark isolates the economics of the context boundary. The native task-tool run shows the real OpenHands mechanism you would reach for after the boundary has earned its cost.

<details>
<summary>References</summary>

- [OpenHands SDK: Sub-Agent Delegation](https://docs.openhands.dev/sdk/guides/agent-delegation): `TaskToolSet`, the `task` tool, and consolidated child results.
- [OpenHands SDK: File-Based Agents](https://docs.openhands.dev/sdk/guides/agent-file-based): project-level and user-level subagent definitions.
- [Laminar: Observability for OpenHands Software Agent SDK](https://laminar.sh/docs/tracing/integrations/openhands-sdk): conversation, agent step, tool, token, latency, and cost traces.
- [`openhands-subagent-patterns`](https://github.com/rajshah4/openhands-subagent-patterns): working oh_conversations, sdk_subagents, and github_control patterns.
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching): the main confounder when comparing single-context vs. multi-conversation token counts.
- [Anthropic: How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system): a production research workload where independent agent branches explore broad information spaces and a lead agent synthesizes.
- [MACU: A Multi-Agent Framework for Complex Agentic Computer Use](https://arxiv.org/abs/2606.01533): reports multi-agent computer-use gains on several benchmarks, with parallelism as part of the value proposition.
- [BOAD: Balancing Orchestration and Action Dichotomy in Hierarchical Multi-Agent Systems](https://arxiv.org/abs/2512.23631): reports hierarchical SWE-agent gains, useful context for orchestration-heavy software tasks.
- [Multi-Agent Systems with Organization, Communication and Autonomy: A Realistic Evaluation](https://arxiv.org/abs/2604.02460): a counterpoint showing that equal-budget single agents can beat multi-agent systems, which is why P11 measures instead of assuming.

</details>

## What Students Should Leave With

Keep a short subagent policy, backed by your own table. It should say what kind of task earns a separate context, what kind does not, and which cheaper alternative you would try first.

The reusable artifact is not the child-agent code. It is the habit of treating the context boundary as a harness decision that needs evidence.
