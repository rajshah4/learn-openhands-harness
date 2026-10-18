# Inspect the saved conversations

Download the [19-conversation workshop package](https://github.com/rajshah4/learn-openhands-harness/releases/tag/odsc-conversations-2026-10-18-v2). Unzip the named ZIP asset and open `harness-conversations/package/index.html`. No model key is needed. Workshop 1 contains 01A OpenHands (batched reads), 01B Pi (edge assertions), and 01C OpenCode (separate reads).

If local HTML is restricted, run `python3 serve_transcripts.py` inside the extracted folder and open http://127.0.0.1:28081/. Windows users can use `py -3 serve_transcripts.py`. Stop with Ctrl-C.

The included README explains the optional pinned Canvas viewer, checksums, recovery, and uninstall. Canvas runtime acceptance is verified on macOS; the HTML transcripts are the simplest starting point.

Read the prompt, inspect the tool evidence, and check the final claim. Pi has separately linked recovered outputs, and the validator example includes its child history. These are curated teaching examples with useful failures, not a performance benchmark.

Use [exercise prompts](./prompts) when you want to perform the work yourself. Start new work in a separate coding environment; the saved histories are read-only.
