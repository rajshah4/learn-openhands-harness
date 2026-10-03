"""Command line entry point for the starter application."""

from __future__ import annotations

import argparse

from .service import IncidentService
from .web import create_server


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    subcommands = result.add_subparsers(dest="command", required=True)
    serve = subcommands.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8080)
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "serve":
        server = create_server(IncidentService(), args.host, args.port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
