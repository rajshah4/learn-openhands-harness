# P08: Dynamic Workflows

| | |
|---|---|
| **What You Do** | Start from a manual deep-research orchestrator, then replace the fixed Python loop with a workflow-capable harness where the model chooses angles, fans out research, verifies claims, and synthesizes the report. |
| **Harness Mechanism** | Workflow tool + model-authored orchestration + skills that constrain when and how the model may coordinate sub-agents |

**Phase: REDUCE ORCHESTRATION CODE.** P04 taught decomposition where your application code owns the sequence: docs check, setup check, safety check, aggregate. This lesson uses the deep-research example from [rajshah4/workflow-demos](https://github.com/rajshah4/workflow-demos): the old way is a hand-written loop over research angles, verification passes, and final synthesis; the new way gives the model a workflow tool and a skill so it can write the short-lived fan-out/fan-in plan itself.

The shift is not "give up control." You still own the harness contract: available sub-agent roles, tool surface, safety limits, max fan-out, artifact paths, and evaluation criteria. What moves out of application code is the brittle orchestration glue: choosing angles, deciding which independent work can run in parallel, and reducing the results.

## Directory guide

| Directory | What's inside |
|---|---|
| `starter/` | `run_dynamic_workflow.py` is the manual deep-research baseline. Python owns the angles, runs each research pass, runs each fact-check pass, and aggregates the report. |
| `solution/` | `run_dynamic_workflow.py` is only the dynamic workflow build: it loads the workflow skill, registers `web_searcher`, `fact_checker`, and `synthesizer` sub-agents, creates the parent workflow agent, and sends one research objective. |

## Read these first

Before building the solution, skim the docs and examples that define the moving parts:

- [OpenHands Agent Skills & Context](https://docs.openhands.dev/sdk/guides/skill): how reusable instructions enter the agent context.
- [OpenHands Sub-Agent Delegation](https://docs.openhands.dev/sdk/guides/agent-delegation): the underlying fan-out/fan-in pattern and why sub-agents need bounded roles.
- [workflow-demos deep research](https://github.com/rajshah4/workflow-demos): the open example this lesson adapts.
- [Dynamic Workflows deep-dive video](https://www.youtube.com/watch?v=PtbrKTgj3X8): walkthrough of the deep-research example and model-authored orchestration.
- [Claude Code dynamic workflows](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code): the product pattern behind model-authored orchestration.
- [Cursor 2.4 skills and subagents](https://cursor.com/changelog/2-4): another example of moving procedural knowledge into model-readable skills.

## Current SDK status

As of June 4, 2026, OpenHands dynamic workflow support is still in [software-agent-sdk PR #3426](https://github.com/OpenHands/software-agent-sdk/pull/3426), not necessarily in the default released SDK package. The dry-run commands in this lesson work today because they avoid live workflow imports. Live dynamic mode requires either the PR branch or a future SDK release that includes `WorkflowToolSet`.

## Agent-assisted path

1. Open this `README.md` and `starter/` only.
2. Ask your coding agent to explain the manual deep-research loop: fixed angles, research passes, verification passes, final synthesis.
3. Ask it what should remain in harness code versus what can move into a skill.
4. Ask it to build the solution without reading `solution/`.
5. Require it to run the dry-run smoke check. Only run live dynamic mode if your SDK install includes workflow support.
6. Compare against `solution/`, read `solution/README.md` for the solution brief, and write down what orchestration code disappeared and what guardrails had to be added.

## Before you run

Pause and predict:

- Which research angles are stable enough for a manual baseline?
- Which angles should the model be allowed to choose from the question?
- What claims need independent fact-checking because they go stale quickly?
- What should the workflow summary expose so the run is debuggable?
- How much additional cost is acceptable if the dynamic workflow improves coverage or removes repeated orchestration code?

## Setup

The starter dry run uses only the Python standard library:

```bash
cd projects/p08-dynamic-workflows/starter
uv run python run_dynamic_workflow.py --dry-run
```

The solution dry run shows the dynamic workflow setup without model calls:

```bash
cd projects/p08-dynamic-workflows/solution
uv run python run_dynamic_workflow.py --dry-run
```

Default research question:

```text
What is changing about AI coding assistants for software teams?
```

Override it by passing a question:

```bash
uv run python run_dynamic_workflow.py --dry-run \
  "How are coding agents changing release engineering?"
```

Live manual mode uses the same remote Agent Server path as P01-P05:

```bash
cd projects/p08-dynamic-workflows/starter
WORKSPACE_DIR=/path/to/repo \
uv run --with openhands-sdk --with openhands-tools \
  python run_dynamic_workflow.py \
  "How are coding agents changing release engineering?"
```

Live dynamic mode requires an OpenHands SDK build with `WorkflowToolSet`; see the current SDK status note above. If your installed SDK does not expose `openhands.tools.workflow`, the script exits with a clear message and the dry run still teaches the code-shape comparison.

```bash
cd projects/p08-dynamic-workflows/solution
WORKSPACE_DIR=/path/to/repo \
uv run --with openhands-sdk --with openhands-tools \
  python run_dynamic_workflow.py \
  "How are coding agents changing release engineering?"
```

## The comparison

Config A is the old way:

1. Python names the research angles.
2. Python sends one prompt per angle.
3. Python sends one fact-check prompt per angle.
4. Python decides when synthesis happens.
5. The model acts as a worker inside your fixed loop.

Config B is the dynamic workflow:

1. Python registers available roles: `web_searcher`, `fact_checker`, and `synthesizer`.
2. A skill tells the model when workflows are appropriate, what limits apply, and what artifacts must exist.
3. The model writes the short-lived workflow: which angles to research, which checks can run in parallel, and how to reduce results.
4. The trace and final report show whether that autonomy earned itself.

## General advice

- Keep hard guarantees in code: tool access, sandbox, max fan-out, artifact paths, and safety policy.
- Put reusable procedure in the skill: when to fan out, how to verify, how to preserve uncertainty, and what final shape to write.
- Start with the manual loop. If the same loop appears in three tasks, consider moving it into a workflow skill.
- Require a workflow summary. Dynamic orchestration is only useful if you can inspect what the model decided.
- Treat research claims as unstable by default. Ask fact-checkers to mark stale-risk claims rather than smoothing them into confident prose.
- Keep deterministic or compliance-critical sequences in code. Dynamic workflows are for adaptive planning, not for replacing auditably fixed control flow.

## What to look for

- Did the dynamic run choose research angles that fit the question better than the fixed list?
- Did it stay inside the skill limits?
- Did fact-checkers preserve uncertainty and stale-risk claims?
- Did the final report cite sources or clearly mark tool limitations?
- Did the workflow summary expose enough of the generated plan to debug?
- Did orchestration code shrink, or did complexity move into an untestable prompt?

## What you keep

Two artifacts:

- `workflow_orchestrator_skill.md`: the reusable deep-research workflow skill.
- `dynamic_workflow_decision_rule.md`: the rule for when dynamic workflows earn their complexity.

Good default decision rule:

> Use a dynamic workflow when the task has many independent research angles, the exact angles depend on the question, parallel exploration is useful, and the harness can verify or cite the output. Keep orchestration in code when the sequence is compliance-critical, tiny, or easier to test as deterministic control flow.

-> End of advanced path. Use the decision rule to decide whether dynamic workflows belong in your own `harness.py`.
