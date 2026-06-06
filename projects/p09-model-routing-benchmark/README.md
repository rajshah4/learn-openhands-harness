# P09: Model Routing Benchmark

## What Problem Are You Solving?

Routing is harness engineering. A harness should not blindly assign every task to the most expensive model. It should use the cheapest model it trusts, protect high-risk work with a risk floor, and escalate when the current model shows evidence that it is stuck.

The problem in this lesson is to test that idea empirically. Students run the same 10 coding tasks three ways:

1. Use a single frontier model for every task. This is the control group.
2. Build a static rules router with `RouterLLM`. This routes once at the start of the task.
3. Build a cascade with OpenHands profiles and `SwitchLLMTool`. This can change models during the run when evidence says the current model is not making progress.

The comparison is not just raw cost. A cheap run that fails the task is not a win. The headline metric is cost per solved task, alongside task pass rate, token usage, total cost, models used, and escalation reasons.

The frontier model is the consultant, not the default employee.

## Start With These Files

This project has starter code and completed solutions. Start with the starter files when teaching the lesson, then use the solution files to compare the intended design.

After you attempt the starter, read `solution/README.md` for the solution brief. It explains why the reference implementation is split into a frontier baseline, static router, cascade runner, and shared routing core.

| Purpose | Starter | Solution |
|---|---|---|
| Baseline run and static rules routing | `starter/run_routing.py` | `solution/run_frontier.py`, `solution/run_static_rules.py` |
| Cascading routing with profile switching | `starter/run_switch_cascade.py` | `solution/run_switch_cascade.py` |
| Shared benchmark behavior | | `solution/routing_core.py` |
| Run all checks and dry runs | | `solution/run_all.py` |

The benchmark edits `toy_repo/`, reads task definitions from `tasks.json`, and validates work with `check_task.py`. Live runs create fresh copies of the repo under `.openhands-runs/p09/...`, so each task starts from the same clean state.

This lesson is the advanced follow-up to [P02: Model Routing](../p02-model-routing/). P02 shows a simple harness decision before a conversation starts. P09 turns that idea into a measured benchmark with real OpenHands agents, model metrics, profile switching, Agent Canvas events, and Laminar traces.

## The Tasks In The Benchmark

The task set is intentionally skewed toward routine software work. That is where routing can save money. A few tasks are harder or higher risk so students can see why rules and escalation matter.

| ID | Task | Difficulty | Routing lesson |
|---|---|---|---|
| 01 | Rename a variable across one file | trivial | Cheap should be enough |
| 02 | Add docstrings for 3 functions | trivial | Cheap should be enough |
| 03 | Fix a wrong assertion value | trivial | Cheap should be enough |
| 04 | Add a `--verbose` CLI flag | easy | Cheap or mid |
| 05 | Write date parser unit tests | easy | Cheap or mid |
| 06 | Fix pagination off by one | medium | Good cheap-tier stress test |
| 07 | Refactor a long report function | medium | Mid may be worth it |
| 08 | Debug async race condition | hard | Escalation candidate |
| 09 | Review auth middleware | hard | Risk floor to frontier |
| 10 | Design API caching layer | hard | Expected cascade smoke test |

Before building a router, students should make a routing hypothesis. Which tasks should never start cheap? Which tasks look routine? Which tasks might start cheap but need a way to recover? That prediction gives the results table something meaningful to compare against.

## Start With The Baseline, Then Design Routing

There are three runs, but only two routing solutions to design.

The single-model run is the baseline. It answers: what happens if we use the expensive model for everything? This gives a quality and cost reference point.

The first routing solution is static rules. It answers: how far can we get with a small amount of deterministic harness logic? This is the direct extension of P02.

The second routing solution is a cascade. It answers: what should the harness do after the first model choice turns out to be wrong? This is the main lesson because routing is not only a preflight decision. In agentic work, evidence arrives while the task is running.

The policy students are designing has three layers:

1. A risk floor for auth and security work.
2. A cheap-first static route for routine tasks.
3. Evidence-based escalation when the current model repeats the same failure or stops making progress.

