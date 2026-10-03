# ODSC 2026: Engineering the Harness

This is the participant path for the two-hour ODSC workshop. You will not spend the session filling in starter code. You will make design decisions, compare them with a neighbor, and inspect what those decisions change in a real coding-agent trace.

Follow [Get started for the workshop](/workshops/odsc-2026/setup) to install Canvas, connect a model, and add OpenCode or Pi through ACP. Open [Exercise prompts](/workshops/odsc-2026/prompts) for direct links to the tasks and templates. You can also follow the instructor demonstrations and complete the worksheet.

## What You Will Build

You will leave with an annotated harness design covering:

- Trace and loop observability
- Retrieval and codebase understanding
- Context, memory, and skills
- Long-running execution state
- Tools, verification, and safety boundaries
- Model and reasoning routing
- Multi-agent architecture

## How Each Exercise Works

1. Inspect a problem or changed constraint.
2. Choose among plausible harness techniques.
3. Discuss your choice with a neighbor.
4. Predict what the trace or measured result will show.
5. Compare your prediction with the evidence.
6. Mark the claim as supported, supported with a narrower condition, or not
   supported in this test.
7. Record the decision and its tradeoff in the [workshop worksheet](/workshops/odsc-2026/worksheet).

Agent Canvas is our microscope. The instructor will use it to show conversation history, model decisions, tool calls, observations, edits, verification, compaction, and final answers in order.

## Workshop Route

| Exercise | Question |
|---|---|
| [Same Model, Different Harnesses](/workshops/odsc-2026/exercises/00-working-harness) | How do calls, context, time, and evidence change when the model stays fixed? |
| [Do You Need an MCP?](/workshops/odsc-2026/exercises/01-add-harness-capability) | Does MCP improve the result over an API the terminal can already reach? |
| [What Should the Agent Remember?](/workshops/odsc-2026/exercises/02-place-context) | Which instructions, skills, and memories earn their cost on future tasks? |
| [Use the Strongest Model for Everything?](/workshops/odsc-2026/exercises/03-model-routing) | Can verification and escalation make routing cheaper without lowering quality? |
| [Let It Run Until It Figures It Out?](/workshops/odsc-2026/exercises/04-let-it-run) | Does more time create progress, and what must the harness still enforce? |
| [What You Want Is a Multi-Agent System?](/workshops/odsc-2026/exercises/05-multi-agent) | Does another agent add useful parallel work or coordination cost? |

## After the Workshop

The [optional long-project lab](/workshops/odsc-2026/long-project) contains the exact incident benchmark prompt, reproduction steps, and guidance for adapting it to your own application.

The full self-paced course contains the runnable starter and solution projects behind the other exercises. Begin with [P01: Agent Trace](/projects/p01-agent-trace), then select projects based on the parts of your harness you want to investigate.
