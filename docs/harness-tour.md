# Harness Tour

The full tour lives in [`02-harness-tour.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/02-harness-tour.md). This page introduces what you will look for before you start.

## The Task

After Agent Canvas onboarding is complete, ask a real code-reading question against `agent-canvas`:

```text
Find every place VITE_BACKEND_HOST and VITE_BACKEND_BASE_URL are read or set
in this project, and write a short note explaining how the dev script picks
the backend.
```

This task is useful because it is narrow, repeatable, and traceable. The agent has to search, read files, connect evidence, and answer without making broad edits.

## The Five Parts To Watch

| Harness part | What to inspect | Project that changes it |
|---|---|---|
| Model | Which model answered and how much it cost | [P02](/projects/p02-model-routing) |
| Tools | Which tools were available and used | [P03](/projects/p03-retrieval) |
| Memory | What the agent knew before searching | [P05](/projects/p05-memory) |
| Safety | What could run automatically or needed approval | [P06](/projects/p06-safety) |
| Architecture | Where the work ran and how state persisted | [P07](/projects/p07-capstone) |

## The Trace Is The Unit Of Diagnosis

Do not start by judging the final answer. Read the events:

- user message
- assistant planning
- tool call
- tool result
- edit or command
- confirmation
- compaction
- final answer

When a run fails, the trace shows where to look. That is why this course uses OpenHands.
