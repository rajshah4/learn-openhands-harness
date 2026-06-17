#!/usr/bin/env python3
"""Deterministic probes for the OpenHands goal MVP.

These are not replacements for unit tests. They ask product-level questions:
can the MVP enforce budgets, evidence, blockers, and mission-contract state
without trusting the agent's final narration?
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from types import SimpleNamespace
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(os.environ.get("GOAL_MVP_REPO", str(PROJECT_ROOT))).expanduser()
if not (REPO / "goal_mvp").exists():
    raise SystemExit(
        "Could not find goal_mvp package. Set GOAL_MVP_REPO to a checkout or run from P12."
    )

os.environ.setdefault("OPENHANDS_SUPPRESS_BANNER", "1")
sys.path.insert(0, str(REPO))

from goal_mvp import GoalState, GoalStatus, read_goal, run_until_goal, set_goal, write_goal  # noqa: E402
from goal_mvp.controller import goal_token_usage  # noqa: E402


@dataclass
class Probe:
    name: str
    result: str
    severity: str
    summary: str
    detail: str


class FakeState:
    def __init__(self) -> None:
        self.agent_state: dict = {}
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

    def add_tokens(self, prompt: int = 0, completion: int = 0, cache_read: int = 0) -> None:
        self._usage.prompt_tokens += prompt
        self._usage.completion_tokens += completion
        self._usage.cache_read_tokens += cache_read


class FakeConversation:
    def __init__(self, script: list[Callable[["FakeConversation"], None]] | None = None):
        self.state = FakeState()
        self.sent: list[str] = []
        self.runs = 0
        self._script = list(script or [])

    def send_message(self, message, sender=None) -> None:  # noqa: ARG002
        self.sent.append(str(message))

    def run(self) -> None:
        self.runs += 1
        if self._script:
            self._script.pop(0)(self)


def mark(status: GoalStatus):
    def step(conv: FakeConversation) -> None:
        goal = read_goal(conv.state)
        assert goal is not None
        goal.status = status
        write_goal(conv.state, goal)

    return step


def burn(prompt: int = 0, completion: int = 0, cache_read: int = 0):
    def step(conv: FakeConversation) -> None:
        conv.state.add_tokens(prompt=prompt, completion=completion, cache_read=cache_read)

    return step


def burn_and_mark(prompt: int, status: GoalStatus):
    def step(conv: FakeConversation) -> None:
        conv.state.add_tokens(prompt=prompt)
        goal = read_goal(conv.state)
        assert goal is not None
        goal.status = status
        write_goal(conv.state, goal)

    return step


def probe_baseline_continuation() -> Probe:
    conv = FakeConversation([burn(prompt=10), mark(GoalStatus.COMPLETE)])
    set_goal(conv, "finish a thing", token_budget=1000)
    final = run_until_goal(conv, max_turns=5)
    ok = final is not None and final.status is GoalStatus.COMPLETE and final.turns == 2
    return Probe(
        name="baseline_continuation",
        result="pass" if ok else "fail",
        severity="info",
        summary="Controller continues active goals and stops on complete.",
        detail=f"runs={conv.runs}, sent_messages={len(conv.sent)}, final={final}",
    )


def probe_budget_active_cutoff() -> Probe:
    conv = FakeConversation([burn(prompt=250)])
    set_goal(conv, "expensive unfinished task", token_budget=100)
    final = run_until_goal(conv, max_turns=5)
    ok = final is not None and final.status is GoalStatus.BUDGET_LIMITED and conv.runs == 1
    return Probe(
        name="budget_active_cutoff",
        result="pass" if ok else "fail",
        severity="info",
        summary="Budget limits stop active unfinished goals.",
        detail=(
            f"runs={conv.runs}, final_status={getattr(final, 'status', None)}, "
            f"tokens={getattr(final, 'tokens_used', None)}"
        ),
    )


def probe_budget_complete_override_gap() -> Probe:
    conv = FakeConversation([burn_and_mark(prompt=250, status=GoalStatus.COMPLETE)])
    set_goal(conv, "complete after overspending", token_budget=100)
    final = run_until_goal(conv, max_turns=5)
    gap = final is not None and final.status is GoalStatus.COMPLETE and final.tokens_used >= 100
    return Probe(
        name="budget_complete_override_gap",
        result="gap" if gap else "pass",
        severity="high" if gap else "info",
        summary="Agent can complete after exceeding token budget.",
        detail=(
            f"final_status={getattr(final, 'status', None)}, "
            f"tokens={getattr(final, 'tokens_used', None)}, budget=100"
        ),
    )


def probe_blocked_first_turn_gap() -> Probe:
    conv = FakeConversation([mark(GoalStatus.BLOCKED)])
    set_goal(conv, "hard task")
    final = run_until_goal(conv, max_turns=5)
    gap = final is not None and final.status is GoalStatus.BLOCKED and final.turns == 1
    return Probe(
        name="blocked_first_turn_gap",
        result="gap" if gap else "pass",
        severity="medium" if gap else "info",
        summary="Tool permits blocked on the first turn despite the prompt's 3-turn rule.",
        detail=f"final_status={getattr(final, 'status', None)}, turns={getattr(final, 'turns', None)}",
    )


def probe_completion_without_evidence_gap() -> Probe:
    try:
        from goal_mvp.tools import UpdateGoalAction, UpdateGoalExecutor
    except Exception as exc:  # noqa: BLE001
        return Probe(
            name="completion_without_evidence_gap",
            result="skip",
            severity="info",
            summary="SDK tool unavailable, skipped.",
            detail=str(exc),
        )

    conv = FakeConversation()
    set_goal(conv, "prove something")
    obs = UpdateGoalExecutor()(UpdateGoalAction(status="complete"), conv)
    final = read_goal(conv.state)
    gap = obs.ok is True and final is not None and final.status is GoalStatus.COMPLETE
    return Probe(
        name="completion_without_evidence_gap",
        result="gap" if gap else "pass",
        severity="high" if gap else "info",
        summary="update_goal complete accepts an empty message and no verifier evidence.",
        detail=f"obs_ok={obs.ok}, obs_status={obs.status}, message_len=0",
    )


def probe_status_terminal_semantics_gap() -> Probe:
    paused_terminal = GoalStatus.PAUSED.is_terminal
    blocked_terminal = GoalStatus.BLOCKED.is_terminal
    gap = not paused_terminal or not blocked_terminal
    return Probe(
        name="status_terminal_semantics_gap",
        result="gap" if gap else "pass",
        severity="low" if gap else "info",
        summary="GoalStatus.is_terminal excludes paused/blocked even though they do not continue.",
        detail=f"paused_is_terminal={paused_terminal}, blocked_is_terminal={blocked_terminal}",
    )


def probe_max_turns_leaves_active_gap() -> Probe:
    conv = FakeConversation()
    set_goal(conv, "never completes")
    final = run_until_goal(conv, max_turns=2)
    gap = final is not None and final.status is GoalStatus.ACTIVE and final.turns == 2
    return Probe(
        name="max_turns_leaves_active_gap",
        result="gap" if gap else "pass",
        severity="medium" if gap else "info",
        summary="Max-turn safety cap stops the driver but leaves goal status active.",
        detail=f"runs={conv.runs}, final_status={getattr(final, 'status', None)}, turns={getattr(final, 'turns', None)}",
    )


def probe_contract_schema_gap() -> Probe:
    state_fields = {field.name for field in fields(GoalState)}
    expected = {
        "criteria",
        "verifier",
        "sensors",
        "actuators",
        "envelope",
        "evidence",
        "blocked_reason",
    }
    missing = sorted(expected - state_fields)
    gap = bool(missing)
    return Probe(
        name="contract_schema_gap",
        result="gap" if gap else "pass",
        severity="high" if gap else "info",
        summary="GoalState stores objective, budget, and lifecycle, but not a full mission contract.",
        detail=f"missing_fields={missing}",
    )


def probe_token_formula_cached_discount() -> Probe:
    state = FakeState()
    state.add_tokens(prompt=1000, cache_read=800, completion=100)
    used = goal_token_usage(state)
    ok = used == 300
    return Probe(
        name="token_formula_cached_discount",
        result="pass" if ok else "fail",
        severity="info",
        summary="Budget metric discounts cached prompt tokens.",
        detail=f"prompt=1000, cache_read=800, completion=100, counted={used}",
    )


PROBES = [
    probe_baseline_continuation,
    probe_budget_active_cutoff,
    probe_budget_complete_override_gap,
    probe_blocked_first_turn_gap,
    probe_completion_without_evidence_gap,
    probe_status_terminal_semantics_gap,
    probe_max_turns_leaves_active_gap,
    probe_contract_schema_gap,
    probe_token_formula_cached_discount,
]


def main() -> int:
    results = [probe() for probe in PROBES]
    print(json.dumps([asdict(result) for result in results], indent=2))
    return 1 if any(result.result == "fail" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
