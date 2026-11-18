# MLOps saved conversations

Choose how you want to participate. **Open the public Canvas to follow along without installing anything.** You can inspect the saved conversations without a login, model key or new model calls.

| Option | What you do | When to choose it |
|---|---|---|
| **[1. Browse the public Canvas](http://34.215.46.146:8080/)** | Open the read-only MLOps workshop archive and expand tool calls and results. No installation, login or model key is needed. | Fastest way to follow the workshop and inspect the recorded work. |
| [2. Inspect in your own Canvas](./conversations#inspect-in-your-own-agent-canvas) | Download and import the same histories into a local Canvas. | Keep the conversations after the temporary server is removed. |
| [3. Run the exercises yourself](./setup#run-a-fresh-exercise) | Start fresh conversations with your own configured model and workspace. | Change the harness and compare new runs. |

The public server is temporary and read-only. It uses plain HTTP. Do not enter credentials or private information. New runs, edits and resumed conversations are blocked.

## Browse the public Canvas

[Open the public MLOps Canvas](http://34.215.46.146:8080/). Choose a workshop in the conversation list, then expand its tool cards and returned output. No installation, login or model key is needed. This is the same selection as the download: 15 histories and 575 events. Use the [exercise table below](#find-each-exercise) to open a specific history or either Exercise 4 animation.

Download the archive below to keep the histories after the temporary server is removed.

## Download the conversations

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

| Exercise | Open the recorded work |
|---|---|
| 1. Compare harnesses | [1A OpenHands](http://34.215.46.146:8080/conversations/7ca26ccf-45fb-58aa-9359-57f8fae10912?backend=workshop) · [1B Pi](http://34.215.46.146:8080/conversations/b473027b-9cc7-523d-811f-64a9e3b45774?backend=workshop) · [1C OpenCode](http://34.215.46.146:8080/conversations/877b6eb1-2027-553f-848c-a86f05c88346?backend=workshop) |
| 2. Choose tools | [2A Terminal](http://34.215.46.146:8080/conversations/b9f6e3c2-fa97-56f7-b740-ea2b4f5cfa24?backend=workshop) · [2B Four GitHub operations](http://34.215.46.146:8080/conversations/8f974c97-dd8c-57cc-adaf-e24b9a3fb700?backend=workshop) · [2C Custom PR tool](http://34.215.46.146:8080/conversations/9dcdd5f6-7cf5-510c-913c-1ed12b4b7867?backend=workshop) |
| 3. Choose context | [3A No supplied task memory](http://34.215.46.146:8080/conversations/222caa22-3db1-52a9-9a7e-51778cadaf5c?backend=workshop) · [3B Useful saved route](http://34.215.46.146:8080/conversations/596382e4-51f6-565d-af65-8f2a12d14519?backend=workshop) · [3C Stale route, earlier take](http://34.215.46.146:8080/conversations/2e49f27f-ce2e-5e49-b369-17cce45ff32a?backend=workshop) |
| 4. Model choice | [Flash SVG](http://34.215.46.146:8080/packet/animations/workshop4-hedgehog-flash.svg) · [Pro SVG](http://34.215.46.146:8080/packet/animations/workshop4-hedgehog-pro.svg) · [Shared prompt](http://34.215.46.146:8080/packet/animations/workshop4-hedgehog-prompt.txt). Original outputs, also in package/animations/. |
| 5. Verification | [M5-A API migration and external HTTP replay](http://34.215.46.146:8080/conversations/5780556d-6e1d-59d5-bc96-fc450f8613bd?backend=workshop) |
| 6. Multi-agent systems | [6A Single owner](http://34.215.46.146:8080/conversations/8fa59cf0-f6b8-5c0f-a8a1-4aa2e129264a?backend=workshop) · [6B Lead and three workers](http://34.215.46.146:8080/conversations/21f36b96-8332-5f1d-b213-db2c7f514832?backend=workshop) · [6B.1 Codec worker](http://34.215.46.146:8080/conversations/a7fffbb5-1f45-5e81-bc7c-ecc633b693d7?backend=workshop) · [6B.2 Reducer worker](http://34.215.46.146:8080/conversations/dccff88a-e193-5ff1-9095-7003ce45f597?backend=workshop) · [6B.3 Checkpoint worker](http://34.215.46.146:8080/conversations/18ee8eca-04f1-5943-ada5-410740e4eba4?backend=workshop) |

In M5-A, the agent invokes the controller-written replay. It sees seven mismatches, adds a serializer and passes the same 15 cases. The visible Error status is the 40-iteration cap after the pass. No Stop hook executed. The recorded final artifact is not supplied as a correct solution. For fresh runs, use the [Exercise 5 starter](./exercises/04-api-migration).

## Keep ODSC separate

This bundle has its own MLOps tag, archive, workspaces and import receipt. Its import UUIDs are namespaced so both editions can coexist. Original source UUIDs and event IDs are retained in package/manifest.json and package/source-provenance.json. Old Workshop 5 report/goal histories, the failed DeepSeek authentication attempt and Opus reviews are excluded.

The offline package/index.html maps the selected evidence and original SVGs. Use Canvas for the conversation walkthrough. The index is provenance, not a replacement participation path.

## Custom stores and recovery

The npm launcher normally uses ~/.openhands/agent-canvas/dev_conversations. For a custom local store or backend port, pass `--store /absolute/path/dev_conversations` and `--backend-url http://127.0.0.1:PORT` to both import commands. The importer refuses symlinks, collisions, changed installed histories and a running backend when installing a new import. Repeating an unchanged import verifies it without adding duplicates.

Keep the extracted package and its hashes. The mlops-lecture-import.json receipt beside the store records exact imported IDs, event hashes and historical type compatibility mappings. Stop Canvas before removing only the histories/workspaces named in that receipt. Leave other data and settings alone. Imported agents contain no model credentials, executable tools, plugins or hooks; stopped histories are not an immutable security boundary. Start fresh conversations for exercises.

The MLOps release is published separately from ODSC. Verification records describe the tested archive at build time; its bytes are unchanged for publication.
