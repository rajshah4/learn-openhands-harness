# Incident Operations Center

The existing `incident_ops` application tracks incidents in memory. Turn it into a durable incident-operations system that can ingest repeated alerts, coordinate operators and background workers, survive process restarts, and provide a useful browser interface.

Preserve the existing in-memory API and regression tests. Do not add third-party runtime dependencies.

## Incident model

Add these durable fields to the existing incident concept:

- `id`: stable string identifier
- `fingerprint`: alert deduplication key
- `title`: human-readable summary
- `severity`: `P1`, `P2`, `P3`, or `P4`
- `status`: `open`, `acknowledged`, or `resolved`
- `owner`: optional string
- `alert_count`: number of alerts merged into the incident
- `version`: integer incremented by every change
- `escalation_level`: integer starting at zero
- `created_at`, `updated_at`, and `sla_deadline`: numeric Unix timestamps

Expose durable `Incident` and `AuditEvent` values from `incident_ops.models`. Values returned by the store must not change when a later operation updates the database.

## SQLite store

Add `incident_ops.sqlite_store.SQLiteIncidentStore`. Creating a store must initialize its database automatically. Separate store instances opened on the same file must observe the same state.

The constructor accepts a database path, optional `clock` callable, `dedupe_window`, and `lease_seconds`.

Provide these methods:

```python
ingest_alert(
    fingerprint,
    title,
    severity,
    source="unknown",
    details=None,
    idempotency_key=None,
    now=None,
) -> tuple[Incident, bool]

get(incident_id) -> Incident | None
list(status=None, severity=None, owner=None) -> list[Incident]
update(
    incident_id,
    expected_version,
    owner=None,
    status=None,
    idempotency_key=None,
    now=None,
) -> Incident

events(incident_id) -> list[AuditEvent]
claim_due_escalation(worker_id, now=None) -> Incident | None
complete_escalation(incident_id, worker_id, now=None) -> Incident
recover_expired_claims(now=None) -> int
```

Define useful exceptions for missing incidents, invalid transitions, and version conflicts.

### Alert deduplication

The first alert for a fingerprint creates an open incident and returns `(incident, True)`. A later alert with the same fingerprint merges into the newest unresolved incident when its `updated_at` is inside the deduplication window. It increments `alert_count`, updates `updated_at`, increments `version`, appends an audit event, and returns `(incident, False)`.

A resolved incident is never reused. An alert outside the deduplication window creates a new incident. Concurrent processes ingesting the same new fingerprint must still create only one active incident.

Repeating an `idempotency_key` returns the result of the original operation without changing the incident, its version, or its audit history.

### Operator updates

Only these status transitions are valid:

- `open` to `acknowledged`
- `open` to `resolved`
- `acknowledged` to `resolved`

An update must compare `expected_version` with the current version. A stale version raises a conflict instead of overwriting newer work. Assignment and status changes append audit events in the same transaction as the incident update.

### Audit events

Audit events are append-only and ordered. `AuditEvent` exposes `id`, `incident_id`, `type`, `timestamp`, and JSON-compatible `details` fields. Use these event types: `created`, `duplicate_alert`, `owner_changed`, `status_changed`, `escalation_claimed`, `escalated`, and `claim_recovered`.

### Escalation worker

Set the initial SLA deadline from severity:

- P1: 60 seconds
- P2: 300 seconds
- P3: 900 seconds
- P4: 3600 seconds

`claim_due_escalation` atomically claims the oldest overdue unresolved incident for a worker. Separate workers must not claim the same incident. `complete_escalation` verifies ownership of the claim, increments the escalation level and version, clears the claim, advances the next deadline using the same severity interval, and appends an audit event.

A claim expires after `lease_seconds`. `recover_expired_claims` clears expired claims so another worker can continue. Resolved incidents must never be claimed.

Add `incident_ops.escalation.EscalationWorker`. It accepts a store and worker ID and exposes `run_once(now=None)` and `run_until_idle(max_incidents=None, now=None)`.

The worker methods return the durable incident snapshots they complete:

```python
run_once(now=None) -> Incident | None
run_until_idle(max_incidents=None, now=None) -> list[Incident]
```

## HTTP API

Extend the existing standard-library server with these JSON routes:

```text
POST  /api/alerts
GET   /api/incidents
GET   /api/incidents/{id}
PATCH /api/incidents/{id}
POST  /api/escalations/run
GET   /api/summary
```

`POST /api/alerts` accepts the alert fields from `ingest_alert`. Return the incident JSON directly with HTTP 201 when it creates an incident and HTTP 200 when it merges a duplicate. `GET /api/incidents` returns a JSON array and supports `status`, `severity`, and `owner` filters. The incident detail response includes an `events` array. `GET /api/summary` returns an object with at least a numeric `total` and counts by status and severity.

`PATCH /api/incidents/{id}` accepts `expected_version`, optional `owner`, optional `status`, and optional `idempotency_key`. Return HTTP 409 for a stale version. Invalid JSON, invalid severities, and invalid transitions must return useful 4xx JSON responses.

The server accepts a database path and port from the CLI. State must survive stopping and restarting the server.

The starter's `create_server(...)` function constructs and binds a server but does not start its request loop. The CLI calls `serve_forever()`. Any automated HTTP test must likewise start the server in a background thread, then shut down and join that thread. Put explicit time limits on commands that could block so a failed server or browser check cannot strand the agent run.

## Browser interface

Build a complete operator interface, not a wireframe. Show summary counts, filters, an incident list, incident details, owner and status controls, and the audit timeline. Make conflicts and invalid actions visible. Keep the interface usable at a 390 by 844 pixel viewport without horizontal page overflow.

Add these stable markers:

- `data-testid="incident-app"` on the application root
- `data-testid="summary"`
- `data-testid="incident-list"`
- `data-testid="incident-row"` on each incident row
- `data-testid="incident-detail"`
- `data-testid="timeline"`
- `data-testid="status-filter"`
- `data-testid="severity-filter"`
- `data-testid="owner-input"`
- `data-testid="acknowledge-action"`
- `data-testid="resolve-action"`
- `data-testid="feedback"`

Expose this small browser contract after the page loads:

```javascript
window.incidentOps = {
  refresh(),
  selectIncident(id),
  getState()
}
```

`getState()` returns the active filters, selected incident ID, loaded incidents, and latest feedback message.

## Export and import

Extend `python -m incident_ops.cli` with:

```text
--db PATH serve [--port PORT]
--db PATH ingest JSON_ALERT
--db PATH list [--status STATUS] [--severity SEVERITY] [--owner OWNER]
--db PATH update INCIDENT_ID JSON_UPDATE
--db PATH escalate [--worker-id ID] [--max-incidents N]
--db PATH export
--db PATH import
```

Export writes newline-delimited JSON to stdout. Import reads that format from stdin. Export followed by import into a new database must preserve incidents and ordered audit events. Repeating the same import must not duplicate records.

Write one JSON value per output line for the other commands. Invalid JSON and invalid arguments must produce a useful error and a nonzero exit status.

## Completion expectations

Keep storage, HTTP, worker, CLI, and browser concerns separated. Add focused tests without modifying the existing tests. Run the full test suite, exercise the CLI across separate processes, test concurrent ingestion and escalation, start the server, inspect the browser workflow and mobile layout, and check the browser console. Use bounded waits and clean up every server process or thread created by a check. Inspect the final Git status and diff before finishing. Report files changed, checks run, and any remaining uncertainty.
