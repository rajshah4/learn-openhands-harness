# Saved project guidance — snapshot after decisions 002 and 003
Provenance: simulated project notes refreshed after the export consolidation.

Catalog browsing and exports share toyapp.pagination. Add CursorPage and
paginate_cursor there; toyapp.catalog.browse_next is a thin caller. Reuse the
canonical v2 resume-token helpers in toyapp.tokens, as export_window does.
Keep page-number browsing and report exports compatible; preserve order and
never mutate input. Consumers import from the owning module; __init__.py stays
empty. Keep frozen typed dataclasses and simple functions; no dependency needed.

Current accepted records are in docs/current; decision 002 supersedes the
separate cursor module and decimal tokens in decision 001. Add focused tests
in tests/test_pagination.py, run that file, then python3 -m pytest -q to cover
both callers. Read repository records and follow the latest accepted decision
if these notes ever disagree. Report any mismatch.
