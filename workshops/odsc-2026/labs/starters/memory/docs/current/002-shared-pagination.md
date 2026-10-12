# Decision 002: one pagination boundary, one resume protocol
Status: accepted; supersedes 001. This workshop history is simulated.

The report exporter is now a second paging caller alongside catalog browsing.
Keep paging result types and implementations together in toyapp.pagination:
export_window and ExportWindow have moved there. Package __init__.py is empty;
consumers import from the owning module. The exporter is a real caller and its
regression tests exercise traversal, bounds and token validation.

Decimal offsets leaked the wire representation to callers. Shared helpers in
toyapp.tokens now encode opaque, canonical URL-safe base64 without padding,
with payload v2:<zero-based offset>. decode_offset rejects malformed tokens,
wrong versions, negative offsets and noncanonical encodings with ValueError.
The exported functions preserve caller-supplied ordering; they do not sort or
mutate the source. These are snapshot offsets, not stable database cursors.

The existing one-based paginate and Page contract remains public. Adding a new
paging caller must preserve both existing callers. Extend test_pagination.py
for focused tests, then run python3 -m pytest -q for caller regressions. Keep
frozen dataclasses, type hints and simple functions; no new dependency is needed.
