# P10: Indexing Agent History

## What Problem Are You Solving?

An agent produces an enormous amount of unstructured data just by running. Every turn is more event JSON on disk. The moment the harness wants to *reuse* that history, it has to answer questions like "have I hit this error before?" or "which past session set this up the way I need now?" There are only two ways to answer them over a pile of event logs.

The problem in this lesson is to test, empirically, which one to include in your harness. You will run the same three queries two ways over the same corpus of past sessions:

1. **Scan everything.** Read every event file, substring-match, hand back the hits. No setup. This is the control group.
2. **Build a database/index.** Load the event text into an index once, then answer each query with a ranked top-K lookup.

The comparison is not just speed. The headline metric is the **cost and token size of the result the model has to consume**, alongside search latency and the number that decides it: whether the result fits in the model's context window at all.

## Start With These Files

This project has starter code and a completed solution. Start with the starter when teaching the lesson, then use the solution to compare the intended design. After you attempt the starter, read `solution/README.md` for the solution brief.

| Purpose | Starter | Solution |
|---|---|---|
| Download the corpus into `./data` | `starter/download_dataset.py` | same |
| Scan baseline + your index | `starter/run_search.py` | `solution/run_search.py` |
| Real billed cost from the API | | `solution/measure_real_cost.py` |
| Shared scaffolding (loading, `scan()`, `report()`) | `history_index.py` | same |

The benchmark reads the dataset from `./data`, extracts event text in `history_index.py`, and prints a tokens/cost/latency table with `report()`. The scan baseline is given. Your job is `build_index()` and `indexed_search()` in `starter/run_search.py`.

This lesson is the counterpart to [P03: Retrieval](../p03-retrieval/). P03 asks *whether* to add a search tool over a bounded codebase, and the answer is often "no, `grep` wins."

P10 is the case where you don't have that choice. History is unbounded and grows with every run, so a scan has no upper bound. While you could use BM25, the type of data across various fields leans toward another approach. The big hint is to try a database/index and you will see the difference for yourself.

## The Corpus And The Queries

The dataset is [`rajistics/openhands-synthetic-conversations`](https://huggingface.co/datasets/rajistics/openhands-synthetic-conversations): 28 real OpenHands agent conversations, 1,064 events, about 7.6 MB. Each conversation is a coding task run end to end, stored in the V1 event-log format OpenHands Cloud exports. It is a realistic stand-in for "my agent's history," and 28 conversations is deliberately the toy size. The lesson is what happens when you 10×, 100×, 1000× it.

The three queries each stress a different design decision:

| Query | Type | What it tests |
|---|---|---|
| `error` | Common keyword, hundreds of hits | **Ranking and precision.** Every approach returns hits; can yours return the few that matter, without matching schema noise? |
| `pip install` | Multi-word phrase | **Phrase matching.** A naive tokenizer matches `pip` and `install` separately. |
| `Traceback` | Rare CamelCase identifier | **Tokenization.** Many tokenizers split `Traceback` and miss the exact term. |

Before you build anything, make a prediction. Which query will the scan struggle with most? Will `error` and `Error` return the same hits in your index? Should `pip install` match an event that contains only one of the two words? The results table means more once you have written down what you expect.

## Start With The Baseline, Then Build The Index

The scan is the baseline. It answers: what does it cost to just read everything every time? It is given to you in `history_index.py`:

```python
def scan(query, dataset):
    needle = query.lower()
    for path in event_files(dataset):
        raw = path.read_text(errors="ignore")
        if needle in raw.lower():
            matches.append((path.parent.name, path.name))  # return the whole event
```

It is correct and simple, and it has two structural problems that get worse with every session the agent runs. It returns *every* hit in full, and it has no notion of structure: searching the raw JSON for `error` also matches the `"is_error": false` field in every observation event.

The index is the design, and the decisions are yours: what to index, which backend, how to tokenize. There are many possible good solutions. Implement `build_index()` and `indexed_search()` in `starter/run_search.py`, then run the benchmark and compare against the scan.

## Why This Is Harness Engineering

The shape of your event log determines the cost of every downstream consumer, forever. A scan-everything answer leaks that cost into the LLM context and into the user's wait time, and it grows linearly with everything the agent has ever done. An index pays the cost once at build time and hands the agent a tool it can call as cheaply as `grep`. Wrapped as a `search_history` tool, the index is something the agent can call three times in a single turn without anyone noticing. Three scans of the full history would be three multi-second, multi-megabyte stalls.

## Run It And Collect Metrics

Download the corpus once:

```bash
pip install huggingface_hub
python starter/download_dataset.py        # writes ./data
```

Run the offline comparison as often as you like while you tune. It is free and reproducible, and reports matches, bytes returned, and latency for each approach:

```bash
python starter/run_search.py              # scan + your index
python solution/run_search.py             # scan + the reference index
```

Then get the token counts and real cost. `ANTHROPIC_API_KEY` is read from the nearest `.env`:

```bash
uv run --with anthropic python solution/measure_real_cost.py
```

`measure_real_cost.py` builds the actual result each approach hands a model (the raw JSON of every matching event for the scan, the top-K snippets for the index) and reports exact token counts from `count_tokens` plus the billed cost of a real `claude-sonnet-4-5` call. Oversized scan payloads are counted in chunks so the total is exact even though the call can never be made.

## Record The Results

Fill these in from your own runs. Reference numbers are in `solution/README.md`.

Offline comparison (`run_search.py`):

| Query | scan matches | scan bytes | index bytes | data reduction |
|---|---:|---:|---:|---:|
| `error` | | | | |
| `pip install` | | | | |
| `Traceback` | | | | |

Token counts and real cost (`measure_real_cost.py`):

| Query | scan tokens | scan cost | fits one call? | index tokens | index cost |
|---|---:|---:|:--:|---:|---:|
| `error` | | | | | |
| `pip install` | | | | | |
| `Traceback` | | | | | |

Watch for two things. For most queries the scan result does not fit the model's context window at all, so it cannot be sent in one call regardless of price. And even on the one query whose scan result does fit, the index is still meaningfully cheaper. Label demo numbers as "measured on this corpus, your mileage varies." The costs come from real token counts and configured pricing, not per-query guesses.

<details>
<summary>References</summary>

- [SQLite FTS5](https://www.sqlite.org/fts5.html): a full-text index that ships in the Python standard library, including the `bm25()` ranking function and tokenizer options.
- [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25): the relevance ranking behind FTS5's `rank`.
- [`rajistics/openhands-synthetic-conversations`](https://huggingface.co/datasets/rajistics/openhands-synthetic-conversations): the dataset and its V1 event-log schema.
- [Anthropic token counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting): how `measure_real_cost.py` gets exact input-token totals.

</details>

## What Students Should Leave With

A one-line policy on when agent history needs an index, defensible with the numbers you recorded:

- Unbounded, append-only history that the agent queries every run gets an index. Scanning has no upper bound and routinely exceeds the context window.
- Index extracted text, not raw events, so search matches content and not schema fields.
- Return ranked top-K, because the structural win is bounded, relevant results.

The reusable artifact is not the index code. It is the habit of treating "scan vs. structure" as a measured harness decision.

Counterpart retrieval lesson: [P03: Retrieval](../p03-retrieval/)
