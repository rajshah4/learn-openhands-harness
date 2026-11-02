# MLOps conference workshop

Six exercises for the MLOps conference edition of Harness Engineering. Exercises 1 to 4 and 6 carry over the existing workshop material into a separate conference path. Exercise 5 uses a Pydantic API migration and an external HTTP verifier.

Start with [setup](./setup), open the [exercise prompts](./prompts), and record decisions in the [worksheet](./worksheet). You can follow the instructor's recorded examples or run a fresh attempt with your own configured model.

| Exercise | Open the instructions | Harness decision |
|---|---|---|
| 1 | [Compare harnesses](./exercises/00-working-harness) | Same task and model, different harnesses. |
| 2 | [Choose tool access](./exercises/01-add-harness-capability) | Match tool access to the task. |
| 3 | [Choose context](./exercises/02-place-context) | Inspect what context changes in the trace. |
| 4 | [Route models](./exercises/03-model-routing) | Write a routing and escalation policy. |
| 5 | [Verify an API migration](./exercises/04-api-migration) | Compare actual HTTP responses with frozen expectations. |
| 6 | [Delegate work](./exercises/05-multi-agent) | Choose ownership, delegation and integration boundaries. |

The separate [MLOps saved-conversation bundle](./conversations) is built and verified in a fresh local Canvas store. It includes all six exercises, with original SVG outputs for Exercise 4 and the migration history for Exercise 5. Download the published edition from the saved-conversation page.
