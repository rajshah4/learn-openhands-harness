"""P10 solution: reference index over agent history (SQLite FTS5).

`scan` (the baseline) is given in ../history_index.py. This file implements
the database approach: build a full-text index over extracted event text
once, then answer each query with a ranked top-K lookup.

Run:
    python starter/download_dataset.py     # once, downloads ./data
    python solution/run_search.py
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from history_index import (  # noqa: E402
    DATASET, DB_PATH, TOP_K, event_files, event_text, scan, report,
)

_CAMEL = re.compile(r"(?<=[a-z])(?=[A-Z])")


def build_index(dataset: Path = DATASET, db_path: Path = DB_PATH) -> tuple[float, int, int]:
    """One-time build. SQLite FTS5 over the extracted text of every event.

    Design choices made here:
      - Index `event_text()` (thoughts, commands, observation text), NOT the
        raw JSON, so a search for `error` never matches the `is_error` field.
      - porter + unicode61 tokenizer, plus a CamelCase-split copy of the body
        so `Traceback`/`NameError` match whether written as one token or two.
    """
    if db_path.exists():
        db_path.unlink()
    t0 = time.perf_counter()
    con = sqlite3.connect(db_path)
    con.execute(
        "CREATE VIRTUAL TABLE events USING fts5("
        "conv UNINDEXED, event UNINDEXED, body, "
        "tokenize='porter unicode61')"
    )
    rows = []
    for path in event_files(dataset):
        try:
            ev = json.loads(path.read_text())
        except Exception:
            continue
        text = event_text(ev)
        if not text.strip():
            continue
        text = text + "\n" + _CAMEL.sub(" ", text)
        rows.append((path.parent.name, path.name, text))
    con.executemany("INSERT INTO events(conv, event, body) VALUES (?,?,?)", rows)
    con.commit()
    con.close()
    return time.perf_counter() - t0, len(rows), db_path.stat().st_size


def _fts(query: str) -> str:
    """Multi-word inputs become a phrase query; single tokens stay bare."""
    cleaned = query.strip().replace('"', "")
    return f'"{cleaned}"' if " " in cleaned else cleaned


def indexed_search(query: str, dataset: Path = DATASET) -> dict:
    """Top-K ranked lookup over the FTS5 index. Returns ranked snippets:
    a bounded, relevance-ordered result, not every hit."""
    db_path = dataset.parent / "history.db"
    if not db_path.exists():
        build_index(dataset, db_path)
    con = sqlite3.connect(db_path)
    t0 = time.perf_counter()
    rows = con.execute(
        "SELECT conv, event, snippet(events, 2, '', '', ' ... ', 32) "
        "FROM events WHERE events MATCH ? ORDER BY rank LIMIT ?",
        (_fts(query), TOP_K),
    ).fetchall()
    elapsed = time.perf_counter() - t0
    con.close()
    returned = sum(len((c + e + s).encode("utf-8")) for c, e, s in rows)
    return {
        "name": "indexed_search",
        "matches": [(c, e) for c, e, _ in rows],
        "bytes": returned,
        "elapsed_s": elapsed,
    }


if __name__ == "__main__":
    elapsed, n, size = build_index()
    print(f"index build: {elapsed*1000:.0f} ms, {n} items, {size/1e6:.1f} MB\n")
    report([scan, indexed_search])
