#!/usr/bin/env python3
"""Starter probes for the OpenHands goal MVP.

Complete this file after reading `goal_mvp/state.py`, `goal_mvp/controller.py`,
and `goal_mvp/tools.py`. Your probes should produce JSON so the results can be
compared across implementations.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass


@dataclass
class Probe:
    name: str
    result: str
    severity: str
    summary: str
    detail: str


def probe_budget_complete_override() -> Probe:
    # TODO: create a fake conversation that burns more tokens than the budget
    # and then marks the goal complete. Does the final status become complete
    # or budget_limited?
    return Probe(
        name="budget_complete_override",
        result="todo",
        severity="high",
        summary="Check whether completion can override the token budget.",
        detail="not implemented",
    )


def probe_completion_without_evidence() -> Probe:
    # TODO: call the update_goal tool with status='complete' and no message.
    # Does the tool require verifier output or evidence references?
    return Probe(
        name="completion_without_evidence",
        result="todo",
        severity="high",
        summary="Check whether update_goal complete requires evidence.",
        detail="not implemented",
    )


def probe_contract_schema() -> Probe:
    # TODO: inspect dataclasses.fields(GoalState). Does it contain criteria,
    # verifier, sensors, actuators, envelope, and evidence?
    return Probe(
        name="contract_schema",
        result="todo",
        severity="high",
        summary="Check whether GoalState stores a full mission contract.",
        detail="not implemented",
    )


def main() -> int:
    probes = [
        probe_budget_complete_override(),
        probe_completion_without_evidence(),
        probe_contract_schema(),
    ]
    print(json.dumps([asdict(probe) for probe in probes], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
