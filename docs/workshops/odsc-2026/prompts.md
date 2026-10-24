# Exercise prompts

Prepare a fresh workspace before sending a task. Run commands from the course
checkout after [setup](/workshops/odsc-2026/setup).

| Exercise | Complete task and run instructions |
|---|---|
| 1. Harness choice | [Pagination repair](/workshops/odsc-2026/exercises/00-working-harness) |
| 2. Tool design | [PR explanation and MCP modes](/workshops/odsc-2026/exercises/01-add-harness-capability) |
| 3. Memory | [Prior customer agreement](/workshops/odsc-2026/exercises/02-place-context) |
| 4. Routing | [Counter and controlled security repair](/workshops/odsc-2026/exercises/03-model-routing) |
| 5. Goals | [Staged checkpoint and native continuation](/workshops/odsc-2026/exercises/04-let-it-run) |
| 6. Delegation | [Reservation and optional ledger prompts](/workshops/odsc-2026/exercises/05-multi-agent) |

Open your exercise page above, follow its configuration steps, and copy the task prompt into a new Canvas conversation. Use a separate fresh workspace for each condition; the updated pages provide preparation commands.

Where a prompt contains `/absolute/path/to/.workshop-venv/bin/python`, replace it with the Python interpreter path printed by `prepare-all`. Keep the rest of the task unchanged for a harness comparison.

<details>
<summary>Optional: get a prompt from the terminal</summary>

Prompt copies for all six exercises are saved in your session’s `prompts/` folder. W1/W2 copies include the Python interpreter path. You can also print a task without creating a workspace:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/classroom.py prompt w3-agreement-accepted
```

</details>

Keep the course checkout outside the agent workspace. Run its external checker from your own terminal after the agent stops. If you cannot run an exercise, inspect its saved conversation in [Agent Canvas](./conversations).
