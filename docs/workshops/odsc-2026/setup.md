# Get started for the workshop

<a href="/learn-openhands-harness/slides/odsc-draft/s/odsc-cut-review/" target="_blank" rel="noreferrer">Full slide deck (draft, October 19)</a>

Choose how you want to participate. **We recommend inspecting the saved conversations in your own Agent Canvas.** You can follow the recorded decisions and tool results without waiting for a new run or paying for model calls.

| Option | What you do | When to choose it |
|---|---|---|
| **[1. Inspect in Agent Canvas (recommended)](./conversations#inspect-the-conversations-in-your-own-canvas)** | Import the lecture histories, filter the conversation list, and expand tool calls and results. | Follow along with the instructor and investigate the traces yourself. |
| [2. Run the full exercises](#run-new-exercises) | Start fresh conversations and perform the tasks with your own model access. | You have time to configure the tools and compare new runs. |

Download the [lecture examples](https://github.com/rajshah4/learn-openhands-harness/releases/download/odsc-lecture-conversations-2026-10-21/harness-lecture-conversations-2026-10-21.zip) and unzip the student ZIP. See [saved-conversation directions](./conversations) for the recommended Canvas import.

## Run the full exercises {#run-new-exercises}

The workshop uses Agent Canvas because it's open source and flexible. You can also try some of these exercises in another harness.

For the workshop, use **DeepSeek Flash through OpenHands** in all three harnesses: OpenHands, Pi, and OpenCode. You need one OpenHands **LLM API Key**. You do not need separate Anthropic, OpenAI, or DeepSeek keys. You will save the key and create the three profiles in the Canvas UI. One preparation command writes the provider files needed by Pi and OpenCode; you do not need to edit JSON.

## 1. Check your prerequisites

On macOS or Linux, open a terminal and run:

```bash
node --version
npm --version
python3 --version
git --version
```

Use Node.js 22.19 or newer, Python 3.11 or newer, and Git. If a command is missing, install [Node.js](https://nodejs.org/en/download), [Python](https://www.python.org/downloads/), or [Git](https://git-scm.com/downloads) before continuing. On Windows, use WSL and run all commands inside WSL.

## 2. Install and launch Canvas

Install the tested versions of Canvas and the two additional harnesses:

```bash
npm install -g @openhands/agent-canvas@1.29.0 @earendil-works/pi-coding-agent@0.83.0 pi-acp@0.0.33 opencode-ai@1.18.23
agent-canvas
```

Open the URL printed in your terminal. Leave Canvas running and open a **second terminal** for the remaining commands.

Use the local npm installation for this workshop. Canvas and the lab's Python environment need access to the same local files. The [Canvas installation docs](https://docs.openhands.dev/openhands/usage/agent-canvas/setup) cover other installation options.

## 3. Download the workshop materials

In your second terminal, choose a folder for the course and run:

```bash
git clone https://github.com/rajshah4/learn-openhands-harness.git
cd learn-openhands-harness
python3 -m venv .workshop-venv
.workshop-venv/bin/python -m pip install -r workshops/odsc-2026/labs/requirements.txt
```

If you already have a current course checkout, open a terminal in that folder and skip the clone. If `python3 --version` reported an older version, use your installed Python 3.11 or newer interpreter in the `-m venv` command.

Run the remaining commands from the `learn-openhands-harness` folder.

Prepare the workspaces for all six exercises:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare-all
```

This creates a fresh session outside the checkout with the workspaces for all six exercises. Open `WORKSPACES.txt` for each workspace’s Canvas profile, task prompt and check command. It also prints the Python interpreter path to use in the exercise prompts. Preparation makes no model requests. Running it again creates a new session and preserves earlier work.

## 4. Prepare the Pi and OpenCode connection files

In your course terminal, run:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/setup_canvas.py files
```

This writes provider settings in `~/.openhands/odsc-2026/` and prints **two Command lines**, one for Pi and one for OpenCode. Keep that terminal open so you can copy them into Canvas in step 6. Each command contains paths for your machine; copy the entire printed line.

This step asks for no key and makes no changes to Canvas. The files contain secret references, not credential values.

## 5. Add your key and model in Canvas

The official [first-time setup guide](https://docs.openhands.dev/openhands/usage/agent-canvas/first-time-setup) explains the initial Canvas configuration. Use the workshop-specific key and model settings below for these exercises.

Sign in to [OpenHands Cloud](https://app.all-hands.dev). Open **Settings → API Keys** and copy your **LLM API Key**. A Cloud API Key is a different credential and will not work here.

### Save the key for Pi and OpenCode

In your **local Canvas browser tab**:

1. Open **Settings → Secrets → Add a new secret**.
2. Set **Name** to `ODSC_LLM_API_KEY` exactly.
3. Paste your OpenHands LLM key into **Value**.
4. Click **Add secret**.

Keep the key out of prompts and exercise files. You will reuse this same key in the OpenHands LLM profile below; you do not need another provider account.

### Create the OpenHands LLM profile

1. Open **Settings → LLM → Add LLM Profile**.
2. Set **Profile Name** to `Workshop-DeepSeek`.
3. Select the **Basic** tab.
4. Set **LLM Provider** to **OpenHands**.
5. Set **LLM Model** to `deepseek-v4-flash`. Select that exact entry.
6. Leave **Provider connection** as **None** and paste the same LLM key into **API Key**.
7. Click **Save**.

If your model picker does not list Flash, use the **Advanced** tab: set **Custom Model** to `openhands/deepseek-v4-flash`, **Base URL** to `https://llm-proxy.app.all-hands.dev/v1`, and **API Key** to your OpenHands LLM key. Do not substitute another model silently.

Check your account's current model access and pricing before running. See [OpenHands model access](https://github.com/OpenHands/docs/blob/main/openhands/usage/llms/openhands-llms.mdx).

## 6. Create the three agent profiles in Canvas

An **LLM profile** describes a model connection. An **agent profile** chooses the harness. OpenHands uses the LLM profile you just saved. Pi and OpenCode use their own provider files plus the saved secret.

### OpenHands

Open **Settings → Agent → Add agent profile** and fill in:

| Field | Value |
|---|---|
| Profile Name | `Workshop-OpenHands` |
| Agent | **OpenHands** |
| LLM profile | **Workshop-DeepSeek** |
| Tools | Choose tools; leave only **terminal** and **file_editor** enabled for the first comparison |

For this initial setup, set **MCP servers** to **Choose servers** and turn every server off. Under **Secrets**, select **Choose secrets** and enable only `ODSC_LLM_API_KEY`. Click **Save**.

### Pi

See the official [ACP agents guide](https://docs.openhands.dev/openhands/usage/agent-canvas/acp-agents) for how Canvas connects to external agents such as Pi and OpenCode. The settings below use the workshop’s shared model configuration.

Click **Add agent profile** again and fill in:

| Field | Value |
|---|---|
| Profile Name | `Workshop-Pi` |
| Agent | **ACP (external subprocess)** |
| Preset | **Custom** |
| Command | Paste the complete **Workshop-Pi Command** printed in step 4 |
| Model | `openhands/deepseek-v4-flash` |

Under **Secrets**, select **Choose secrets** and turn on only `ODSC_LLM_API_KEY`. Set **MCP servers** to **Choose servers** and turn every server off. Click **Save**.

Use **Custom** here so Canvas launches Pi with the supplied OpenHands provider configuration. Typing a model name into an ordinary Pi preset is not enough. You do not need Pi's Anthropic key or `PI_AUTH_JSON` for this setup.

### OpenCode

Click **Add agent profile** once more:

| Field | Value |
|---|---|
| Profile Name | `Workshop-OpenCode` |
| Agent | **ACP (external subprocess)** |
| Preset | **Custom** |
| Command | Paste the complete **Workshop-OpenCode Command** printed in step 4 |
| Model | `openhands/deepseek-v4-flash` |

Under **Secrets**, select **Choose secrets** and turn on only `ODSC_LLM_API_KEY`. Set **MCP servers** to **Choose servers** and turn every server off. Click **Save**.

ACP (Agent Client Protocol) lets Canvas communicate with these external agents. Each makes its own model requests. All three profiles now point to the same OpenHands-hosted Flash model. Start a new conversation after changing profiles.

## 7. Check all three harnesses

Run this before starting the exercises:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/setup_canvas.py verify
```

This runs the small pagination repair in three separate fresh workspaces using the profiles you saved in the UI. It checks the resolved model, then independently runs pytest and checks the repaired behavior and allowed file changes. It prints a Canvas conversation link for each run. Look for:

```text
PASS Workshop-OpenHands
PASS Workshop-Pi
PASS Workshop-OpenCode
```

The full lines also include the model and check result. Verification makes real model requests. Its workspaces and reports are stored in a new `../odsc-runs/setup-check-*` folder each time. They are separate from your exercise workspaces. If any run fails, open its conversation and fix the setup before comparing harnesses. A setup failure is not a model result.

## 8. Open Exercise 1

Use the session folder and `WORKSPACES.txt` printed in step 3. You already have these fresh copies:

| Folder inside your session | Canvas profile |
|---|---|
| `w1-openhands` | `Workshop-OpenHands` |
| `w1-pi` | `Workshop-Pi` |
| `w1-opencode` | `Workshop-OpenCode` |

1. In Canvas, choose **Open Workspace** and select the full `w1-openhands` path from the index.
2. Select **Workshop-OpenHands**.
3. Open the [Exercise 1 page](/workshops/odsc-2026/exercises/00-working-harness), copy its task prompt, and replace the Python interpreter placeholder with the path printed by `prepare-all`. Paste it into a new Canvas conversation.
4. Check that the conversation's workspace matches the printed path. The Files panel should contain `toyapp/pagination.py` and `tests/test_pagination.py`.

For Pi or OpenCode, open its own folder, choose the matching profile, and start a new conversation with the same task prompt from the Exercise 1 page. Do not open the entire course checkout or session folder as the agent's editing workspace. Each harness needs the original bug, so do not reuse a repaired copy.

After each run, copy its exact **After the run, check** command from `WORKSPACES.txt` into your course terminal. The command already contains your interpreter and workspace paths.

For a fresh set of all six exercises, run `prepare-all` again and use its new session. To retry one condition, use the preparation command on its exercise page with a new workspace path. For example:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w1 --workspace ../odsc-runs/w1-pi-retry
```

Single-workspace preparation also refuses existing directories, so it will not overwrite your work.

The untouched Exercise 1 starter should fail its checks because it contains the planted bug. The repaired version should pass. Other exercises have different expected baselines; follow their preparation and checking instructions.

Open [Exercise 1](/workshops/odsc-2026/exercises/00-working-harness) or the [prompt index](/workshops/odsc-2026/prompts) to continue. These profiles are a starting configuration. Follow each exercise when it asks you to change tools, models, or goal settings. If a capability is unavailable, inspect the [saved conversations in Agent Canvas](./conversations).

## If setup stops

- **Cannot connect to Canvas or missing API-key file:** start local Canvas first. If it prints a different port, add `--canvas-url http://localhost:PORT` to both helper commands. If you use a different Canvas state directory, supply its `api-key.txt` with `--key-file /path/to/api-key.txt`.
- **HTTP 401 or 403 from model access:** use the OpenHands **LLM API Key**, not the Cloud API Key, and confirm your account can access the model.
- **Pi or OpenCode shows another model:** use the named Workshop profile, not an older profile with “Agent default.” Start a new conversation after changing profiles and rerun verification.
- **Empty workspace:** choose the directory printed by `prepare`. Do not ask the agent to search your laptop for the course files.
- **Want to use your own provider:** you can configure another supported provider, but record the model change. A comparison with different models does not isolate the harness.

<details>
<summary>Optional: create the profiles automatically</summary>

If you prefer a command to the UI steps, run this after installing the harnesses and cloning the course:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/setup_canvas.py configure
```

It prompts for your OpenHands LLM key, checks model access, writes the provider files, and creates the same three Workshop profiles through Canvas's API. It leaves existing profiles available and updates only the named Workshop profiles and their shared LLM profile and secret when rerun.

If your OpenHands key is already saved as `LLM_API_KEY` in Canvas, add `--use-canvas-key` to reuse it without pasting it again. This option validates access; it does not assume a differently named provider key is equivalent.

</details>
