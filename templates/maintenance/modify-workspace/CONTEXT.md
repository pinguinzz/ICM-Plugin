# modify-workspace — create + change structure (room; = /new)

> The HEAVY, gated structural authority. Two modes: **create-new** (additive — the 5-stage build pipeline)
> and **change-existing** (structural/major edits). Mid–high tier, **clean context**, full-canon read,
> CR / human approval required (`../docs/model-tiers.md`). Front-door: `/icm:new` (portable: `/icm -new`).

## When to use
- Build/add a room, sub-room, or dept (additive) → **create-new mode** (stages below).
- Change a contract's I/O, routing, or names; rename/move; retire → **change-existing mode** (CR first).
- Cheap in-convention room edits → `../modify-room/`. File hygiene/pointers → `../janitor/`. Conformance audit → `../audit/`.

## Inputs
| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Tools | `tools.json` | Full file | what this room may call (read FIRST) |
| Canon | `../docs/conventions.md` · `architecture.md` | Full | rules + skeleton + state/markers (full read — heavy tier) |
| Contract shape | `../docs/room-contract.md` | Full | the fixed room shape |
| CR | `../docs/pipeline-change-requests.md` | the approved CR | authority for change-existing |

## Create-new mode (stages, run in order)
| Stage | Job |
|---|---|
| discovery | capability, shape (sequential/parallel), I/O, consumers, sub-room need |
| mapping | contracts + dependency graph + sub-room axis (one-way refs) |
| scaffolding | generate folders+files into the fixed skeleton from `templates/` |
| config | local conventions + config knobs + `tools.json` |
| validation | enforce invariants + skeleton integrity (scripted) before promote |
Works in `workbench-<target>/`; human-gated; promote into the tree; log in `../docs/changelog.md`.

## Change-existing mode
1. Require an APPROVED CR. 2. Read the FULL canon (clean context). 3. Edit; update every downstream pointer. 4. Re-run the validation checker. 5. Log the change.

## Outputs / Done-when
New or changed structure that passes the validation checker, is human-promoted, and is logged. Never declare done with a failing checker.

## Boundaries
The only structural authority; works in `workbench-<target>/` until promoted; never edits `projects/` runs; never writes `_state.json`. Additive = human-gated; anything touching existing structure = CR. Base rules: the `icm` skill · invariants: `../docs/conventions.md`.

## Tools
Read `tools.json` first. (Intake/grilling: the `grill-me` skill; authoring: `write-a-skill` — when available.)
