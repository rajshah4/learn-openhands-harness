# Reference library

`harness-references.json` is the shared source for the reference page. It records linked citations in the current exported ODSC deck and selected backup collections as of October 25, 2026. The metadata records source paths and hashes. Membership does not establish whether material was presented at an event.

When updating the deck, reconcile exported slide order, slide anchors, and speaker-note URLs. Keep one entry per source, preserve specific versions and timestamps in `locators`, and keep sources that appear in the current deck under `main`. Backup-only sources belong under `additional`. Review moved URLs and title mismatches before changing them. Preserve correction notes and unresolved citation notes.

Run `npm run references:check` and `npm run docs:build` after edits. The companion harness-engineering repository links to the same hosted page rather than maintaining a second reference list.

Extraction evidence and original link checks are retained locally under `Documents/TikTok/outputs/harness-reference-library-2026-10-25/`.
