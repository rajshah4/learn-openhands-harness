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

## Recommended workshop reveal

Use three lanes on the main slide:

1. **Broad catalog:** 17 visible tools, 123 seconds, 12 tool calls, 6/6.
2. **Terminal/API:** 5 visible tools, 101 seconds, 6 tool calls, 4/6.
3. **Task-shaped tool:** 6 visible tools, 72 seconds, 1 tool call, 6/6.

Keep the four-primitive-tool lane in the speaker notes or trace walkthrough. It
explains the mechanism: typed access alone did not help because the operations
were too low-level, so the agent repeatedly fetched individual files.

Suggested headline:

> One task-shaped tool beat both the terminal and a broad catalog.

Suggested debrief:

> Tool quality is an interface-design problem. Give the model the smallest
> action that returns enough bounded evidence to finish the task.

### One-shot delivery decision

Treat this as a teaching demonstration, not a live benchmark. Run the
task-shaped lane once in the room because its three confirmation runs were
both short and consistent. Show prepared trace snapshots for the terminal and
broad-catalog lanes so ordinary model variance cannot replace the lesson.

Reveal only three measures: elapsed time, tool calls, and evidence quality.
The important comparison is the path through the system:

```text
Broad catalog -> inspect -> inspect -> inspect -> inspect -> answer
Terminal      -> compose commands -> filter -> recover -> answer
Task-shaped   -> request evidence bundle -> answer
```

Show the task-shaped tool contract before asking for predictions. State that
it selects evidence through a general rule, not knowledge of this particular
pull request. Otherwise the result can look like a hard-coded answer rather
than an interface-design result.

The workshop should not teach that specialized tools always win. End with the
reversal case: unfamiliar, exploratory work often needs primitives or a
terminal. Task-shaped tools earn their place when the evidence workflow is
repeated, bounded, and stable enough to encode.

Recommended participant decision rule:

> Create a higher-level tool when it compresses a recurring evidence workflow
> into one bounded, reliable action. Retain primitives for exploration and
> exceptions.

## What the result supports

The strong claim, "connecting more tools creates a better agent," failed. The
broad lane exposed twelve real GitHub operations. The agent ignored the eight
extra operations and followed almost the same primitive sequence, while paying
for their schemas in every model request.

The opposite claim, "the terminal is always the most efficient interface," also
failed. The terminal had the smallest initial prompt, but its final answers
usually cited the PR or API endpoint globally rather than linking file-level
claims. The task-shaped tool made the desired evidence structure explicit and
returned direct citation URLs with the relevant content.

The narrower rule that survives is:

> Add a typed tool when it compresses a repeated evidence-gathering workflow
> into one bounded, reliable action. Keep lower-level tools for exploration and
> exceptions; do not make the model rebuild a predictable pipeline every run.

## Method and caveats

- Task: inspect `OpenHands/OpenHands` PR #16860, explain the change and
  validation, and cite GitHub evidence for every claim.
- Fixed: Claude Sonnet 4.6 at high reasoning, OpenHands Agent Server 1.42.1,
  identical prompt, empty local Git repository, no saved skills, no repair
  round, and anonymous read-only access to GitHub's public REST API.
- The primitive and terminal trials ran first; the broad and task-shaped trials
  ran in a second same-day block. This is adequate for a preliminary workshop
  result, but a publishable comparison should interleave all four conditions.
- The final task-shaped result is bounded to 30K characters and uses a general
  PR evidence recipe rather than hard-coded facts about PR #16860. It selects
  the three largest production changes and two largest test changes. A separate
  three-trial rerun confirmed the result after removing topic-specific filename
  selection from the first prototype.
- The rubric checks the allow-list explanation, important files, test coverage,
  PR citation, citation count, and file/commit citation. It is a presentation
  aid, not a semantic judge.
- The terminal is one visible schema but a large implicit capability surface.
  A terminal action can make and filter multiple HTTP requests, so raw tool-call
  counts do not represent equal amounts of work.
- This run does not test authentication quality. Every lane used anonymous
  public access. A workshop claim about OAuth or credential handling needs a
  separate authenticated preflight.
- Provider cost was absent from the common ledger and is intentionally reported
  as unavailable rather than estimated.

## Evidence

- Initial raw result: `results/raw/generated/workshop2-prelim-20260905-github-tool-surface.json`
- Tool-shape raw result: `results/raw/generated/workshop2-tool-shape-20260905-github-tool-surface.json`
- Generic task-shaped confirmation: `results/raw/generated/workshop2-task-shaped-general-20260905-github-tool-surface.json`
- Provider ledgers: `results/provider-ledgers/20260905-workshop2-prelim-ledger.jsonl`, `results/provider-ledgers/20260905-workshop2-tool-shape-ledger.jsonl`, and `results/provider-ledgers/20260905-workshop2-task-shaped-general-ledger.jsonl`
- Complete traces: `results/traces/github-tool-surface/`
- Reproducible runner and MCP server: `experiments/github-tool-surface/`
