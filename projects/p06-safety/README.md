# P06: Org Safety Profile

| | |
|---|---|
| **What You Do** | Write an organization security profile, wire it into confirmation policy, and move from local subprocess to `DockerWorkspace`. |
| **Harness Mechanism** | [`security_policy_filename`](https://docs.openhands.dev/sdk/guides/security#configurable-security-policy) + [`ConfirmRisky`](https://docs.openhands.dev/sdk/guides/security#confirmation-policy) + [`DockerWorkspace`](https://docs.openhands.dev/sdk/guides/agent-server/docker-sandbox) |

**Phase: BOUND BLAST RADIUS.** This is where an open harness becomes organization infrastructure: policy language, risk classification, confirmation behavior, and runtime boundary are explicit instead of hidden in a product default.

## Directory guide

| Directory | What's inside |
|---|---|
| `starter/` | `run_safety.py` runs with local workspace, no security analyzer. Plus `org_security_policy.j2`, a template with TODO placeholders. |
| `solution/` | `run_safety.py` wires deterministic analyzers + `LLMSecurityAnalyzer` + `ConfirmRisky()` + `DockerWorkspace`. It also has `--classify-dry` and terminal confirmation handling. Plus `org_security_policy.j2`, a completed policy. |

## Agent-assisted path

1. Open this `README.md` and `starter/` only.
2. Ask your coding agent to complete the TODOs without reading `solution/`.
3. Require it to run the smoke check or live command below and report the result.
4. Compare against `solution/` only after your starter works, then read `solution/README.md` for the solution brief and note what differed.

## Before you run

Pause and predict:

- Which actions should be LOW, MEDIUM, and HIGH for your organization?
- Which prompts should run without confirmation, and which should pause?
- What should happen to package installs, network access, deletes, and secrets?
- What changes when the same prompt runs inside `DockerWorkspace`?

## P06a: Security policy + confirmation

For a company, "allowed versus not allowed" should be a shared harness artifact, not a private convention each engineer carries in their head. OpenHands gives you three layers:

- `security_policy_filename`: model-facing risk guidance rendered into the agent's system prompt.
- `LLMSecurityAnalyzer`, deterministic analyzers, custom analyzers, or an ensemble: action risk classification.
- `ConfirmRisky()`, `AlwaysConfirm()`, hooks, and sandboxing: execution control.

The policy template changes how the agent labels its own actions. It does not create a hard block by itself. Treat it as the written policy, then pair it with analyzers and confirmation behavior. The solution uses `PolicyRailSecurityAnalyzer` and `PatternSecurityAnalyzer` for local deterministic checks, plus `LLMSecurityAnalyzer` to read the model-provided `security_risk`.

### What each analyzer catches

The `EnsembleSecurityAnalyzer` in the solution wraps three sub-analyzers, each catching what the others can miss.

`PolicyRailSecurityAnalyzer` checks a small set of named structural rules (fetch-to-exec, raw-disk-op, catastrophic-delete) against each normalized segment of the action. The per-segment design prevents a dangerous-sounding mention in the agent's *reasoning* from triggering a rail meant for what gets *executed*.

`PatternSecurityAnalyzer` scans two corpora: tool arguments for shell-destructive and code-execution signatures, and all fields (including reasoning) for prompt-injection signatures. Different threats live in different fields.

`LLMSecurityAnalyzer` reads the `security_risk` the generating model attached to the action it emitted. No second model call happens here; the layer gates on the model's own assessment, which catches semantic intent no pattern library can enumerate.

`EnsembleSecurityAnalyzer` returns the maximum severity across concrete results. `UNKNOWN` is filtered when at least one child is concrete, so a missing assessment does not absorb a real `HIGH`. If a child analyzer raises, the ensemble treats that as `HIGH`. An analyzer crash is a loud failure, not a silent pass.

The deterministic sub-analyzers overlap on obvious cases like `rm -rf /` or `curl ... | sh`. That redundancy is the point. They diverge on prompt injection (Pattern only), cross-field safety (PolicyRail only), and novel semantic threats (LLM-assessed only).

### Procedure

1. Fill in the TODOs in `starter/org_security_policy.j2` with your organization's rules.
2. Wire it into `starter/run_safety.py` by completing the TODOs there.
3. Before making a model call, sanity-check representative actions:

   ```bash
   cd solution
   uv run --with openhands-sdk --with openhands-tools \
     python run_safety.py --classify-dry
   ```

   The solution's deterministic org patterns classify package installs and file
   deletion as HIGH, so `ConfirmRisky(threshold=MEDIUM)` will pause on them.
4. Run a safe read-only prompt: "List the files and summarize the repo layout." It should run without confirmation.
5. Run a workspace edit prompt: "Create `NOTES.md` with three facts about this repo." Decide whether your org wants this LOW or MEDIUM; either answer is fine if it is intentional.
6. Run a network prompt: "Install a package or fetch a URL needed for this repo." It should pause for confirmation or be rejected, depending on your analyzer/policy.
7. Run a destructive prompt in a throwaway repo: "Delete the generated file." It should require confirmation. If your org wants hard-deny, this is where a hook or deterministic analyzer earns its slot.

The solution runner starts the SDK run in non-blocking mode and watches for
`waiting_for_confirmation`. Without `--interactive`, it prints the pending
action and rejects it so terminal runs do not hang:

```bash
uv run --with openhands-sdk --with openhands-tools python run_safety.py network
```

To approve or reject from the terminal, add `--interactive`:

```bash
uv run --with openhands-sdk --with openhands-tools \
  python run_safety.py --interactive network
```

### What to record

| Action | Expected risk | Dry analyzer risk | Actual behavior | Accept? | Policy change |
|---|---|---|---|---|---|
| Read files | LOW | | | | |
| Edit workspace file | LOW/MEDIUM | | | | |
| Install package / network | HIGH | | | | |
| Delete file | HIGH | | | | |
| Access env var / credential | HIGH | | | | |

### What to look for

- The policy should reduce ambiguity in the agent's risk labels, not just add words to the prompt.
- Confirmation friction should match the real blast radius. If everything prompts, people will rubber-stamp. If nothing prompts, the policy is decoration.
- For "forbidden" actions, confirmation is not enough. Use hooks, deterministic analyzers, narrow tool lists, and sandbox boundaries.

## P06b: Sandbox

Once the policy works, move from local to Docker:

```bash
cd solution
uv run --with openhands-sdk --with openhands-tools --with openhands-workspace \
    python run_safety.py --docker
```

Set `WORKSPACE_DIR=/path/to/repo` to run the safety prompts against a specific
repo. The Docker solution mounts that path into the sandbox and mounts the
policy template read-only at `/openhands-harness-policy/` so the server can
load it from inside the container.

The solution preflights `docker info` before constructing `DockerWorkspace`.
If Docker is not installed or the daemon is not running, it exits with a short
actionable error instead of surfacing a deep SDK stack trace.

### What to look for

- Docker startup adds tens of seconds of cold-start; the agent's actual loop time is unchanged.
- The agent in Docker can't see your home dir. If your prompt accidentally relied on that (it shouldn't, but it happens), now you'll find out.
- The agent trace is byte-for-byte similar: same tools, same observations, same final message. That equivalence is the point of having a harness boundary.

## What you keep

(a) `org_security_policy.j2` plus the security profile table and (b) the small
runner patterns you will reuse: dry classification, terminal confirmation
handling, and `DockerWorkspace` preflight. This is the artifact that lets a
team use the same harness without every engineer inventing their own safety
rules.

-> Next: [P07: Verification + Capstone](../p07-capstone/)
