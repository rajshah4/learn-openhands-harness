# Workshop catalog

A small Python catalog library. browse(items, page=2, per_page=2) gives direct
page-number access. export_all(records, batch_size=2) already resumes a report
across several windows. Both use toyapp.pagination; resume tokens are shared
through toyapp.tokens. Run python3 -m pytest -q (Python 3.11+, pytest).

Current accepted decisions are in docs/current. docs/history contains the
superseded export design and its working source snapshot. This history was
constructed for the workshop; it is not an organic production history.

The new request is next-page catalog browsing. Read the accepted design for its
public API and the prior export implementation for the repository conventions.
