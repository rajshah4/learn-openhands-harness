# MLOps harness decision worksheet

Make the prediction before opening the result. Record evidence from the trace rather than the agent's claim of success.

| Exercise | Our choice | Expected observation | What happened | What we would change |
|---|---|---|---|---|
| 1. Harness | | | | |
| 2. Tools | | | | |
| 3. Context | | | | |
| 4. Routing | | | | |
| 5. Verification | | | | |
| 6. Multi-agent systems | | | | |

## Exercise 5: Verification

What evidence should the harness require before accepting the agent’s work?

```text
The client behavior we would freeze before migration:

What the agent's own model test establishes:

What an HTTP replay checks in addition:

The exact expected/actual mismatch:

The code change that responds to it:

Who invoked the verifier in this recorded run:

What the passing replay establishes:
```

## Exercise 6: Multi-agent systems

When should you use multiple agents, and how should they work together?

```text
Keep one agent when:

Add another agent when:

The independent work each agent owns:

The context and tools each agent needs:

Who verifies and integrates the results:

The coordination cost we would accept:

The evidence that would change our choice:
```
