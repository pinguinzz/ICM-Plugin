# ICM Plugin — Agent Contract

You are inside the **ICM plugin source tree**, not an ICM workspace. This folder is the plugin that gets
installed and used elsewhere.

## What this plugin ships

- `skills/icm/SKILL.md` — the guardrail skill that auto-loads when an agent enters an ICM workspace
  (5 layers, base rules, invariants, the two commands).
- `skills/dispatch-subagent/SKILL.md` — canonical primitive: spawn a subagent that enters as a generic ICM
  agent and self-routes (worker or reviewer mode).
- `commands/new.md`, `commands/assimilate.md` — the two slash commands (`/icm:new`, `/icm:assimilate`).
- `scripts/icm_check.py` — the single stdlib checker that enforces the Invariants (`/icm:assimilate` runs it).
- `templates/parts/` — atomic templates (`root-AGENTS`, `workspace-CONTEXT`, `dept-CONTEXT`, `room-CONTEXT`,
  `tool-SKILL`); `templates/stubs/` — one-line `CLAUDE.md`/`GEMINI.md`/`.cursorrules` pointers.
- `docs/` — the methodology source of truth (LAYERS, CONVENTIONS, ROOM-CONTRACT, ROUTING). Read before
  editing anything else.
- `examples/content-creator-demo/` — a minimal worked workspace used as a checker fixture by the tests.
- `tests/` — stdlib unittest suite that runs `icm_check.py` against the demo + temp workspaces.

## If you are editing this plugin

1. Read `docs/CONVENTIONS.md` first. The plugin itself follows ICM principles.
2. Keep it thin — don't re-add the retired command/script proliferation. Deep workflow logic belongs in a
   workspace's `maintenance` dept, not here; this plugin is the generic, brand-agnostic distillation.
3. Keep the scripts stdlib-only. No `pip install`.
4. Keep templates agent-agnostic (stubs keep us multi-tool).
5. Keep each `SKILL.md` under ~200 lines.
6. After any change, run `python -m unittest discover tests` from the plugin root.
7. Bump `.claude-plugin/plugin.json` version, commit + push, then sync the cache (see the 02-ICM room
   `CONTEXT.md`).

## If you are NOT editing this plugin

You probably don't need to be here. End-users touch the templates and the two commands, not the source.

## Compatibility stubs

This file is the canonical agent contract. `CLAUDE.md`, `GEMINI.md`, `.cursorrules` (if present) are
one-line pointers to it.
