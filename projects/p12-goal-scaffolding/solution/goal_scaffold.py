"""Reference goal scaffold for P12.

This is deliberately small. It is a schema sketch that names the state a goal
feature needs before a harness can make trustworthy completion decisions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field


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
    criteria: list[Criterion]
    verifier: Verifier
    sensors: list[str]
    actuators: list[str]
    envelope: Envelope
    token_budget: int
    max_goal_turns: int
    evidence: list[str] = field(default_factory=list)

    def validation_errors(self) -> list[str]:
        errors: list[str] = []
        if not self.objective.strip():
            errors.append("objective is required")
        if not self.criteria:
            errors.append("at least one completion criterion is required")
        if not self.verifier.command.strip():
            errors.append("verifier.command is required")
        if not self.sensors:
            errors.append("at least one sensor is required")
        if not self.actuators:
            errors.append("at least one actuator is required")
        if not self.envelope.allowed_paths:
            errors.append("envelope.allowed_paths is required")
        if not self.envelope.allowed_tools:
            errors.append("envelope.allowed_tools is required")
        if self.token_budget <= 0:
            errors.append("token_budget must be positive")
        if self.max_goal_turns <= 0:
            errors.append("max_goal_turns must be positive")
        return errors


def slugify_dot_scaffold() -> GoalScaffold:
    return GoalScaffold(
        objective=(
            "Preserve dots in slugify so slugify('api.v1 endpoint') returns "
            "'api.v1-endpoint'."
        ),
        criteria=[
            Criterion(
                id="regression-test",
                description=(
                    "tests/test_slugify.py contains a regression test for "
                    "slugify('api.v1 endpoint') == 'api.v1-endpoint'."
                ),
                satisfied_by=["file_diff", "pytest_output"],
            ),
            Criterion(
                id="pre-fix-failure",
                description=(
                    "The regression test fails before the implementation change "
                    "when run with the agreed pytest command."
                ),
                satisfied_by=["command_exit_code", "stderr_or_stdout"],
            ),
            Criterion(
                id="implementation",
                description="src/slugify.py preserves dots without deleting existing behavior.",
                satisfied_by=["file_diff"],
            ),
            Criterion(
                id="post-fix-pass",
                description="The full slugify test file passes after the implementation change.",
                satisfied_by=["command_exit_code", "stdout"],
            ),
        ],
        verifier=Verifier(
            command="python -m pytest tests/test_slugify.py -q",
            expected_exit_code=0,
            must_run_after_paths=["src/slugify.py", "tests/test_slugify.py"],
        ),
        sensors=[
            "tool event stream",
            "workspace diff",
            "pytest command output",
            "exit status",
            "token metrics",
        ],
        actuators=[
            "edit src/slugify.py",
            "edit tests/test_slugify.py",
            "run pytest verifier",
        ],
        envelope=Envelope(
            allowed_paths=["src/slugify.py", "tests/test_slugify.py"],
            allowed_tools=["read_file", "edit_file", "run_command", "update_goal"],
            allowed_commands=["python -m pytest tests/test_slugify.py -q"],
            denied_commands=["pip install", "uv pip install", "python -m ensurepip"],
        ),
        token_budget=20_000,
        max_goal_turns=2,
    )


def main() -> int:
    scaffold = slugify_dot_scaffold()
    errors = scaffold.validation_errors()
    print(json.dumps(asdict(scaffold), indent=2))
    if errors:
        print("\nValidation errors:")
        print("\n".join(errors))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
