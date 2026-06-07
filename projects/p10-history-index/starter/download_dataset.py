"""
Download the agent-history dataset into ./data.

The corpus is `rajistics/openhands-synthetic-conversations` on Hugging Face:
28 real OpenHands V1 agent conversations (1,064 events, ~7.6 MB). Each
conversation is a directory of sequentially-numbered event JSON files, the
same format OpenHands Cloud produces from "Download Conversation".

Usage:
    pip install huggingface_hub
    python starter/download_dataset.py
"""
from __future__ import annotations

from pathlib import Path

from huggingface_hub import snapshot_download

REPO = "rajistics/openhands-synthetic-conversations"
DEST = Path(__file__).resolve().parent.parent / "data"


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=REPO, repo_type="dataset", local_dir=str(DEST))
    convs = sorted(DEST.glob("conversation_*"))
    events = sum(1 for _ in DEST.glob("conversation_*/event_*.json"))
    print(f"Downloaded {len(convs)} conversations, {events} events into {DEST}")


if __name__ == "__main__":
    main()
