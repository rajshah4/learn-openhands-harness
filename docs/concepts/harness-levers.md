# Harness Levers

Each project changes one lever. Keep the task stable, change the harness, then inspect whether behavior improves.

## The Levers

| Lever | Question | Project |
|---|---|---|
| Trace | Can you explain what happened? | [P01](/projects/p01-agent-trace) |
| Model | Did the task need the expensive model? | [P02](/projects/p02-model-routing) |
| Retrieval | Did extra search improve the answer? | [P03](/projects/p03-retrieval) |
| Decomposition | Did smaller prompts beat one large prompt? | [P04](/projects/p04-decomposition) |
| Memory | Did durable context reduce re-discovery? | [P05](/projects/p05-memory) |
| Safety | Did the harness bound the blast radius? | [P06](/projects/p06-safety) |
| Critic | Did evaluation stop false completion? | [P07](/projects/p07-capstone) |
| Workflow | Did model-authored orchestration reduce glue code? | [P08](/projects/p08-dynamic-workflows) |
| Escalation | Did routing recover when cheap got stuck? | [P09](/projects/p09-model-routing-benchmark) |
| History | Did indexing past sessions beat scanning them? | [P10](/projects/p10-history-index) |

## The Rule

Excessive harness features can lead to bloat. Use traces and metrics to ensure your harness is optimized for your work.

That is why the course teaches: predict, run, inspect, measure, keep.
