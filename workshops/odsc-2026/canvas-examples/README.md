# ODSC workshop participation

Students have two options:

1. **Inspect the saved conversations in their own Agent Canvas (recommended)**. Import the current lecture package and filter by `lecture=odsc2026`.
2. **Run the full exercises** if they have time to configure model access and the required tools.

Follow the [student setup guide](../../../docs/workshops/odsc-2026/setup.md) and [conversation import directions](../../../docs/workshops/odsc-2026/conversations.md). The current lecture selection is 13 conversations, three worker histories and two original animation outputs. It excludes superseded experiments and reserves.

The updated student ZIP includes `import_into_canvas.py`. Use it from the extracted current lecture bundle, which contains its matching `package/manifest.json`; the script previews by default. Stop the local Canvas backend before `--install`, then restart Canvas and choose View, Filter by tags, `lecture=odsc2026`. No model key is needed to inspect the imported histories. The tested local versions are Canvas 1.29.0 and Agent Server 1.56.0 on macOS.

Use the release ZIP for the matching scripts and payload. The importer source in this directory is provided for review; running it requires the matching extracted `package/` folder.

Imported names start with the workshop and scenario, for example `W1 - 1A - OpenHands`. The filter tag is `lecture=odsc2026`.
