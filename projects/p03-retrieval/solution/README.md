# Solution Brief: P03 Retrieval

## What This Solution Proves

This solution proves that retrieval tools have to earn their place in the harness. The reference answer does not assume MCP search is better because it is more advanced. It compares lexical search against lexical plus MCP on the same repo and asks whether the trace improved.

That is the core P03 lesson: a retrieval feature is useful only when it improves correctness, reduces misses, or shortens expensive wandering. If `grep`, `find`, and targeted file reads already solve the task cleanly, the right solution may be to leave MCP off by default.

## Start With These Files

| File | Why it matters |
|---|---|
| `run_retrieval.py` | Runs lexical-only and lexical-plus-MCP configs, then compares events, cost, wall-clock time, and `search_code` use. |
| `mcp_decision_rule.md` | The artifact to keep. It states when semantic/MCP search earns a default slot. |
| `../code_search_mcp.py` | The small stdio MCP server used by the experiment. |

Read the decision rule first if you want the harness policy. Read the runner and MCP server if you want to understand how the tool is attached.

## Key Design Choices

The solution keeps lexical search as the baseline. That matters because exact identifier queries are common in code-reading tasks, and exact tools are often faster and clearer than semantic tools.

The runner compares two prompt shapes:

- exact-symbol prompt: `VITE_BACKEND_HOST` and `VITE_BACKEND_BASE_URL`
- synonym prompt: "How does the canvas pick which backend to talk to?"

The synonym prompt is the stress test. It asks whether extra retrieval helps when the user's words do not match the code's words.

The solution also includes two cheap checks before spending real budget:

- `--mcp-smoke` tests the included server without model calls.
- `--mcp-live-smoke` verifies the remote Agent Server can launch the MCP subprocess and that the agent can call `search_code`.

## How OpenHands Fits In

OpenHands attaches the MCP server through the agent's `mcp_config`. The solution keeps the ordinary `terminal`, `file_editor`, and `task_tracker` tools, then adds the `search_code` tool through a stdio MCP server.

That setup makes the trace the deciding evidence. If `search_code` is available but never called, the model did not need or choose it. If it is called and improves the answer or avoids wandering, the harness has evidence to keep it.

## What To Compare Against Your Attempt

| Question | What to check |
|---|---|
| Did exact lexical search already solve the task? | Count searches, file reads, and correctness on the exact prompt. |
| Did MCP get used? | Check the `search_code` count, not just whether the tool was configured. |
| Did synonym search improve? | Compare the synonym prompt with and without MCP. |
| Did the tool earn its cost? | Look at correctness, events, wall-clock time, and cost together. |

If your result is "lexical only for now," that can be a correct P03 outcome. The point is to write the rule from evidence.

## Valid Variations

A valid solution might use an embeddings-backed MCP server, a different synonym prompt, or a repo-specific search tool. It might also attach MCP only for certain task families rather than globally.

Be careful with solutions that add retrieval because it feels sophisticated. P03 is successful when the trace tells you when the extra tool helps and when it is just another branch for the agent to explore.

## What To Keep

Keep a one-line retrieval policy. For example:

- exact identifier and file-path tasks stay lexical
- MCP search is enabled for vocabulary mismatch, cross-file concepts, or repeated lexical misses
- the policy changes only after trace comparisons show better correctness or lower cost

The reusable artifact is not the specific `code_search_mcp.py` implementation. It is the habit of treating retrieval as a measured harness lever.
