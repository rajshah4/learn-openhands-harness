#!/usr/bin/env python3
"""Smoke tests for the P12 goal-loop fixture."""

from __future__ import annotations

from types import SimpleNamespace

from goal_mvp import GoalStatus, read_goal, run_until_goal, set_goal, write_goal


class FakeState:
    def __init__(self) -> None:
        self.agent_state = {}
        self.execution_status = SimpleNamespace(value="running")
        self._usage = SimpleNamespace(
            prompt_tokens=0,
            completion_tokens=0,
            cache_read_tokens=0,
        )
        self.stats = SimpleNamespace(
            get_combined_metrics=lambda: SimpleNamespace(
                accumulated_token_usage=self._usage
            )
        )

    def add_tokens(self, prompt: int = 0, completion: int = 0, cache_read: int = 0):
        self._usage.prompt_tokens += prompt
        self._usage.completion_tokens += completion
        self._usage.cache_read_tokens += cache_read


class FakeConversation:
    def __init__(self, script=None):
        self.state = FakeState()
        self.sent = []
        self.runs = 0
        self._script = list(script or [])

    def send_message(self, message, sender=None):  # noqa: ARG002
        self.sent.append(str(message))

    def run(self):
        self.runs += 1
        if self._script:
            self._script.pop(0)(self)


def mark(status: GoalStatus):
    def step(conv: FakeConversation):
        goal = read_goal(conv.state)
        assert goal is not None
        goal.status = status
        write_goal(conv.state, goal)

    return step


def burn(prompt: int):
    def step(conv: FakeConversation):
        conv.state.add_tokens(prompt=prompt)

    return step


def test_active_goal_continues_until_complete():
    conv = FakeConversation([burn(10), mark(GoalStatus.COMPLETE)])
    set_goal(conv, "finish a thing", token_budget=1000)
    final = run_until_goal(conv, max_turns=5)
    assert final is not None
    assert final.status is GoalStatus.COMPLETE
    assert final.turns == 2
    assert conv.runs == 2
    assert len(conv.sent) == 2


def test_active_goal_becomes_budget_limited():
    conv = FakeConversation([burn(250)])
    set_goal(conv, "expensive unfinished task", token_budget=100)
    final = run_until_goal(conv, max_turns=5)
    assert final is not None
    assert final.status is GoalStatus.BUDGET_LIMITED
    assert final.tokens_used == 250


def test_max_turns_stops_without_completing():
    conv = FakeConversation()
    set_goal(conv, "never completes")
    final = run_until_goal(conv, max_turns=2)
    assert final is not None
    assert final.status is GoalStatus.ACTIVE
    assert final.turns == 2


def main() -> int:
    test_active_goal_continues_until_complete()
    test_active_goal_becomes_budget_limited()
    test_max_turns_stops_without_completing()
    print("3 passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
