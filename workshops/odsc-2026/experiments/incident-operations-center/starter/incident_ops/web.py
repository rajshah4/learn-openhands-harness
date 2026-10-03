"""Small standard-library HTTP server for the starter interface."""

from __future__ import annotations

import json
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .service import IncidentService


STATIC_DIR = Path(__file__).with_name("static")


def json_value(value: object) -> object:
    if hasattr(value, "value"):
        return value.value
    raise TypeError(f"cannot encode {type(value).__name__}")


def create_server(
    service: IncidentService,
    host: str = "127.0.0.1",
    port: int = 8080,
) -> ThreadingHTTPServer:
    """Construct and bind a server without starting its request loop."""

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path == "/api/incidents":
                self._json(200, [asdict(item) for item in service.list()])
                return
            if self.path in {"/", "/index.html"}:
                self._file("index.html", "text/html; charset=utf-8")
                return
            if self.path == "/app.js":
                self._file("app.js", "text/javascript; charset=utf-8")
                return
            if self.path == "/styles.css":
                self._file("styles.css", "text/css; charset=utf-8")
                return
            self.send_error(404)

        def do_POST(self) -> None:
            if self.path != "/api/incidents":
                self.send_error(404)
                return
            try:
                payload = self._body()
                incident = service.create(payload["title"], payload["severity"])
            except (KeyError, ValueError, json.JSONDecodeError) as exc:
                self._json(400, {"error": str(exc)})
                return
            self._json(201, asdict(incident))

        def _body(self) -> dict:
            length = int(self.headers.get("Content-Length", "0"))
            return json.loads(self.rfile.read(length))

        def _file(self, name: str, content_type: str) -> None:
            body = (STATIC_DIR / name).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, value: object) -> None:
            body = json.dumps(value, default=json_value).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    return ThreadingHTTPServer((host, port), Handler)
