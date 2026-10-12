"""Simulated initial implementation, superseded by decision 002."""
from dataclasses import dataclass
from typing import Sequence, TypeVar, Generic
T = TypeVar("T")

@dataclass(frozen=True)
class ExportWindow(Generic[T]):
    records: list[T]
    resume_token: str | None

def export_window(records: Sequence[T], resume_token: str | None = None, limit: int = 100) -> ExportWindow[T]:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    offset = 0 if resume_token is None else int(resume_token)
    if offset < 0:
        raise ValueError("offset must be >= 0")
    batch = list(records[offset:offset + limit])
    end = offset + len(batch)
    return ExportWindow(batch, str(end) if end < len(records) else None)