## Solution 1: Static Rules With RouterLLM

Use `RouterLLM` when the harness should choose the model and the agent should not need to know routing is happening. The agent receives one `llm`, but that object is a router. Inside `select_llm(messages)`, the router returns the key for one of the configured LLMs.

The starter file is `starter/run_routing.py`. The completed versions are `solution/run_frontier.py` and `solution/run_static_rules.py`.

The rules are intentionally simple:

```python
if touches_auth_or_security(task):
    return "frontier"
if prompt_tokens(task.prompt) < 200 and "```" not in task.prompt:
    return "cheap"
if task.difficulty == "hard":
    return "frontier"
return "mid"
```

This gives students a clear first design:

1. Load the task metadata.
2. Attach the task to the router instance.
3. Configure three LLMs: cheap, mid, and frontier.
4. Let `RouterLLM` choose the tier before the task runs.
5. Collect `llm.metrics` after the task to report tokens and cost.

The important limitation is also part of the lesson. `RouterLLM.select_llm(messages)` receives conversation messages, not the raw SDK event stream. That is fine for static routing because the decision mostly comes from task metadata. It is not enough by itself for a clean cascade unless the router also tracks state across calls or parses tool-result messages. That is why the cascade solution uses a different OpenHands mechanism.

## Solution 2: Cascading With Profiles And SwitchLLMTool

Use `SwitchLLMTool` when the model needs to change during an ongoing OpenHands conversation. The run starts with one profile, then the agent can call `switch_llm` to move to another profile. The conversation history, files, and task state are preserved, and Agent Canvas renders the switch as a visible event.

The starter file is `starter/run_switch_cascade.py`. The completed version is `solution/run_switch_cascade.py`.

In this design, the harness still owns the policy. The model does not get a vague instruction like "use your judgment." It gets concrete escalation criteria:

- Same test failing twice.
- Same file edited 3 or more times.
- Identical error string repeating.
- Turn budget exceeded.
- Diff unchanged for 2 turns.

When one of those signals appears, the agent should switch up one tier and include the reason:

```json
{"profile_name": "p09-mid", "reason": "same pagination assertion failed twice after two edits"}
```

This is the teaching moment to record in Agent Canvas. Students should see the task begin on a cheaper profile, hit repeated evidence, call `switch_llm`, and finish with a different model. The trace should show why the harness paid for the stronger model only after evidence appeared.

The cascade uses OpenHands profiles named `p09-cheap`, `p09-mid`, and `p09-frontier`. Those profiles are saved with `LLMProfileStore`, and `SwitchLLMTool` switches by profile name.

## How OpenHands Fits In

This lesson shows two different ways to integrate routing into OpenHands.

With `RouterLLM`, the harness controls selection directly. The agent code is unchanged because the router behaves like an LLM. This is useful when the routing decision can be made from task metadata or conversation messages.

With `SwitchLLMTool`, the running conversation can change profiles. This is useful when the decision depends on runtime evidence that appears after the agent has tried tests, edited files, or repeated the same error. It is also useful for teaching because Agent Canvas shows the model switch in the timeline.

Both approaches preserve the main point: model choice is part of the harness design. The model is not the whole system.

## Configure The Model Tiers

The single-model and `RouterLLM` runs select models from environment variables.

| Tier     | Env var              | Default                               |
| -------- | -------------------- | ------------------------------------- |
| CHEAP    | `P09_MODEL_CHEAP`    | `anthropic/claude-haiku-4-5-20251001` |
| MID      | `P09_MODEL_MID`      | `anthropic/claude-sonnet-4-6`         |
| FRONTIER | `P09_MODEL_FRONTIER` | `anthropic/claude-opus-4-8`           |

Set `LLM_API_KEY` in your shell or repo-level `.env`. Set `LLM_BASE_URL` only if you use a gateway or proxy.

The cascade run uses Agent Server profiles because `SwitchLLMTool` switches by profile name. Use `--setup-profiles` to create or update `p09-cheap`, `p09-mid`, and `p09-frontier`.

## Run The Three Strategies And Collect Metrics

After students design the baseline, static router, and cascade, these commands turn the designs into measured evidence. Use the dry run and model preflight first, then run each strategy and compare pass rate, token usage, cost, and cost per solved task.

From the solution directory:

```bash
cd projects/p09-model-routing-benchmark/solution
```

Dry-run routes without paid model calls:

```bash
uv run --with openhands-sdk --with openhands-tools --with pytest python run_all.py --dry-run
```

Check configured models:

```bash
uv run --with openhands-sdk --with openhands-tools --with pytest python run_all.py --print-models
uv run --with openhands-sdk --with openhands-tools --with pytest python run_all.py --preflight-models
```

Run the single-model baseline and the static router:

```bash
uv run --with openhands-sdk --with openhands-tools --with pytest python run_frontier.py
uv run --with openhands-sdk --with openhands-tools --with pytest python run_static_rules.py
```

Run one Canvas-visible cascade task:

```bash
LLM_API_KEY=... \
uv run --with openhands-sdk --with openhands-tools --with pytest \
  python run_switch_cascade.py --setup-profiles --save-profile-secrets --task p09-task-10
