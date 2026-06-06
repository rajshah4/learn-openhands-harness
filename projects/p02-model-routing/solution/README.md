# Solution Brief: P02 Model Routing

## What This Solution Proves

This solution proves that model choice is a harness decision, not only a user preference. The same prompt runs three ways: flagship model, small model, and a routed configuration. The point is not to declare one model best. The point is to learn when the expensive model earns its cost.

The reference solution keeps routing intentionally small. It chooses one concrete `LLM` before the remote conversation starts, then builds the agent with that model. That makes the routing behavior easy to reason about and safe for remote Agent Server runs.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_routing.py` | Runs the flagship, small, and routed configurations and prints comparable metrics. |

There is only one solution file because this project is about the policy shape, not a larger artifact tree. The reusable thing is the routing function and the result table you record after running it.

## Key Design Choices

The solution separates three questions that are easy to mix together:

1. What does the flagship model cost on this exact task?
2. What does the small model cost and does it still answer correctly?
3. Can a simple policy choose the cheaper model for routine prompts while preserving a path to the flagship?

The routing rule is deliberately conservative. It sends ordinary text and code-search prompts to the small model, but routes prompts containing markers such as `security`, `architecture`, `image`, `screenshot`, or `multi-file edit` to the flagship.

That is not meant to be a universal taxonomy. It is a starter policy that a learner can challenge with traces.

## Why Routing Happens Before Agent Construction

The project uses a remote-safe pattern:

1. Build the flagship `LLM`.
2. Build the small `LLM`.
3. Classify the prompt in the harness.
4. Create the OpenHands agent with the selected concrete `LLM`.
5. Run the conversation.

That avoids depending on model switching mid-run. It also makes the result table honest: each configuration's cost belongs to one model choice. P02 is intentionally about the first, simplest model lever.

## How This Relates To P09

P02 is the introductory routing lesson: classify the task, choose one concrete model, then run the conversation. Later in the course, [P09: Model Routing Benchmark](../../p09-model-routing-benchmark/) turns the same idea into an advanced benchmark with `RouterLLM`, model tiers, profile switching, Agent Canvas-visible escalations, Laminar traces, and cost per solved task.

That progression is intentional. A learner should leave P02 with a small policy they can reason about before they try dynamic escalation.

## What To Compare Against Your Attempt

Your implementation should help you answer these questions:

| Question | What to check |
|---|---|
| Did the small model solve the default task? | Compare correctness against the flagship trace, not just final confidence. |
| Did cost move for the right reason? | Separate model price from extra turns, redundant retrieval, or failed searches. |
| Did the routed config choose what you expected? | Run the default prompt and at least one flagship-marker prompt. |
| Is the policy defensible? | You can explain which task types stay cheap and which route up. |

If your policy routes differently but you can defend it with trace and cost evidence, it can still be a good solution.

## Valid Variations

A valid solution might use different model names, more flagship markers, a small classifier function, or an `LLMRegistry` shape instead of two direct `LLM` variables. It might also record more fields from P01, such as files read or tool calls by type.

Be careful with policies that look smart but are hard to audit. P02 is not asking for a perfect router. It is asking for a policy small enough that you can predict its behavior before the run and compare that prediction against evidence after the run.

## What To Keep

Keep the routing policy only if it improves cost without hiding correctness loss. A useful P02 artifact is a short policy you would be willing to paste into the capstone harness:

- routine code-reading and text-only search tasks use the small model
- security, architecture, image, diagram, or multi-file edit tasks use the flagship
- the result table records cost, tokens, events, and correctness for each config
- the policy is revised when traces show the cheap branch is too aggressive

The final deliverable is not the exact marker list. It is the discipline of treating model choice as an explicit, measured harness rule.
