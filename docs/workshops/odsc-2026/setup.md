# Get started for the workshop

Use Agent Canvas to run the exercises and inspect the agent's work. This tutorial works with the free models available through OpenHands Cloud, or with your own provider keys and models. You can learn the same harness techniques with either path; results and run times will differ.

## Install Agent Canvas

```bash
npm install -g @openhands/agent-canvas
```

Launch it with `agent-canvas` and open the URL printed in your terminal. Follow the [Agent Canvas installation docs](https://github.com/OpenHands/docs/blob/main/openhands/usage/agent-canvas/setup.mdx) for prerequisites, platform instructions, and other installation options.

## Get model access

### OpenHands Cloud models

1. Sign in to [OpenHands Cloud](https://app.all-hands.dev).
2. Open **Settings → API Keys** and copy your **LLM API Key**, not a Cloud API Key.
3. In Agent Canvas, open **Settings → LLM**, choose **OpenHands**, paste the key, and select a model marked **Free**.
4. Save the configuration and select it for your OpenHands agent profile.

No separate provider key is needed for this path. Free-model availability and limits can change; choose a currently available free model. See the [OpenHands model-access docs](https://github.com/OpenHands/docs/blob/main/openhands/usage/llms/openhands-llms.mdx).

### Your own provider and model

Choose your provider in Canvas and enter its API key and a tool-capable model available to your account. For an OpenAI-compatible service, also enter its documented base URL; your provider's usage charges apply.

Keep keys in settings, not in prompts or exercise files.

## Add OpenCode and Pi through ACP

The harness-comparison exercises use OpenHands, OpenCode, and Pi. ACP (Agent Client Protocol) lets Canvas communicate with these other coding agents.

Install them on the machine running your Canvas backend. For a local setup, this is your laptop.

**OpenCode:**

```bash
npm install -g opencode-ai
```

**Pi and its ACP adapter:**

```bash
npm install -g @earendil-works/pi-coding-agent pi-acp
```

In Canvas's agent settings, select **ACP**, then a matching preset or **Custom**, and use the appropriate launch command:

| Agent | ACP launch command |
|---|---|
| OpenCode | `opencode acp` |
| Pi | `pi-acp` |

Configure the provider and model in each agent before starting the comparison. Saving an OpenHands model profile in Canvas does not automatically configure these external agents; using the OpenHands Cloud LLM key may require a custom provider configuration in each CLI. Follow the [Canvas ACP docs](https://github.com/OpenHands/docs/blob/main/openhands/usage/agent-canvas/acp-agents.mdx), [OpenCode provider docs](https://opencode.ai/docs/providers/), and [Pi provider instructions](https://www.npmjs.com/package/@earendil-works/pi-coding-agent). The [OpenCode ACP guide](https://opencode.ai/docs/acp/) and [Pi ACP adapter guide](https://github.com/svkozak/pi-acp) describe their launch requirements.

Start a new conversation after changing the agent. For a controlled comparison, use the same model and a separate copy of the starting workspace for each harness.

## Open the exercises

Go to [Exercise prompts](/workshops/odsc-2026/prompts) for direct links to every exercise's prompts and templates. Each exercise explains the starting files, configuration, and checks; use the copy button on its code blocks to copy a prompt into Canvas.

The [course repository](https://github.com/rajshah4/learn-openhands-harness) contains the starter projects. Download or clone it when an exercise needs local files, open the specified workspace in Canvas, and prepare its test dependencies before running the prompt.

To check your setup, open a tutorial workspace and ask:

```text
Read README.md in the current workspace using a tool.
Summarize what it teaches. Do not change any files.
```

Check that the conversation finishes, the trace shows a file-reading or terminal action, and the answer matches the file. Then start [Exercise 1](/workshops/odsc-2026/exercises/00-working-harness).
