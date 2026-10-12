from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Page(Generic[T]):
    number: int
    per_page: int
    total_items: int
    total_pages: int
    items: list[T]


def paginate(items: Sequence[T], page: int, per_page: int) -> Page[T]:
    """Return one page using the package's existing one-based page API."""
    if page < 1:
        raise ValueError("page must be >= 1")
    if per_page < 1:
        raise ValueError("per_page must be >= 1")

    source_items = list(items)
    total_items = len(source_items)
    total_pages = ceil(total_items / per_page) if total_items else 0
    start = (page - 1) * per_page
    end = start + per_page
    return Page(
        number=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
        items=source_items[start:end],
    )


def page_numbers(total_items: int, per_page: int) -> list[int]:
    if per_page < 1:
        raise ValueError("per_page must be >= 1")
    if total_items <= 0:
        return []
    return list(range(1, ceil(total_items / per_page) + 1))



@dataclass(frozen=True)
class ExportWindow(Generic[T]):
    records: list[T]
    resume_token: str | None


def export_window(records: Sequence[T], resume_token: str | None = None, limit: int = 100) -> ExportWindow[T]:
    """Resume a snapshot export using the shared v2 token protocol."""
    from .tokens import decode_offset, encode_offset

    if limit < 1:
        raise ValueError("limit must be >= 1")
    offset = decode_offset(resume_token)
    batch = list(records[offset:offset + limit])
    end = offset + len(batch)
    return ExportWindow(batch, encode_offset(end) if end < len(records) else None)
