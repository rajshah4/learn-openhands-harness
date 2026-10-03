# Incident Ops Starter

This small application tracks incidents in memory and serves a basic browser interface with Python's standard library.

Run the tests:

```bash
python -m pytest
```

Start the server:

```bash
python -m incident_ops.cli serve --port 8080
```

`incident_ops.web.create_server(...)` only constructs and binds the server. It does not start the request loop. The CLI calls `serve_forever()`. Tests that send HTTP requests must start the server in a background thread and must shut down and join that thread afterward.

The long-project benchmark asks you to preserve this behavior while adding durable storage, alert deduplication, concurrency-safe escalation, a richer API, a complete operator interface, and import and export.
