from incident_ops import IncidentService, IncidentStatus, MemoryIncidentStore, Severity


def test_create_assign_acknowledge_and_resolve() -> None:
    ticks = iter([10.0, 11.0, 12.0, 13.0])
    clock = lambda: next(ticks)
    service = IncidentService(MemoryIncidentStore(clock), clock)

    incident = service.create("Database errors", Severity.P1)
    assert incident.status is IncidentStatus.OPEN
    assert service.assign(incident.id, "Rajiv").owner == "Rajiv"
    assert service.acknowledge(incident.id).status is IncidentStatus.ACKNOWLEDGED
    assert service.resolve(incident.id).status is IncidentStatus.RESOLVED


def test_list_uses_creation_order_and_returns_immutable_values() -> None:
    ticks = iter([20.0, 10.0])
    store = MemoryIncidentStore(lambda: next(ticks))
    later = store.create("Later", "P3")
    earlier = store.create("Earlier", "P2")

    assert [item.id for item in store.list()] == [earlier.id, later.id]
    assert store.get(later.id) == later


def test_rejects_blank_title_and_acknowledging_resolved_incident() -> None:
    service = IncidentService(clock=lambda: 1.0)
    try:
        service.create(" ", "P2")
    except ValueError as exc:
        assert "title" in str(exc)
    else:
        raise AssertionError("blank title should fail")

    incident = service.create("Network issue", "P2")
    service.resolve(incident.id)
    try:
        service.acknowledge(incident.id)
    except ValueError as exc:
        assert "resolved" in str(exc)
    else:
        raise AssertionError("resolved incident should not be acknowledged")
