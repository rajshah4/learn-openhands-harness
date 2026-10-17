# Exercise prompts

Prepare a fresh workspace before sending a task. Run commands from the course
checkout after [setup](/workshops/odsc-2026/setup).

| Exercise | Complete task and run instructions |
|---|---|
| 1. Harness choice | [Pagination repair](/workshops/odsc-2026/exercises/00-working-harness) |
| 2. Tool design | [PR explanation and MCP modes](/workshops/odsc-2026/exercises/01-add-harness-capability) |
| 3. Memory | [Next-page browsing](/workshops/odsc-2026/exercises/02-place-context) |
| 4. Routing | [Four runnable tasks](/workshops/odsc-2026/exercises/03-model-routing) |
| 5. Goals | [Ordinary repair, native goal, and blocked-goal probe](/workshops/odsc-2026/exercises/04-let-it-run) |
| 6. Delegation | [Two architecture prompts](/workshops/odsc-2026/exercises/05-multi-agent) |

Open your exercise page above, follow its configuration steps, and copy the task prompt into a new Canvas conversation. Use the matching workspace listed in your session's `WORKSPACES.txt`.

Where a prompt contains `/absolute/path/to/.workshop-venv/bin/python`, replace it with the Python interpreter path printed by `prepare-all`. Keep the rest of the task unchanged for a harness comparison.

<details>
<summary>Optional: get a prompt from the terminal</summary>

Local prompt copies are saved in your session's `prompts/` folder with the interpreter path already filled in. You can also print one without creating a workspace:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prompt w3-current
```

</details>

Keep the course checkout outside the agent workspace. Run its external checker
from your own terminal after the agent stops. The [worksheet](/workshops/odsc-2026/worksheet)
records predictions, evidence, and decisions. [Saved results](/workshops/odsc-2026/results)
provide a fallback when live access is unavailable.
