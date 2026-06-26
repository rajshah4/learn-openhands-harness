# Deep Research Workflow Skill

Use this skill when a user asks for broad research where the right angles are not fully known until the question is inspected.

## When to use a dynamic workflow

Use a workflow when all of these are true:

- The question has 3 to 6 independent research angles.
- Parallel research can improve coverage or wall-clock time.
- Claims can be verified through sources, citations, or explicit stale-risk labels.
- A final synthesis step can combine findings without hiding uncertainty.

Do not use a workflow when the question is tiny, purely subjective, compliance-critical, or better represented by deterministic application code.

## Workflow shape

1. Read the user question and choose 4 to 6 research angles.
2. Use `web_searcher` sub-agents to research each angle.
3. Use `fact_checker` sub-agents to verify source quality, stale-risk claims, unsupported claims, and overbroad conclusions.
4. Use `synthesizer` to write the final report and workflow summary.
5. Preserve uncertainty from the verification step.

## Hard limits

- Do not read `.env` or print secret values.
- Prefer primary sources and cite URLs or exact document names.
- If web browsing or current search is unavailable, say so explicitly.
- Use at most 6 research angles.
- Do not invent sources.
- Do not convert unsupported claims into confident prose.

## Expected artifacts

Write these files under `.harness_workflow/dynamic/`:

- `DEEP_RESEARCH_REPORT.md`: the synthesized report.
- `WORKFLOW_SUMMARY.md`: the chosen angles, sub-agents used, evidence limits, and dynamic decisions.

## Suggested workflow API usage

Use the workflow tool's map/reduce pattern. Keep concurrency modest for LLM-heavy work:

```python
research = await wf.map_agents(
    items=research_angles,
    prompt="Research this angle with primary sources: {item}",
    subagent_type="web_searcher",
    max_concurrency=3,
)

verified = await wf.map_agents(
    items=research,
    prompt="Verify source quality and mark stale-risk claims: {item}",
    subagent_type="fact_checker",
    max_concurrency=3,
)

final_report = await wf.reduce_agent(
    items=verified,
    prompt="Synthesize into DEEP_RESEARCH_REPORT.md and WORKFLOW_SUMMARY.md.",
    subagent_type="synthesizer",
)
```

`wf.pipeline(...)` is also available when each item should move through the same stages without waiting for a global barrier. For this lesson, the explicit research map, verification map, and synthesis reduce are easier to inspect in the trace.

The model may choose the research angles, but it may not ignore the artifact contract or verification requirements.
