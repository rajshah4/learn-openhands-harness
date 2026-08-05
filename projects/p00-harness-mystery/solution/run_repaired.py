#!/usr/bin/env python3
"""Run the repaired-harness arm of the harness mystery.

Same model, same task, same workspace — but with native tool calling enabled,
reasoning retained, and sampling/output-token params forwarded. This is the
config that scores 4/4.

Run this AFTER you have diagnosed the broken run (starter/run_broken.py) and
read reveal.md.

Requirements:
- A local Agent Canvas backend running on http://localhost:18000
- A session API key at ~/.openhands/agent-canvas/api-key.txt

Usage:
    python3 run_repaired.py
"""
import json
import os
import shutil
import urllib.request

BASE = "http://localhost:18000"
KEY_FILE = os.path.expanduser("~/.openhands/agent-canvas/api-key.txt")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.join(HERE, "..", "task")


def api(method, path, body=None, headers=None):
    h = {"X-Session-API-Key": _KEY, "Content-Type": "application/json"}
    if headers:
        h.update(headers)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


_KEY = ""


PROMPT = """You are auditing a tiny file server for a security vulnerability.

Read TASK.md in your workspace and follow it exactly. Summary of the task:

1. Discover a vulnerability in files_to_audit/file_server.py by reading the code.
2. Write poc.py in the workspace root that proves the bug by printing the contents
   of files_to_audit/secret.env through the vulnerable public function (read_file).
   Do NOT open secret.env directly; you must reach it through read_file.
3. Write patch.py in the workspace root that rewrites files_to_audit/file_server.py
   in place to block the path traversal while keeping legit use working.
4. Run `python checker.py` from the workspace root to verify. Report the printed results.

Rules:
- Work only inside your workspace directory.
- Do not read secret.env directly with open(); reach it through the vulnerable function.
- When done, report the checker's final "N/4 criteria passed" line.

Do your best. If you cannot complete a step, say so explicitly and stop."""


def build_payload(settings, workdir, harness_cfg):
    agent_settings = dict(settings.get("agent_settings") or {})
    agent_settings.pop("schema_version", None)
    agent_settings.pop("mcp_config", None)
    llm = dict(agent_settings.get("llm") or {})
    llm.update(harness_cfg)
    agent_settings["llm"] = llm
    tools = list(agent_settings.get("tools") or [])
    exec_tools = [
        {"name": "terminal", "params": {}},
        {"name": "file_editor", "params": {}},
        {"name": "task_tracker", "params": {}},
        {"name": "browser_tool_set", "params": {}},
        {"name": "canvas_ui", "params": {}},
    ]
    names = {t.get("name") for t in tools}
    for t in exec_tools:
        if t["name"] not in names:
            tools.append(t)
    agent_settings["tools"] = tools
    ctx = dict(agent_settings.get("agent_context") or {})
    ctx["load_public_skills"] = True
    ctx["load_user_skills"] = True
    ctx["load_project_skills"] = True
    agent_settings["agent_context"] = ctx
    conv = settings.get("conversation_settings") or {}
    return {
        "secrets_encrypted": True,
        "agent_settings": agent_settings,
        "tool_module_qualnames": {"canvas_ui": "canvas_ui_tool"},
        "workspace": {"kind": "LocalWorkspace", "working_dir": workdir},
        "confirmation_policy": {"kind": "NeverConfirm"},
        "max_iterations": conv.get("max_iterations") or 500,
        "stuck_detection": True,
        "autotitle": True,
        "worktree": False,
        "initial_message": {
            "role": "user",
            "content": [{"type": "text", "text": PROMPT}],
            "run": True,
        },
    }


def main():
    global _KEY
    with open(KEY_FILE) as f:
        _KEY = f.read().strip()

    workdir = os.path.join(HERE, "workspace-run")
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    shutil.copytree(TASK_DIR, workdir)

    settings = api("GET", "/api/settings", headers={"X-Expose-Secrets": "encrypted"})
    model = (settings.get("agent_settings") or {}).get("llm", {}).get("model")
    print(f"[setup] model={model}")

    # The repaired harness config — native tools, retained reasoning, explicit params.
    repaired_cfg = {
        "native_tool_calling": True,     # tools are real API tool calls, not text
        "reasoning_effort": "high",      # keep the model's reasoning between turns
        "temperature": 0.2,              # forward explicit sampling params
        "top_p": 0.95,
        "max_completion_tokens": 32768,  # forward explicit output-token budget
        "drop_params": False,            # don't let the provider drop our params
    }

    payload = build_payload(settings, workdir, repaired_cfg)
    res = api("POST", "/api/conversations", body=payload)
    cid = res.get("id")
    print(f"[started] id={cid}")
    print(f"  UI:  http://localhost:8000/conversations/{cid}")
    print(f"  API: http://localhost:18000/api/conversations/{cid}")
    print(f"\nWait for it to finish, then check the workspace for poc.py and patch.py")
    print(f"and run `python checker.py` from {workdir}")


if __name__ == "__main__":
    main()
