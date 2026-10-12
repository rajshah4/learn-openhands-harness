# Saved project guidance — snapshot after decision 001
Provenance: simulated project notes captured when resumable exports first shipped.

Catalog browsing uses one-based pages and must keep working. The prior resume
feature lives in toyapp/export_cursor.py; put cursor result types and cursor
paging functions in this separate module. Resume tokens are decimal zero-based
offsets. Consumers import cursor functionality from the cursor module and call
it from the catalog. Keep frozen typed dataclasses, preserve order, and avoid
new dependencies. Add focused tests for the cursor module; this feature has an
isolated caller, so its unit tests are the primary check.

These notes reflect the project at decision 001. Read repository design records
before changing code; if a later accepted decision supersedes these notes,
follow the later decision and mention the mismatch in your final report.
