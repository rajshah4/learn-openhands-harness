# Set up for the MLOps workshop

Choose whether to follow the instructor's saved traces or run the exercises. Reading traces needs no model key. New coding attempts need a model configured in your own harness.

## Inspect recorded work

Use [saved conversations](./conversations) for the current selection and availability. Download the separate MLOps ZIP and follow its preview, import and tag-filter steps. The bundle was tested with a fresh ordinary Canvas store and no model key. See the saved-conversation page for the tested versions and recovery directions.

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
