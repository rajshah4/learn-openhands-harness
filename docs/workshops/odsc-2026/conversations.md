# Lecture conversation examples

These are the examples shown in the lecture, organized by workshop. The download excludes reserves and superseded experiments.

## Read online or offline

- [Open the lecture examples](/workshop-examples/2026-10-19-lecture/index.html).
- [Download all lecture examples in one ZIP](https://github.com/rajshah4/learn-openhands-harness/releases/download/odsc-lecture-conversations-2026-10-19-v2/harness-lecture-conversations-2026-10-19-v2.zip). Unzip it and open `harness-lecture-conversations/package/index.html`.

No API key or Canvas installation is required. The two Workshop 4 animations are included as model outputs. The Workshop 6 team example includes its three worker histories.

Each selected conversation includes its full recorded history, including later repairs or failures. Private context and credentials have been removed; the evidence documents those redactions. These are teaching examples, not a representative benchmark.

## Open the examples in Agent Canvas

These steps put the saved histories into a dedicated, read-only Canvas archive. They need **Python 3.13 and Node.js/npm**. No model key is needed, and you do not need to launch your regular Canvas first.

1. Download and unzip the lecture ZIP above. Open a terminal in the extracted `harness-lecture-conversations` folder.
2. Install the histories into a new archive folder and prepare the pinned viewer:

   ```bash
   python3.13 setup_examples.py --destination "$PWD/lecture-store" --install
   python3.13 prepare_runtime.py --store "$PWD/lecture-store" --install
   ```

3. Start the viewer from the same folder:

   ```bash
   ./lecture-store/.venv/bin/python view_w3.py --store "$PWD/lecture-store" --canvas "$PWD/lecture-store/ui/node_modules/@openhands/agent-canvas" --port 28080
   ```

4. Open **http://127.0.0.1:28080**. The connection is named **ODSC lecture examples**. Choose a `Workshop N · scenario · description` conversation in the sidebar. The archive contains 16 histories, including the three team workers. Workshop 4's two animations open from the HTML index instead.

Each history has collection, workshop-number and scenario tags. The “sandbox no longer available” message is expected: you can inspect all recorded messages and tool results, but cannot resume these archived agents. Stop the viewer with Ctrl-C.

This opens a separate lecture archive rather than merging old recordings into your normal Canvas history. If the destination already exists, reuse its viewer or choose a fresh folder; the installer will not overwrite it. If port 28080 is occupied, change `--port` and open that port instead. On Windows, run these commands in WSL.

[Set up your own runs](./setup#run-new-exercises) only if you want to perform the exercises yourself.
