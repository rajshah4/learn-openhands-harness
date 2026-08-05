# P00: The Harness Mystery

## What You Do

A colleague wired up a new model and ran the discover-prove-fix benchmark. It
failed: no PoC, no patch, nothing saved. But the model's response contains
a correct solution. Read the trace and figure out what went wrong.

## Harness Mechanism

Native tool calling, reasoning retention, and explicit sampling/output-token
parameter forwarding. The harness, not the model, determines whether the model
can act.

## Open First

- [`projects/p00-harness-mystery/README.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p00-harness-mystery/README.md)
- [`starter/incident.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p00-harness-mystery/starter/incident.md)
- [`starter/diagnose.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p00-harness-mystery/starter/diagnose.md)

## Why This Comes First

Every later project teaches you to read a trace and tune a lever. This one
motivates the whole course as a debugging exercise: a bad harness can make a
strong model look broken, and you find it by reading the trace, not by guessing.

Two real-world cases hit the same class of bug:

- A CyberGym-E2E run where fixing three harness settings raised S1 from 40.7%
  to 70.0%: same model, same tasks.
- An OpenAI experiment where enabling two API settings tripled their ARC-AGI-3
  score and cut output tokens 6×.

The lesson: a benchmark score measures the whole stack, not just the model.
