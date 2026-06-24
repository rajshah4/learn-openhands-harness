#!/usr/bin/env python3
"""Smoke probe for the official OpenHands goal controller.

This intentionally avoids a real model call. The fake judge returns one
incomplete verdict followed by one complete verdict, which lets the course test
the control-flow contract that `run_goal` is built on:

objective -> judge says missing -> GoalContinue
follow-up -> judge says complete -> GoalDone(status="complete")
"""

from __future__ import annotations

import json

from openhands.sdk.conversation.goal import GoalContinue, GoalController, GoalDone
from openhands.sdk.llm import Message, TextContent


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.message = Message(
            role="assistant",
            content=[TextContent(text=json.dumps(payload))],
        )


class FakeJudgeLLM:
    stream = False

    def __init__(self, verdicts: list[dict[str, object]]) -> None:
        self.verdicts = list(verdicts)
        self.calls = 0

    def completion(self, messages):  # noqa: ANN001, ARG002
        self.calls += 1
        if not self.verdicts:
            raise AssertionError("fake judge called more times than expected")
        return FakeResponse(self.verdicts.pop(0))


def test_continue_then_complete() -> None:
    judge = FakeJudgeLLM(
        [
            {
                "score": 0.25,
                "complete": False,
                "missing": "Need passing pytest output.",
            },
            {"score": 1.0, "complete": True, "missing": ""},
        ]
    )
    controller = GoalController(
        "Create mathx.py and prove python -m pytest -q passes.",
        judge,  # type: ignore[arg-type]
        max_iterations=3,
    )

    assert controller.start().startswith("Create mathx.py")
    first = controller.on_run_finished([])
    assert isinstance(first, GoalContinue)
    assert "Need passing pytest output." in first.followup

    second = controller.on_run_finished([])
    assert isinstance(second, GoalDone)
    assert second.outcome.status == "complete"
    assert second.outcome.iterations == 2
    assert second.outcome.verdict.score == 1.0


def test_caps_when_missing_persists() -> None:
    judge = FakeJudgeLLM(
        [
            {
                "score": 0.1,
                "complete": False,
                "missing": "Still no verifier output.",
            }
        ]
    )
    controller = GoalController(
        "Prove the verifier passed.",
        judge,  # type: ignore[arg-type]
        max_iterations=1,
    )

    step = controller.on_run_finished([])
    assert isinstance(step, GoalDone)
    assert step.outcome.status == "capped"
    assert step.outcome.iterations == 1
    assert step.outcome.verdict.missing == "Still no verifier output."


def main() -> int:
    test_continue_then_complete()
    test_caps_when_missing_persists()
    print("official goal controller probe: 2 passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
