# Harness Decision Worksheet

Use one row for each workshop exercise. The goal is not to collect every possible feature. The goal is to justify each component with evidence.

## Claim Verdict

Complete this after every evidence reveal:

```text
Claim:

Our verdict:
[ ] Supported in this test
[ ] Supported with a narrower condition
[ ] Not supported in this test

The evidence:

The boundary of this test:

What we would test next:
```

| Decision | Our choice | Evidence we expect | Cost or new failure mode | Escalation trigger |
|---|---|---|---|---|
| Working trace |  |  |  |  |
| Tool surface |  |  |  |  |
| Scaffolding and context |  |  |  |  |
| Model routing |  |  |  |  |
| Long-running control |  |  |  |  |
| Multi-agent design |  |  |  |  |

## Opening Trace

```text
Our selected task:

We predicted the largest difference would be:

I trust the result because:

The harness, rather than the model alone, supplied:

The first efficiency measurement I would add is:

The trace explains:

The provider ledger measures:

If these disagree, I will:

After an interruption, the first thing I would reverify is:
```

## Tool-Surface Rule

```text
Use the terminal or API when:

Add an MCP connection when:

Load a tool by default when:

Make it discoverable on demand when:

Prefer a small API or CLI interface when:

Block or require approval when:

The evidence that would change our choice is:
```

## Context Budget

```text
A line earns a place in AGENTS.md when:

A procedure becomes a skill when:

A fact earns persistent memory when:

Keep state in a task checkpoint when:

Retrieve information again when:

Enforce a rule outside the model when:

Delete saved context when:

We will review and prune these artifacts when:
```

## Long-Running Contract

Select the state that must survive an interruption:

- [ ] Objective
- [ ] Explicit completion criteria
- [ ] Current plan and next action
- [ ] Changed files and repository state
- [ ] Latest verifier evidence
- [ ] Failed approaches
- [ ] Environment identity
- [ ] Remaining token, cost, or iteration budget
- [ ] Allowed actions and workspace boundary

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
```

## Model Routing Matrix

| Task | Initial model or tier | Reasoning level | Verifier | Escalation signal |
|---|---|---|---|---|
| Simple edit |  |  |  |  |
| Off-by-one bug |  |  |  |  |
| Async bug |  |  |  |  |
| Authentication review |  |  |  |  |

## Multi-Agent Boundary

```text
Another agent earns its cost when:

The work can be separated because:

Keep one agent when:

Use an independent agent as validator when:

Use code or another deterministic gate when:

Each child owns:

The child returns:

Agents may share:

Agents must not share:

The synthesis owner is:

The independent verifier is:

The total compute budget is:

Stop parallel work when:
```

## Final Recovery Plan

List the next three actions in order. Each action should cite state, evidence, risk, or budget.

1.
2.
3.
