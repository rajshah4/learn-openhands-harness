# Facilitator notes

The student front door is the workshop overview. Keep saved results and this
key closed until students record their prediction. Pair discussion is optional
for self-paced learners; write a rationale before viewing the reveal.

| Lab | Expected starting state | Check or debrief |
|---|---|---|
| 1 | Pagination tests and external boundary check fail | Passing code plus actual read/edit/check trace; tool requests are unequal work |
| 2 | Empty scratch workspace | Verify citation support and distinguish retrieved tests from executed checks |
| 3 | Existing 11 tests pass; next-page checker fails | Preserve catalog and exports, accepted public API, token codec; older notes can be reconciled |
| 4 | Rename behavior green; bug lanes red; security report absent | Route by evidence and consequence; term coverage needs semantic review |
| 5 | Original five tests pass; independent dot assertion fails | New regression fails then passes; judge and external verifier can disagree |
| 6 | Async counter tests fail | Repeat checks, test concurrency, inspect fresh child return and synthesis |

Do not manufacture a winner. Let students reject or narrow each claim using
the evidence. Static routing, supplied memory notes, goal audits, and sequential
validation each answer a different question. Check [saved results](/workshops/odsc-2026/results)
for the exact scope of each finding.

For a live workshop, rehearse on a clean laptop with the same published install
commands. If a provider or capability is unavailable, switch to the evidence
route and record that choice. Do not silently swap models inside a comparison.
For routing, judge prompts and budgets must be recorded. For delegation,
include all child calls and any retry in total expenditure.

The checker runs outside the editing workspace but is not a sandbox. Use
isolated workspaces or a container for access control. The security review's
term screen is deliberately not a semantic judge. A report listing rubric words
without explaining affected code and fixes must be rejected by a human.

Prepare new directories for reruns. Never restore or reset a student's current
work. The one-command helper refuses overwrites. For package validation, run
`python workshops/odsc-2026/labs/validate_package.py`; it uses temporary copies
and no provider calls. It validates known good and bad candidates, not model
performance.
