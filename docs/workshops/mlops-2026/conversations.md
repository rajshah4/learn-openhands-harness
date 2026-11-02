# MLOps saved conversations

[Download the MLOps conversation bundle](/downloads/mlops-2026/mlops-lecture-conversations-2026-11-02-v2.zip) and extract it. [Checksums](/downloads/mlops-2026/SHA256SUMS.txt) and [import verification](/downloads/mlops-2026/IMPORT-VERIFICATION.json) accompany this archive. The [final archive check](/downloads/mlops-2026/VERIFICATION.json) binds the tested final ZIP to its SHA-256 checksum.

This separate conference edition covers all six exercises: 12 primary Canvas histories, three team-worker histories and 575 retained events. Exercise 4 uses two original animated SVG outputs and their shared prompt, not a Canvas conversation. Exercise 5 is M5-A, the Pydantic migration with the real verifier failure, agent repair and passing replay. Its complete capped history is included.

You can also download the same files from the [MLOps GitHub release](https://github.com/rajshah4/learn-openhands-harness/releases/tag/mlops-lecture-conversations-2026-11-02).

## Inspect in your own Agent Canvas

Use a local npm installation of Canvas. No model key is needed to inspect the imported histories.

1. Stop Canvas with Ctrl-C in its terminal before installing the import.
2. Open a terminal in the extracted mlops-lecture-conversations folder and run:

   ```sh
   python3 import_into_canvas.py
   python3 import_into_canvas.py --install
   ```

   The first command previews the destination. The second verifies package hashes and adds the histories without overwriting existing conversation IDs.

3. Start Canvas:

   ```sh
   agent-canvas
   ```

   Open the URL printed in its terminal. On first launch, choose your usage-data preference and Skip for now on model setup. The LLM setup banner affects new runs, not inspection of these saved histories.

4. Beside Conversations, choose View, Filter by tags, and `lecture=mlops2026`. Open a title beginning with MLOps. Expand the tool cards and their returned output. Click More if your version collapses the list.

The import was tested on macOS using Canvas 1.33.0 and Agent Server/SDK 1.58.1, an ordinary npm Canvas startup, a fresh home/store and no model credentials. All 15 histories and their full 575-event sequences loaded. Restarting Canvas preserved the import. Other versions, Windows, Linux, Docker and remote backend imports have not been verified.

## Find each exercise

| Exercise | Selection |
|---|---|
| 1. Compare harnesses | 1A OpenHands, 1B Pi, 1C OpenCode. |
| 2. Choose tools | 2A Terminal, 2B Four GitHub operations, 2C Custom PR tool. |
| 3. Choose context | 3A No supplied task memory, 3B Useful saved route, 3C Stale route from an earlier take. |
| 4. Model choice | Open the two SVG files and shared prompt in package/animations/. These are original outputs, not conversation histories. |
| 5. Verify an API migration | M5-A API migration and external HTTP replay. The source conversation UUID is f5bdbb0e-e907-4959-85c5-204c96a41000. |
| 6. Delegate work | 6A Single owner, 6B Lead and three workers, and worker histories 6B.1 to 6B.3. |

In M5-A, the agent invokes the controller-written replay. It sees seven mismatches, adds a serializer and passes the same 15 cases. The visible Error status is the 40-iteration cap after the pass. No Stop hook executed. The recorded final artifact is not supplied as a correct solution. For fresh runs, use the [Exercise 5 starter](./exercises/04-api-migration).

## Keep ODSC separate

This bundle has its own MLOps tag, archive, workspaces and import receipt. Its import UUIDs are namespaced so both editions can coexist. Original source UUIDs and event IDs are retained in package/manifest.json and package/source-provenance.json. Old Workshop 5 report/goal histories, the failed DeepSeek authentication attempt and Opus reviews are excluded.

The offline package/index.html maps the selected evidence and original SVGs. Use Canvas for the conversation walkthrough. The index is provenance, not a replacement participation path.

## Custom stores and recovery

The npm launcher normally uses ~/.openhands/agent-canvas/dev_conversations. For a custom local store or backend port, pass `--store /absolute/path/dev_conversations` and `--backend-url http://127.0.0.1:PORT` to both import commands. The importer refuses symlinks, collisions, changed installed histories and a running backend when installing a new import. Repeating an unchanged import verifies it without adding duplicates.

Keep the extracted package and its hashes. The mlops-lecture-import.json receipt beside the store records exact imported IDs, event hashes and historical type compatibility mappings. Stop Canvas before removing only the histories/workspaces named in that receipt. Leave other data and settings alone. Imported agents contain no model credentials, executable tools, plugins or hooks; stopped histories are not an immutable security boundary. Start fresh conversations for exercises.

The MLOps release is published separately from ODSC. Verification records describe the tested archive at build time; its bytes are unchanged for publication.
