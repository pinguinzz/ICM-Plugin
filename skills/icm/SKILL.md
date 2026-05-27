---
name: icm
description: Use whenever you enter a folder that follows the Interpretable Context Methodology (ICM) — recognizable by an `AGENTS.md` or `CONTEXT.md` at the root, numbered `stages/` folders, or a `_config/` + `shared/` pair. Also triggers when the user asks to set up, audit, remap, debloat, or extend an ICM workspace, or mentions "ICM", "folder architecture", "stage contract", or "routing table". This skill loads the 5-layer context rules, the conventions every agent must follow, and surfaces the `/icm:*` slash commands.
---

# ICM — Interpretable Context Methodology

You are operating inside (or about to operate on) an ICM workspace. ICM replaces multi-agent frameworks with filesystem structure. A single agent navigates a tree of folders and markdown files that tell it where to go, what to read, and where to write. **Do not break the structure.**

## Before doing anything in this workspace

1. Read the workspace's root `AGENTS.md`. It is the contract.
2. Read the `Routing` table in that file. Match the user's request to a row.
3. Go to the folder named in `Go to`. Read the files in `Read`. Do not load anything else.
4. If you are about to modify the structure (move folders, rename stages, add files outside `output/`), STOP and call `/icm:remap` or ask the user.

## Detecting nested ICM

ICM workspaces can be nested. The "real" entry-point `AGENTS.md` may be ABOVE your CWD.

When you enter a workspace:

1. Start at CWD. Is there an `AGENTS.md`? If yes — read it.
2. **Also look above:** is there an `AGENTS.md` in the parent? If yes — THAT is the real entry-point.
   Read the parent first, then the nested one.
3. If two `AGENTS.md` exist at different levels, the higher one routes between
   sub-workspaces; the lower one routes between stages inside the selected sub-workspace.

Operating on the nested `AGENTS.md` without reading the parent is a recurring bug — it
loses meta-level context (cross-workspace routing, shared Layer 3 references, parent-scoped operator memory).

## The five layers (memorize)

| Layer | File | Job |
|---|---|---|
| 0 | `AGENTS.md` (+ stubs `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) | Global identity, routing |
| 1 | root `CONTEXT.md` | Workspace overview |
| 2 | stage `CONTEXT.md` | The stage contract: Inputs / Process / Outputs |
| 3 | `references/`, `_config/`, `shared/` | Stable rules — **read-only during a run** |
| 4 | `output/`, `drafts/`, `builds/` | Per-run artifacts — the only place you write |

Full detail: see `docs/LAYERS.md` (sibling of this skill in the plugin).

## The invariants you may not break

- A stage writes ONLY to its own `output/`.
- A stage NEVER edits another stage's folders.
- A stage NEVER edits `references/` / `_config/` / `shared/` during a run.
- Naming conventions are documented in root `AGENTS.md` — follow them exactly.
- Compatibility stubs (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`) are one-liners pointing to `AGENTS.md`. Don't put content in them.

Full list: `docs/CONVENTIONS.md`.

## The stage contract

Every stage `CONTEXT.md` declares **Inputs**, **Process**, **Outputs**, and **Done when**. If you're authoring or editing a stage, follow `docs/STAGE-CONTRACT.md`.

## Commands you may invoke

When the situation calls for it, invoke a slash command rather than doing the work by hand. These exist to save tokens and prevent structural drift.

| Command | When to invoke |
|---|---|
| `/icm:set-up` | The folder is not yet an ICM workspace, or the user asks to scaffold one. |
| `/icm:remap` | The structure has changed (folder added, renamed, deleted) or the routing table looks stale. |
| `/icm:debloat` | A folder feels heavy — oversized CONTEXTs, dead outputs, naming violations. |
| `/icm:new-tool` | The user needs a new reusable capability (skill) wired into a specific workspace/stage. |
| `/icm:help` | The user asks a methodology question ("what's a stage contract", "where do voice files go"). |

Do not invoke commands speculatively. Invoke when the trigger condition is clearly met.

## When the user asks you to do work

1. Read root `AGENTS.md`.
2. Match request → row in Routing table.
3. Read the files in `Read`.
4. Do the work. Write outputs to the row's stage `output/`.
5. If the stage's `Done when` checklist isn't met, say so explicitly. Do not declare done early.

## When the user asks a methodology question

Invoke `/icm:help`. Don't paraphrase the docs from memory — load them.

## What this skill is not

- Not a framework. There is no orchestration code.
- Not a multi-agent system. One agent, one workspace, structure on disk.
- Not opinionated about your domain. The methodology works for content pipelines, research workflows, dev projects, consulting practices, anything sequential with human review.
