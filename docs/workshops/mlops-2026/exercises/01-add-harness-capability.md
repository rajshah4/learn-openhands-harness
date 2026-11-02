# Exercise 2: Do You Need an MCP?

The usual move is to connect an MCP server when an agent needs another
system. We will start there. Then we will remove the MCP server and see what
the agent can do through the terminal and the same system's API.

Keep the model, prompt, workspace, system instructions, and verifier fixed.
Change only how the agent reaches GitHub.

## Start With GitHub MCP

Give the agent this task:

```text
Inspect OpenHands/OpenHands pull request #16860. Explain what changed,
identify the important files, and report what validation was added. Cite
GitHub evidence for every claim.
```

The first configuration includes the Agent Canvas baseline tools plus GitHub
MCP:

- `terminal`
- `file_editor`
- `task_tracker`
- GitHub MCP tools

Before the run, inspect the available GitHub operations. With a neighbor,
predict the first operation, how many GitHub tools the agent will use, and
which evidence it must collect. Then run the task and follow the trace from
the first tool choice through the final citations.

MCP should look useful. It gives the agent named GitHub operations, typed
parameters, structured results, and an established authentication path. The
question is what the harness paid for those benefits.

Record how many GitHub tools were visible, how many the agent used, whether it
made selection or parameter errors, and how much data came back. When
provider-reported usage is available, record the initial input and total input
tokens. Tool definitions and tool results both consume context, but at
different points in the run.

## Wait, the Terminal Was Already There

Start a fresh conversation and remove GitHub MCP. Keep the prompt and all
other conditions unchanged. Leave the GitHub CLI installed and authenticated.
Do not tell the agent which command to run.

The terminal appears to be one tool, but it exposes Git, repository search,
test runners, package managers, command-line applications, and HTTP APIs. For
this task, the agent can discover GitHub through commands such as `gh help`
and `gh api`. It can also filter the response before returning it to the
model.

Before the second run, predict whether the agent will find the API, how much
time it will spend discovering commands, and whether its final evidence will
be better or worse. Then compare the two traces.

| Measurement | GitHub MCP | Terminal and API |
|---|---:|---:|
| Authentication passed preflight | | |
| Model-visible tool definitions | | |
| Initial input tokens | | |
| Model calls | | |
| Tool calls | | |
| Failed calls | | |
| Time to first useful evidence | | |
| Wall time | | |
| Evidence correct | | |
| Citations complete | | |

Do not assume either lane should win. MCP may reduce command discovery and
parameter mistakes. The terminal may provide the same capability through one
compact, composable interface. Similar final answers would shift the decision
to reliability, security, context, and maintenance rather than raw
capability.

## Decide What Earns a Tool

Complete the rules from the evidence:

```text
Use the terminal or API when:

Add an MCP connection when:

Load an MCP tool by default when:

Make an MCP tool discoverable on demand when:

Block or require approval when:

The evidence that would change our choice is:
```

The terminal is not a small capability surface merely because the model sees
one schema. It gives the agent a large implicit action space. MCP can make one
part of that space easier to discover, safer, and more reliable, but it also
adds definitions, permissions, and another integration to maintain.

## Retrieval Beyond the Workshop

This live comparison uses GitHub retrieval because the result is easy to
inspect and verify. The same design choice appears inside a codebase.

The full [P03 Retrieval lesson](/projects/p03-retrieval) compares lexical
search through the terminal with a dedicated `search_code` MCP tool. Exact
symbols often favor `rg`; conceptual questions create a better test for
specialized search. The optional GitNexus example goes further by retrieving
code relationships for architecture and change-impact questions. Students can
run those longer comparisons after the workshop.

## Check the Tool Configuration

Before a new run, check GitHub MCP and terminal API authentication separately.
Record the Agent Canvas and Agent Server versions, which MCP definitions reach
the native OpenHands model, and which token fields are available in the trace.
An authentication failure does not tell us which tool design is better.
