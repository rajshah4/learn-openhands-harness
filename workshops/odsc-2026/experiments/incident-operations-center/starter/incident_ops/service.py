"""Business operations for the original in-memory application."""

from __future__ import annotations

import time
from collections.abc import Callable

from .memory_store import MemoryIncidentStore
from .models import Incident, IncidentStatus, Severity


class IncidentService:
    def __init__(
        self,
        store: MemoryIncidentStore | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self.store = store or MemoryIncidentStore(clock=clock)
        self.clock = clock

    def create(self, title: str, severity: Severity | str) -> Incident:
        if not title.strip():
            raise ValueError("title is required")
        return self.store.create(title.strip(), severity)

    def list(self) -> list[Incident]:
        return self.store.list()

    def assign(self, incident_id: str, owner: str) -> Incident:
        incident = self._required(incident_id)
        return self.store.save(
            incident.changed(owner=owner.strip() or None, updated_at=self.clock())
        )

    def acknowledge(self, incident_id: str) -> Incident:
        incident = self._required(incident_id)
        if incident.status is IncidentStatus.RESOLVED:
            raise ValueError("a resolved incident cannot be acknowledged")
        return self.store.save(
            incident.changed(
                status=IncidentStatus.ACKNOWLEDGED,
                updated_at=self.clock(),
            )
        )

    def resolve(self, incident_id: str) -> Incident:
        incident = self._required(incident_id)
        return self.store.save(
            incident.changed(status=IncidentStatus.RESOLVED, updated_at=self.clock())
        )

    def _required(self, incident_id: str) -> Incident:
        incident = self.store.get(incident_id)
        if incident is None:
            raise KeyError(incident_id)
        return incident
