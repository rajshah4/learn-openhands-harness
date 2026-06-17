# Learn Harness Engineering with OpenHands

Website: [rajshah4.github.io/learn-openhands-harness](https://rajshah4.github.io/learn-openhands-harness/)

Every coding agent ships two things: a model that reasons and a harness that does everything else. The harness decides what the model sees, which tools it can call, what it remembers across turns, when it stops, and whether it runs in a sandbox or on your bare machine. This translates into implications for performance, reliability, and latency.

This tutorial gives you a working harness you can open, run, and change. You'll use two open-source projects, [Agent Server](https://docs.openhands.dev/sdk/arch/agent-server) (the HTTP API that owns the workspace, conversation state, and tool dispatch) and [Agent Canvas](https://github.com/OpenHands/agent-canvas) (the operator UI), as a microscope. You'll give the agent real tasks, read the trace of what happened, and then change one lever at a time to see the behavior shift.

By the end you'll have a `harness.py` you built yourself, with model routing, retrieval config, memory policy, a security profile, and a critic. More importantly, you'll be able to look at any agent product and answer: *what would I change about its harness if I owned the source?*

> **Background.** If you want the conceptual frame first, read the [harness-engineering README](https://github.com/rajshah4/harness-engineering) and watch the [talk](https://www.youtube.com/watch?v=KijChx7q2nY). This tutorial assumes you understand the role and importance of the harness.

---

## How to use this tutorial

Use this as a guided lab, not an autonomous agent task. The goal is to learn
which harness lever changed and how that change shows up in the trace. Do not
ask an agent to run the whole tutorial end-to-end.

For each phase:

1. Read the project overview.
2. Inspect the starter code.
3. Predict what the harness should do.
4. Run one small experiment.
5. Inspect the trace.
6. Record the takeaway before moving on.

Start live runs in Agent Canvas when learning a new concept. Use the coding agent
as a learning point: prompts, tool calls, observations, confirmations,
compaction, and final answers are visible in order. Use the SDK scripts after
the trace behavior is clear and you need repeatable measurements such as events,
tokens, cost, pass rate, or saved trace JSON.

If you use an AI coding agent to help with this tutorial, give it this
instruction first:

```text
You are helping me through this as a guided lab. Do not run ahead. For each
section, explain the concept, inspect the starter, ask me to predict the result,
then wait for me before running live commands. Prefer Agent Canvas for first
trace inspection and scripts for repeatable measurement.
```

---

## Why an open harness

There are good harnesses you can't see (Claude Code, Cursor) and good ones you can (SWE-agent, OpenHands, deepagents). For learning, only the open ones work. You need to read the code to understand what a harness *is*.

OpenHands is a useful learning framing for three reasons:

1. **Clean client/server split.** The agent server is a stateless-ish HTTP API; the canvas is a thin client. The harness boundary is literally an OpenAPI spec. You can replace either side without rewriting the other.
2. **Three deployment shapes from one codebase.** Local process, Docker sandbox, hosted API, all by swapping a `Workspace` class. That makes the cost of *where work runs* visible.
3. **The trace is a first-class object.** The chronological record of messages, tool calls, results, compaction, and confirmations is right there in the canvas. You don't have to grep logs to see what the harness is doing.

The Anthropic [post-mortem on Claude Code's reasoning-effort regression](https://www.anthropic.com/engineering/april-23-postmortem) is a good reminder of what closed harnesses cost you. When the model didn't change but quality did, users had no way to diagnose it. The whole point of running an open harness is that you *can*.

---

## What you'll do

Three phases, in order. Each builds on the previous one.

1. **[Quickstart](./01-quickstart.md).** Install, get a green health check, and have a working canvas in front of you.
2. **[Harness tour](./02-harness-tour.md).** Give the agent a real task, read the trace, and see the five parts of a harness (model, tools, memory, safety, architecture) in the context of what actually happened.
3. **[Projects](./projects/).** Seven cumulative projects plus five advanced extensions, each with a `starter/` and `solution/`. Change one lever at a time, keep the artifact, move on.

Each project follows the [walkinglabs/learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) pattern: `starter/` is your starting point, `solution/` is the reference. Each solution becomes the next project's foundation; by P07 you have a complete `harness.py` and an evaluation trace you can defend. P08, P09, P10, P11, and P12 are advanced extensions: dynamic workflows, measured model routing, indexing agent history, measuring subagent context isolation, and turning long-running goals into mission contracts.

The most important habit is separating constants from variables. A model
router, security profile, default tool list, memory policy, and sandbox belong
in `harness.py` only after repeated runs show they should be stable defaults.
Task prompt, repo path, budget, and one-off exceptions stay outside the harness.

| Project | Focus |
|---|---|
| [P01: Agent Trace](./projects/p01-agent-trace/) | Read the agent loop from its event trace |
| [P02: Model Routing](./projects/p02-model-routing/) | Right-size the model to the task |
| [P03: Retrieval](./projects/p03-retrieval/) | Decide when search tools earn their slot |
| [P04: Task Decomposition](./projects/p04-decomposition/) | Split large work into smaller runs |
| [P05: Memory](./projects/p05-memory/) | Add durable context to cut re-discovery |
| [P06: Safety](./projects/p06-safety/) | Bound the agent's blast radius and sandbox it |
| [P07: Capstone](./projects/p07-capstone/) | Add evaluation and compose the full harness |
| [P08: Dynamic Workflows](./projects/p08-dynamic-workflows/) | Move orchestration into reusable workflows |
| [P09: Model Routing Benchmark](./projects/p09-model-routing-benchmark/) | Select the most appropriate model |
| [P10: Indexing Agent History](./projects/p10-history-index/) | Add a database/index over conversation traces |
| [P11: Subagents](./projects/p11-subagents/) | When do subagents make sense? |
| [P12: Goal And Mission Harness](./projects/p12-goal-mission-harness/) | Make long-running goals verifiable |

---

## Prerequisites

- macOS or Linux (Windows works but the canvas dev script assumes a POSIX shell)
- **Node.js 22.12+** and `npm`
- **`uv`** ([install](https://docs.astral.sh/uv/getting-started/installation/))
- **An LLM API key** (Anthropic, OpenAI, or anything [LiteLLM](https://docs.litellm.ai/docs/providers) supports)
- **Docker** is optional for the first walkthrough but recommended for real work

Details on how `uv`, the API key, and Docker fit together are in the [quickstart](./01-quickstart.md).

---

## Setup

Live agent runs need one secret: `LLM_API_KEY`. The checked-in scripts default to Sonnet 4.5, so `LLM_MODEL` is optional unless you want a different model.

```bash
cp .env.example .env
# Edit .env and set LLM_API_KEY to a provider key.
set -a
source .env
set +a
```

Optional knobs: `LLM_MODEL` for the main model, `LLM_MODEL_SMALL` for routing experiments, `WORKSPACE_DIR` for the repo the agent inspects. Never commit a real `.env`. If a key leaks, rotate it.

**Safety note.** This tutorial starts dockerless on purpose. That's the easiest way to see the agent server, HTTP API, filesystem, and trace without another layer in the way. Current Agent Canvas uses `npm run dev` for this local stack, and tool calls run directly on your host. Point it at a scratch repo, not one you care about. P06 moves you to Docker. Until then, treat dockerless mode as a learning microscope, not a safe operating mode.

---

## Further reading

None of this is required. The tutorial is self-contained.

**Harness engineering:**

- [Engineering the Harness (talk + slides)](https://github.com/rajshah4/harness-engineering#presentation-materials). The framing this repo is built around.
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/). Codex team's take on their own harness design.
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). Compaction and long-running loop design.
- [walkinglabs / learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering). Project-based course. Heavier on convention than on plumbing; complements this tutorial well.
- [Claude Code: Introducing dynamic workflows](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code). The closed-harness product pattern behind the P08 extension.
- [Cursor 2.4: Subagents, Skills, and Image Generation](https://cursor.com/changelog/2-4). Another example of moving procedural knowledge into skills and specialized subagents.

**OpenHands specifics:**

- [Agent Server architecture](https://docs.openhands.dev/sdk/arch/agent-server). Design intent.
- [Agent Server: Local](https://docs.openhands.dev/sdk/guides/agent-server/local-server) and [Docker Sandbox](https://docs.openhands.dev/sdk/guides/agent-server/docker-sandbox) guides.
- [`OpenHands/agent-canvas`](https://github.com/OpenHands/agent-canvas). The UI. The `DEVELOPMENT.md` is unusually honest about which knobs you actually have.
- [`OpenHands/software-agent-sdk`](https://github.com/OpenHands/software-agent-sdk). The SDK the server is built on.

---

## Where to go from here

After P07 you have a working `harness.py` and the mental model to extend it. P08, P09, P10, P11, and P12 show five extensions in detail: dynamic workflows, where reusable orchestration policy moves into skills; model routing, where the harness chooses the cheapest model it trusts and escalates on evidence; indexing agent history, where unbounded past sessions move into a queryable index instead of being scanned; subagents, where a context boundary becomes a measured tradeoff; and goals, where a persistent objective becomes a mission contract with criteria, verifiers, budgets, and envelopes. A few other directions worth exploring:

- **More use cases.** The [OpenHands use cases overview](https://docs.openhands.dev/openhands/usage/use-cases/overview) shows what people are building with coding harnesses beyond the tutorial tasks: migrations, test generation, documentation, issue triage. Good source of fresh prompts to stress-test your harness against.
- **Multi-agent orchestration.** This tutorial builds a single-agent harness. The [openhands-multi-agent-demo](https://github.com/rajshah4/openhands-multi-agent-demo) shows the next step: composing multiple harnesses (Claude Code, Gemini CLI, OpenHands) into an implement, test, review pipeline. Three orchestration patterns, same workflow, different isolation and state-sharing tradeoffs.
- **Extend the harness.** The tutorial covers the core levers, but there is more surface area to work with: [custom tools](https://docs.openhands.dev/sdk/guides/tool), [MCP servers](https://docs.openhands.dev/sdk/guides/mcp), [skills](https://docs.openhands.dev/sdk/guides/skill), [hooks](https://docs.openhands.dev/sdk/guides/hooks), [custom condensers](https://docs.openhands.dev/sdk/arch/condenser), [browser and computer use](https://docs.openhands.dev/sdk/guides/computer-use), evaluation against benchmarks. Each one is another knob in `harness.py` waiting for a reason to turn it.
- **Your own harness decisions.** You can now look at any agent product and ask concrete questions. Which model is it using? What tools does it expose? What does it remember? What can it break? Where does the loop stop? If you can answer those for your own `harness.py`, you can answer them for anything.
