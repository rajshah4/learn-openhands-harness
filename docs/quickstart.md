# Quickstart

The quickstart gets you from zero to a visible OpenHands trace. The full runnable instructions live in the repo at [`01-quickstart.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/01-quickstart.md).

## Download Agent Canvas

Use the [official Agent Canvas installer page](https://docs.openhands.dev/openhands/usage/agent-canvas/setup) for current downloads and installation options. For the source-reading exercises below, use the source checkout.

## What You Are Proving

You are checking that Agent Server and Agent Canvas are working, that the model can run through the harness, and that you can inspect the resulting events.

The first run is intentionally small:

```text
Read the current repo and write three facts about it into FACTS.txt.
```

## Minimal Flow

1. Clone the [OpenHands source repository](https://github.com/OpenHands/OpenHands) into an `agent-canvas` folder: `git clone https://github.com/OpenHands/OpenHands.git agent-canvas`, then `cd agent-canvas`.
2. Run `npm install`.
3. Run `npm run dev`.
4. Open `http://localhost:8000`.
5. Complete onboarding: choose OpenHands, confirm the backend is connected, and configure the LLM provider, model, and API key.
6. Start a new chat against the `agent-canvas` workspace.
7. Send the first prompt.
8. Inspect the trace.

The quickstart also shows how to call the same server through the Python SDK, which makes the key point visible: Canvas and the SDK are different clients on the same harness runtime.

## Safety Note

The first setup is dockerless so the moving parts are easy to see. Be careful and use a scratch repo. For regular work, you will want to use a sandbox. P06 moves the harness into `DockerWorkspace`.

## Continue

After the health check passes, take the [Harness Tour](/harness-tour).
