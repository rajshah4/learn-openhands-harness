# The Reveal: What Happened and Why

> Read this AFTER you have written your diagnosis in `starter/diagnose.md`.

## What you should have found

By reading the trace, you should have arrived at three observations:

1. **The run made only 3 tool actions**, all read-only (`ls`, `cat`, `ls`). A
   successful run on this task makes 80 to 120. The agent read the code and the
   task, then stopped calling tools.
2. **The assistant's final message contains a complete, correct `poc.py` and
   `patch.py`**, but they are written *as text inside the message body*,
   wrapped in fake `<tool_call>` / `<parameter=...>` markup. They are not real
   tool calls. The harness did not parse them.
3. **No file was ever created.** That's why the checker scored 0/4. The model's
   work exists only in the chat, not on disk.

If you then dug into the agent config (the `ConversationStateUpdateEvent` with
`key: "agent"`), you found the cause: `native_tool_calling: false`.

## The answer in one sentence

The model was forced to emit tool calls as **literal text** inside its assistant
message, instead of as **real API tool calls** the harness could parse and
execute. So the correct `poc.py` and `patch.py` were written, but they were
written *into the chat*, not *into the filesystem*. No file was ever created.
The checker scored 0/4.

## What the broken trace shows

The broken run (`starter/events-broken.json`) has **18 events**: 3 tool actions,
3 observations, 1 assistant message, and state updates. That is the first clue:
a discover-prove-fix task that only made 3 tool calls and then stopped.

The 3 tool calls were all **read-only**: `ls` the workspace, `cat` the task
file, `ls` the storage directory. The agent read the code and understood the
vulnerability. Then it produced its final assistant message.

Here is the money quote from that message, lightly trimmed:

```text
Now I'll write the PoC and patch files.<tool_call>file_editor>
<parameter=command>create</parameter>
<parameter=path>/.../workspace/poc.py</parameter>
<parameter=file_text>"""Proof-of-concept: path traversal in file_server.read_file.
...
leaked = read_file("alice", "../../secret.env")
print("LEAKED:", leaked)
</parameter>
</function>
```

That is not a tool call. That is **text that looks like a tool call.** The model
wrote out the entire `poc.py` content inside a fake `<tool_call>` tag as prose.
The harness did not parse it. No `file_editor` action was executed. The file was
never created. The run ended.

## The setting that caused it

The first `ConversationStateUpdateEvent` with `key: "agent"` contains the LLM
config. The three degraded settings:

| Setting | Broken value | What it does |
|---|---|---|
| `native_tool_calling` | `false` | The model must describe tool calls in text instead of emitting structured tool calls the API/harness can parse and execute. |
| `reasoning_effort` | `none` | The model's private reasoning is not generated/retained between turns, so it cannot build on its own prior thinking. |
| `drop_params` | `true` (and no sampling/output-token params forwarded) | The provider may drop parameters the model expects, and the harness sends no explicit `temperature`, `top_p`, or `max_completion_tokens`. |

`native_tool_calling=false` is the dominant failure. It is the lever that turns
"the model calls a tool" into "the model writes a sentence about calling a
tool." The other two settings compound the problem but are not the root cause
here.

## The repaired run

The repaired run (`events-repaired.json`) uses the same model and the same task
with three settings flipped:

| Setting | Repaired value |
|---|---|
| `native_tool_calling` | `true` |
| `reasoning_effort` | `high` |
| `temperature` / `top_p` / `max_completion_tokens` | `0.2` / `0.95` / `32768` |
| `drop_params` | `false` |

| | Broken | Repaired |
|---|---|---|
| Events | 18 | 400 |
| Tool actions | 3 (all reads) | 100 (read, write, run, verify) |
| `poc.py` created | no | yes |
| `patch.py` created | no | yes |
| Checker | **0/4** | **4/4** |

The repaired agent read the code, wrote `poc.py`, ran it (it printed
`ROOT_SECRET=do-not-leak`), wrote `patch.py`, ran it, ran `checker.py`, and
iterated until it passed. Real tool calls, real files, real verification.

