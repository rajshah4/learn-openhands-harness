---
layout: home

hero:
  name: Learn Harness Engineering with OpenHands
  text: ""
  tagline: "Agent = Model + Harness. A hands-on course for the system around the model: routing, tools, memory, safety, critics, traces, metrics, and workflow design."
  image:
    src: /images/harness-course-hero.png
    alt: Diagram showing coding models connected through a harness to course modules
  actions:
    - theme: brand
      text: Start The Course
      link: /start-here
    - theme: alt
      text: See The Visual Intro
      link: /concepts/visual-intro
    - theme: alt
      text: View Projects
      link: /projects/
    - theme: alt
      text: Open GitHub
      link: https://github.com/rajshah4/learn-openhands-harness

features:
  - title: Run The OpenHands Harness
    details: Start with the basics through Agent Canvas and Agent Server by running a request and viewing the trace.
  - title: Change One Lever
    details: Swap model routing, retrieval, memory, safety, critic, workflow, or escalation policy while keeping the task fixed.
  - title: See the Effect
    details: Compare events, tools, tokens, cost, pass rate, traces, and cost per solved task for different configurations.
---

<div class="harness-equation">
  <span class="he-term">Agent</span>
  <span class="he-op">=</span>
  <span class="he-term">Model</span>
  <span class="he-op">+</span>
  <span class="he-term he-emphasis">Harness</span>
  <span class="he-caption">The system around the model decides agent performance</span>
</div>

<HomeFlightTeaser />

# A Friendly Front Door To The OpenHands Lab

The GitHub repo is where the runnable labs live. This site is the guide: what to watch first, what to read, which files to open, and how the pieces connect.

Harness engineering is the work around the model. The model writes code. The harness decides what the model sees, which tools it can use, what it remembers, what it can break, how work is verified, which model gets called, and when the loop stops. See the [harness engineering experiments repo](https://github.com/rajshah4/harness-engineering) and the [blog post](https://rajivshah.com/blog/harness-engineering.html) for the deeper argument behind this course.

<div class="course-grid">
  <div class="course-card">
    <h3>Understand The Thesis</h3>
    <p>Start with the harness engineering framing, the Visual Intro, the talk, and the experiments that show why harness design matters as much as model capability.</p>
    <p><a href="/learn-openhands-harness/concepts/">Read the concepts</a></p>
  </div>
  <div class="course-card">
    <h3>Build The Harness</h3>
    <p>Work through P01 to P10. Each project changes one harness lever and asks you to inspect the trace before keeping the policy.</p>
    <p><a href="/learn-openhands-harness/projects/">Open the projects</a></p>
  </div>
  <div class="course-card">
    <h3>Copy The Artifacts</h3>
    <p>Use the library for trace checklists, routing policies, safety profiles, critic rubrics, and result tables you can adapt to your own repos.</p>
    <p><a href="/learn-openhands-harness/library/">Open the library</a></p>
  </div>
</div>

## What Makes This Course Different?

This is not a general prompt engineering course. It is not about copying and pasting the latest skill. It is designed to help you understand the core principles behind modern coding agents and harnesses. The examples are built so you can see the effect of each choice, which is more useful than only reading about it.

You use:

- **Agent Server** as the harness runtime.
- **Agent Canvas** as the trace and operator surface.
- **OpenHands SDK** as the programmable harness.
- **Laminar traces and SDK metrics** for observability.
- **Starter and solution projects** as controlled experiments.

The goal is not to memorize APIs. The goal is deeper understanding, so on your next project you know which harness levers to pull to solve your problem.

## Start Here

1. Read [Start Here](/start-here).
2. Run the [Quickstart](/quickstart).
3. Take the [Harness Tour](/harness-tour).
4. Start [P01: Agent Trace](/projects/p01-agent-trace).
