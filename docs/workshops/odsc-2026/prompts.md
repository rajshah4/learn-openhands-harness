# Exercise prompts

Prepare a fresh workspace before sending a task. Run commands from the course
checkout after [setup](/workshops/odsc-2026/setup).

| Exercise | Case names for `lab.py` | Complete task and run instructions |
|---|---|---|
| 1. Harness choice | `w1` | [Pagination repair](/workshops/odsc-2026/exercises/00-working-harness) |
| 2. Tool design | `w2` | [PR explanation and MCP modes](/workshops/odsc-2026/exercises/01-add-harness-capability) |
| 3. Memory | `w3-none`, `w3-older`, `w3-current` | [Next-page browsing](/workshops/odsc-2026/exercises/02-place-context) |
| 4. Routing | `w4-rename`, `w4-pagination`, `w4-async`, `w4-security` | [Four runnable tasks](/workshops/odsc-2026/exercises/03-model-routing) |
| 5. Goals | `w5`, `w5-goal` | [Ordinary repair and native-goal objective](/workshops/odsc-2026/exercises/04-let-it-run) |
| 6. Delegation | `w6-single`, `w6-validator` | [Two architecture prompts](/workshops/odsc-2026/exercises/05-multi-agent) |

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prepare w3-current --workspace ../odsc-runs/my-memory-run
```

This prints the complete task and that lane's supplied notes with your Python
interpreter path. Copy the entire output prompt into a fresh agent conversation.
To print it again without creating another workspace:

```bash
.workshop-venv/bin/python workshops/odsc-2026/labs/lab.py prompt w3-current
```

Keep the course checkout outside the agent workspace. Run its external checker
from your own terminal after the agent stops. The [worksheet](/workshops/odsc-2026/worksheet)
records predictions, evidence, and decisions. [Saved results](/workshops/odsc-2026/results)
provide a fallback when live access is unavailable.
