# Harness Engineering conversation examples

Inspect 19 saved conversations across six workshop lessons. No model key or paid account is needed. These are read-only histories, not resumable workspaces. Their original failures and missing-output cards remain visible.

## Download and open

Download **harness-conversations-2026-10-18-v2.zip** from the [GitHub release](https://github.com/rajshah4/learn-openhands-harness/releases/tag/odsc-conversations-2026-10-18-v2), unzip it, and open `harness-conversations/package/index.html` in your browser. Do not use GitHub's automatic source ZIP for these instructions; use the named release asset.

If your browser restricts local HTML, open a terminal inside the extracted `harness-conversations` folder and run:

```sh
python3 serve_transcripts.py
```

Open **http://127.0.0.1:28081/**. Windows users can use `py -3 serve_transcripts.py`. The server verifies every packaged file before starting, binds only to this computer, and stops with Ctrl-C. If the port is occupied, use `--port 28082` and leave the other service alone.

Select a conversation, read the task, follow the tool evidence, and compare the final answer with the checks. Expand **Full event evidence** for complete stored output. The validator example includes its child conversation.

## Choose a lesson

| Lesson | Conversations |
|---|---|
| Harness choice | 01A OpenHands, 01B Pi, 01C OpenCode |
| Tools | 02A Terminal, 02B Four operations, 02C Twelve operations, 02D Custom PR tool |
| Context | 03A No notes, 03B Older notes, 03C Current notes |
| Models | 04C Flash counter, 04D Flash review, 04G Pro counter, 04H Pro review |
| Completion | 05A Ordinary repair, 05B Native goal, 05C Blocked goal |
| Multiple agents | 06A Single owner, 06B Owner plus validator |

Workshop 1 uses selected October 3 recordings: OpenHands batches reads, OpenCode reads separately, and Pi asserts edge cases. Original IDs, timestamps, prompts, and outcomes are preserved. No model reruns were needed. Historical runtime versions were not recorded; the pinned viewer versions below describe the archive reader.

The numbering matches the workshop. Some candidates were omitted for repetition or superseded by the selected pair. This is a curated teaching set, not a representative performance sample. The slides' earlier quantitative experiments are separate from these conversations. See [exercise prompts](https://rajshah4.github.io/learn-openhands-harness/workshops/odsc-2026/prompts) to run new work in your own environment.

## Optional: use the Canvas interface

Use Python 3.13 and Node.js/npm. This route was tested on macOS. Linux, WSL, and AWS acceptance are not yet verified; use HTML if the optional runtime is unavailable. Native Windows runtime paths are not supported by these launch commands.

From the extracted folder, preview the new store, then install it:

```sh
python3 setup_examples.py --destination "$PWD/student-store"
python3 setup_examples.py --destination "$PWD/student-store" --install
```

The installer refuses an existing destination or a normal OpenHands conversation directory. It checks file hashes and rebases only structural workspace paths. Commands inside the histories are evidence and are never executed.

Prepare a private runtime. The first command previews the dependency downloads; the second performs them:

```sh
python3.13 prepare_runtime.py --store "$PWD/student-store"
python3.13 prepare_runtime.py --store "$PWD/student-store" --install
```

This downloads Canvas 1.27.1 and Agent Server, SDK, Tools, and Workspace 1.53.0 from their official npm/Python registries. It does not modify a global Canvas installation. Then start:

```sh
student-store/.venv/bin/python view_canvas.py \
  --store "$PWD/student-store" \
  --canvas "$PWD/student-store/ui/node_modules/@openhands/agent-canvas"
```

Open **http://127.0.0.1:28080/**. The sandbox-unavailable notice is expected. The dedicated host blocks execution, settings changes, forks, terminal access, and WebSockets. Some stock UI controls remain visible. For complete transcripts and verification evidence, use **http://127.0.0.1:28080/packet/**. No Docker daemon, Pi executable, OpenCode executable, or model key is required.

## Verify the download

The release includes `SHA256SUMS.txt`. On macOS, put it beside the ZIP and run `shasum -a 256 -c SHA256SUMS.txt`. On Linux use `sha256sum -c SHA256SUMS.txt`. On Windows compare `Get-FileHash .\harness-conversations-2026-10-18-v2.zip -Algorithm SHA256` with that file. The setup and transcript server also verify the included per-file manifest.

## Stop, recover, or uninstall

Press Ctrl-C in the terminal running either viewer. For a busy Canvas port, add `--port 28082` to `view_canvas.py`; do not stop another service.

To recover from a failed dependency download, stop the viewer and rename `student-store` to `student-store.backup`. Install into a new `student-store`. The installer never merges or overwrites a store. Keep the backup until the replacement works.

To uninstall the optional runtime, stop it and remove only the dedicated `student-store` after checking that it contains `.workshop-install.json`. The transcripts remain available. Remove the extracted folder when you no longer need it. Your normal Canvas conversations are untouched.

## What the archive preserves

The package contains 726 parent events and 19 validator child events, complete sanitized HTML transcripts, and saved verification results. Credentials, original execution configuration, and raw session archives are excluded. Current archive agent settings are inert placeholders; use the titles, manifest, and historical events to identify the original harness. Stored paths point to the instructor's original environment and are not student commands.

Local acceptance covered all 19 conversation read routes, 17 automated tests, blocked write routes and WebSockets, and browser checks. This is a workshop read-only host, not a stock Canvas import feature.
