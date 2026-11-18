# MLOps conference workshop

<a href="/learn-openhands-harness/slides/mlops-2026-workshop-slides.pdf" target="_blank" rel="noreferrer">Workshop slides (PDF)</a>

Six exercises for the MLOps conference edition of Harness Engineering. Each exercise asks you to make a harness design decision and use the trace to assess it.

Choose how you want to participate. **Open the public Canvas to follow along without installing anything.** You can inspect the saved conversations without a login, model key or new model calls.

| Option | What you do | When to choose it |
|---|---|---|
| **[1. Browse the public Canvas](http://34.215.46.146:8080/)** | Open the read-only MLOps workshop archive and expand tool calls and results. No installation, login or model key is needed. | Fastest way to follow the workshop and inspect the recorded work. |
| [2. Inspect in your own Canvas](./conversations#inspect-in-your-own-agent-canvas) | Download and import the same histories into a local Canvas. | Keep the conversations after the temporary server is removed. |
| [3. Run the exercises yourself](./setup#run-a-fresh-exercise) | Start fresh conversations with your own configured model and workspace. | Change the harness and compare new runs. |

The public server is temporary and read-only. It uses plain HTTP. Do not enter credentials or private information. New runs, edits and resumed conversations are blocked.

Use [Get started](./setup) for setup details and [saved conversations](./conversations#browse-the-public-canvas) for direct workshop links. Open the [exercise prompts](./prompts) when running a fresh attempt.

| Exercise | Open the instructions | Harness decision |
|---|---|---|
| 1 | [Compare harnesses](./exercises/00-working-harness) | Same task and model, different harnesses. |
| 2 | [Choose tool access](./exercises/01-add-harness-capability) | Match tool access to the task. |
| 3 | [Choose context](./exercises/02-place-context) | Inspect what context changes in the trace. |
| 4 | [Route models](./exercises/03-model-routing) | Write a routing and escalation policy. |
| 5 | [Verification](./exercises/04-api-migration) | What evidence should the harness require before accepting the agent’s work? |
| 6 | [Multi-agent systems](./exercises/05-multi-agent) | When should you use multiple agents, and how should they divide and integrate the work? |

The separate [MLOps saved-conversation bundle](./conversations) is built and verified in a fresh local Canvas store. It includes all six exercises, with original SVG outputs for Exercise 4 and the migration history for Exercise 5. Download the published edition from the saved-conversation page.
