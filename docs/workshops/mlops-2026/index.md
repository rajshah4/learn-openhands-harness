# MLOps conference workshop

Six exercises for the MLOps conference edition of Harness Engineering. Each exercise asks you to make a harness design decision and use the trace to assess it.

Exercise 5 focuses on verification: deciding what evidence establishes that an agent’s work meets the task’s requirements. The API migration makes that decision concrete. Exercise 6 focuses on multi-agent systems: deciding when another agent helps, how to divide the work, and who checks and integrates the results.

Start with [setup](./setup) and open the [exercise prompts](./prompts). You can follow the instructor's recorded examples or run a fresh attempt with your own configured model.

| Exercise | Open the instructions | Harness decision |
|---|---|---|
| 1 | [Compare harnesses](./exercises/00-working-harness) | Same task and model, different harnesses. |
| 2 | [Choose tool access](./exercises/01-add-harness-capability) | Match tool access to the task. |
| 3 | [Choose context](./exercises/02-place-context) | Inspect what context changes in the trace. |
| 4 | [Route models](./exercises/03-model-routing) | Write a routing and escalation policy. |
| 5 | [Verification](./exercises/04-api-migration) | What evidence should the harness require before accepting the agent’s work? |
| 6 | [Multi-agent systems](./exercises/05-multi-agent) | When should you use multiple agents, and how should they divide and integrate the work? |

The separate [MLOps saved-conversation bundle](./conversations) is built and verified in a fresh local Canvas store. It includes all six exercises, with original SVG outputs for Exercise 4 and the migration history for Exercise 5. Download the published edition from the saved-conversation page.
