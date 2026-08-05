# P11: Subagents and Context Isolation

## What You Do

Run the same work two ways: one single conversation vs. isolated child conversations plus a synthesis step, and measure quality, tokens, cost, wall time, and compaction. Decide, with numbers, whether a branch earned its own context window. Three task shapes stress the boundary: a small repo audit, a breadth-first research corpus, and a large-repo investigation.

## Harness Mechanism

Manual `RemoteConversation` children give per-child cost, tokens, wall time, and compaction so the context boundary is measured directly. A companion runner uses native OpenHands `TaskToolSet`, exposed to the parent as the `task` tool, and traces the parent and child conversations in Laminar. Child model routing, parallelism, and probe delay are knobs for testing why isolation might help.

## Open First

- [`projects/p11-subagents/README.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p11-subagents/README.md)
- [`starter/run_compare.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p11-subagents/starter/run_compare.py)
- [`starter/run_scenario_b.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p11-subagents/starter/run_scenario_b.py)
- [`solution/`](https://github.com/rajshah4/learn-openhands-harness/tree/main/projects/p11-subagents/solution)

## Keep

A "when to use subagents" decision rule, grounded in your own table: what kind of task earns a separate context, what kind does not, and which cheaper alternative you would try first.

The reusable artifact is not the child-agent code. It is the habit of treating the context boundary as a harness decision that needs evidence, one you settle with your own numbers rather than a prior belief about whether subagents help.
