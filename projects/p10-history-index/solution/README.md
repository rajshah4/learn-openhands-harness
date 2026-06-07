# Solution Brief: P10 Indexing Agent History

## What This Solution Proves

This solution proves that for unbounded agent history, scanning is not a cheaper-but-slower option. Past a small corpus it stops being an option at all. It compares a substring scan against a SQLite FTS5 index on the same 28 conversations and the same three queries, and reports the tokens, cost, and latency of the result each approach would hand a model.

The core P10 lesson: raw event logs are cheap to produce and expensive to query. The fix is to give them structure once, so every query after that is a bounded, ranked, microsecond lookup instead of a linear re-read of everything the agent has ever done.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_search.py` | The reference index: `build_index()` (FTS5 over extracted text) and `indexed_search()` (ranked top-K). Run it for the offline comparison. |
| `measure_real_cost.py` | The real numbers: exact token counts and billed cost from the Anthropic API. |
| `../history_index.py` | Shared scaffolding: dataset loading, `event_text()`, the `scan()` baseline, and `report()`. |

## Key Design Choices

**Index extracted text, not raw JSON.** `build_index()` indexes the output of `event_text()` (thoughts, commands, observation text) and deliberately skips schema fields. That single choice is why a search for `error` doesn't match the `"is_error": false` boolean that sits in every observation event. On the scan side, **61% of the `error` hits are exactly that field**, noise the scan can't distinguish from a real error.

**Return ranked top-K, not every hit.** The scan returns all 621 `error` matches unranked. The index returns the 5 best by BM25. Ranking is the structural advantage; no scan optimization produces it.

**Tokenize for code.** A CamelCase-split copy of the body is indexed alongside the original, so `Traceback` and `NameError` match whether written as one token or two. Multi-word queries (`pip install`) become phrase matches.

## Reference Numbers

### Offline, free: what each approach returns (`python solution/run_search.py`)

| Query | scan (matches / bytes / time) | index (matches / bytes / time) | data reduction |
|---|---|---|---:|
| `error` | 621 / 4.9 MB / 55 ms | 5 / 1.8 KB / 0.6 ms | 2,762× |
| `pip install` | 73 / 881 KB / 48 ms | 5 / 1.9 KB / 0.2 ms | 471× |
| `Traceback` | 10 / 29 KB / 47 ms | 5 / 1.7 KB / 0.2 ms | 17× |

Index build is a one-time ~150 ms, 8.1 MB on disk. The scan re-reads all 1,064 files on every query (~50 ms); the index answers in microseconds.

### Real cost (`uv run --with anthropic python solution/measure_real_cost.py`)

Measured against `claude-sonnet-4-5` ($3/M in, $15/M out, 200 K context):

| Query | Approach | Real tokens | Real cost | Fits one call? |
|---|---|---:|---:|:--:|
| `error` | scan | 1,985,919 | $5.96\* | ❌ ~10× over |
| | **index** | 826 | **$0.0039** | ✅ |
| `pip install` | scan | 246,274 | $0.74\* | ❌ ~1.2× over |
| | **index** | 919 | **$0.0044** | ✅ |
| `Traceback` | scan | 10,890 | $0.0355 | ✅ |
| | **index** | 788 | **$0.0038** | ✅ |

\* Input-only. The payload exceeds the context window and cannot be sent in one call.

The two findings that matter:

1. For two of the three queries, the scan answer is not expensive, it is **impossible**. `error` returns about 2.0 M tokens (roughly 10× a 200 K window) and `pip install` 246 K (about 1.2× over). The index returns under 1,000 tokens every time and always fits.
2. On its best case (`Traceback`, the one scan that fits), the index is still about **9× cheaper**, $0.0038 versus $0.0355, while reading nothing but its own index.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Does your index beat scan on latency? | Microseconds vs ~50 ms. Easy win. |
| Does it return a *bounded, ranked* result? | Top-K, not every hit. This is the structural point. |
| Did you avoid the `is_error` trap? | Search `error`; if you get hundreds of matches, you indexed raw JSON, not extracted text. |
| Do `Traceback` and `pip install` both work? | Tests tokenization (CamelCase) and phrase matching. |

## Valid Variations

A valid solution might use DuckDB FTS, Whoosh, or a vector store (Chroma) for semantic rather than lexical match; index different fields; or store the index in-memory instead of on disk. The backend is not the lesson; the shape of the win is. Be skeptical of any design that re-reads the whole corpus per query, which is a scan wearing a different hat.

## What To Keep

A one-line policy: *unbounded append-only history that the agent queries every run gets an index. Scanning has no upper bound and routinely exceeds the context window. Index extracted text (not raw events), and return ranked top-K.* The reusable artifact is the habit of treating "scan vs. structure" as a measured harness decision, not the FTS5 code itself.
