---
aside: false
---

# Visual Intro

<div class="harness-equation">
  <span class="he-term">Agent</span>
  <span class="he-op">=</span>
  <span class="he-term">Model</span>
  <span class="he-op">+</span>
  <span class="he-term he-emphasis">Harness</span>
  <span class="he-caption">The model writes code. The harness decides everything else.</span>
</div>

This visual explains the central course claim: the model is not the whole agent. A coding agent becomes useful when the harness gives the model a loop, tools, memory, safety boundaries, verification, routing, and a trace you can inspect.

Use this page before the [Harness Tour](/harness-tour). The tour gives you a real OpenHands task. This page gives you the mental model for what you are watching.

## What Problem Are You Solving?

The common mistake is to treat agent quality as a model-only question. Better models matter, but the same model can behave very differently depending on the harness around it.

For a coding agent, the harness answers practical questions:

- What context does the model see?
- Which tools can it call?
- Where does code execution happen?
- What state persists across turns or sessions?
- What risky actions need approval?
- How is completion verified?
- When should the system use a different model?
- What trace can a human inspect when something fails?

The visual below scrolls through those questions one failure mode at a time.

<AgentFlightConsole />

## How To Read The Visual

Start at the top and watch what changes in the diagram. The early steps are intentionally small. A bare model call is not wrong. It is just insufficient once the answer needs repo evidence, command output, tests, or recovery from mistakes.

The key move is the ReAct loop: the model reasons, asks to act, receives an observation, and updates the next step. Once that loop exists, the rest of the harness becomes visible. Tools determine what actions are possible. Memory determines what the agent does not need to rediscover. Safety decides what can run automatically. Critics and metrics decide whether the result is good enough to keep.

That is why the course asks you to predict, run, inspect, measure, and keep. You are not collecting traces for decoration. You are using traces to decide which harness component is load-bearing.

## Where Terminal-Bench Fits

Terminal-Bench is useful evidence because it evaluates agents in real terminal environments. Its own README describes the benchmark as a task dataset plus an execution harness that connects a language model to a sandboxed terminal environment.

That makes it a good teaching example, with one caveat: public leaderboard rows are agent plus model submissions. A score is not only a property of the model. It also reflects the loop, tool interface, sandbox, retry behavior, stopping rule, and verifier.

Use Terminal-Bench as a reminder to ask better questions:

- What agent was wrapped around the model?
- What tools and terminal affordances did it have?
- How did it decide when to stop?
- What verifier judged success?
- What would change if the harness changed but the model stayed fixed?

## What Students Should Leave With

After this page, you should be able to look at a trace and name the harness component that shaped it. If a run fails, do not only ask for a bigger model. Ask which part of the harness failed to provide evidence, context, boundaries, or feedback.

Then move to [P01: Agent Trace](/projects/p01-agent-trace) and practice reading the loop on a real OpenHands run.

## References

- [Harness Engineering blog post](https://rajivshah.com/blog/harness-engineering.html): the longer argument behind the course
- [Harness engineering experiments repo](https://github.com/rajshah4/harness-engineering): runnable measurements for retrieval, memory, loops, tools, and architecture
- [Google Research: ReAct](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)
- [Anthropic: Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/)
- [OpenHands Agent Server architecture](https://docs.openhands.dev/sdk/arch/agent-server)
- [Terminal-Bench leaderboard](https://www.tbench.ai/leaderboard)
