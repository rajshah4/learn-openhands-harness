"""Prompt strings for the P12 goal-loop teaching fixture."""

from __future__ import annotations

from .state import GoalState


def _budget_line(goal: GoalState) -> str:
    if goal.token_budget is None:
        return f"- Tokens used so far: {goal.tokens_used} (no token budget set)."
    return (
        f"- Tokens used: {goal.tokens_used} / budget {goal.token_budget} "
        f"(~{goal.remaining_tokens()} remaining)."
    )


def initial_goal_message(goal: GoalState) -> str:
    return f"""You are now working toward a persistent GOAL.

<objective>
{goal.objective}
</objective>

This goal persists across turns. When you believe it is done, call
`update_goal` with status "complete".

{_budget_line(goal)}
"""


def continuation_message(goal: GoalState) -> str:
    return f"""Continue working toward the active goal.

<objective>
{goal.objective}
</objective>

Completion audit:
- Derive concrete requirements from the objective.
- Find authoritative evidence for each requirement.
- If anything is missing or unverified, keep working.
- If the audit passes, call `update_goal` with status "complete".

Blocked audit:
- Use "blocked" only after the same blocker repeats for three consecutive goal
  turns and progress requires user input or external state.

{_budget_line(goal)}
"""
