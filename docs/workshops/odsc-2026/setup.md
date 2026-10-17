# Get started for the workshop

The workshop uses Agent Canvas because it's open source and flexible. You can also try some of these exercises in another harness.

Use the free models available through OpenHands Cloud or connect your own provider keys and models. The choice is yours.

## Install Agent Canvas

```bash
npm install -g @openhands/agent-canvas
```

Run `agent-canvas` in your terminal, then open the URL it prints. Use this local npm installation for the workshop so the Python paths printed by the lab helper are available to the agent. Follow the [Agent Canvas installation docs](https://github.com/OpenHands/docs/blob/main/openhands/usage/agent-canvas/setup.mdx) for prerequisites, platform instructions, and other installation options.

## Get model access

### OpenHands Cloud models

1. Sign in to [OpenHands Cloud](https://app.all-hands.dev).
2. Open **Settings → API Keys** and copy your **LLM API Key**, not a Cloud API Key.
3. In Agent Canvas, open **Settings → LLM**, choose **OpenHands**, paste the key, and select a model marked **Free**.
4. Save the configuration and select it for your OpenHands agent profile.

No separate provider key is needed for this path. Free-model availability and limits can change; choose a currently available free model. See the [OpenHands model-access docs](https://github.com/OpenHands/docs/blob/main/openhands/usage/llms/openhands-llms.mdx).

### Your own provider and model

Choose your provider in Canvas, enter its API key, and select a model that supports tool use. You can use Anthropic, OpenAI, or another supported provider. For an OpenAI-compatible service, also enter its documented base URL. Your provider's usage charges apply.

Keep keys in settings, not in prompts or exercise files.

## Add other harnesses through ACP (optional)

OpenHands is enough to start every exercise. Adding OpenCode or Pi is optional for exploring another harness. ACP (Agent Client Protocol) lets Canvas communicate with these other coding agents.

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

Start a new conversation after changing the agent so you can explore how each harness works.

## Prepare the local lab package

Install Python 3.11 or newer and Git. On macOS or Linux, open a terminal and run:

```bash
git clone https://github.com/rajshah4/learn-openhands-harness.git
cd learn-openhands-harness
python3 -m venv .workshop-venv
.workshop-venv/bin/python -m pip install -r workshops/odsc-2026/labs/requirements.txt
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py list
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-openhands
```

Check `python3 --version` before creating the environment. It must report 3.11 or newer; if your machine has an older default, use your installed `python3.11` or newer interpreter in the `-m venv` command.

On Windows use WSL for this workshop's shell commands and ACP agents.
The helper prints the workspace and full prompt with your interpreter path.
In Canvas, choose **Open Workspace**, select the printed directory, start a new conversation, and paste the prompt. Prepare a different path
for each run you want to compare. The helper refuses to prepare an existing directory, so it won't overwrite
previous work. Set `PYTHONPATH=src` for the slugify workspace; its printed
prompt includes this instruction. The other packages import from their root.

Keep the course checkout's checker and saved results outside
the agent's editing workspace. After a run, execute the checker yourself:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py check w1 --workspace ../odsc-runs/w1-openhands
```

The untouched pagination starter should fail. That is the planted defect,
not an installation error. Exercise 3 starts with passing regression tests but
fails the new-feature checker. Exercise 5's original tests pass while its dot
assertion fails. Check the exercise page for its expected baseline.

## Check your agent before starting

Ask it to read `README.md` in the prepared workspace without changing files.
Check that the trace shows the agent reading the file and that its answer matches the contents. Then use a new
conversation for the exercise. If you want to compare runs, record the Canvas, Agent Server, and agent
versions, resolved model, enabled tools, automatic memory/skills, and limits.
If your setup supports OpenTelemetry (OTel), you can connect a compatible observability tool to save traces.

## Start an exercise

Open [Exercise prompts](/workshops/odsc-2026/prompts). Each exercise has a
preparation command, complete prompt, optional check or citation checklist,
and decision worksheet. If live model access, MCP, goals, or delegation is
unavailable, inspect the [saved runs and results](/workshops/odsc-2026/results) instead of running that exercise yourself. Use the small scenarios to explore memory, tools, routing, goals, and delegation. After trying the supplied prompt, you can adapt the task to your own interests. Your model's results may differ from the saved measurements.

