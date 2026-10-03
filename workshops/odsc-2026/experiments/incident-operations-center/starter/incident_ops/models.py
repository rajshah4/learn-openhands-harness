"""Core values used by the starter application."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum


class Severity(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class IncidentStatus(StrEnum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


@dataclass(frozen=True, slots=True)
class Incident:
    id: str
    title: str
    severity: Severity
    status: IncidentStatus
    owner: str | None
    created_at: float
    updated_at: float

    def changed(self, **values: object) -> "Incident":
        return replace(self, **values)
