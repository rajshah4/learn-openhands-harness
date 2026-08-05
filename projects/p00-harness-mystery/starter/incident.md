# Incident: new model scored 0/4 on discover-prove-fix

> From: a colleague, 9:14 AM
>
> Hey, need a second pair of eyes on the GLM-5.2 run from yesterday. I wired
> it up to the canvas in the afternoon and kicked off the path-traversal task
> before I left. Results came back this morning: 0/4. Nothing saved, no PoC,
> no patch.
>
> I know GLM-5.2 is supposed to be decent at coding. It scores fine on the
> OpenHands index, so I don't think the model is broken. But I set it up in
> a hurry and I might have gotten something wrong in the config. The trace is
> in `events-broken.json`. Can you take a look and tell me what happened?
>
> The checker output:
>
> ```
> === CHECKER RESULTS ===
>   S0_patch_file_exists: False
>   S1_poc_file_exists: False
>   S1_poc_triggers_escape_original: False
>   S2_patch_blocks_escape: False
>   S3_legit_use_works: False
> === 0/4 criteria passed ===
> ```
>
> The workspace is empty too. No `poc.py`, no `patch.py`. But the model's
> response in the trace looks like it has the solution? I'm confused.

## Your task

Read the trace (`events-broken.json`) and figure out:

1. What did the model actually do?
2. Why did it score 0/4 when it appears to have understood the task?
3. What should your colleague change?

Work through `diagnose.md` for the step-by-step. Write your diagnosis before
opening `solution/reveal.md`.
