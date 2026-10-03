#!/usr/bin/env python3
"""Instructor-owned verifier for the incident operations benchmark."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterator


class Checks:
    def __init__(self) -> None:
        self.results: list[tuple[str, bool, str]] = []

    def run(self, name: str, check: Callable[[], None]) -> None:
        try:
            check()
        except Exception as exc:
            self.results.append((name, False, f"{type(exc).__name__}: {exc}"))
        else:
            self.results.append((name, True, ""))

    def report(self) -> bool:
        for name, passed, detail in self.results:
            print(f"{'PASS' if passed else 'FAIL'}: {name}")
            if detail:
                print(f"  {detail}")
        passed = sum(result[1] for result in self.results)
        print(f"\n{passed}/{len(self.results)} checks passed")
        return passed == len(self.results)


def enum_value(value: Any) -> Any:
    return getattr(value, "value", value)


def assert_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def load_api(workspace: Path) -> tuple[type, type]:
    sys.path.insert(0, str(workspace))
    importlib.invalidate_caches()
    store_module = importlib.import_module("incident_ops.sqlite_store")
    worker_module = importlib.import_module("incident_ops.escalation")
    return store_module.SQLiteIncidentStore, worker_module.EscalationWorker


def test_public_regressions(workspace: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=workspace,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    if result.returncode:
        raise AssertionError(result.stdout[-2000:])


def test_persistence_deduplication_and_idempotency(store_type: type) -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "incidents.db"
        store = store_type(path, clock=lambda: 1000.0, dedupe_window=300)
        first, created = store.ingest_alert(
            "db-errors",
            "Database errors",
            "P1",
            source="payments",
            details={"region": "west"},
            idempotency_key="alert-1",
            now=1000.0,
        )
        assert created is True
        assert_equal(first.alert_count, 1, "initial alert count")
        assert_equal(enum_value(first.status), "open", "initial status")
        assert_equal(first.sla_deadline, 1060.0, "P1 deadline")

        replay, replay_created = store.ingest_alert(
            "db-errors",
            "Ignored replay title",
            "P1",
            idempotency_key="alert-1",
            now=1001.0,
        )
        assert replay_created is True
        assert_equal(replay.id, first.id, "idempotent incident")
        assert_equal(replay.version, first.version, "idempotent version")

        duplicate, duplicate_created = store.ingest_alert(
            "db-errors",
            "Database errors continue",
            "P1",
            idempotency_key="alert-2",
            now=1002.0,
        )
        assert duplicate_created is False
        assert_equal(duplicate.id, first.id, "deduplicated incident")
        assert_equal(duplicate.alert_count, 2, "deduplicated alert count")
        assert_equal(first.alert_count, 1, "returned values must be snapshots")

        reopened = store_type(path, clock=lambda: 1003.0, dedupe_window=300)
        persisted = reopened.get(first.id)
        assert persisted is not None
        assert_equal(persisted.alert_count, 2, "persisted alert count")
        assert len(reopened.events(first.id)) >= 2

        reopened.update(
            first.id,
            expected_version=persisted.version,
            status="resolved",
            now=1004.0,
        )
        new_incident, new_created = reopened.ingest_alert(
            "db-errors",
            "New database incident",
            "P1",
            idempotency_key="alert-3",
            now=1005.0,
        )
        assert new_created is True
        assert new_incident.id != first.id


def test_versions_transitions_and_audit(store_type: type) -> None:
    with tempfile.TemporaryDirectory() as directory:
        store = store_type(Path(directory) / "incidents.db", clock=lambda: 50.0)
        incident, _ = store.ingest_alert("api", "API latency", "P2", now=50.0)
        assigned = store.update(
            incident.id,
            expected_version=incident.version,
            owner="sam",
            idempotency_key="assign-1",
            now=51.0,
        )
        assert_equal(assigned.owner, "sam", "owner")

        try:
            store.update(
                incident.id,
                expected_version=incident.version,
                owner="lee",
                now=52.0,
            )
        except Exception:
            pass
        else:
            raise AssertionError("stale version update should fail")

        acknowledged = store.update(
            incident.id,
            expected_version=assigned.version,
            status="acknowledged",
            now=53.0,
        )
        resolved = store.update(
            incident.id,
            expected_version=acknowledged.version,
            status="resolved",
            now=54.0,
        )
        assert_equal(enum_value(resolved.status), "resolved", "resolved status")

        try:
            store.update(
                incident.id,
                expected_version=resolved.version,
                status="acknowledged",
                now=55.0,
            )
        except Exception:
            pass
        else:
            raise AssertionError("resolved incident should not reopen")

        events = store.events(incident.id)
        timestamps = [event.timestamp for event in events]
        assert timestamps == sorted(timestamps)
        event_types = {event.type for event in events}
        if not {"created", "owner_changed", "status_changed"}.issubset(event_types):
            raise AssertionError(f"missing audit event types: {event_types}")


def test_concurrent_deduplication(store_type: type) -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "incidents.db"
        store_type(path, clock=lambda: 200.0, dedupe_window=300)
        barrier = threading.Barrier(8)

        def ingest(index: int) -> tuple[str, bool]:
            store = store_type(path, clock=lambda: 200.0, dedupe_window=300)
            barrier.wait(timeout=10)
            incident, created = store.ingest_alert(
                "shared-fingerprint",
                "Concurrent alert",
                "P2",
                idempotency_key=f"concurrent-{index}",
                now=200.0,
            )
            return incident.id, created

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(ingest, range(8)))

        assert_equal(len({result[0] for result in results}), 1, "incident count")
        assert_equal(sum(result[1] for result in results), 1, "created results")
        final = store_type(path).list(status="open")
        matching = [item for item in final if item.fingerprint == "shared-fingerprint"]
        assert_equal(len(matching), 1, "active deduplicated incidents")
        assert_equal(matching[0].alert_count, 8, "concurrent alert count")


def test_escalation_concurrency_and_recovery(store_type: type, worker_type: type) -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "incidents.db"
        first_store = store_type(path, clock=lambda: 1000.0, lease_seconds=10)
        incident, _ = first_store.ingest_alert("overdue", "Overdue P1", "P1", now=1000.0)
        second_store = store_type(path, clock=lambda: 1000.0, lease_seconds=10)

        claimed = first_store.claim_due_escalation("worker-a", now=1061.0)
        assert claimed is not None
        assert_equal(claimed.id, incident.id, "claimed incident")
        assert second_store.claim_due_escalation("worker-b", now=1061.0) is None

        try:
            second_store.complete_escalation(incident.id, "worker-b", now=1062.0)
        except Exception:
            pass
        else:
            raise AssertionError("a different worker should not complete a claim")

        escalated = first_store.complete_escalation(incident.id, "worker-a", now=1062.0)
        assert_equal(escalated.escalation_level, 1, "escalation level")
        assert escalated.sla_deadline > 1062.0

        claimed_again = first_store.claim_due_escalation(
            "worker-a", now=escalated.sla_deadline + 1
        )
        assert claimed_again is not None
        recovered = second_store.recover_expired_claims(
            now=escalated.sla_deadline + 12
        )
        assert_equal(recovered, 1, "expired claims recovered")
        reclaimed = second_store.claim_due_escalation(
            "worker-b", now=escalated.sla_deadline + 12
        )
        assert reclaimed is not None

        worker_path = Path(directory) / "worker.db"
        worker_store = store_type(worker_path, clock=lambda: 2000.0, lease_seconds=10)
        second_incident, _ = worker_store.ingest_alert(
            "worker-run",
            "Worker run once",
            "P1",
            now=2000.0,
        )
        worker = worker_type(worker_store, "worker-c")
        finished = worker.run_once(now=2061.0)
        assert finished is not None
        assert_equal(finished.id, second_incident.id, "worker incident")
        assert_equal(finished.escalation_level, 1, "worker escalation level")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def http_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
) -> tuple[int, Any]:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


@contextmanager
def running_server(workspace: Path, database: Path) -> Iterator[str]:
    port = free_port()
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "incident_ops.cli",
            "--db",
            str(database),
            "serve",
            "--port",
            str(port),
        ],
        cwd=workspace,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(50):
            if process.poll() is not None:
                output = process.stdout.read() if process.stdout else ""
                raise AssertionError(f"server exited early: {output[-1500:]}")
            try:
                with urllib.request.urlopen(f"{base}/", timeout=1):
                    break
            except Exception:
                time.sleep(0.1)
        else:
            raise AssertionError("server did not become ready")
        yield base
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def test_http_api(workspace: Path) -> None:
    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "api.db"
        with running_server(workspace, database) as base:
            status, created = http_json(
                "POST",
                f"{base}/api/alerts",
                {
                    "fingerprint": "http-alert",
                    "title": "HTTP alert",
                    "severity": "P2",
                    "idempotency_key": "http-1",
                },
            )
            assert_equal(status, 201, "create status")
            incident_id = created["id"]
            version = created["version"]

            status, duplicate = http_json(
                "POST",
                f"{base}/api/alerts",
                {
                    "fingerprint": "http-alert",
                    "title": "HTTP alert again",
                    "severity": "P2",
                    "idempotency_key": "http-2",
                },
            )
            assert_equal(status, 200, "duplicate status")
            assert_equal(duplicate["id"], incident_id, "duplicate HTTP incident")

            status, listing = http_json("GET", f"{base}/api/incidents?severity=P2")
            assert_equal(status, 200, "list status")
            assert len(listing) == 1

            status, _ = http_json(
                "PATCH",
                f"{base}/api/incidents/{incident_id}",
                {"expected_version": version, "owner": "stale-owner"},
            )
            assert_equal(status, 409, "version conflict status")

            status, detail = http_json("GET", f"{base}/api/incidents/{incident_id}")
            assert_equal(status, 200, "detail status")
            assert len(detail["events"]) >= 2

            status, summary = http_json("GET", f"{base}/api/summary")
            assert_equal(status, 200, "summary status")
            assert "total" in summary


def run_cli(
    workspace: Path,
    database: Path,
    *arguments: str,
    input_text: str | None = None,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "incident_ops.cli", "--db", str(database), *arguments],
        cwd=workspace,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )


def test_cli_export_import(workspace: Path) -> None:
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "source.db"
        target = Path(directory) / "target.db"
        alert = json.dumps(
            {
                "fingerprint": "cli-alert",
                "title": "CLI alert",
                "severity": "P3",
                "idempotency_key": "cli-1",
            }
        )
        ingested = run_cli(workspace, source, "ingest", alert)
        assert_equal(ingested.returncode, 0, "CLI ingest")
        exported = run_cli(workspace, source, "export")
        assert_equal(exported.returncode, 0, "CLI export")
        records = [json.loads(line) for line in exported.stdout.splitlines() if line]
        assert records

        imported = run_cli(workspace, target, "import", input_text=exported.stdout)
        assert_equal(imported.returncode, 0, "CLI import")
        repeated = run_cli(workspace, target, "import", input_text=exported.stdout)
        assert_equal(repeated.returncode, 0, "repeat CLI import")
        listed = run_cli(workspace, target, "list")
        assert_equal(listed.returncode, 0, "CLI list")
        incidents = [json.loads(line) for line in listed.stdout.splitlines() if line]
        assert_equal(len(incidents), 1, "idempotent imported incident count")

        invalid = run_cli(workspace, source, "ingest", "not-json")
        if invalid.returncode == 0:
            raise AssertionError("invalid CLI JSON should fail")


def test_browser(workspace: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise AssertionError("Playwright is required by the verifier") from exc

    with tempfile.TemporaryDirectory() as directory:
        with running_server(workspace, Path(directory) / "browser.db") as base:
            http_json(
                "POST",
                f"{base}/api/alerts",
                {
                    "fingerprint": "browser-alert",
                    "title": "Browser alert",
                    "severity": "P1",
                },
            )
            console_errors: list[str] = []
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 390, "height": 844})
                page.on(
                    "console",
                    lambda message: console_errors.append(message.text)
                    if message.type == "error"
                    else None,
                )
                page.goto(base, wait_until="networkidle")
                for test_id in (
                    "incident-app",
                    "summary",
                    "incident-list",
                    "incident-row",
                    "status-filter",
                    "severity-filter",
                    "feedback",
                ):
                    page.get_by_test_id(test_id).first.wait_for(state="visible")
                state = page.evaluate("window.incidentOps.getState()")
                assert state["incidents"]
                page.evaluate(
                    "incidentId => window.incidentOps.selectIncident(incidentId)",
                    state["incidents"][0]["id"],
                )
                page.get_by_test_id("incident-detail").wait_for(state="visible")
                page.get_by_test_id("timeline").wait_for(state="visible")
                overflow = page.evaluate(
                    "document.documentElement.scrollWidth > document.documentElement.clientWidth"
                )
                if overflow:
                    raise AssertionError("page has horizontal root overflow at 390px")
                browser.close()
            if console_errors:
                raise AssertionError(f"browser console errors: {console_errors}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        raise SystemExit(f"workspace does not exist: {workspace}")

    checks = Checks()
    checks.run("existing regression tests", lambda: test_public_regressions(workspace))
    try:
        store_type, worker_type = load_api(workspace)
    except Exception as exc:
        detail = f"{type(exc).__name__}: {exc}"
        for name in (
            "persistence, deduplication, and idempotency",
            "versions, transitions, and audit history",
            "concurrent alert deduplication",
            "escalation concurrency and recovery",
        ):
            checks.results.append((name, False, detail))
    else:
        checks.run(
            "persistence, deduplication, and idempotency",
            lambda: test_persistence_deduplication_and_idempotency(store_type),
        )
        checks.run(
            "versions, transitions, and audit history",
            lambda: test_versions_transitions_and_audit(store_type),
        )
        checks.run(
            "concurrent alert deduplication",
            lambda: test_concurrent_deduplication(store_type),
        )
        checks.run(
            "escalation concurrency and recovery",
            lambda: test_escalation_concurrency_and_recovery(store_type, worker_type),
        )
    checks.run("HTTP API workflow and conflicts", lambda: test_http_api(workspace))
    checks.run("CLI export and idempotent import", lambda: test_cli_export_import(workspace))
    checks.run("responsive browser workflow", lambda: test_browser(workspace))
    return 0 if checks.report() else 1


if __name__ == "__main__":
    raise SystemExit(main())
