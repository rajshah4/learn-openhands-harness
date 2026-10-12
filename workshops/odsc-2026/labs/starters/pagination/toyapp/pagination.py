from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Page:
    number: int
    per_page: int
    total_items: int
    total_pages: int
    items: list[object]


def paginate(items: Sequence[T], page: int, per_page: int) -> Page:
    if page < 1:
        raise ValueError("page must be >= 1")
    if per_page < 1:
        raise ValueError("per_page must be >= 1")

    raw_items = list(items)
    total_items = len(raw_items)
    total_pages = ceil(total_items / per_page) if total_items else 0
    start = (page - 1) * per_page
    end = start + per_page - 1
    return Page(
        number=page,
        per_page=per_page,
        total_items=total_items,
        total_pages=total_pages,
        items=raw_items[start:end],
    )


def page_numbers(total_items: int, per_page: int) -> list[int]:
    if total_items <= 0:
        return []
    total_pages = ceil(total_items / per_page)
    return list(range(1, total_pages + 1))
