# Solution Brief: P08 Dynamic Workflows

## What This Solution Proves

This solution proves that some orchestration belongs in code, and some can move into a bounded model-authored workflow. P04 used a fixed Python sequence. P08 asks a different question: when the right research angles depend on the question, can the harness give the model a workflow tool and a tight skill instead of hard-coding every branch?

The answer is conditional. Dynamic workflows are useful only when the generated plan is bounded, inspectable, and easier to maintain than repeated application code.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_dynamic_workflow.py` | Registers roles, loads the workflow skill, builds the parent workflow agent, and writes dynamic research artifacts. |
| `workflow_orchestrator_skill.md` | The reusable skill that constrains when and how the model may orchestrate sub-agents. |
| `dynamic_workflow_decision_rule.md` | The artifact to keep. It states when dynamic workflows earn their complexity. |

Read the decision rule first if you want the policy. Read the skill next to see what moved from Python code into model-readable procedure.

## Key Design Choices

The solution keeps hard guarantees in code:

- registered sub-agent roles
- available tools
- artifact paths
- max-iteration limit
- workspace copying
- SDK import checks

The model gets flexibility only inside those boundaries. The skill tells it when to use a workflow, how many research angles to choose, when to fact-check, how to preserve uncertainty, and which artifacts to write.

The dry run is intentionally useful. Because workflow support may depend on a specific OpenHands SDK build, `--dry-run` still shows the roles, skill path, and parent prompt without requiring live workflow imports.

## How OpenHands Fits In

The solution uses OpenHands skills, sub-agent registration, and `WorkflowToolSet`. The parent agent has the workflow tool and the orchestration skill. Child agents are registered as `web_searcher`, `fact_checker`, and `synthesizer`.

The trace should show the generated fan-out/fan-in plan. If the workflow is not visible enough to debug, it is not a good harness feature.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Did orchestration code shrink for the right reason? | The skill should replace brittle glue, not hide important policy. |
| Did the chosen research angles fit the question? | Compare model-chosen angles against the fixed manual baseline. |
| Did verification preserve uncertainty? | Fact-checkers should mark stale-risk or unsupported claims. |
| Were artifacts inspectable? | `DEEP_RESEARCH_REPORT.md` and `WORKFLOW_SUMMARY.md` should explain what happened. |

P08 is a bad fit if every task would use the same fixed sequence or if the sequence must be compliance-auditable line by line.

## Valid Variations

A valid solution might register different roles, use a different artifact contract, or keep some research angles fixed while letting the model choose the rest. It might also decide that dynamic workflows do not belong in the learner's final harness yet.

The boundary is control. Code owns safety, roles, limits, and artifacts. The model may author the short-lived plan only inside that contract.

## What To Keep

Keep:

- the workflow skill if it made the generated plan better and debuggable
- the decision rule for when workflows are appropriate
- the artifact contract for workflow summaries

P08 is successful when you can explain which orchestration moved out of code and why that did not remove accountability from the harness.
