# Projects: Learning Path

Seven small projects, in order, each changing one harness lever and producing a config artifact that carries forward. By P07 you'll have a runnable `harness.py` and an agent-trace evaluation record that wires together everything you kept: your trace-reading checklist, model routing, retrieval decision, decomposition plan, memory policy, security profile, sandbox, and critic.

If you're using this as a first learning path, treat P01-P05 as the core concepts. P06-P07 are the advanced path where safety, verification, and composition start looking like production harness design.

The pattern is behavior first: decide what agent behavior you want, change the smallest harness surface that could affect it, then observe whether the trace changed.

> **Inspired by [walkinglabs/learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering)**, which organizes harness learning as a sequence of cumulative projects on the same Electron app rather than disconnected one-off ablations. That's a better shape for learning than the standard "here are some experiments" format, and it adapts naturally to OpenHands. The phase names, the two-column "What You Do / Harness Mechanism" preamble, and the "each project's solution becomes the next project's starter" property are all borrowed from there. Credit where it's due.

> **Common task for P01-P03 and P05.** Pick one repo and one prompt, and freeze them. A good default: clone [`OpenHands/agent-canvas`](https://github.com/OpenHands/agent-canvas) and use the prompt `"Find every place VITE_BACKEND_HOST is read or set, and write a short note explaining how the dev script picks the backend."`, narrow, repeatable, doesn't write code, and forces real retrieval. P04 intentionally switches to a larger release-readiness task so decomposition has something real to improve.

---

## Lab rhythm: Canvas first, scripts second

Agent Canvas is the teaching surface. Use it to watch the trace: prompts, tool
calls, observations, confirmations, compaction, and final answers. Start in the
GUI whenever a project introduces a new harness concept.

The SDK scripts are the measurement surface. Use them after you understand the
trace behavior and need to repeat the same task, compare configs, save traces,
or tabulate events, tokens, cost, and correctness.

Do not run every script up front. For each project, first understand the harness
lever, then run the smallest experiment that tests it.

Before every live run, pause and predict:

- What harness lever changes in this project?
- What should the trace look like if the harness is working?
- What metric would prove the change helped?
- What failure mode would prove it did not?

Use scratch clones for experiments where prior generated notes could pollute
retrieval. If an earlier run wrote files like `FACTS.txt` or
`VITE_BACKEND_HOST_NOTES.md`, either remove them from the target workspace or
copy a clean repo before measuring.

---

## Project evolution

```text
PROJECT EVOLUTION (OpenHands harness)
=====================================

  P01  Canvas + agent trace          → SEE THE LOOP
       |                               keep: a baseline trace
       |                                     + trace-reading checklist
       v
  P02  Model routing                 → RIGHT-SIZE THE THINKING
       |                               keep: a routing policy / LLMRegistry config
       v
  P03  Retrieval                     → GET BETTER RESULTS FASTER
       |                               keep: a one-line decision rule
       |                                     for when MCP earns its slot
       v
  P04  Task decomposition            → BREAK DOWN THE WORK
       |                               keep: decomposition plan
       |                                     + aggregation rule
       v
  P05  Memory + compaction           → REDUCE RE-DISCOVERY
       |                               keep: a hand-written AGENTS.md
       |                                     + condenser/memory notes
       v
  P06  Org safety profile            → BOUND BLAST RADIUS
       |                               keep: org security profile
       |                                     + DockerWorkspace runner
       v
  P07  Verification + capstone       → STOP "LOOKS FINE"
                                       keep: Critic + rubric + harness.py

  Each project produces a concrete artifact.
  P07 is where they merge into one runnable harness.
```

---

## How each project is organized

Every project directory follows the same shape:

```
p01-agent-trace/
├── README.md       ← instructions, setup, procedure, what to record
├── starter/        ← starting point. Run this first
└── solution/       ← reference implementation. Check your work
```

Each project README has:
- A two-row preamble: **What You Do** / **Harness Mechanism**.
- Setup, procedure, and what to record.
- A **What you keep** callout at the end. The artifact that carries forward.

Use a fresh conversation per run. Save agent traces.

## Agent-assisted path

These projects are designed to work with OpenHands as your coding assistant, not
just as something you run after writing the answer yourself:

1. Open the project `README.md` and `starter/` directory only.
2. Ask the agent to explain the harness lever and the expected trace before it
   edits or runs anything.
3. Ask the agent to complete the TODOs without reading `solution/`.
4. Require it to run the smallest smoke check or live command listed in the
   README, and only after you approve that run.
5. Compare against `solution/` only after the starter works, then write down
   what differed.

---

## Running the scripts

All scripts are designed to be run with `uv run`:

```bash
cd projects/p01-agent-trace/starter
WORKSPACE_DIR=/path/to/agent-canvas \
uv run --with openhands-sdk --with openhands-tools python run_baseline.py
```

The early project scripts use the local agent server from the quickstart. That
is useful for learning because you can inspect every API call and filesystem
effect directly, but it is not the right safety boundary for real work. Keep
`WORKSPACE_DIR` pointed at a scratch clone or a repo you can restore until P06,
where the runner moves into `DockerWorkspace`.

Required environment variable for every live agent script:

```bash
export LLM_API_KEY="sk-..."
```

`LLM_MODEL` is optional. If omitted, the scripts use
`anthropic/claude-sonnet-4-5-20250929` (Sonnet 4.5). You can also use the
repo-level `.env.example`:

```bash
cd /path/to/learn-openhands-harness
cp .env.example .env
# Edit .env, then:
set -a
source .env
set +a
```

`WORKSPACE_DIR` should point at the repo you are studying. If omitted, the
scripts use the current directory.

If your Agent Canvas server is Dockerized (`npm run dev` or `npm run dev:docker`
in some checkouts), remember that the server sees your project root at
`/projects`. Either pass a server-visible path:

```bash
WORKSPACE_DIR=/projects/agent-canvas \
uv run --with openhands-sdk --with openhands-tools python run_baseline.py
```

or keep `WORKSPACE_DIR` as a host path and tell the scripts how to map it:

```bash
AGENT_WORKSPACE_HOST_ROOT=/path/to/your/projects \
AGENT_WORKSPACE_SERVER_ROOT=/projects \
WORKSPACE_DIR=/path/to/your/projects/agent-canvas \
uv run --with openhands-sdk --with openhands-tools python run_baseline.py
```

For scripts that copy a workspace before running, such as P05, use the host-path
form with the mapping variables so the script can copy locally and then pass the
mapped `/projects/...` path to the server.

---

## Tabulating your results

Keep a `results.md` next to your fork:

```markdown
# Harness projects: <date>

Repo: agent-canvas @ <SHA>
Model: anthropic/claude-sonnet-4-5-20250929 (unless noted)
Prompt: "Find every place VITE_BACKEND_HOST is read or set..."

## P01: Canvas + agent trace
| Trace field | Value |
|---|---|
| Tool calls by type | |
| Files read | |
| Compaction fired? | |
| Final answer correct? | |

## P02: Model routing
| Config | Turns | Tokens (in/out) | Cost | Correct |
|---|---|---|---|---|
| Sonnet 4.5 | | | | |
| Small model | | | | |
| Routed | | | | |

## P03: Retrieval
| Config | Tool calls (grep) | Tool calls (MCP) | Correct | Notes |
|---|---|---|---|---|
| Lexical exact | | - | | |
| Lexical synonym | | - | | |
| MCP synonym | | | | |

## P04: Task decomposition
| Config | Events | Cost | Correct | Notes |
|---|---|---|---|---|
| Monolithic | | | | |
| Decomposed | | | | |

## P05: Memory + compaction
| Config | Turns | Tokens | Correct | Notes |
|---|---|---|---|---|
| No AGENTS.md | | | | |
| Minimal AGENTS.md | | | | |

## P06: Org safety profile
| Action | Expected risk | Actual behavior | Accept? |
|---|---|---|---|
| Read files | LOW | | |
| Edit workspace file | LOW/MEDIUM | | |
| Network/package install | HIGH | | |
| Delete file | HIGH | | |

## P07: Verification + capstone
| Config | Pass rate (n=5) | Median iterations | Median cost | Wall-clock |
|---|---|---|---|---|
| No critic | | | | |
| Critic | | | | |
```

Three runs is barely a signal; ten is convincing; thirty is real. Pick a budget and stick to it.

---

## Where to go from here

`harness.py` exists. The next question is whether you are turning it into a shared platform or just adding integrations.

Prioritize these if the harness will be used by a team:

- **Persistence as the audit substrate.** Persist events, agent configuration, execution state, tool outputs, metrics, workspace context, activated skills, and secrets so every run can be replayed and evaluated. ([Persistence guide](https://docs.openhands.dev/sdk/guides/convo-persistence).)
- **Observability before shared service.** Emit OpenTelemetry traces for agent steps, tool calls, LLM calls, browser sessions, and conversation lifecycle events. This is how operations teams debug the harness instead of reading screenshots. ([Observability guide](https://docs.openhands.dev/sdk/guides/observability).)
- **AgentSettings for admin-controlled profiles.** If Canvas or an internal UI will select "local dev", "company repo", or "regulated" profiles, serialize those knobs as validated settings rather than loose Python. ([Agent Settings guide](https://docs.openhands.dev/sdk/guides/agent-settings).)
- **Secret handling as part of P06.** `conversation.update_secrets(...)` injects secrets only when needed and masks values in output. Do not treat secrets as generic environment variables once real systems are involved. ([Secret Registry guide](https://docs.openhands.dev/sdk/guides/secrets).)
- **LLM fallback for production reliability.** `FallbackStrategy` retries alternate model profiles for rate limits and timeouts while keeping cost metrics visible. ([LLM Fallback guide](https://docs.openhands.dev/sdk/guides/llm-fallback).)

Future project ideas:

- **Guidance layer from rubric failures.** Keep the grading rubric hidden, run repeated evaluations, then convert recurring failure modes into agent-facing guidance that does not leak the answer key. A good starter artifact would be `guidance.yaml` with `look_at`, `common_misses`, positive examples, negative examples, and output requirements per task family. Measure before/after, because guidance can over-correct the model.
- **Severity-aware scorecards.** Track P0/P1/P2 pass rates separately instead of one average score. This matters when one missed secret-handling issue is more important than ten minor documentation nits.

Keep these as supporting tools, not the tutorial spine:

- **Hooks** are useful for hard-deny rules and protocol checks, but Claude Code has hooks too. Use them when they enforce your P06 safety profile. ([Hooks guide](https://docs.openhands.dev/sdk/guides/hooks).)
- **Custom tools** matter when the schema changes behavior. "The agent can call another API" is not interesting by itself. ([Custom tools guide](https://docs.openhands.dev/sdk/guides/custom-tools).)
- **MCP** belongs in the retrieval ablation. P03 ships a small `search_code` MCP server so the experiment is real, but the decision rule still has to come from traces: keep it off unless it improves a vocabulary-mismatch task.
- **File-based agents and parallel tool execution** should wait until the single-agent trace is boring. They add coordination cost and shared-state risk. ([File-Based Agents guide](https://docs.openhands.dev/sdk/guides/agent-file-based), [Parallel Tool Execution guide](https://docs.openhands.dev/sdk/guides/parallel-tool-execution).)

That is the line this tutorial should hold: integrations are supporting cast; open harness ownership is the point.
