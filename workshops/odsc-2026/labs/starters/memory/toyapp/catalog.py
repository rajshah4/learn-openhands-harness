"""The existing catalog supports direct page-number access."""
from typing import Sequence, TypeVar
from .pagination import Page, paginate

T = TypeVar("T")


def browse(items: Sequence[T], page: int = 1, per_page: int = 20) -> Page[T]:
    return paginate(items, page, per_page)
