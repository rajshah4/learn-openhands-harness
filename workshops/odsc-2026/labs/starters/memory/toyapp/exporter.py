"""Background exports already resume across multiple windows."""
from typing import Sequence, TypeVar
from .pagination import export_window

T = TypeVar("T")


def export_all(records: Sequence[T], batch_size: int = 100) -> list[T]:
    result: list[T] = []
    cursor = None
    while True:
        batch = export_window(records, cursor, batch_size)
        result.extend(batch.records)
        cursor = batch.resume_token
        if cursor is None:
            return result
