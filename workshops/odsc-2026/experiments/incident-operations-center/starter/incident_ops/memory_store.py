"""The original process-local incident store."""

from __future__ import annotations

import time
import uuid
from collections.abc import Callable

from .models import Incident, IncidentStatus, Severity


class MemoryIncidentStore:
    def __init__(self, clock: Callable[[], float] = time.time) -> None:
        self._clock = clock
        self._incidents: dict[str, Incident] = {}

    def create(self, title: str, severity: Severity | str) -> Incident:
        now = self._clock()
        incident = Incident(
            id=str(uuid.uuid4()),
            title=title,
            severity=Severity(severity),
            status=IncidentStatus.OPEN,
            owner=None,
            created_at=now,
            updated_at=now,
        )
        self._incidents[incident.id] = incident
        return incident

    def get(self, incident_id: str) -> Incident | None:
        return self._incidents.get(incident_id)

    def list(self) -> list[Incident]:
        return sorted(self._incidents.values(), key=lambda item: item.created_at)

    def save(self, incident: Incident) -> Incident:
        if incident.id not in self._incidents:
            raise KeyError(incident.id)
        self._incidents[incident.id] = incident
        return incident
