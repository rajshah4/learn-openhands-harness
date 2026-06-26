# P08: Dynamic Workflows

## What Problem Are You Solving?

P04 taught decomposition where your application code owns the sequence. This lesson asks what happens when you hand that sequencing to the model. Starting from a manual deep-research orchestrator (a hand-written Python loop over angles, verification passes, and synthesis), you replace the fixed loop with a workflow-capable harness where the model chooses angles, fans out research, verifies claims, and synthesizes the report.

The shift is not "give up control." You still own the harness contract: available sub-agent roles, tool surface, safety limits, max fan-out, artifact paths, and evaluation criteria. What moves out of application code is the brittle orchestration glue, choosing angles, deciding what can run in parallel, and reducing results.

Before you run, predict. Which research angles are stable enough for a manual baseline, and which should the model pick from the question? What claims need independent fact-checking because they go stale quickly? What should the workflow summary expose so the run is debuggable? How much extra cost is acceptable if the dynamic version improves coverage or removes repeated orchestration code?

## Start With These Files

Open this README and `starter/` only. Ask your coding agent to explain the manual loop, decide what stays in code versus what moves into a skill, build the solution without reading `solution/`, run the dry run, then compare and read `solution/README.md`. Write down what orchestration code disappeared and what guardrails had to be added.

| Purpose | Starter | Solution |
|---|---|---|
| Deep-research orchestrator | `starter/run_dynamic_workflow.py` (manual: Python owns angles, passes, aggregation) | `solution/run_dynamic_workflow.py` (dynamic: loads the skill, registers sub-agents, sends one objective) |
| Artifacts to keep | | `solution/workflow_orchestrator_skill.md`, `solution/dynamic_workflow_decision_rule.md` |

## The Two Configs

**A, the old way:** Python names the angles, sends one research prompt and one fact-check prompt per angle, and decides when synthesis happens. The model is a worker inside your fixed loop.

**B, the dynamic workflow:** Python registers the available roles (`web_searcher`, `fact_checker`, `synthesizer`) and a skill that tells the model when workflows are appropriate, what limits apply, and what artifacts must exist. The model writes the short-lived plan: which angles to research, which checks run in parallel, how to reduce results. The trace and final report show whether that autonomy earned itself.

The dividing line: keep hard guarantees in code (tool access, sandbox, max fan-out, artifact paths, safety policy); put reusable procedure in the skill (when to fan out, how to verify, how to preserve uncertainty, what final shape to write).

## Run It

The starter dry run uses only the standard library; the solution dry run shows the dynamic setup without model calls:

```bash
cd projects/p08-dynamic-workflows/starter
uv run python run_dynamic_workflow.py --dry-run

cd projects/p08-dynamic-workflows/solution
uv run python run_dynamic_workflow.py --dry-run
```

The default question is "What is changing about AI coding assistants for software teams?"; pass your own as an argument. Live mode uses the same remote Agent Server path as P01 to P05:

```bash
WORKSPACE_DIR=/path/to/repo \
uv run --with 'openhands-sdk>=1.29.2' --with 'openhands-tools>=1.29.2' \
  python run_dynamic_workflow.py "How are coding agents changing release engineering?"
```

Most course scripts default to `AGENT_SERVER=http://127.0.0.1:18000`. If your local Agent Canvas ingress exposes Agent Server on port `8000`, add `AGENT_SERVER=http://127.0.0.1:8000` to the command.

**SDK status:** verified June 26, 2026. [software-agent-sdk PR #3426](https://github.com/OpenHands/software-agent-sdk/pull/3426) was merged on June 6, 2026, and the released `openhands-tools>=1.29.2` package exposes `openhands.tools.workflow.WorkflowToolSet`. The command above asks `uv` for current SDK packages so live dynamic mode can import the workflow tool. If an older environment shadows those packages, the solution script exits with a clear message and the dry run still teaches the code-shape comparison.

## Record The Results

| Question | A manual | B dynamic |
|---|:--:|:--:|
| Angles fit the question? | (fixed) | |
| Stayed inside skill limits? | n/a | |
| Fact-checkers preserved uncertainty? | | |
| Final report cited sources / marked limits? | | |
| Workflow summary debuggable? | n/a | |
| Orchestration code shrank? | baseline | |
| Cost | | |

## How To Read The Results

- Did the dynamic run pick angles that fit the question better than the fixed list, and stay inside the skill limits?
- Did fact-checkers preserve uncertainty and stale-risk claims instead of smoothing them into confident prose?
- Did orchestration code actually shrink, or did the complexity just move into an untestable prompt?

Guidance for your own use: start with the manual loop, and only move it into a workflow skill if the same loop shows up in three tasks. Always require a workflow summary, since dynamic orchestration is only worth it if you can inspect what the model decided. Keep deterministic or compliance-critical sequences in code; dynamic workflows are for adaptive planning, not for replacing auditably fixed control flow.

<details>
<summary>References</summary>

- [OpenHands Agent Skills and Context](https://docs.openhands.dev/sdk/guides/skill) and [Sub-Agent Delegation](https://docs.openhands.dev/sdk/guides/agent-delegation): the moving parts.
- [workflow-demos deep research](https://github.com/rajshah4/workflow-demos) and the [deep-dive video](https://www.youtube.com/watch?v=PtbrKTgj3X8): the example this lesson adapts.
- [Claude Code dynamic workflows](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) and [Cursor 2.4 skills and subagents](https://cursor.com/changelog/2-4): the product patterns behind model-authored orchestration.

</details>

## What Students Should Leave With

Two artifacts: `workflow_orchestrator_skill.md` (the reusable deep-research skill) and `dynamic_workflow_decision_rule.md` (when dynamic workflows earn their complexity). A good default:

> Use a dynamic workflow when the task has many independent research angles, the exact angles depend on the question, parallel exploration is useful, and the harness can verify or cite the output. Keep orchestration in code when the sequence is compliance-critical, tiny, or easier to test as deterministic control flow.

Other advanced extensions: [P09: Model Routing Benchmark](../p09-model-routing-benchmark/) and [P10: Indexing Agent History](../p10-history-index/).
