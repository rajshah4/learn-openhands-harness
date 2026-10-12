#!/usr/bin/env python3
"""Small read-only GitHub MCP server for the Workshop 2 comparison."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request

from fastmcp import FastMCP


API_ROOT = "https://api.github.com"
USER_AGENT = "odsc-workshop-tool-surface/1.0"

MODE = os.environ.get("WORKSHOP_MCP_MODE", "primitive")

mcp = FastMCP(
    "github-pr-evidence",
    instructions=(
        "Read public GitHub pull-request evidence. Every result includes a GitHub URL "
        "that can be cited in the final answer. This server is read-only."
    ),
)


def github_get(path: str) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"{API_ROOT}{path}",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        if token:
            detail = detail.replace(token, "[redacted]")
        detail = detail[:1000]
        raise RuntimeError(f"GitHub API returned HTTP {error.code}: {detail}") from error


def get_pull_request(owner: str, repo: str, pull_number: int) -> dict:
    """Get a pull request's title, description, status, counts, branches, and citation URL."""
    item = github_get(f"/repos/{owner}/{repo}/pulls/{pull_number}")
    assert isinstance(item, dict)
    return {
        "number": item.get("number"),
        "title": item.get("title"),
        "body": item.get("body"),
        "state": item.get("state"),
        "merged_at": item.get("merged_at"),
        "html_url": item.get("html_url"),
        "base": (item.get("base") or {}).get("ref"),
        "head": (item.get("head") or {}).get("ref"),
        "changed_files": item.get("changed_files"),
        "commits": item.get("commits"),
        "additions": item.get("additions"),
        "deletions": item.get("deletions"),
    }


def list_pull_request_files(owner: str, repo: str, pull_number: int) -> list[dict]:
    """List every changed file with change counts and a directly citable GitHub blob URL."""
    items = github_get(
        f"/repos/{owner}/{repo}/pulls/{pull_number}/files?per_page=100"
    )
    assert isinstance(items, list)
    return [
        {
            "filename": item.get("filename"),
            "status": item.get("status"),
            "additions": item.get("additions"),
            "deletions": item.get("deletions"),
            "changes": item.get("changes"),
            "blob_url": item.get("blob_url"),
        }
        for item in items
    ]


def list_pull_request_commits(owner: str, repo: str, pull_number: int) -> list[dict]:
    """List pull-request commits with their messages and directly citable GitHub URLs."""
    items = github_get(
        f"/repos/{owner}/{repo}/pulls/{pull_number}/commits?per_page=100"
    )
    assert isinstance(items, list)
    return [
        {
            "sha": item.get("sha"),
            "message": (item.get("commit") or {}).get("message"),
            "html_url": item.get("html_url"),
        }
        for item in items
    ]


def get_file_at_revision(owner: str, repo: str, path: str, revision: str) -> dict:
    """Read one UTF-8 text file at a revision and return its content and citation URL."""
    quoted_path = urllib.parse.quote(path, safe="/")
    item = github_get(f"/repos/{owner}/{repo}/contents/{quoted_path}?ref={revision}")
    assert isinstance(item, dict)
    import base64

    raw = base64.b64decode(item.get("content") or b"").decode(
        "utf-8", errors="replace"
    )
    return {
        "path": item.get("path"),
        "sha": item.get("sha"),
        "content": raw[:30000],
        "truncated": len(raw) > 30000,
        "html_url": item.get("html_url"),
    }


def get_repository(owner: str, repo: str) -> dict:
    """Get repository metadata, default branch, topics, and its citation URL."""
    item = github_get(f"/repos/{owner}/{repo}")
    assert isinstance(item, dict)
    return {
        "full_name": item.get("full_name"),
        "description": item.get("description"),
        "default_branch": item.get("default_branch"),
        "topics": item.get("topics"),
        "html_url": item.get("html_url"),
    }


def get_issue(owner: str, repo: str, issue_number: int) -> dict:
    """Get a GitHub issue or pull request's title, description, state, labels, and URL."""
    item = github_get(f"/repos/{owner}/{repo}/issues/{issue_number}")
    assert isinstance(item, dict)
    return {
        "number": item.get("number"),
        "title": item.get("title"),
        "body": item.get("body"),
        "state": item.get("state"),
        "labels": [label.get("name") for label in item.get("labels") or []],
        "html_url": item.get("html_url"),
    }


def list_issue_comments(owner: str, repo: str, issue_number: int) -> list[dict]:
    """List issue or pull-request discussion comments with author and citation URL."""
    items = github_get(
        f"/repos/{owner}/{repo}/issues/{issue_number}/comments?per_page=100"
    )
    assert isinstance(items, list)
    return [
        {
            "author": (item.get("user") or {}).get("login"),
            "body": item.get("body"),
            "created_at": item.get("created_at"),
            "html_url": item.get("html_url"),
        }
        for item in items
    ]


def list_pull_request_reviews(owner: str, repo: str, pull_number: int) -> list[dict]:
    """List pull-request reviews with state, body, author, and citation URL."""
    items = github_get(
        f"/repos/{owner}/{repo}/pulls/{pull_number}/reviews?per_page=100"
    )
    assert isinstance(items, list)
    return [
        {
            "author": (item.get("user") or {}).get("login"),
            "state": item.get("state"),
            "body": item.get("body"),
            "submitted_at": item.get("submitted_at"),
            "html_url": item.get("html_url"),
        }
        for item in items
    ]


