# Debugging the Run

Work through this from `events-broken.json` only. Do not read `solution/`
until you have written down your hypothesis in Step 5.

Think of this as a real incident: your colleague handed you the trace and asked
what happened. You have no idea yet. Build the picture from the evidence.

## Step 1: What did the run actually do?

Read the trace in order. Get a rough sense of the arc.

How many events are there total? How many are tool actions vs. observations vs.
assistant messages? Is this a lot or a little for a task that requires reading
code, writing two files, and running a checker?

> A successful discover-prove-fix run on this task makes roughly 80 to 120 tool
> actions. This one made far fewer. That's your first clue.

| Event kind | Count |
|---|---|
| ActionEvent | |
| ObservationEvent | |
| MessageEvent (assistant) | |

## Step 2: What tools did the agent actually call?

For each `ActionEvent`, look at the `tool_calls` array. What tool did the agent
invoke, and what did it do with it?

| # | Tool | What it did |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

Now the key question: did the agent ever call `file_editor` to create a file?
Did it ever run `checker.py`? Did it write `poc.py` or `patch.py` to disk?

> If the agent never called a tool to write a file, but the checker says
> `poc.py` and `patch.py` don't exist, that's consistent. The files were never
> created. So where did the solution go?

## Step 3: The assistant's final message

Find the `MessageEvent` with `role: assistant`. Read its content carefully.

This is the strangest part of the trace. The model's message contains a
`poc.py` and a `patch.py`. You can see the full code. But look at the
*format*. Is the model calling a tool, or is it writing text that *looks like*
a tool call?

> Look for markup like `<tool_call>` or `<parameter=...>` inside the assistant
> message. That is not a tool call. That is prose that describes a tool call.
> The harness does not parse it. No file gets created.

Answer these:

- Does the assistant message contain the code for `poc.py` and `patch.py`?
- Is that code inside a real tool call, or inside text in the message body?
- If the harness doesn't parse text-as-tool-call, what happens to that code?

## Step 4: The gap

You now have the core of the mystery. State it plainly:

> The model [did / did not] understand the vulnerability.
> The model [did / did not] produce a correct PoC and patch.
> That work [was / was not] saved to disk.
> The reason it was not saved is: ______

Fill in the blank. That's the gap between "the model knew the answer" and "the
checker scored 0/4."

## Step 5: Why did the harness do that?

You know *what* happened: the model wrote tool calls as text instead of as real
tool calls. Now figure out *why*.

The trace records the agent's configuration. Find the `ConversationStateUpdateEvent`
with `key: "agent"`. Its `value` is an object containing the `llm` config the
run used.

Look at that config. Ask yourself:

- Which of these settings would cause a model to emit tool calls as text rather
  than as structured tool calls?
- Which would cause the model to do less reasoning between turns?
- Are there parameters you would expect to see forwarded (`temperature`,
  `top_p`, `max_completion_tokens`) that are missing or null?

> You are now doing what the rest of this course teaches systematically:
> reading a config and asking which lever produced the behavior you saw in the
> trace.

## Your diagnosis

Write what you would tell your colleague:

> **What happened:**
>
> **Which harness setting caused it:**
>
> **What to change to fix it:**

Once you have written all three, open `../solution/reveal.md`.
