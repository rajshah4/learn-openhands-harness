# Set up for the MLOps workshop

<a href="/learn-openhands-harness/slides/mlops-2026-workshop-slides.pdf" target="_blank" rel="noreferrer">Workshop slides (PDF)</a>

Choose how you want to participate. **Open the public Canvas to follow along without installing anything.** You can inspect the saved conversations without a login, model key or new model calls.

| Option | What you do | When to choose it |
|---|---|---|
| **[1. Browse the public Canvas](http://34.215.46.146:8080/)** | Open the read-only MLOps workshop archive and expand tool calls and results. No installation, login or model key is needed. | Fastest way to follow the workshop and inspect the recorded work. |
| [2. Inspect in your own Canvas](./conversations#inspect-in-your-own-agent-canvas) | Download and import the same histories into a local Canvas. | Keep the conversations after the temporary server is removed. |
| [3. Run the exercises yourself](#run-a-fresh-exercise) | Start fresh conversations with your own configured model and workspace. | Change the harness and compare new runs. |

The public server is temporary and read-only. It uses plain HTTP. Do not enter credentials or private information. New runs, edits and resumed conversations are blocked.

## Inspect recorded work

Open the [public MLOps Canvas](http://34.215.46.146:8080/) or use the [direct workshop links](./conversations#find-each-exercise). It contains all 15 saved histories and 575 events, plus both original Exercise 4 SVG outputs.

To keep a local copy, use [saved conversations](./conversations) to download the separate MLOps ZIP and follow its preview, import and tag-filter steps. The bundle was tested with a fresh ordinary Canvas store and no model key. See the saved-conversation page for the tested versions and recovery directions.

## Run a fresh exercise

Use your existing Agent Canvas installation, or follow the [official Canvas setup guide](https://docs.openhands.dev/openhands/usage/agent-canvas/setup). Open a fresh conversation and a separate workspace for each editing agent. Put keys in your own harness settings, never in task prompts or files you share.

For comparisons, hold the task, initial files, model and budget fixed. Record the actual model and harness versions. Do not assume the DeepSeek binding or availability from an older rehearsal still works.

Exercises 1 to 4 and 6 link their source projects and task instructions. Their historical recorded results remain attributed to those runs. There is no MLOps prepare-all command in this edition.

## Prepare Exercise 5

Use Python 3.12. From this course checkout:

```bash
python3 workshops/mlops-2026/exercise5/prepare.py
```

The command creates a unique session outside the checkout, prints its path and writes WORKSPACES.txt with exact interpreter and verifier commands. It makes no model calls and preserves previous sessions. Follow the printed commands to create separate old and new dependency environments. Verify the old service before handing the service directory to the agent.

The recorded migration used Canvas and SDK 1.49.6 server components with Canvas UI 1.24.0; a current local installation may differ. Record your versions and check actual event behavior rather than assuming that a configured hook executed.
