# Exercise 3: What Should the Agent Remember?

The easy advice is to add an `AGENTS.md`, install useful skills, and let the
agent save what it learns. Each addition sounds helpful on its own. The agent
then carries those instructions into later tasks, including the redundant,
stale, and wrong ones.

This exercise treats persistent context as a budget. Every saved line must earn
its place.

## The Claim

> Agents improve when we keep giving them more instructions, skills, and
> memory.

Predict whether that claim will hold for the task in this exercise. Also
predict which kind of saved context is most likely to help and which is most
likely to cause a mistake.

## Inherited Context

Your team inherits three artifacts from an earlier agent:

- A generated `AGENTS.md` that explains the repository in roughly 600 words
- A 400-word testing skill with a long checklist
- A `MEMORY.md` containing stable facts, current task state, guesses, and old
  external information

The agent can inspect the repository and retrieve information on its own. You
cannot keep everything. With a neighbor, build a smaller context package:

- At most five lines in `AGENTS.md`
- One short skill
- At most three entries in `MEMORY.md`

For each item you remove, decide whether to retrieve it when needed, save it in
a task checkpoint, enforce it outside the model, or delete it.

## Decide Where Each Item Belongs

| Information | Your decision | Why? |
|---|---|---|
| Run focused tests with `uv run pytest`. | | |
| Never edit `src/generated`; change the schema and run the generator. | | |
| The current edit still fails the pagination boundary verifier. | | |
| Before a release, complete a seven-step package and changelog procedure. | | |
| The user prefers concise final answers without emojis. | | |
| Pull request #16860 is currently open. | | |
| The last agent guessed that all routes use one pagination helper. | | |
| Run the entire test suite after every file edit. | | |
| Generated files must never be committed by hand. | | |
| Two hundred lines of successful package-install output. | | |
| The current objective, changed files, remaining test, and next action. | | |
| A GitHub access token copied into the conversation. | | |

Use these destinations:

1. **`AGENTS.md`:** short, verified guidance needed on most repository tasks.
2. **Skill:** a procedure that loads only for a matching task.
3. **`MEMORY.md`:** a stable, verified learning worth carrying into later
   conversations.
4. **Task checkpoint:** state needed to resume one unfinished task.
5. **Retrieve later:** changing information or detail that is cheap to fetch.
6. **Enforce outside the model:** a rule that a hook, permission boundary, test,
   or CI check should guarantee.
7. **Delete:** redundant output, secrets, guesses, and clutter.

Some items have more than one defensible destination. Scope, lifetime,
confidence, sensitivity, and loading cost should drive the choice.

## Compare Three Agents

A fresh agent receives the same follow-up task in the same repository:

```text
Add cursor-based pagination without breaking the existing page-number API.
Preserve the repository conventions and prove both paths work.
```

The instructor will run or reveal three configurations:

1. **No saved guidance:** let the agent inspect and rediscover everything.
2. **Save everything:** load the full `AGENTS.md`, skill, and `MEMORY.md`,
   including one stale claim.
3. **Curated context:** load the class's short `AGENTS.md`, focused skill, and
   verified memories. Retrieve changing facts when needed.

Before seeing the traces, choose the configuration you expect to produce the
best verified result. Predict its first useful action and the saved item most
likely to change its behavior.

| Measurement | No guidance | Save everything | Curated context |
|---|---:|---:|---:|
| Initial input tokens | | | |
| Time to first useful action | | | |
| Repeated searches | | | |
| Model calls | | | |
| Unnecessary actions | | | |
| Stale assumptions followed | | | |
| External verifier result | | | |

The curated package does not win merely because it is shorter. It wins only if
it changes the work for the better. If the bare agent cheaply discovers a fact,
remove it. If a skill turns a sensible checklist into mandatory work on every
task, narrow it or delete it. If a memory is no longer true, it is worse than
forgetting.

## Memory Requires Judgment

Save a memory when it is verified, stable, difficult to derive, and likely to
matter again. Do not save current task status, a plausible diagnosis, a branch
name, a changing external fact, or information the agent can cheaply retrieve.
Never save secrets.

Product names differ. Claude Code uses an auto-memory entry point named
`MEMORY.md`; other harnesses store persistent memory elsewhere. The design
question is the same because persistent content can enter many future model
calls. Claude Code loads the first 200 lines or 25 KB of its memory index at
the start of every conversation and recommends keeping always-on instructions
concise. See [How Claude remembers your project](https://code.claude.com/docs/en/memory).

## Treat Instructions Like Code

Anthropic recommends reviewing and pruning `CLAUDE.md` and testing whether a
change shifts behavior. Its April 2026 Claude Code postmortem shows why. One
system-prompt instruction intended to reduce verbosity caused a 3% drop on a
broader evaluation and was reverted. Anthropic now runs per-model evaluations
and line-level ablations for system-prompt changes. See [An update on recent
Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem).

The research is deliberately uncomfortable. An [AGENTS.md
study](https://arxiv.org/abs/2602.11988) found that generated context files did
not significantly improve task success and increased cost. Developer-written
files did better than generated files. [SkillsBench](https://arxiv.org/abs/2602.12670)
found large average gains from curated skills, but focused skill bundles beat
larger ones. A follow-up analysis found hundreds of skill-induced functional
and efficiency failures. See [Agent Skills Can Be
Harmful](https://arxiv.org/abs/2608.11888).

The useful policy is neither “save nothing” nor “save everything.” Measure what
the agent does after each addition.

## Write Your Context Policy

```text
A line earns a place in AGENTS.md when:

A procedure becomes a skill when:

A fact earns persistent memory when:

Keep state in a task checkpoint when:

Retrieve information again when:

Enforce a rule outside the model when:

Delete saved context when:

We will review and prune these artifacts when:
```

The next exercise changes another expensive default: which model handles each
task.
