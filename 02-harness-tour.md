# 2: A Tour of the Harness

A coding agent is not just a model. It's a model wrapped in a **harness**: the code that decides which model to call, what tools it can use, what it remembers, how the loop runs, and where the work happens. Claude Code, Codex CLI, Cursor, OpenHands all ship a harness. Most of them don't let you see it.

In this tour you'll give the agent a real task, watch it work, and then walk through the trace to see each part of the harness in action. The [projects](./projects/) will have you change each one.

> **Prerequisites:** a running agent server and canvas from the [quickstart](./01-quickstart.md), completed Agent Canvas onboarding, and the `agent-canvas` repo cloned locally.

---

## 2.1 Give it a real task

You just set up the agent-canvas project in the quickstart. The canvas frontend needs to know where the backend server lives, and that wiring now uses both `VITE_BACKEND_BASE_URL` for direct browser requests and `VITE_BACKEND_HOST` for the Vite proxy. Those values are set in dev scripts and overridden in different configurations. How that wiring works is a real question a developer would ask when joining this project.

It also makes a good harness test. The agent has to search across multiple files, read what it finds, connect the dots, and produce a written summary, without modifying anything. You'll reuse this same prompt across the early projects so you can compare how different harness configurations change the agent's behavior on the same task.

Open the canvas at `http://localhost:8000`. If the first-run wizard appears, finish the agent, backend, and LLM setup from the quickstart. Then start a new conversation and paste this prompt:

```
Find every place VITE_BACKEND_HOST and VITE_BACKEND_BASE_URL are read or set
in this project, and write a short note explaining how the dev script picks
the backend.
```

Watch the agent work. When it finishes, come back here.

---

## 2.2 Read the trace

Click into the conversation in the canvas. You'll see a list of events, top to bottom:

1. **Your message.** The prompt you sent.
2. **Tool calls.** The agent decided to run `terminal` (probably `grep -rn VITE_BACKEND_HOST`) or `file_editor` (to read a file).
3. **Tool results.** What came back from each tool call.
4. **More tool calls.** Maybe it grepped, then read specific files, then grepped again.
5. **A final message.** The agent's written answer.

That sequence is the **agent trace**, the chronological record of every decision the harness made: what the model proposed, what tool ran, what came back, what it did next. With a closed harness you'd be guessing. Here you can read it.

Count the events. Note what tools the agent used, how many times, and in what order. You'll compare this baseline against different harness configurations in the projects.

> The trace is built on OpenHands' [Event](https://docs.openhands.dev/sdk/arch/events) framework. Each row is one typed event. The SDK exposes the same data via `conversation.state.events`, and `conversation.conversation_stats.get_combined_metrics()` gives you token counts and cost.

---

## 2.3 Part 1: The model

Somewhere in that trace, an LLM read the context and decided what to do next. Which model was it?

If you used the canvas defaults, it's whatever you configured during the LLM setup step. If you ran `quickstart.py`, it's the `LLM_MODEL` you exported (or the Sonnet 4.5 default). Either way, one model did all the work: reasoning, tool selection, writing the answer.

