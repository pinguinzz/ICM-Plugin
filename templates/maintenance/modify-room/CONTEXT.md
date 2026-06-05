# modify-room — in-convention room-local edits (room)

> Parallel capability, **cheap** tier (`../docs/model-tiers.md`). A room evolving its OWN process within
> convention. Minimal rules; anything structural or cross-room → `../modify-workspace/` (gated). The
> condensed rules live here: `docs/how-to-evolve-a-room.md` — the canonical home (root `AGENTS.md` points here).

## Inputs
| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Tools | `tools.json` | Full file | what this room may call (read FIRST) |
| Rules | `docs/how-to-evolve-a-room.md` | Full file | the minimal in-convention checklist |
| Target room | `<the room's CONTEXT.md + docs/>` | Full | what is being evolved |

## Process
1. Read `tools.json` + `docs/how-to-evolve-a-room.md`.
2. Confirm the edit is **in-convention + room-local** (no contract I/O, routing, name, or another room). If not → STOP, hand to `../modify-workspace/` (CR).
3. Make the edit; keep the room within the contract shape + line caps.
4. Re-run the validation checker; log in `../docs/changelog.md` (minor+double-checked).

## Outputs
| Artifact | Location | Format |
|----------|----------|--------|
| Edited room file | the target room (its own folder) | `.md` |
| Changelog line | `../docs/changelog.md` | one line |

## Done-when
The room's own process is updated, still in convention, checker clean, and logged — no structural/cross-room change.

## Hand-off
None — or escalate to `../modify-workspace/` if the edit turned out structural.

## Boundaries
Edits only the room it's invoked on, within convention; never touches contracts/routing/names/another room (→ modify-workspace); never edits `projects/` runs; never writes `_state.json`. Base rules: the `icm` skill · invariants: `../docs/CONVENTIONS.md`.

## Tools
Read `tools.json` first.
