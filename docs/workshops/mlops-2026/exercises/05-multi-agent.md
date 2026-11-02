# Exercise 6: What You Want Is a Multi-Agent System?

Another agent adds another context window, another tool loop, and another path
through the problem. It also adds setup, tokens, handoffs, and coordination.
This exercise tests whether a hard problem contains enough independent work to
earn those costs.

## The Claim

> Hard problems need multiple agents. Parallel workers and specialized critics
> will outperform one general agent.

Anthropic reported that its multi-agent research system outperformed a single
agent by 90.2% on an internal research evaluation. It also reported that token
use explained 80% of performance variance and that multi-agent systems used
about fifteen times as many tokens as ordinary chat. Research often contains
many independent searches. Anthropic warns that coding tasks usually contain
fewer independent branches. See [How we built our multi-agent research
system](https://www.anthropic.com/engineering/multi-agent-research-system).

The first question is whether multiple agents improved the strategy or simply
spent more compute.

## Why Sixteen Agents Chased One Bug

Anthropic's C compiler experiment ran sixteen agents in parallel. At first,
they encountered the same compiler failure, chased the same bug, and risked
overwriting one another. The task was difficult, but the next useful action was
still one shared action.

Parallel work became useful after the harness used GCC as a known-good oracle
to isolate different failing file sets. Each agent then owned a distinct
failure surface. See [Building a C compiler with a team of parallel
Claudes](https://www.anthropic.com/engineering/building-c-compiler).

Difficulty did not create parallelism. The harness had to find separable work
and objective feedback.

## Spend Three Agent Cards

Your pair receives three agent cards and one shared compute budget. Allocate
them across two problems.

### Problem A: Coupled repair

An async defect spans one shared execution path. Every new finding changes what
the next step should inspect. Workers need the same repository state and are
likely to edit the same files.

### Problem B: Independent investigation

The Incident Operations Center needs separate evidence about persistence and
restart behavior, browser workflows, and concurrency recovery. These branches
can inspect isolated workspaces and return findings to one owner.

Choose one architecture for each problem:

1. **One generalist:** one context, plan, implementation, and verifier loop.
2. **Worker and validator:** one agent implements while a fresh agent evaluates
   the validation contract from Exercise 5.
3. **Parallel specialists:** isolated workers investigate independent branches
   and return evidence to a synthesis owner.

| Decision | Coupled repair | Independent investigation |
|---|---|---|
| Architecture | | |
| Independent branches | | |
| State every worker needs | | |
| Files workers may change | | |
| Handoff required | | |
| Synthesis owner | | |
| Total compute budget | | |

## Match the Compute

If the single agent receives 60,000 tokens, the multi-agent system does not
receive 60,000 tokens per agent. Predict what happens when every architecture
receives the same total model-call or token budget.

| Architecture | Verified result | Wall time | Total calls | Total tokens | Duplicate work | Conflicts | Synthesis cost |
|---|---:|---:|---:|---:|---:|---:|---:|
| One generalist | | | | | | | |
| Worker and validator | | | | | | | |
| Parallel specialists | | | | | | | |

Agent Canvas makes the hidden work visible. Inspect parent and child traces,
repeated repository orientation, overlapping files, messages, returned
evidence, and work the parent repeats after a weak handoff.

## Does the Validator Need to Be an Agent?

Exercise 5 established the need for an independent completion standard. A
test, static check, browser script, external evaluator, or person may enforce
that standard more cheaply than another model.

Another agent earns the validator role when judgment is difficult to encode
and the evaluator has a separate goal, fresh context, authority to reject the
work, and a bounded output contract. Copying the implementer's context into a
new model and asking whether the work looks good provides little independence.

## Inspect the Handoff

A useful child return tells the parent:

- What it checked
- Evidence it found
- Files it changed, if any
- Remaining uncertainty
- Its recommended next action

A transcript dump makes the parent repeat the investigation. A conclusion
without evidence makes the result hard to trust.

## Write a Delegation Policy

```text
Another agent earns its cost when:

The work can be separated because:

Keep one agent when:

Use an independent agent as validator when:

Use code or another deterministic gate when:

Each child owns:

Each child returns:

Agents may share:

Agents must not share:

The synthesis owner is:

The total compute budget is:

Stop parallel work when:
```

Multi-agent systems make separable work parallel and can give independent
judgments fresh context. Tightly coupled work often turns the extra agents into
coordination work.
