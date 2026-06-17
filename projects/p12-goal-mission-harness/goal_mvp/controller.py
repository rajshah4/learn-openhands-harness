"""Caller-side continuation loop for the P12 goal fixture."""

from __future__ import annotations

from typing import Any

from .prompts import continuation_message, initial_goal_message
from .state import GoalState, GoalStatus, read_goal, write_goal


def goal_token_usage(state: Any) -> int:
    metrics = state.stats.get_combined_metrics()
    usage = getattr(metrics, "accumulated_token_usage", None)
    if usage is None:
        return 0
    return max(
        0,
        usage.prompt_tokens - usage.cache_read_tokens + usage.completion_tokens,
    )


def set_goal(
    conversation: Any,
    objective: str,
    token_budget: int | None = None,
) -> GoalState:
    goal = GoalState(objective=objective.strip(), token_budget=token_budget)
    write_goal(conversation.state, goal)
    conversation.send_message(initial_goal_message(goal))
    return goal


def _refresh_usage_and_budget(state: Any, goal: GoalState) -> GoalState:
    goal.tokens_used = goal_token_usage(state)
    if (
        goal.status is GoalStatus.ACTIVE
        and goal.token_budget is not None
        and goal.tokens_used >= goal.token_budget
    ):
        goal.status = GoalStatus.BUDGET_LIMITED
    return goal


def run_until_goal(
    conversation: Any,
    max_turns: int = 50,
    on_turn: Any = None,
) -> GoalState | None:
    goal = read_goal(conversation.state)
    if goal is None:
        conversation.run()
        return None

    while True:
        conversation.run()

        goal = read_goal(conversation.state) or goal
        goal = _refresh_usage_and_budget(conversation.state, goal)
        goal.turns += 1
        write_goal(conversation.state, goal)

        if on_turn is not None:
            on_turn(goal)

        if not goal.status.keeps_running:
            break
        if goal.turns >= max_turns:
            break

        exec_status = getattr(conversation.state, "execution_status", None)
        if getattr(exec_status, "value", exec_status) in ("stuck", "error"):
            break

        conversation.send_message(continuation_message(goal))

    return read_goal(conversation.state)