def list_pull_request_review_comments(
    owner: str, repo: str, pull_number: int
) -> list[dict]:
    """List inline pull-request review comments with path, line, body, and URL."""
    items = github_get(
        f"/repos/{owner}/{repo}/pulls/{pull_number}/comments?per_page=100"
    )
    assert isinstance(items, list)
    return [
        {
            "author": (item.get("user") or {}).get("login"),
            "path": item.get("path"),
            "line": item.get("line") or item.get("original_line"),
            "body": item.get("body"),
            "html_url": item.get("html_url"),
        }
        for item in items
    ]


def list_commit_check_runs(owner: str, repo: str, revision: str) -> list[dict]:
    """List CI check runs for a commit with status, conclusion, and details URL."""
    item = github_get(
        f"/repos/{owner}/{repo}/commits/{revision}/check-runs?per_page=100"
    )
    assert isinstance(item, dict)
    return [
        {
            "name": run.get("name"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "details_url": run.get("details_url"),
        }
        for run in item.get("check_runs") or []
    ]


def compare_revisions(owner: str, repo: str, base: str, head: str) -> dict:
    """Compare two revisions and return commit and file summaries with GitHub URLs."""
    item = github_get(f"/repos/{owner}/{repo}/compare/{base}...{head}")
    assert isinstance(item, dict)
    return {
        "status": item.get("status"),
        "ahead_by": item.get("ahead_by"),
        "behind_by": item.get("behind_by"),
        "total_commits": item.get("total_commits"),
        "html_url": item.get("html_url"),
        "files": [
            {
                "filename": file.get("filename"),
                "changes": file.get("changes"),
                "blob_url": file.get("blob_url"),
            }
            for file in item.get("files") or []
        ],
    }


def get_commit(owner: str, repo: str, revision: str) -> dict:
    """Get one commit's message, changed-file summaries, and citation URL."""
    item = github_get(f"/repos/{owner}/{repo}/commits/{revision}")
    assert isinstance(item, dict)
    return {
        "sha": item.get("sha"),
        "message": (item.get("commit") or {}).get("message"),
        "html_url": item.get("html_url"),
        "files": [
            {
                "filename": file.get("filename"),
                "changes": file.get("changes"),
                "blob_url": file.get("blob_url"),
            }
            for file in item.get("files") or []
        ],
    }


def get_pull_request_evidence_bundle(
    owner: str, repo: str, pull_number: int
) -> dict:
    """Get a compact, citation-ready evidence bundle for explaining one pull request."""
    pull = github_get(f"/repos/{owner}/{repo}/pulls/{pull_number}")
    files = github_get(
        f"/repos/{owner}/{repo}/pulls/{pull_number}/files?per_page=100"
    )
    commits = github_get(
        f"/repos/{owner}/{repo}/pulls/{pull_number}/commits?per_page=100"
    )
    assert isinstance(pull, dict)
    assert isinstance(files, list)
    assert isinstance(commits, list)

    body = pull.get("body") or ""
    validation_start = body.lower().find("automated:")
    validation_end = body.lower().find("## video/screenshots")
    validation = (
        body[validation_start : validation_end if validation_end > validation_start else None]
        if validation_start >= 0
        else ""
    )
    def is_test(item: dict) -> bool:
        filename = (item.get("filename") or "").lower()
        return (
            filename.startswith(("test/", "tests/", "__tests__/"))
            or "/__tests__/" in filename
            or ".test." in filename
            or ".spec." in filename
        )

    production = sorted(
        (item for item in files if not is_test(item)),
        key=lambda item: item.get("changes") or 0,
        reverse=True,
    )
    tests = sorted(
        (item for item in files if is_test(item)),
        key=lambda item: item.get("changes") or 0,
        reverse=True,
    )
    # Keep the selection task-independent: the three largest production changes
    # and two largest test changes provide a compact implementation/validation
    # cross-section without knowing this PR's filenames or subject.
    important = production[:3] + tests[:2]
    return {
        "pull_request": {
            "number": pull.get("number"),
            "title": pull.get("title"),
            "summary": body[:5500],
            "state": pull.get("state"),
            "merged_at": pull.get("merged_at"),
            "html_url": pull.get("html_url"),
            "changed_files": pull.get("changed_files"),
            "commits": pull.get("commits"),
            "additions": pull.get("additions"),
            "deletions": pull.get("deletions"),
        },
        "validation_evidence": validation[:3500],
        "files": [
            {
                "filename": item.get("filename"),
                "status": item.get("status"),
                "changes": item.get("changes"),
                "blob_url": item.get("blob_url"),
            }
            for item in files
        ],
        "important_file_patches": [
            {
                "filename": item.get("filename"),
                "patch": (item.get("patch") or "")[:2500],
                "blob_url": item.get("blob_url"),
            }
            for item in important[:5]
        ],
        "commits": [
            {
                "sha": item.get("sha"),
                "message": ((item.get("commit") or {}).get("message") or "").splitlines()[0],
                "html_url": item.get("html_url"),
            }
            for item in commits
        ],
    }


PRIMITIVE_TOOLS = (
    get_pull_request,
    list_pull_request_files,
    list_pull_request_commits,
    get_file_at_revision,
)
BROAD_TOOLS = PRIMITIVE_TOOLS + (
    get_repository,
    get_issue,
    list_issue_comments,
    list_pull_request_reviews,
    list_pull_request_review_comments,
    list_commit_check_runs,
    compare_revisions,
    get_commit,
)

if MODE == "task-shaped":
    mcp.tool(get_pull_request_evidence_bundle)
elif MODE == "broad":
    for tool in BROAD_TOOLS:
        mcp.tool(tool)
else:
    for tool in PRIMITIVE_TOOLS:
        mcp.tool(tool)


if __name__ == "__main__":
    mcp.run()
