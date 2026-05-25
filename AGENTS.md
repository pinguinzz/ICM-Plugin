# ICM Plugin — Agent Contract

You are inside the **ICM plugin source tree**, not an ICM workspace. This folder is the plugin that gets installed and used elsewhere.

## What this plugin ships

- `skills/icm/SKILL.md` — the skill that auto-loads when an agent enters an ICM workspace.
- `commands/ICM-*.md` — slash commands for setup, remap, debloat, tool authoring, help.
- `scripts/*.py` — Python helpers (stdlib only) that do the token-heavy structural work.
- `templates/{pipeline,workspaces}/` — two populated example scaffolds the agent can copy.
- `templates/parts/` — atomic templates (single CONTEXT.md, stub files, tool skill).
- `docs/` — the methodology source of truth. Read before editing anything else.
- `examples/content-creator-demo/` — a real worked workspace used by the test suite.
- `tests/` — pytest-style tests that run the scripts against the demo.

## If you are editing this plugin

1. Read `docs/CONVENTIONS.md` first. The plugin itself follows ICM principles.
2. Don't add features that duplicate what a script already does.
3. Don't make templates that depend on Claude-specific behavior. Stubs make us agent-agnostic.
4. Keep the scripts stdlib-only. No `pip install`.
5. Keep `SKILL.md` under ~200 lines.
6. After any change, run `python -m pytest tests/` from the plugin root.

## If you are NOT editing this plugin

You probably don't need to be here. The end-user touches the templates and commands, not the source.

## Compatibility stubs

This file is the canonical agent contract. `CLAUDE.md`, `GEMINI.md`, and `.cursorrules` (if present) are one-line pointers to this file.
