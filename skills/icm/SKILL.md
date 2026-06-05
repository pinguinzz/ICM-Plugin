---
name: icm
description: Use when you enter a folder that follows the Interpretable Context Methodology (ICM) — signs are an `AGENTS.md` or `CONTEXT.md` at the root, numbered department/room folders (`01-`, `02.1-`), or a per-folder `docs/`. Also on "ICM", "room contract", "routing table", "sub-room", or a request to set up / audit / extend such a workspace. Loads how to enter + the base rules; points to the commands and the canon (it does not inline them).
---

# ICM — how to operate here

ICM replaces multi-agent frameworks with filesystem structure: an agent navigates a tree of folders and
markdown that says where to go, what to read, and where to write. **Do not break the structure.** The canon
is NOT inlined below — load it on demand from `docs/` (pointers at the end).

## Detect

Root `AGENTS.md` / `CONTEXT.md`, numbered dept/room folders (`01-`, `02.1-`), a per-folder `docs/`. The real
entry-point `AGENTS.md` may be ABOVE your CWD — if a parent folder also has one, read it first (it routes
between sub-workspaces), then the nested one.

## Start — every productive agent (the light path)

1. Read root **`AGENTS.md`** (identity + base rules), then root **`CONTEXT.md`** (routing); match your task
   to a Routing row.
2. Go to that folder's `CONTEXT.md`; if it's a department, follow its inner table to the room.
3. Read the room's `CONTEXT.md` and its **`tools.json`**; load only what the room's **Inputs** name (incl.
   its own `docs/memory/`) — nothing else.
4. Do the work; write only to the **Outputs** target; drop markers (a script owns state). If **Done-when**
   isn't met, say so — don't declare done early.

Productive agents **never detour through `maintenance/`** — that path is for the commands below.

## Base rules (always)

1. Read `AGENTS.md` first; load only what a contract's Inputs name.
2. Write only to your run's output target + your own `docs/memory/`. Never another room's or run's folder;
   never edit Layer 3 (`docs/`) during a run; never hand-edit machine state — drop markers.
3. Never mutate structure (move/rename/add rooms, change a contract or routing). File a CR; a human disposes.
4. A room MAY evolve its OWN process in place **if it stays within convention** — read the `modify-room`
   rules first. Anything structural or cross-room → `modify-workspace` (gated).

## Commands — maintenance ops (these route through the maintenance dept first)

- **`/icm:new`** (or `/icm -new`) — create or change structure → the **modify-workspace** room.
- **`/icm:assimilate`** (or `/icm -assimilate`) — audit an existing ICM workspace, read-only → the **audit**
  room.

Full procedures: `commands/new.md`, `commands/assimilate.md`.

## Dispatch + canon

- Hand work to another room, or run a review pre-pass → the **`dispatch-subagent`** skill.
- Canon, loaded only when needed: `docs/LAYERS.md` (the 5 layers) · `docs/CONVENTIONS.md` (invariants +
  tooling model) · `docs/ROOM-CONTRACT.md` (the contract shape) · `docs/ROUTING.md` (routing).
