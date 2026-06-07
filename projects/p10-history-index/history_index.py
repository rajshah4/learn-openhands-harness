"""
Shared scaffolding for P10, searching a pile of past agent history.

Given to you:
  - dataset loading over the OpenHands V1 event-log format
  - event_text(), which pulls the meaningful text out of one event
  - scan(), the naive baseline: read every event, substring-match
  - report(), which runs a set of approaches over the queries and prints
    matches, bytes returned, and search latency so you can compare

These are all real, free, offline measurements. Dollar cost and token counts
come from solution/measure_real_cost.py, which calls the model directly.

Your job (in run_search.py) is build_index() and indexed_search(): turn this
pile of files into something queryable.
"""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent

# The dataset lives in ./data after `python starter/download_dataset.py`.
# Override with DATASET=/some/dir for a different corpus of
# conversation_*/event_*.json files.
DATASET = Path(os.environ.get("DATASET", PROJECT / "data"))
DB_PATH = DATASET.parent / "history.db"   # where your index gets written

QUERIES = ["error", "pip install", "Traceback"]
TOP_K = 5


def event_files(dataset: Path = DATASET) -> list[Path]:
    """Every event JSON across every conversation, in order."""
    files: list[Path] = []
    for conv in sorted(dataset.iterdir()):
        if not conv.is_dir() or conv.name.startswith("_"):
            continue
        files.extend(sorted(conv.glob("event_*.json")))
    return files


# ─── What's in an event (OpenHands V1 schema) ───────────────────────────────
_CAMEL = re.compile(r"(?<=[a-z])(?=[A-Z])")


def event_text(ev: dict) -> str:
    """Pull the human/agent-meaningful text out of one V1 event.

    This is a design decision, not a fixed fact. What you index determines
    both what your search can find and how clean the results are. (Try adding
    the is_error boolean here and watch precision collapse.)
    """
    parts: list[str] = []

    def add(v):
        if isinstance(v, str) and v.strip():
            parts.append(v)

    add(ev.get("thought"))
    add(ev.get("system_prompt"))
    add(ev.get("message"))
    action = ev.get("action")
    if isinstance(action, dict):
        for k in ("command", "code", "content", "path", "thought"):
            add(action.get(k))
    elif isinstance(action, str):
        add(action)
    tc = ev.get("tool_call")
    if isinstance(tc, dict):
        add(json.dumps(tc.get("function", tc), default=str))

    obs = ev.get("observation")
    if isinstance(obs, dict):
        content = obs.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    add(block.get("text"))
        add(obs.get("command"))
        add(obs.get("path"))
    elif isinstance(obs, str):
        add(obs)

    return "\n".join(parts)


# ─── The baseline: scan everything (given) ──────────────────────────────────
def scan(query: str, dataset: Path = DATASET) -> dict:
    """Read every event JSON, substring-match the raw text, return every hit
    in full. Correct, simple, and O(corpus) on every query."""
    needle = query.lower()
    matches: list[tuple[str, str]] = []
    matched_bytes = 0
    t0 = time.perf_counter()
    for path in event_files(dataset):
        raw = path.read_text(errors="ignore")
        if needle in raw.lower():
            matches.append((path.parent.name, path.name))
            matched_bytes += len(raw.encode("utf-8"))
    return {
        "name": "scan",
        "matches": matches,
        "bytes": matched_bytes,
        "elapsed_s": time.perf_counter() - t0,
    }


# ─── Reporting helpers ──────────────────────────────────────────────────────
def _fmt_t(s: float) -> str:
    if s < 1e-3:
        return f"{s*1e6:.0f} µs"
    if s < 1.0:
        return f"{s*1e3:.1f} ms"
    return f"{s:.2f} s"


def _fmt_bytes(n: int) -> str:
    if n >= 1e6:
        return f"{n/1e6:.1f} MB"
    if n >= 1e3:
        return f"{n/1e3:.1f} KB"
    return f"{n} B"


def report(approaches: list, dataset: Path = DATASET, queries: list[str] = QUERIES) -> None:
    """Run each approach over each query and print matches, bytes returned, and
    latency. All free and offline. An approach that raises NotImplementedError
    is reported as a TODO so the baseline still runs.
    """
    n_conv = len({p.parent.name for p in event_files(dataset)})
    print(f"Dataset: {dataset}  ({n_conv} conversations)\n")
    print(f"{'Query':<14}{'Approach':<16}{'Matches':>9}{'Bytes back':>12}{'Time':>10}")
    print("-" * 61)
    for q in queries:
        rows = {}
        for fn in approaches:
            try:
                r = fn(q, dataset)
            except NotImplementedError:
                print(f"{q:<14}{getattr(fn,'__name__','?'):<16}"
                      f"{'(not implemented yet, your turn)':>30}")
                continue
            rows[r["name"]] = r
            print(f"{q:<14}{r['name']:<16}{len(r['matches']):>9}"
                  f"{_fmt_bytes(r['bytes']):>12}{_fmt_t(r['elapsed_s']):>10}")
        if "scan" in rows and len(rows) > 1:
            for name, r in rows.items():
                if name == "scan" or r["bytes"] == 0:
                    continue
                ratio = rows["scan"]["bytes"] / r["bytes"]
                print(f"{'':<14}{'scan vs '+name:<16}{'':>9}"
                      f"{str(round(ratio)) + '× less':>12}{'data back':>10}")
        print("-" * 61)
