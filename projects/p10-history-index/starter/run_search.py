"""P10 starter: turn a pile of agent logs into something queryable.

The baseline (`scan`) is given in ../history_index.py: it reads every event
file and substring-matches. It works, and it gets slower and more expensive
with every session the agent has ever run.

Your job is the two functions below: build an index over the events, then
answer each query from the index instead of by scanning. Then run this file
to compare your index against the scan on matches, bytes returned, and latency.

Run:
    python starter/download_dataset.py     # once, downloads ./data
    python starter/run_search.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from history_index import (  # noqa: E402
    DATASET, DB_PATH, TOP_K, event_files, event_text, scan, report,
)


# ─── YOUR WORK ───────────────────────────────────────────────────────────────
def build_index(dataset: Path = DATASET, db_path: Path = DB_PATH) -> tuple[float, int, int]:
    """Build an index over the events so a query can return the top-K most
    relevant WITHOUT reading every file.

    Decisions to make (there's no single right answer):
      - Which fields do you index?  `event_text()` is a starting point you can tune.
      - Which backend?  SQLite FTS5 ships in the Python stdlib (`import sqlite3`,
        `CREATE VIRTUAL TABLE ... USING fts5(...)`). DuckDB FTS, Whoosh, or a
        vector store like Chroma also work.
      - How do you tokenize?  Will `Traceback` match? Will `pip install` match
        as a phrase? What happens to CamelCase identifiers?

    Return (elapsed_s, n_items_indexed, on_disk_bytes).
    """
    raise NotImplementedError("Build your index. See the README.")


def indexed_search(query: str, dataset: Path = DATASET) -> dict:
    """Answer `query` from your index, returning the top-K most relevant hits.

    Contract (so report() can compare it to scan):
      {
        "name":      "indexed_search",
        "matches":   list[(conv_dir: str, event_file: str)],  # rank order, <= TOP_K
        "bytes":     int,    # size of what you'd hand back to the model (snippets)
        "elapsed_s": float,  # search wall time, NOT index-build time
      }

    The structural win over scan is *ranking*: return the K best, not all hits.
    """
    raise NotImplementedError("Implement indexed_search. See the README.")


# ─── Run the comparison ──────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        elapsed, n, size = build_index()
        print(f"index build: {elapsed*1000:.0f} ms, {n} items, {size/1e6:.1f} MB\n")
    except NotImplementedError as e:
        print(f"[build_index not implemented yet] {e}\n")
    report([scan, indexed_search])
