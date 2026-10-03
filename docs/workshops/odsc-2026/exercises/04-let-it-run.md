# Exercise 5: Let It Run Until It Figures It Out?

A capable agent can plan, edit, test, and recover from errors. The popular
move is to give it a goal, keep it in a loop, and allow enough time to finish.
This exercise tests who decides that the goal has actually been reached.

## The Claim

> Give a capable agent a goal and enough time. It can manage the work and
> decide when it is done.

Long-running work separates four decisions that a short prompt can hide:

1. **Goal:** the outcome that must remain active across turns and interruptions.
2. **Plan:** the agent's current approach, which should change when evidence
   contradicts it.
3. **Validation contract:** independent evidence that establishes completion.
4. **Autonomy policy:** when the harness continues, replans, escalates, or
   stops.

## Factory's Uncomfortable Result

Factory compared a single coding agent with a system that established an
independent completion measure before implementation. In one GDAL recreation,
the single agent wrote 17,000 lines of C++, reproduced 36% of the reference
behavior, and stopped because it believed it was done. It had not exhausted
its time or budget. The system run with the same model reached 90%.

The system used far more time and compute, and Factory reported one run per
cell rather than repeated averages. The result still exposes the failure we
care about: more available compute cannot help an agent that has already
decided to stop. Read [What it Takes for Coding Agents to Complete Large
Software Tasks](https://factory.ai/news/what-it-takes-for-coding-agents-to-complete-large-software-tasks).

## Write the Goal

The Incident Operations Center task asks an agent to add persistence,
concurrency, recovery, APIs, and a browser workflow to an existing application.
Choose what should remain active after compaction or a fresh session:

```text
A. Improve the incident application.

B. Implement the requested persistence and recovery features.

C. Deliver the requested incident system, preserve its existing behavior,
   satisfy the agreed acceptance contract, and stay inside the workspace and
   approval boundary.
```

The durable goal should describe the outcome and constraints. The plan belongs
in the checkpoint because implementation discoveries may invalidate it.

## Define Done Before Seeing the Work

Choose six checks for the validation contract. You will not see the agent's
implementation first.

- [ ] Existing regression tests pass
- [ ] Incidents survive a process restart
- [ ] Repeated alerts are deduplicated
- [ ] Stale concurrent updates are rejected
- [ ] Escalation leases recover after failure
- [ ] Import and export round-trip correctly
- [ ] HTTP behavior works through the public API
- [ ] The browser workflow works at mobile width
- [ ] The agent reports that every requested file was changed
- [ ] The implementation contains at least 1,000 new lines

The last two are easy to measure but do not establish the outcome. After pairs
commit to their checks, the instructor reveals the full eight-part external
verifier.

## The Agent Says It Is Done

Inspect the prepared OpenHands trace. The agent completed its plan and its own
tests pass, but the external verifier reports seven of eight requirements. The
browser workflow still has a defect.

Choose the next harness action:

1. Accept completion because the agent completed its plan.
2. Give it another twenty calls with no new information.
3. Return the failed gate as evidence and require a changed plan.
4. Escalate immediately to another model or a person.

The failed gate changes the agent's understanding of the remaining work.
Additional turns alone do not.

## Should the Loop Continue Again?

After one repair attempt, decide whether another continuation is justified:

| Evidence | Continue | Replan | Escalate | Stop |
|---|---|---|---|---|
| Workspace changed and the gate improved | | | | |
| Workspace changed but the same gate still fails | | | | |
| The same gate failed and the workspace did not change | | | | |
| The call budget is exhausted | | | | |
| The agent requests an out-of-scope action | | | | |

Prime Agent implements this separation directly. A persistent goal stores the
objective and its budget across turns. Autonomous mode decides whether to add
another continuation based on quality gates and turn, token, or wall-clock
limits. It also avoids rerunning the same failed gate when the workspace has
not changed. See [Prime Agent's long-running agent
documentation](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/long-running-agents.md).

## Write the Long-Running Contract

```text
Goal:

Completion requires:

Progress requires new evidence such as:

Continue when:

Change strategy when:

Reverify after:

Escalate when:

Stop when:

Maximum turns, time, tokens, or cost:

State that must survive compaction:
```

A long-running harness needs more than a bigger loop. It must preserve the
goal, keep the completion standard independent of the implementation, and
decide whether another turn has earned its cost.
