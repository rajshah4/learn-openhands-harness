# Workshop 2 preliminary result: tool shape beats tool count

## Slide-ready result

The strongest result is not MCP versus terminal. It is that one task-shaped
tool beat both a broad tool catalog and lower-level primitives while producing
the most reliable evidence.

| Median across 3 fresh trials | Terminal + API | 4 primitive MCP tools | 12-tool GitHub MCP | 1 task-shaped MCP tool |
|---|---:|---:|---:|---:|
| Evidence rubric, maximum 6 | 4 | 6 | 6 | 6 |
| Strict rubric passes | 0/3 | 2/3 | 3/3 | 3/3 |
| GitHub citations | 2 | 22 | 18 | 17 |
| Wall time | 101.1s | 131.6s | 123.2s | **72.4s** |
| Model calls | 5 | 4 | 4 | **2** |
| Tool calls | 6 | 11 | 12 | **1** |
| Fresh input across run | 32,006 | 42,800 | 48,741 | **18,706** |
| Processed tokens | 107,827 | 110,935 | 113,355 | **30,895** |
| Output tokens | 5,141 | 7,590 | 7,093 | **3,443** |
| Initial provider input | 8,541 | 9,342 | 10,889 | 8,745 |
| Model-visible tools | 5 | 9 | 17 | 6 |
| Tool-definition payload | 17,037 B | 19,876 B | 25,394 B | 17,756 B |
| Time to first useful evidence | 5.85s | 6.38s | 6.78s | **5.10s** |
| Failed tool/provider calls | 0 | 0 | 0 | 0 |

Compared with terminal/API, the task-shaped tool:

- preserved the full 6/6 evidence score in all three trials;
- finished 28% faster;
- used 60% fewer model calls and 83% fewer tool calls;
- used 42% less fresh input and 71% fewer processed tokens;
- produced 8.5 times the median number of GitHub citations.

Compared with the four primitive MCP tools, the task-shaped tool finished 45%
faster and used 72% fewer processed tokens. It removed the trace's 8–11
one-file-at-a-time retrieval calls by returning PR metadata, file summaries,
selected patches, commit summaries, validation evidence, and citable URLs in
one bounded result.

