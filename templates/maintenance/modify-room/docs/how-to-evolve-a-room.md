# How to evolve a room (condensed — the in-convention checklist)

> The minimal rules for a room editing its OWN process in place. Root `AGENTS.md` points here; this is the
> single canonical home of these rules (nothing restates them). If an edit fails ANY check below, it is
> NOT a modify-room edit → hand to `../../modify-workspace/` (CR).

## You MAY (in-convention, room-local)
- Refine the room's own Process steps, prompts, or `docs/` wording.
- Tighten its Inputs **scope** (which section to load) without changing WHICH artifacts it consumes.
- Add to / curate the room's own `docs/memory/`.

## You MAY NOT (→ modify-workspace, CR)
- Change the room's Inputs/Outputs/Done-when **contract** (its I/O), its routing, or its name.
- Touch another room, another run, or any `projects/` output.
- Add / move / rename folders, or change how rooms interact.
- Bend an Invariant (`../../docs/CONVENTIONS.md`).

## Keep it in shape
- `CONTEXT.md` stays < 80 lines, follows the canon `../../docs/ROOM-CONTRACT.md`.
- A file over ~200 lines → don't grow it; hand to `../../janitor/` (split via CR).
- Re-run `scripts/icm_check.py`; log in `../../docs/changelog.md` (minor+double-checked).
