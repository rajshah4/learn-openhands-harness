# Decision 003: next-page catalog browsing
Status: accepted; builds on 002. This workshop history is simulated.

Add CursorPage and paginate_cursor to toyapp.pagination. CursorPage is a frozen
generic dataclass with items: list[T], next_cursor: str | None, has_more: bool.
Signature: paginate_cursor(items, cursor=None, per_page=20). Reuse the existing
shared v2 token protocol; next_cursor points to the first item of the next page.
It is None at the end, including empty input and a valid offset beyond the end.
has_more is true exactly when next_cursor is not None. Reject per_page < 1 and
invalid cursors with ValueError. Preserve ordering and do not mutate inputs.

Add browse_next(items, cursor=None, per_page=20) in toyapp.catalog as a thin
caller of paginate_cursor. Existing browse, paginate, page_numbers, exports and
their validation remain unchanged. Public consumers import the new API from
toyapp.pagination and toyapp.catalog; no package-root re-exports are required.
The current implementation and tests for exports are the sibling feature to
learn from. Focused cursor tests and the full suite cover different contracts.
