# janitor procedures — file hygiene + pointer rewiring

> Mechanical maintenance within invariants. Every procedure: (1) classify, (2) read global Invariants
> (`../../docs/conventions.md`), (3) act within invariants or escalate to a CR, (4) re-run
> `scripts/icm_check.py`, (5) log in `../../docs/changelog.md`. Anything touching a contract/routing/name
> is NOT janitor — file a CR → `../../modify-workspace/`.

## split-oversize
A reference/doc file exceeds ~200 lines → split into atomic bite-size docs by topic + leave a short index
file that points to the parts. Repoint every referrer to the right atomic file. Re-validate.

## re-point
A pointer's target moved → repoint it to the live target. Re-validate. (If the move itself isn't done yet,
that's structural → escalate.)

## rewire-pointer
A pointer drifted/stale (target renamed or relocated) → find every referrer (grep) and repoint each. Re-validate.

## organize
A file is in the wrong folder → move it to its right home (`git mv`); repoint referrers. If the move changes
how folders interact (routing/contract), it's structural → CR → `modify-workspace`.

## Escalate (NOT janitor)
modify-contract · rename/move a room or dept · retire-to-archive · anything cross-room → CR → `../../modify-workspace/`.

## Logging (always)
Append to `../../docs/changelog.md`: `date · target · what · minor+double-checked · result`.
