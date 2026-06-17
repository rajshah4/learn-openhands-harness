"""Persistent goal state for the P12 teaching fixture.

This file intentionally mirrors the shape of the modified OpenHands SDK goal
MVP without depending on the SDK. The goal is stored in a generic
``state.agent_state`` dictionary so the controller and probes can run with a
fake conversation.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


GOAL_KEY = "goal_mvp"


class GoalStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    BLOCKED = "blocked"
    BUDGET_LIMITED = "budget_limited"
    COMPLETE = "complete"

    @property
    def is_terminal(self) -> bool:
        """Terminal states never auto-resume.

        Kept deliberately narrow to reproduce a semantic gap students should
        discover: paused and blocked do not continue, but are not terminal here.
        """
        return self in (GoalStatus.COMPLETE, GoalStatus.BUDGET_LIMITED)

    @property
    def keeps_running(self) -> bool:
        return self is GoalStatus.ACTIVE


@dataclass
class GoalState:
    objective: str
    status: GoalStatus = GoalStatus.ACTIVE
    token_budget: int | None = None
    tokens_used: int = 0
    turns: int = 0
    consecutive_blocked_turns: int = 0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def remaining_tokens(self) -> int | None:
        if self.token_budget is None:
            return None
        return max(0, self.token_budget - self.tokens_used)

    def to_dict(self) -> dict[str, Any]:
        raw = asdict(self)
        raw["status"] = self.status.value
        return raw

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "GoalState":
        data = dict(raw)
        data["status"] = GoalStatus(data.get("status", GoalStatus.ACTIVE))
        return cls(**data)


def read_goal(state: Any) -> GoalState | None:
    raw = state.agent_state.get(GOAL_KEY)
    if not raw:
        return None
    return GoalState.from_dict(raw)


def write_goal(state: Any, goal: GoalState) -> GoalState:
    goal.updated_at = time.time()
    state.agent_state = {
        **state.agent_state,
        GOAL_KEY: goal.to_dict(),
    }
    return goal


def clear_goal(state: Any) -> bool:
    if GOAL_KEY not in state.agent_state:
        return False
    new_state = dict(state.agent_state)
    new_state.pop(GOAL_KEY, None)
    state.agent_state = new_state
    return True
