---
name: icm
description: Use whenever you enter a folder that follows the Interpretable Context Methodology (ICM) — recognizable by an `AGENTS.md` or `CONTEXT.md` at the root, numbered department or room folders (`01-`, `1-`, `02.1-`...), or a per-folder `docs/` layer. Also triggers when the user asks to set up, assimilate, audit, or extend an ICM workspace, or mentions "ICM", "folder architecture", "room contract", "department", "routing table", or "sub-room". Loads the 5-layer rules, the base rules every agent must follow.
---

# ICM — Interpretable Context Methodology

You are operating inside (or about to operate on) an ICM workspace. ICM replaces multi-agent frameworks
with filesystem structure: a agent navigates a tree of folders and markdown files that tell it
where to go, what to read, and where to write. **Do not break the structure.**

## The three base rules (always)

1. **Read `AGENTS.md` first** (what this place is + how to enter it), then root **`CONTEXT.md`** for the
   routing table: match your task → a Routing row → go to that folder's `CONTEXT.md` (department → room →
   sub-room). Load only what the room's **Inputs** name — not the whole tree.
2. **Write only to your output target.** A room writes to its run folder (sequential:
   `projects/<run>/<this-room>/v<N>/`; parallel: `<this-room>/workbench-<id>/`) and its own `docs/memory/`.
   Never another room's or another run's folder. Never edit Layer 3 (`docs/`) during a run. Never hand-edit
   machine state (`_state.json`/dashboard) — **drop markers** and let the reconciler script write state.
3. **Never mutate structure.** Don't move/rename/add rooms or change a contract/routing mid-run. Propose
   changes via the workspace's change-request inbox; a human disposes.

## Before doing anything

1. Read root `AGENTS.md` (identity + base rules). 2. Read root `CONTEXT.md` and match the request to a
Routing row. 3. Go to the `Go to` folder, read its `CONTEXT.md`, load nothing else. 4. If it's a
**department** (its own routing table), follow its row to
the room, then read the room's `CONTEXT.md`. 5. Load only the files the contract's **Inputs** name.
6. Do the work; write to the **Outputs** location. 7. If the room's **Done-when** isn't met, say so — don't
declare done early.

## Detecting nested ICM

The real entry-point `AGENTS.md` may be ABOVE your CWD. Start at CWD; if there's an `AGENTS.md`, read it —
but also look up: if a parent also has one, THAT is the real entry-point (read parent first, then the
nested one). The higher routes between sub-workspaces/departments; the lower routes within. Operating on
the nested `AGENTS.md` without reading the parent loses cross-workspace routing and shared Layer 3.

## The five layers

| Layer | Name | File | Job |
|---|---|---|---|
| 0 | Frontdoor | root `AGENTS.md` (+ stubs `CLAUDE.md`/`GEMINI.md`/`.cursorrules`) | What this place is + how to enter + base rules |
| 1 | Reception | root `CONTEXT.md` | Maps + routing (where to go) |
| 2 | Rooms | each dept/room/sub-room `CONTEXT.md` | The contract |
| 3 | HowtoWork | each `docs/` | Stable rules + memory — read-only during a run |
| 4 | Product | `projects/<run>/...` or room-local `workbench-<id>/` | Per-run artifacts — your only write target |

Full detail: `docs/LAYERS.md`.

## Departments, rooms, sub-rooms

A workspace can be flat (rooms under root) or clustered into **departments** (top-level numbered folders
grouping rooms). A **room** is one capability; it may nest **sub-rooms** (`NN.n-<name>`) when a subprocess
ramifies — recursion **by need**, no depth cap. `NN.0` is the QA / auto-review sub-room (runs last);
`NN.1+` are productive. Each node has its own `CONTEXT.md` + `docs/`.

## Work patterns (each department declares one)

- **Sequential pipeline** — centralized `projects/<run>/<NN-room>/`; rooms hand off in order.
- **Parallel pipeline** — room-local `workbench-<id>/`; capability rooms run independently, no fixed order.

## Invariants you may not break

Five layers fixed · routing resolves · `docs/` per node (NOT `docs-<name>/`) · product layer is the only
write target · agents drop markers, a script owns state · no structure mutation without a CR · one-way
cross-references · one canonical home per fact · stubs are pointers · no emoji in names. Full list +
Guidelines: `docs/CONVENTIONS.md`. The room contract shape: `docs/ROOM-CONTRACT.md`.

## Skill control per room (optional)

ICM workspaces often silence skills at root (`.claude/settings.local.json` → all `"off"`) and re-enable
per room via `skillOverrides`, so an agent in a room sees only the skills it needs. Keeps context lean.

## Commands

| Command | When to invoke |
|---|---|
| `/icm:new` | Create new structure — a workspace, department, room, or sub-room. Backbone-locked intake; scaffolds into the fixed skeleton. |
| `/icm:assimilate` | Convert an existing folder into ICM, **or** integrity-check an existing ICM workspace (read-only: grills the structure, reports, emits a plan). |

Dispatching work to another room, or a review pre-pass, is the `dispatch-subagent` skill.

## What this is not

Not a framework (no orchestration code). Not the best multi-agent system — keep one agent, one workspace,
structure on disk. Not opinionated about your domain.
