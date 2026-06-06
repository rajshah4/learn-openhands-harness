# Solution Brief: P09 Model Routing Benchmark

## What This Solution Proves

This solution proves the advanced version of the P02 routing idea: model choice should be measured by cost per solved task, not by raw cheapness. P02 routes once before a conversation starts. P09 turns routing into a benchmark with a frontier baseline, static rules, and evidence-based escalation.

The goal is not to avoid frontier models. The goal is to pay for them when the task risk or runtime evidence justifies it.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_frontier.py` | Runs the control group: frontier model for every task. |
| `run_static_rules.py` | Runs the static `RouterLLM` strategy. |
| `run_switch_cascade.py` | Runs the Agent Canvas-visible cascade with `SwitchLLMTool` profiles. |
| `routing_core.py` | Shared task loading, routing rules, local cascade router, metrics, and result printing. |
| `run_all.py` | Convenience entrypoint for dry runs, model checks, and all strategies. |

Read the project README first for the benchmark design. Use this brief when you are ready to understand how the reference solution is split across files.

## Key Design Choices

The solution has three strategies:

1. **Frontier baseline:** use the strongest model for everything so pass rate and cost have a control group.
2. **Static rules:** use `RouterLLM` to choose cheap, mid, or frontier from task metadata before the task runs.
3. **Cascade:** start with the cheapest trusted tier, then escalate when runtime evidence shows the current model is stuck.

The static route uses simple, auditable rules:

- auth or security work gets a frontier risk floor
- short routine prompts start cheap
- hard tasks route up
- remaining work goes mid

The cascade adds runtime triggers: repeated test failures, repeated errors, repeated edits to the same file, turn-budget exhaustion, or unchanged diffs. Those are evidence signals, not vibes.

## How OpenHands Fits In

P09 shows two OpenHands routing mechanisms.

`RouterLLM` hides routing inside an LLM-like object. The agent receives one `llm`, but the router selects a tier. This is useful when the decision can come from task metadata or conversation messages.

`SwitchLLMTool` changes models during an ongoing remote conversation. The solution stores profiles named `p09-cheap`, `p09-mid`, and `p09-frontier`, then lets the agent call `switch_llm` with a profile name and evidence-based reason. Agent Canvas can show that switch in the trace.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Did static routing preserve pass rate? | Compare each task against the frontier baseline. |
| Did cascade recover from cheap-tier failures? | Inspect escalation reasons and final pass/fail. |
| Did risk floors work? | Auth, security, and high-risk tasks should not start too low. |
| Did routing improve cost per solved task? | Use solved cost, not total cost alone. |

A cheap failed run is not a win. A cascade that escalates constantly may also not be a win. The benchmark exists to make that tradeoff visible.

## Valid Variations

A valid solution might use different model tiers, a stricter risk floor, a deterministic escalation judge, or an LLM escalation judge. It might include the task-specific validator command in the prompt or keep checks opaque with `--opaque-checks`, depending on what behavior the learner wants to study.

The policy should remain explainable. If no one can predict why a task routed cheap, mid, or frontier, the router is hard to trust.

## What To Keep

Keep:

- the routing hypothesis before the run
- the per-task result table
- the strategy summary with tasks passed, total cost, and cost per solved task
- the risk floor
- the escalation criteria that were supported by traces

P09 is successful when you can defend a routing policy with measured outcomes, not just with intuition about model capability.
