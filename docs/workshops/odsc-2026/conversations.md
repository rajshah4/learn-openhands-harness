# Choose your workshop path

Choose how you want to participate. **We recommend inspecting the saved conversations in your own Agent Canvas.** You can follow the recorded decisions and tool results without waiting for a new run or paying for model calls.

| Option | What you do | When to choose it |
|---|---|---|
| **[1. Inspect in Agent Canvas (recommended)](#inspect-the-conversations-in-your-own-canvas)** | Import the lecture histories, filter the conversation list, and expand tool calls and results. | Follow along with the instructor and investigate the traces yourself. |
| [2. Run the full exercises](./setup#run-new-exercises) | Start fresh conversations and perform the tasks with your own model access. | You have time to configure the tools and compare new runs. |

Download the [lecture examples ZIP](https://github.com/rajshah4/learn-openhands-harness/releases/download/odsc-lecture-conversations-2026-10-24/harness-lecture-conversations-2026-10-24.zip) and extract it. The selection contains 12 primary lecture conversations, three worker histories and two original animation outputs.

## Inspect the conversations in your own Canvas

These directions use a **local npm installation of Agent Canvas**. Follow the [Canvas installation prerequisites](https://docs.openhands.dev/openhands/usage/agent-canvas/setup) before continuing.

1. If Canvas is not installed, install it:

   ```sh
   npm install -g @openhands/agent-canvas
   ```

   If Canvas is already installed, skip this step. Leave it stopped until after the import.

2. **Stop Canvas before loading the saved conversations.** If Canvas is running, press **Ctrl-C** in the terminal running it. This is part of the import process: Canvas must be stopped while the importer adds the saved conversations to its local store. If Canvas is not running, continue to step 3.

3. **Load the saved conversations.** Open a terminal in the extracted `harness-lecture-conversations` folder. Preview the import, check the printed destination, then install:

   ```sh
   python3 import_into_canvas.py
   python3 import_into_canvas.py --install
   ```

   No model key or Canvas session credential is needed. The importer checks the package hashes, refuses conflicting conversation IDs, and adds 15 histories: 12 primary lecture conversations and three team-worker histories. It preserves their 472 recorded events. Repeating the same import verifies the installed files without duplicating them.

4. **Start Canvas to view the saved conversations:**

   ```sh
   agent-canvas
   ```

   Open the URL printed in its terminal. On first launch, choose your usage-data preference and **Skip for now** on model setup. The “LLM isn’t set up” banner only affects new runs; saved histories still open. Beside **Conversations**, choose **View → Filter by tags → `lecture=odsc2026`**. Click **More** if the list is collapsed. Open a conversation and expand its tool calls and observations.

**Compatibility note:** The import was tested on macOS with Agent Canvas 1.29.0, Agent Server 1.56.0 and a fresh Canvas store. These are tested versions, not required install pins. Other versions, Windows, Linux, Docker and remote-backend imports have not been verified. If the import does not work with your setup, follow the instructor’s Canvas walkthrough during the session.

The npm launcher normally stores conversations in `~/.openhands/agent-canvas/dev_conversations`. If you configured another local store, pass its absolute path with `--store /absolute/path/dev_conversations`. If your backend uses a custom port, pass its loopback URL with `--backend-url http://127.0.0.1:PORT` so the stopped-backend check uses the right port. The importer previews by default and changes files only with `--install`.

The imported records are for inspection. To try a task yourself, start a fresh conversation in the exercise's workspace. Historical commands refer to the recorded environment, and imported archive agents have no model credentials or executable tools configured.

The earlier stale-memory example uses historical custom tool types. The importer supplies documented generic compatibility wrappers for those records; messages, tool-call arguments, results, IDs, and timestamps are retained. The original package remains unchanged, and `odsc-lecture-import.json` beside the store records the import and compatibility mappings.

## Already imported an earlier download?

Download and extract the current ZIP above. Stop Canvas, run the included `python3 import_into_canvas.py` to preview, then `python3 import_into_canvas.py --install`. For the October 21 package, this updates the display names without replacing recorded events or creating duplicate conversations. Restart Canvas and filter by **`lecture=odsc2026`**.

## Run the full exercises

If you have time, follow [the exercise prompts](./prompts) and [model/tool setup](./setup#run-new-exercises). Start fresh conversations in the specified workspaces. New results may differ from the recorded examples.

## Recover or remove the import

Keep the original ZIP and extracted package. If the importer reports a collision or changed history, keep your existing data; it does not overwrite it. The receipt lists the exact imported IDs and event hashes. Stop Canvas before removing imported history folders, and remove only those listed in the receipt. Leave other conversations, settings, credentials and workspaces alone.
