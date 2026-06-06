# Solution Brief: P06 Org Safety Profile

## What This Solution Proves

This solution proves that safety is a layered harness design, not a single prompt. The organization policy tells the agent how to classify risk, but policy text alone does not enforce anything. The reference solution pairs that policy with analyzers, confirmation behavior, terminal handling, and a Docker runtime boundary.

P06 is where the harness starts to look like shared team infrastructure. The rules are explicit enough that two engineers can run the same prompts and get the same risk posture.

## Start With These Files

| File | Why it matters |
|---|---|
| `org_security_policy.j2` | The model-facing organization risk policy. |
| `run_safety.py` | Wires analyzers, confirmation handling, representative dry classification, and optional Docker workspace. |

Read the policy first to understand the intended risk categories. Then read the runner to see how the policy is enforced.

## Key Design Choices

The solution separates policy from enforcement:

- `org_security_policy.j2` gives the agent LOW, MEDIUM, and HIGH risk language.
- `PolicyRailSecurityAnalyzer` catches structural safety rails.
- `PatternSecurityAnalyzer` catches deterministic high-risk patterns, including project-specific package install and delete rules.
- `LLMSecurityAnalyzer` reads the model-provided `security_risk`.
- `EnsembleSecurityAnalyzer` returns the maximum concrete severity.
- `ConfirmRisky(threshold=MEDIUM)` pauses before medium or high risk actions.

The solution also includes `--classify-dry`. That command classifies representative actions without model calls or workspace changes. It is the cheapest way to find policy/analyzer disagreement before running live prompts.

## How OpenHands Fits In

OpenHands lets the conversation receive a security analyzer and confirmation policy after construction. The runner starts the conversation in non-blocking mode, watches for `WAITING_FOR_CONFIRMATION`, and either rejects pending actions in non-interactive mode or asks the terminal user to approve them.

For sandboxing, the solution can switch to `DockerWorkspace`. The policy file is mounted read-only into the container so the agent server can load the same policy inside the runtime boundary.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Does dry classification match your policy? | Read, edit, network, and delete prompts should land in intentional risk categories. |
| Does confirmation friction match blast radius? | Safe reads should not prompt; risky actions should pause or reject. |
| Does Docker change visibility? | The agent should lose host-home access while preserving the same task behavior. |
| Can terminal runs avoid hanging? | Non-interactive confirmation should print and reject instead of waiting forever. |

If everything prompts, users will rubber-stamp. If nothing prompts, the policy is decoration.

## Valid Variations

A valid organization policy may classify workspace edits as LOW or MEDIUM. Either can be right if the decision is explicit. A valid solution may also hard-deny certain actions with hooks or narrower tool lists rather than allowing confirmation.

The important boundary is that dangerous behavior cannot depend on a private convention in the operator's head. It has to live in the harness.

## What To Keep

Keep:

- the organization security policy
- the dry classification table
- the confirmation threshold
- any deterministic org-specific patterns
- the Docker preflight and read-only policy mount pattern

P06 is successful when the team can explain what the agent may do automatically, what requires confirmation, and what should never run in this harness.
