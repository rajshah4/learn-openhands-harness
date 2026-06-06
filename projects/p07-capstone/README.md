# P07: Verification + Capstone

| | |
|---|---|
| **What You Do** | Add a critic with iterative refinement and a rubric, score repeated runs against the same agent-trace criteria, then wire the kept artifacts into `harness.py`. |
| **Harness Mechanism** | [`Critic`](https://docs.openhands.dev/sdk/guides/critic) + [`IterativeRefinementConfig`](https://docs.openhands.dev/sdk/guides/iterative-refinement) + persisted agent traces |

**Phase: STOP "LOOKS FINE".** The final harness is not "done" because it produced a plausible answer once. It is done when the trace, rubric, and repeated runs show that the behavior is stable enough to trust.

## Directory guide

| Directory | What's inside |
|---|---|
| `starter/` | `evaluate.py` scaffolds the repeated-run critic experiment. `harness.py` is the capstone skeleton with TODO placeholders for every kept artifact from P01-P06. |
| `solution/` | `evaluate.py` runs no-critic vs. critic trials and scores them. `harness.py` wires routing, tools, security policy, Docker sandbox, and an optional API critic. |

## Agent-assisted path

1. Open this `README.md` and `starter/` only.
2. Ask your coding agent to complete the TODOs without reading `solution/`.
3. Require it to run the smoke check or live command below and report the result.
4. Compare against `solution/` only after your starter works, then read `solution/README.md` for the solution brief and note what differed.

## Before you run

Pause and predict:

- What pass-rate lift would justify adding a critic?
- What cost-per-pass would make the critic a bad tradeoff?
- Which P01-P06 decisions are stable harness constants, and which are per-task variables?
- What evidence would make you comfortable running the final `harness.py` on a fresh repo?

---

## P07a: Critic with iterative refinement

The [talk + slides](https://github.com/rajshah4/harness-engineering#presentation-materials) frame critics and iterative refinement as the multi-agent pattern most likely to earn its keep. Reflexion-style critic loops on SWE-bench: 57.9% (random sampling) → 63.6% (success-only) → **73.8%** (iterative critic with rubrics). Boris Cherny's practitioner number is 2–3× quality.

### Setup

- Pick a task with a *checkable* output. The COBOL→Java sample task in the [iterative-refinement guide](https://docs.openhands.dev/sdk/guides/iterative-refinement) works well; so does "write a small Python module with tests" against a public spec.
- Same model, same tools, same prompt across both runs.
- Two configurations:
  - **A: no critic:** `get_default_agent(llm=llm)` and `conversation.run()` once. Whatever it produces is the answer.
  - **B: critic with iterative refinement:** add `critic=...` to the `Agent` and an `IterativeRefinementConfig` with a `success_threshold` and `max_iterations`. `conversation.run()` will loop internally until the critic clears the threshold or you hit the cap.

The solution ships a small checkable `wordstats` task and a deterministic
scorer. Start with the dry run:

```bash
cd solution
uv run --with openhands-sdk --with openhands-tools --with openhands-workspace \
  python evaluate.py --dry-run --trials 1 --config both
```

The critic block used by the evaluator and capstone harness is:

```python
from openhands.sdk.critic import APIBasedCritic, IterativeRefinementConfig

iterative = IterativeRefinementConfig(success_threshold=0.7, max_iterations=3)
critic = APIBasedCritic(
    server_url=os.environ.get("CRITIC_SERVER_URL", "https://llm-proxy.app.all-hands.dev/vllm"),
    api_key=os.environ.get("CRITIC_API_KEY", os.environ["LLM_API_KEY"]),
    model_name=os.environ.get("CRITIC_MODEL_NAME", "critic"),
    iterative_refinement=iterative,
)
```

`success_threshold=0.7` means "keep refining while the API critic estimates
success below 70%." It is not the deterministic pass/fail score. The pass/fail
score comes from the same rubric for every trial:

```text
Pass only if stats.py exposes analyze_file, cli.py runs, empty files return
zeros, word rules handle hyphens/contractions/numbers, and missing files fail
cleanly.
```

### Procedure

**Run each config five times.** This is the project where one-off measurements lie hardest. Score each run pass/fail against the same rubric. Track:

| Config | Pass rate (n=5) | Median iterations | Median cost | Wall-clock |
|---|---|---|---|---|
| A no critic | _e.g._ 2/5 | 1 | $0.04 | 30s |
| B critic, threshold 0.7, max 3 | _e.g._ 4/5 | 2 | $0.11 | 90s |

The solution command prints this table and writes each scored workspace under
`.openhands-runs/p07-evaluate/`:

```bash
uv run --with openhands-sdk --with openhands-tools --with openhands-workspace \
  python evaluate.py --trials 5 --config both
```

To score an existing workspace without model calls:

```bash
uv run --with openhands-sdk --with openhands-tools --with openhands-workspace \
  python evaluate.py --score-only /path/to/generated/workspace
```

If you do not have a hosted critic endpoint yet, first run
`python evaluate.py --trials 1 --config no-critic`. That still verifies the
Docker workspace, task prompt, trace capture, and deterministic scorer before
you spend time wiring `CRITIC_SERVER_URL`, `CRITIC_API_KEY`, and
`CRITIC_MODEL_NAME`.

### What to look for

- Pass-rate lift is the headline number. If it doesn't move at least 10 to 15 percentage points on a non-trivial task, either your rubric is too lenient or the critic isn't actually scoring the right thing. Read the critic's output before you blame the pattern.
- Cost-per-pass (cost ÷ pass rate) is often *flat or better* with the critic, because the critic shortens the long tail of "ran for 30 turns, still wrong." Compute this.
- Specific rubrics drive most of the lift. Vague critics ("looks fine") barely help.

> **What you keep from P07a:** the `Critic` + `IterativeRefinementConfig` block, the rubric prompt, and a pass/fail table over repeated runs.

---

## P07b: Capstone: ship a harness you trust

| | |
|---|---|
| **What You Do** | Wire the keepers from P01-P07a into a single `harness.py` that boots a Docker-sandboxed agent with your routing, retrieval decision, decomposition rule, `AGENTS.md`, organization security policy, and critic. Run it against a fresh repo. |
| **Harness Mechanism** | All of the above. This project doesn't introduce a new lever. It's where the levers stop being hypothetical. |

**Phase: SHIP A HARNESS YOU TRUST.** P01-P07a each produced one artifact. The capstone is where you assemble them and find out whether your decisions compose.

### Procedure

1. Open `starter/harness.py`. Fill in the TODO blocks with the artifacts you kept from P01-P07a.
2. Pick a fresh repo you haven't run the agent against. A public open-source library you actually use is best.
3. Run `WORKSPACE_DIR=/path/to/repo uv run --with openhands-sdk --with openhands-tools --with openhands-workspace python harness.py "your real task"`.
   P07 defaults to Docker host port `8020` so it does not collide with the P06
   `8010` example. If that port is busy, set `HARNESS_PORT=8021` or another
   free port. The capstone mounts the security policy directory read-only at
   `/openhands-harness-policy/`; override it with `HARNESS_SECURITY_POLICY` if
   you keep your policy somewhere else.
4. Watch the agent trace. Confirm:
   - The router sends work to the expected model leg (read per-`usage_id` metrics).
   - Your tool list is the active one.
   - Your `AGENTS.md` was loaded (the first event in the conversation should reflect it).
   - Your `org_security_policy.j2` is reflected in the agent's system message.
   - High-risk actions pause or get rejected according to your security profile.
   - The critic, if you kept one, fires and produces a verdict you can read.
   - The Docker container started clean and tore down clean.

### What "shipped" means

Run the harness on three different tasks across two different repos. If the same `harness.py` produces results you'd be willing to put in a PR, it shipped. If you find yourself tweaking knobs in `harness.py` for each task, you have a *prototype*. Go back to the project that owns the tweak and decide whether the knob belongs in `harness.py` (constant) or in a per-task config (variable).

The line between "constant" and "variable" is the most underrated harness decision. Make it on purpose.

## What you keep

`harness.py` itself. This is the artifact the whole tutorial builds toward. Commit it. Use it. Iterate on it the way you'd iterate on any production tool. Not by rewriting from scratch each time, but by changing one knob at a time and measuring.
