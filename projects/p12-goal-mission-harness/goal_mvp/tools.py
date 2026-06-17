"""SDK-free `update_goal` tool stand-in for the P12 fixture."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .state import GoalStatus, read_goal, write_goal


@dataclass
class UpdateGoalAction:
    status: str
    message: str = ""


@dataclass
class UpdateGoalObservation:
    ok: bool
    status: str = ""
    content: str = ""
    is_error: bool = False


class UpdateGoalExecutor:
    def __call__(
        self,
        action: UpdateGoalAction,
        conversation: Any | None = None,
    ) -> UpdateGoalObservation:
        if conversation is None:
            return UpdateGoalObservation(
                ok=False,
                content="No conversation context; cannot update goal.",
                is_error=True,
            )

        goal = read_goal(conversation.state)
        if goal is None:
            return UpdateGoalObservation(
                ok=False,
                content="There is no active goal to update.",
                is_error=True,
            )

        requested = action.status.strip().lower()
        if requested not in ("complete", "blocked"):
            return UpdateGoalObservation(
                ok=False,
                status=goal.status.value,
                content=f"Invalid status '{action.status}'.",
                is_error=True,
            )

        goal.status = (
            GoalStatus.COMPLETE if requested == "complete" else GoalStatus.BLOCKED
        )
        write_goal(conversation.state, goal)
        detail = f"Goal marked {requested}. {action.message}".strip()
        return UpdateGoalObservation(ok=True, status=goal.status.value, content=detail)