```

Run all cascade tasks:

```bash
LLM_API_KEY=... \
uv run --with openhands-sdk --with openhands-tools --with pytest \
  python run_switch_cascade.py --setup-profiles --save-profile-secrets --all-tasks
```

## Send Traces To Laminar

Observability helps students understand what happened in a run and compare aggregate statistics across strategies. The OpenHands SDK supports OpenTelemetry-compatible tools. Here we are using Laminar.

The scripts load the nearest `.env` before OpenHands imports tracing hooks. To send traces to Laminar:

```bash
export LMNR_PROJECT_API_KEY="..."
export P09_TRACE_USER_ID="raj-p09"
```

Each conversation is tagged with `lesson=p09`, `strategy`, and `task`. Use those tags to compare the baseline, static router, and cascade runs in Laminar.

## Record The Results

Record results per task:

| Task | Model(s) used | Attempts | Escalations | Tokens | Cost | Pass/fail |
|---|---|---:|---:|---:|---:|---|
| p09-task-01 | | | | | | |

Then summarize by strategy:

| Strategy | Tasks passed | Total cost | Cost per solved task |
|---|---:|---:|---:|
| frontier | | | |
| static | | | |
| cascade | | | |

Label demo numbers as "measured on this repo, your mileage varies." The scripts use SDK metrics so the reported costs come from actual token counts and configured model pricing, not invented per-task estimates.

<details>
<summary>References</summary>

- [RouteLLM, LMSYS/Berkeley](https://www.lmsys.org/blog/2024-07-01-routellm/) and [paper](https://arxiv.org/abs/2406.18665): routers can reduce strong-model calls while preserving target quality.
- [Anyscale router tutorial](https://www.anyscale.com/blog/building-an-llm-router-for-high-quality-and-cost-effective-responses): practical classifier and matrix-factorization routing tutorial.
- [GPT-5 system card](https://openai.com/index/gpt-5-system-card/): real-time classifier-style routing between fast and thinking models.
- [Harvey Legal Agent Benchmark initial results](https://www.harvey.ai/blog/legal-agent-benchmark-initial-results): published benchmark results showing cost and quality pressure around frontier-only agents.
- [OpenHands SDK API reference: LLM](https://docs.openhands.dev/sdk/api-reference/openhands.sdk.llm): `RouterLLM`, `LLMProfileStore`, metrics, and token/cost tracking.
- [OpenHands observability guide](https://docs.openhands.dev/sdk/guides/observability): Laminar and OTLP tracing configuration.
- [OpenHands SDK paper](https://arxiv.org/abs/2511.03690): SDK architecture and model routing design.

</details>

## What Students Should Leave With

Students should finish with a routing policy they can defend with traces and metrics:

- Risk floors for tasks you should never route down.
- A cheap default for routine work.
- Evidence-based escalation before paying frontier cost.
- Cost per solved task as the comparison metric.

Previous routing lesson: [P02: Model Routing](../p02-model-routing/)
