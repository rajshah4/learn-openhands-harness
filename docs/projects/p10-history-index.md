# P10: Indexing Agent History

## What You Do

Search a pile of past agent session logs two ways: scan every event file, then build a database/index. Measure the data returned, latency, token counts, and real cost of each, and see where the scan stops fitting in the model's context window at all.

## Harness Mechanism

A naive substring scan over the raw event log vs. a SQLite FTS5 index over extracted event text, returning ranked top-K. Real token counts and billed cost come from the Anthropic API.

## Open First

- [`projects/p10-history-index/README.md`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p10-history-index/README.md)
- [`starter/download_dataset.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p10-history-index/starter/download_dataset.py)
- [`starter/run_search.py`](https://github.com/rajshah4/learn-openhands-harness/blob/main/projects/p10-history-index/starter/run_search.py)
- [`solution/`](https://github.com/rajshah4/learn-openhands-harness/tree/main/projects/p10-history-index/solution)

## Keep

A one-line policy on when agent history needs an index.

The main lesson: unbounded history that the agent queries every run has no upper bound when scanned and routinely exceeds the context window. Index extracted text, not raw events, and return ranked top-K.
