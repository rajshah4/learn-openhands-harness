"""P10 solution: the real numbers, measured against the Anthropic API.

`run_search.py` gives fast, free, offline numbers (matches, bytes, latency).
This script gets the cost truth: real token counts from `count_tokens`, and
real billed cost from actual `messages.create` calls, for the result each
approach hands an agent.

For each query it builds the actual payload (the raw JSON of every matching
event for `scan`, the top-K ranked snippets for the index), then:
  - counts exact input tokens (chunked, so an oversized scan payload still
    yields a real total even though it could never be sent in one call), and
  - makes a real model call for payloads that fit the 200K context window.

Run:
    uv run --with anthropic python solution/measure_real_cost.py

Reads the API key from the nearest .env (ANTHROPIC_API_KEY).
"""
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from history_index import DATASET, DB_PATH, TOP_K, event_files, QUERIES  # noqa: E402
from run_search import _fts, build_index  # noqa: E402


def _load_env() -> None:
    root = Path(__file__).resolve()
    for d in [root.parent, *root.parents]:
        env = d / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip().replace("export ", ""),
                                          v.strip().strip("\"'"))
            return


_load_env()
import anthropic  # noqa: E402

MODEL = "claude-sonnet-4-5"
PRICE_IN = 3.00 / 1_000_000
PRICE_OUT = 15.00 / 1_000_000
CONTEXT_LIMIT = 200_000
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

INSTR = ("You are reviewing past agent session logs. From the material below, "
         "summarize the most relevant errors in 3-5 sentences.\n\n")


def scan_payload(query: str) -> list[str]:
    needle = query.lower()
    out = []
    for p in event_files(DATASET):
        raw = p.read_text(errors="ignore")
        if needle in raw.lower():
            out.append(f"### {p.parent.name}/{p.name}\n{raw}")
    return out


def db_payload(query: str) -> list[str]:
    if not DB_PATH.exists():
        build_index(DATASET, DB_PATH)
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT conv, event, snippet(events, 2, '', '', ' ... ', 32) "
        "FROM events WHERE events MATCH ? ORDER BY rank LIMIT ?",
        (_fts(query), TOP_K),
    ).fetchall()
    con.close()
    return [f"[{c}/{e}] {s}" for c, e, s in rows]


def count_chunked(parts: list[str], budget_chars: int = 300_000) -> int:
    total = 0
    chunk = ""
    for part in parts:
        if chunk and len(chunk) + len(part) > budget_chars:
            total += client.messages.count_tokens(
                model=MODEL, messages=[{"role": "user", "content": chunk}]).input_tokens
            chunk = ""
        chunk += part + "\n"
    if chunk:
        total += client.messages.count_tokens(
            model=MODEL, messages=[{"role": "user", "content": chunk}]).input_tokens
    return total


def real_call(payload: str) -> tuple[int, int]:
    r = client.messages.create(model=MODEL, max_tokens=400,
                               messages=[{"role": "user", "content": INSTR + payload}])
    return r.usage.input_tokens, r.usage.output_tokens


def main() -> None:
    print(f"Model: {MODEL}  |  ${PRICE_IN*1e6:.0f}/M in, ${PRICE_OUT*1e6:.0f}/M out  "
          f"|  context {CONTEXT_LIMIT:,}\n")
    for q in QUERIES:
        sp, dp = scan_payload(q), db_payload(q)
        s_tok = count_chunked(sp)
        if s_tok < CONTEXT_LIMIT - 2000:
            si, so = real_call("\n".join(sp))
            s_cost, s_note = si * PRICE_IN + so * PRICE_OUT, f"SENT (in {si:,}+out {so:,})"
        else:
            s_cost = s_tok * PRICE_IN
            s_note = f"EXCEEDS {CONTEXT_LIMIT//1000}K context, cannot send"
        di, do = real_call("\n".join(dp))
        d_cost = di * PRICE_IN + do * PRICE_OUT
        print(f"── {q!r} ──")
        print(f"  scan: {len(sp):>4} events | {s_tok:>10,} tok | ${s_cost:>8.4f} | {s_note}")
        print(f"  db  : {len(dp):>4} rows   | {di+do:>10,} tok | ${d_cost:>8.4f} | "
              f"SENT (in {di:,}+out {do:,})\n")


if __name__ == "__main__":
    main()