That's fine for a first run, but it's also the most expensive configuration. In a real harness you might route cheap tasks to a small model, hard tasks to a flagship, and vision tasks to a multimodal one. OpenHands supports model configuration through `LLM` and [`LLMRegistry`](https://docs.openhands.dev/sdk/guides/llm-registry), and local/in-process harnesses can also use [`RouterLLM`](https://docs.openhands.dev/sdk/guides/llm-routing). [P02](./projects/p02-model-routing/) uses a remote-safe routing policy before agent construction, then compares the cost.

The model is one part of the harness. Swap it and the cost and capability change, but the rest of the harness stays the same. That's why you can tune each part independently.

---

## 2.4 Part 2: The tools (retrieval)

Look at the tool calls in your trace. The agent probably used `terminal` to run `grep` or `find`, `file_editor` to read specific files, and maybe `task_tracker` to write down what it found so far. No vector database, no embeddings, no RAG pipeline. It found code by grepping for it, the same way you would. For exact symbol names like `VITE_BACKEND_HOST`, grep is fast and reliable.

Now imagine the prompt had been vaguer: "How does the canvas pick which backend to talk to?" Same question, different words. A strong model may still recover by grepping adjacent words like `backend` and `proxy`; sometimes it will not. That's the vocabulary-mismatch problem, and it is where semantic search (via [MCP](https://docs.openhands.dev/sdk/guides/mcp)) can earn its place in the tool list.

The tools the agent can use are set when the conversation starts. You choose them:

```python
agent = Agent(
    llm=llm,
    tools=[
        Tool(name=TerminalTool.name),    # grep, find, shell commands
        Tool(name=FileEditorTool.name),  # read and edit files
    ],
)
```

Add a tool and the agent can reach for it. Remove one and it can't. [P03](./projects/p03-retrieval/) includes a tiny `search_code` MCP server so you can compare lexical-only against lexical + semantic and decide whether the extra tool actually helps.

---

## 2.5 Part 3: Memory

What did the agent know about this repo before it started searching?

Nothing. It had your prompt, the system prompt the harness assembled, and the tools. It had to discover the project structure, the file layout, and the conventions from scratch by grepping and reading.

That's expensive. If this were a repo you work in every day, you'd want the agent to start with some context: "this is a monorepo, the frontend is in `apps/canvas`, the backend is in `apps/server`, config lives in `.env` files." That's what **`AGENTS.md`** does. It's a small file at the repo root that the harness reads at conversation start and injects into the system prompt.

Memory in a harness has three layers:

- **Active context.** The system prompt plus recent events the model can see right now. Managed by [condensers](https://docs.openhands.dev/sdk/arch/condenser) that summarize or drop older events when context gets too long. You can see compaction events in the trace.
- **Working state.** Files the agent creates during a run: plans, notes, partial outputs in the workspace filesystem. The agent reads them back with `file_editor` or `terminal`.
- **Durable memory.** Knowledge that persists across conversations, primarily [`AGENTS.md`](https://docs.openhands.dev) at the repo root plus [skills](https://docs.openhands.dev/sdk/guides/skill) loaded on demand.

Check your trace: did a compaction event fire? On a short task, probably not. On a longer one, you'd see older events replaced by a summary.

[P05](./projects/p05-memory/) has you run the same task with and without an `AGENTS.md` and measure the difference. A few lines of hand-written context can save the agent several rounds of exploratory grepping.

---

## 2.6 Part 4: Safety and the loop

The agent ran shell commands on your machine. It could have run `rm -rf`. It could have run `git push`. It could have curled a URL and exfiltrated your source code. Right now, nothing in the harness stopped it.

That's fine for a tutorial on a scratch repo. Not fine for real work. The harness needs to answer three questions: what is the agent allowed to do automatically, what needs your approval, and what should never run?

OpenHands gives you three layers:

- **Security policy.** A template file (`org_security_policy.j2`) that tells the model what's LOW, MEDIUM, and HIGH risk. It guides the model's own judgment but doesn't enforce anything by itself.
- **Security analyzers.** Code that classifies each proposed action. Deterministic analyzers catch known dangerous patterns; an LLM-based analyzer handles the gray areas. Compose them with `EnsembleSecurityAnalyzer`.
- **Confirmation policy.** `ConfirmRisky()` pauses the loop when the analyzer flags something above a threshold. `AlwaysConfirm()` requires approval for every action. The canvas surfaces these pauses for you to approve or reject.

Together these turn the agent loop from "run everything blindly" into "run safe things, ask about risky things, block dangerous things." The loop itself, `Conversation.run()`, is where this all executes: build prompt, call LLM, propose action, classify risk, run or pause, ingest result, repeat. It also has a [stuck detector](https://docs.openhands.dev/sdk/guides/agent-stuck-detector) that watches for the agent repeating the same failed action, and [hooks](https://docs.openhands.dev/sdk/guides/hooks) where you can inject custom logic at each step.

[P06](./projects/p06-safety/) has you wire up a security analyzer, a confirmation policy, and a Docker sandbox.

---

## 2.7 Part 5: Architecture (where it runs)

Your agent ran as a single process on your laptop, with direct access to your filesystem. That's one architecture. OpenHands ships three:

- A **local subprocess** (what current Agent Canvas `npm run dev` gives you, full filesystem access, fine for learning)
- A **[Docker sandbox](https://docs.openhands.dev/sdk/guides/agent-server/docker-sandbox)** (isolated filesystem and network, kill the container and everything resets)
- A **[cloud workspace](https://docs.openhands.dev/sdk/guides/agent-server/cloud-workspace)** (hosted runtime, no local Docker needed).

Switching from local to Docker is a one-line change in your Python code: swap `Workspace(...)` for `DockerWorkspace(...)`. The agent code, tools, prompts, and trace stay identical. Where the work runs is separate from how it runs.

There's also a "how many agents" axis. Your task ran as a single agent. For harder tasks you might want [sub-agent delegation](https://docs.openhands.dev/sdk/guides/agent-delegation) (spawn a child for a bounded subtask) or a [critic](https://docs.openhands.dev/sdk/guides/critic) (a second LLM that reviews the first agent's work). Default to single. Multi-agent adds coordination cost that has to earn itself. [P07](./projects/p07-capstone/) is where you optionally add a critic. [P08](./projects/p08-dynamic-workflows/) then looks at dynamic workflows: the harness registers the roles and guardrails, while the model writes the short-lived fan-out/fan-in orchestration. For a full multi-agent pipeline (implement, test, review across different harnesses), see the [openhands-multi-agent-demo](https://github.com/rajshah4/openhands-multi-agent-demo).

---

## 2.8 The harness, all together

```
┌─────────────────────────────────────────────────┐
│                   THE HARNESS                    │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Model   │  │  Tools   │  │    Memory      │  │
│  │          │  │          │  │                │  │
│  │ Sonnet   │  │ terminal │  │ AGENTS.md      │  │
│  │ or cheap │  │ file_ed  │  │ condensers     │  │
│  │ or route │  │ +MCP?    │  │ workspace      │  │
│  └──────────┘  └──────────┘  └───────────────┘  │
│                                                  │
│  ┌──────────────────┐  ┌──────────────────────┐  │
│  │  Loop + Safety   │  │    Architecture      │  │
│  │                  │  │                      │  │
│  │ security policy  │  │ local / Docker /     │  │
│  │ analyzers        │  │ cloud                │  │
│  │ confirmation     │  │ single / multi-agent │  │
│  │ stuck detector   │  │                      │  │
│  └──────────────────┘  └──────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

Every coding agent has these five parts. Claude Code has them. Cursor has them. You just can't inspect or change most of them. OpenHands exposes all five, which is why it works for learning what a harness actually is.

Once you see the parts, the diagnostic question changes. When an agent fails, you stop asking "is the model bad?" and start asking which part of the harness needs to change. Maybe the model is fine but the tools are wrong. Maybe the tools are fine but the agent had no memory of the repo. Maybe everything is fine but the agent ran too long without a stuck detector. The trace tells you where to look.

---

## 2.9 What's next

The [projects](./projects/) take each of these five parts and have you change it, measure the difference, and keep the configuration that works. By P07 you'll have a complete `harness.py` that wires together your model routing, tool selection, decomposition policy, memory policy, security profile, and sandbox. P08 is the optional extension for model-authored workflow coordination.

| Project | What you change | What you learn |
|---|---|---|
| [P01: Agent Trace](./projects/p01-agent-trace/) | Nothing, you read the trace | How to diagnose what the harness did |
| [P02: Model Routing](./projects/p02-model-routing/) | The model | Cost vs. capability tradeoffs |
| [P03: Retrieval](./projects/p03-retrieval/) | The tools | When extra search earns its slot |
| [P04: Task Decomposition](./projects/p04-decomposition/) | The workflow shape | When smaller calls beat one large call |
| [P05: Memory](./projects/p05-memory/) | `AGENTS.md` and condensers | How prior knowledge changes behavior |
| [P06: Safety](./projects/p06-safety/) | Security policy + Docker | Bounding what the agent can do |
| [P07: Capstone](./projects/p07-capstone/) | Everything, wired together | A production-shaped harness |
| [P08: Dynamic Workflows](./projects/p08-dynamic-workflows/) | Workflow skill + sub-agent roles | When the model can own orchestration |

For real-world tasks to throw at your harness beyond the tutorial prompt, the [OpenHands use cases overview](https://docs.openhands.dev/openhands/usage/use-cases/overview) covers migrations, test generation, documentation, and more.
