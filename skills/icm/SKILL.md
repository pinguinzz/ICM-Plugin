---
name: icm
description: Use whenever you enter a folder that follows the Interpretable Context Methodology (ICM) — recognizable by an `AGENTS.md` or `CONTEXT.md` at the root, numbered department or room folders (`0-`, `1-`, `02.1-`...), or a `docs-<scope>/` factory layer. Also triggers when the user asks to set up, audit, remap, debloat, or extend an ICM workspace, or mentions "ICM", "folder architecture", "room contract", "department", "Pattern A/B", or "routing table". Loads the 5-layer rules, the conventions every agent must follow, and surfaces the `/icm:*` slash commands.
---

# ICM — Interpretable Context Methodology

You are operating inside (or about to operate on) an ICM workspace. ICM replaces multi-agent frameworks with filesystem structure. A single agent navigates a tree of folders and markdown files that tell it where to go, what to read, and where to write. **Do not break the structure.**

## Before doing anything in this workspace

1. Read the workspace's root `AGENTS.md`. It is the contract.
2. Read the `Routing` table in that file. Match the user's request to a row.
3. Go to the folder named in `Go to`. Read its `CONTEXT.md`. Do not load anything else.
4. If the folder is a **department** (has its own routing table in `CONTEXT.md`), follow its row to the actual **room** folder. Then read that room's `CONTEXT.md`.
5. If you are about to modify the structure (move folders, rename rooms, add files outside the room's output target), STOP and call `/icm:remap` or ask the user.

## Detecting nested ICM

ICM workspaces can be nested. The "real" entry-point `AGENTS.md` may be ABOVE your CWD.

When you enter a workspace:

1. Start at CWD. Is there an `AGENTS.md`? If yes — read it.
2. **Also look above:** is there an `AGENTS.md` in the parent? If yes — THAT is the real entry-point.
   Read the parent first, then the nested one.
3. If two `AGENTS.md` exist at different levels, the higher one routes between
   sub-workspaces or departments; the lower one routes within.

Operating on the nested `AGENTS.md` without reading the parent is a recurring bug — it
loses meta-level context (cross-workspace routing, shared Layer 3 references, parent-scoped operator memory).

## The five layers (memorize)

| Layer | Name | File | Job |
|---|---|---|---|
| 0 | **Frontdoor** | `AGENTS.md` (+ stubs `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) | Global identity, routing |
| 1 | **Reception** | root `CONTEXT.md` | Workspace overview (can be nested) |
| 2 | **Rooms** | room or department `CONTEXT.md` | The contract: Inputs / Process / Outputs / Done-when / Boundaries / Skills |
| 3 | **HowtoWork** | `docs-<scope>/`, `references/`, `_config/`, `shared/` | Stable rules — **read-only during a run** |
| 4 | **Product** | `projects/<id>/`, `workbench-<id>/`, `output/`, `drafts/`, `builds/` | Per-run artifacts — the only place you write |

Full detail: see `docs/LAYERS.md` (sibling of this skill in the plugin).

## Departments and rooms

A workspace can be flat (rooms directly under root) OR clustered into departments.

- **Department** = top-level numbered folder (`0-`, `1-`, `2-`...) that groups related rooms. Has its own `CONTEXT.md` declaring the department's work pattern and routing.
- **Room** = numbered folder containing one specialized capability. Has `CONTEXT.md` (the contract) + `docs-<roomname>/` (room-local factory) + `.claude/` (skill control via `skillOverrides`).
- **Sub-process prefix `NN.1`** = a gate inside stage NN. Rejection at `NN.1` does NOT bump version — only NN's retry does.

Look at root `AGENTS.md` routing first. If a row points to a department, read its `CONTEXT.md` and follow its sub-routing.

## Two work patterns (per department)

A department's `CONTEXT.md` declares which pattern it uses:

- **Pattern A — Centralized Projects.** Department has `projects/<id>/` at the top. Each project has per-room stage subfolders (`<id>/<NN-roomname>/v<N>/`). Used for sequential pipelines with handoffs.
- **Pattern B — Room-Local Workbench.** Each room has its own `workbench-<workID>/`. Used for autonomous / parallel work without pipeline order.

Different departments in the same workspace can use different patterns.

## The invariants you may not break

- A room writes ONLY to its own output target (Pattern A: `projects/<id>/<this-room>/`; Pattern B: `<this-room>/workbench-<id>/`).
- A room NEVER edits another room's folders or another project's folders.
- A room NEVER edits `docs-<scope>/`, `references/`, `_config/`, `shared/` during a run (Layer 3 is factory).
- Naming conventions are documented in root `AGENTS.md` — follow them exactly.
- Compatibility stubs (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`) are one-liners pointing to `AGENTS.md`. Don't put content in them.
- Emoji in folder/file names break tooling on some platforms. Don't introduce them.

Full list: `docs/CONVENTIONS.md`.

## The room contract

Every room `CONTEXT.md` declares **Inputs**, **Process**, **Outputs**, **Done when**, **Hand-off**, **Boundaries**, and **Skills**. The room contract IS the room's `CONTEXT.md` — there is no separate contract file.

If you're authoring or editing a room, follow the shape documented in `docs/ROOM-CONTRACT.md`.

## Skill control per room

ICM workspaces typically silence skills at workspace root and re-enable per room via `skillOverrides`:

- Workspace `.claude/settings.local.json`: all user-scope skills set to `"off"` baseline.
- Each room's `.claude/settings.local.json`: re-enables only what that room uses.

Effect: autonomous agents in rooms that don't need a skill don't see it in the listing. Reduces token bloat.

## Commands you may invoke

When the situation calls for it, invoke a slash command rather than doing the work by hand. These exist to save tokens and prevent structural drift.

| Command | When to invoke |
|---|---|
| `/icm:set-up` | The folder is not yet an ICM workspace, or the user asks to scaffold one (workspace, department, or room). |
| `/icm:remap` | The structure has changed (folder added, renamed, deleted) or the routing table looks stale. |
| `/icm:debloat` | A folder feels heavy — oversized CONTEXTs, dead outputs, naming violations, orphaned `docs-<scope>/` files. |
| `/icm:new-tool` | The user needs a new reusable capability (skill) wired into a specific room. |
| `/icm:help` | The user asks a methodology question ("what's a department", "where do voice files go", "Pattern A vs B"). |

Do not invoke commands speculatively. Invoke when the trigger condition is clearly met.

## When the user asks you to do work

1. Read root `AGENTS.md`.
2. Match request → row in Routing table.
3. Navigate to the target. If it's a department, read its `CONTEXT.md` and follow its sub-routing.
4. Read the destination room's `CONTEXT.md` (the contract).
5. Load the files listed under Inputs.
6. Do the work. Write outputs to the location declared in Outputs.
7. If the room's `Done when` checklist isn't met, say so explicitly. Do not declare done early.

## When the user asks a methodology question

Invoke `/icm:help`. Don't paraphrase the docs from memory — load them.

## What this skill is not

- Not a framework. There is no orchestration code.
- Not the best multi-agent system. Try to keep one agent, one workspace, structure on disk.
- Not opinionated about your domain. The methodology works for content pipelines, research workflows, dev projects, consulting practices, anything sequential or autonomous with structured work.