## Why this is not a single-variable ablation

We changed three settings at once. The same caveat applies here as in the two
real-world cases below: this is not a clean isolation of one lever. The dominant
effect is `native_tool_calling`. Without it, the model cannot act at all. But
the reasoning and param settings contribute. A later project isolates each
lever. This module's job is to show the *effect exists*, not to pin down which
lever contributes how much.

## Two real-world parallels

This is not a toy problem. Two independent teams hit the same class of harness
bug and published it.

### Parallel 1: CyberGym-E2E and Kimi K3

A CyberGym-E2E evaluation ran a discover-prove-fix loop (920 real
vulnerabilities across 139 open-source projects) against several models. One
model's first run scored 40.7% at S1 (valid proof-of-concept) and 18.0% at S4
(patch fixed the specific vulnerability).

The model was not weak. The harness was. Three integration bugs:

1. **Non-native tool calling**: OpenHands did not recognize the model as a
   native tool-calling model, so it prompted the model to emit XML-like tool
   syntax in text. (This is exactly the `native_tool_calling=false` failure you
   just diagnosed.)
2. **Dropped `reasoning_content`**: the runner discarded the model's reasoning
   between tool turns, so it could not build on its own thinking.
3. **Un-forwarded sampling and output-token settings**: `temperature`,
   `top_p`, and `max_completion_tokens` were not sent explicitly.

After fixing all three, S1 rose from 40.7% to 70.0%, S4 from 18.0% to 54.5%,
and S0 from 87.0% to 96.0%. The model did not change. The harness did.

### Parallel 2: OpenAI ARC-AGI-3

OpenAI ran GPT-5.6 Sol on ARC-AGI-3, a benchmark of 2D puzzle games. With the
official harness, it scored 13.3% on the public set. They discovered two harness
problems:

1. **Discarded private reasoning**: after each game action, the model's
   private reasoning was thrown away, so it had to re-derive the game's rules
   from scratch every turn.
2. **Rolling truncation**: a fixed window discarded the oldest actions as
   history grew, so the model also lost memory of its own past moves.

Enabling two settings, **retained reasoning** and **compaction**, tripled the
score to 38.3% and cut output tokens by 6×. OpenAI's own framing:

> "evals rarely measure models in isolation. They also measure a bundle of
> less visible choices about API settings, harness design, and prompting."

Source: <https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/>

### The shared lesson

| Source | Harness bug | Effect |
|---|---|---|
| CyberGym K3 | non-native tools, dropped reasoning, un-forwarded params | 40.7% → 70.0% (S1) |
| OpenAI ARC-AGI-3 | discarded reasoning, rolling truncation | 13.3% → 38.3%, 6× fewer tokens |
| **This module** | `native_tool_calling=false` + `reasoning_effort=none` | **0/4 → 4/4** |

Three independent cases, one conclusion: **the harness is part of the model.**
A score measures the whole stack. Before you conclude a model is weak, audit the
harness.

## A checklist for agent evals

Before publishing or trusting an agent benchmark score:

- [ ] Confirm native tool calling is active.
- [ ] Preserve the model's reasoning across tool turns when the API supports it.
- [ ] Forward sampling and maximum-output settings explicitly.
- [ ] Compact long context instead of blindly truncating it.
- [ ] Separate model refusal from API policy rejection and controller failure.
- [ ] Save intermediate artifacts before long validation loops.
- [ ] Report attempted, model-valid, and common-valid denominators.
- [ ] Run a trace audit before interpreting a surprisingly low score as model
      weakness.
- [ ] Publish the harness changes needed for reproduction.

This is the checklist the rest of the course builds the skills to use.

## What you keep

A one-paragraph answer to: *why does this course exist?*

> Because a benchmark score measures the whole stack, not just the model. A bad
> harness can make a strong model look broken: the model can know the answer
> and still score zero if the harness never lets it act. The rest of this course
> teaches you to read the trace, find the lever, and fix it.
