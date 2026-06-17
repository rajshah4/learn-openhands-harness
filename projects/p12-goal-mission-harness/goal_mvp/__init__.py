"""Tiny, SDK-free `/goal` teaching fixture for P12."""

from .controller import run_until_goal, set_goal
from .state import GoalState, GoalStatus, clear_goal, read_goal, write_goal

__all__ = [
    "GoalState",
    "GoalStatus",
    "clear_goal",
    "read_goal",
    "run_until_goal",
    "set_goal",
    "write_goal",
]
