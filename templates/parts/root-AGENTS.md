# {{PROJECT_NAME}} — Agent Contract (L0, frontdoor)

You are entering an ICM workspace. This file says **what this place is and how to enter it**. Before any
work: 1. Read this file. 2. Read `CONTEXT.md` — the **map + routing** (where to go). 3. Match the request
to a Routing row there. 4. Go to that folder, read its `CONTEXT.md`, load only what its **Inputs** name.

If you have the `icm` skill loaded you know the rules; otherwise read `docs/CONVENTIONS.md`.

## Identity

{{PROJECT_DESCRIPTION}}

## Base rules (always)

1. **Read `AGENTS.md` first**, then root **`CONTEXT.md`** for routing, then the target `CONTEXT.md`
   (department → room → sub-room). Load only the room's **Inputs**.
2. **Write only to your output target** — your run folder + your own `docs/memory/`. Never another room's
   or run's folder; never edit Layer 3 during a run. Drop **markers**; a reconciler script owns machine state.
3. **Never mutate structure.** Propose changes via `{{CR_PATH}}`; a human disposes.
4. **A room may evolve its OWN process in place** if it stays within convention — read the `modify-room`
   rules first (`maintenance/modify-room/docs/how-to-evolve-a-room.md`). Structural or cross-room → the
   `modify-workspace` room (gated).

## Naming conventions

{{NAMING_CONVENTIONS}}

## Invariants you must not break

- A room writes ONLY to its own output target; NEVER another room's/run's folder.
- A room NEVER edits Layer 3 (`docs/`) during a run.
- `docs/` per node — never `docs-<name>/`. No emoji in names.
- `CLAUDE.md` / `GEMINI.md` / `.cursorrules` are stubs pointing here — no content in them.

Full list: `docs/CONVENTIONS.md`. Structural changes → `/icm:assimilate` (check) or a CR. New structure →
`/icm:new`.
