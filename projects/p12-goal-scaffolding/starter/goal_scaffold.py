"""Starter goal scaffold for P12.

Fill this in after reading the goal MVP. The point is to make the hidden
scaffold explicit enough that a harness could enforce it.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Criterion:
    id: str
    description: str
    satisfied_by: list[str] = field(default_factory=list)


@dataclass
class Verifier:
    command: str
    expected_exit_code: int = 0
    must_run_after_paths: list[str] = field(default_factory=list)


@dataclass
class Envelope:
    allowed_paths: list[str] = field(default_factory=list)
    allowed_tools: list[str] = field(default_factory=list)
    allowed_commands: list[str] = field(default_factory=list)
    denied_commands: list[str] = field(default_factory=list)


@dataclass
class GoalScaffold:
    objective: str
    criteria: list[Criterion] = field(default_factory=list)
    verifier: Verifier | None = None
    sensors: list[str] = field(default_factory=list)
    actuators: list[str] = field(default_factory=list)
    envelope: Envelope = field(default_factory=Envelope)
    token_budget: int | None = None
    max_goal_turns: int = 3

    def validation_errors(self) -> list[str]:
        """Return schema-level errors before a goal is allowed to run."""
        # TODO: require at least one criterion.
        # TODO: require a verifier command for code-changing goals.
        # TODO: require at least one sensor that can inform the verifier.
        # TODO: require at least one actuator and an envelope.
        # TODO: require a positive token budget and max_goal_turns.
        return []


def slugify_dot_scaffold() -> GoalScaffold:
    """Return the goal scaffold for the dot-preservation slugify goal."""
    # TODO: encode the goal:
    # "api.v1 endpoint" should become "api.v1-endpoint".
    # The regression test must be added first, pytest must fail before the fix,
    # then pytest must pass after the fix.
    raise NotImplementedError


if __name__ == "__main__":
    scaffold = slugify_dot_scaffold()
    errors = scaffold.validation_errors()
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(scaffold)
