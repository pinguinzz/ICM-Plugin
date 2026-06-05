# janitor — file hygiene + pointer rewiring (room)

> Parallel capability. Splits oversized files into bite-size atomic docs, re-points references, organizes
> misplaced files, and rewires drifted/stale pointers. Cheap–mid tier (`../docs/model-tiers.md`).
> Mechanical work; anything that touches a contract/routing/name → STOP, file a CR → `../modify-workspace/`.

## Inputs
| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Tools | `tools.json` | Full file | what this room may call (read FIRST) |
| Procedures | `docs/procedures.md` | the matching section | how to act within invariants |
| Canon | `../docs/conventions.md` | "Invariants" | what can't break |
| Target | `<file(s)>` | Full | what to split / re-point / organize |

## Process
1. Read `tools.json` + the matching procedure in `docs/procedures.md`.
2. Classify: split-oversize · re-point · organize · rewire-pointer. If it would change a contract/routing/name → STOP, file a CR.
3. Act mechanically within invariants (split >~200-line files into atomic docs + an index; repoint every referrer; move misplaced files via `git mv`).
4. Re-run the structure checker (`tools.json`). Log in `../docs/changelog.md`.

## Outputs
| Artifact | Location | Format |
|----------|----------|--------|
| Split docs + index | in place (the file's own folder) | atomic `.md` + a short index |
| Changelog line | `../docs/changelog.md` | one line |

## Done-when
The oversized file is split + every pointer resolves (checker clean), or the change was escalated to a CR.

## Hand-off
None (terminal hygiene) — or a CR to `../modify-workspace/` if it crossed into structural.

## Boundaries
Edits only docs-hygiene (split/move/repoint) within invariants; never changes a contract/routing/name without a CR; never edits `projects/` runs; never writes `_state.json`. Base rules: the `icm` skill · invariants: `../docs/conventions.md`.

## Tools
Read `tools.json` first.
