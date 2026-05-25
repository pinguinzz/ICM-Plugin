---
description: Scaffold a new ICM workspace in the current folder (or a target folder). Prompts for blank vs assimilate, then pipeline vs workspaces. Wires up AGENTS.md + stubs + routing table.
---

# /ICM-set-up

Scaffold or convert a folder into an ICM workspace.

## What you (the agent) do

1. **Locate the plugin scripts.** Resolve `$SCRIPTS` (the absolute path to the plugin's `scripts/` directory) using this order, stopping at the first hit:
   a. The env var `$CLAUDE_PLUGIN_ROOT` if set → `$CLAUDE_PLUGIN_ROOT/scripts/`.
   b. Walk up from this command file's location until you find a directory containing both `scripts/icm_scaffold.py` and `.claude-plugin/plugin.json` (or the legacy `plugin.json`).
   c. Look in the standard install paths: `~/.claude/plugins/icm/scripts/`, then `~/.claude/plugins/cache/**/icm/scripts/`.
   d. If still not found, ask the user for the plugin path explicitly. Don't guess.

2. **Detect what's already there.** Run:
   ```
   python "$SCRIPTS/icm_detect.py" "$ARGUMENTS"
   ```
   If `$ARGUMENTS` is empty, use the current working directory.

3. **Branch on detection result:**
   - If `is_icm_workspace: true` → tell the user the folder is already an ICM workspace and offer to run `/ICM-remap` or `/ICM-debloat` instead. Stop.
   - If the folder is empty (or has only the user's stray files): proceed to **blank scaffold**.
   - If the folder has content but no AGENTS.md: proceed to **assimilation**.

4. **Blank scaffold flow:**
   a. Ask the user which template fits (use AskUserQuestion, two options):
      - **pipeline** — numbered stages (`01-research/`, `02-script/`, ...). Best for sequential workflows with human review.
      - **workspaces** — named workspaces (`script-lab/`, `production/`, ...). Best for parallel modes of work (content creators, consultants, devs).
   b. Run:
      ```
      python "$SCRIPTS/icm_scaffold.py" --template <choice> --target "<target>"
      ```
   c. Read the new `AGENTS.md`. Ask the user 2–4 short questions to fill identity:
      - Project name?
      - One-line description of the project?
      - Primary audience or stakeholder?
      - Anything to add to or remove from the example structure?
   d. Edit `AGENTS.md` to substitute the example identity with the user's answers. Keep the EXAMPLE marker until they confirm they have replaced all placeholder content.
   e. Run:
      ```
      python "$SCRIPTS/icm_remap.py" "<target>" --write
      ```
   f. Run a final audit:
      ```
      python "$SCRIPTS/icm_audit.py" "<target>"
      ```
   g. Report: files created, what to edit next.

5. **Assimilation flow:**
   a. Walk the existing tree (use Glob / LS). Build a one-page summary of what's there.
   b. Propose a mapping to the 5 layers. Ask the user to confirm each major decision (single AskUserQuestion call with the proposed mapping).
   c. Generate AGENTS.md from `templates/parts/root-AGENTS.md` with the proposed routing table.
   d. Generate workspace / stage CONTEXT.md files from `templates/parts/workspace-CONTEXT.md` and `templates/parts/stage-CONTEXT.md`.
   e. Drop in the stub files from `templates/stubs/` if they don't exist.
   f. Do NOT move or rename any of the user's existing files. Only add the ICM scaffolding around them.
   g. Run `icm_remap.py --write` and `icm_audit.py`. Report.

## Invariants

- Never overwrite a non-empty `AGENTS.md` without explicit confirmation.
- Never delete user files. Use `_archive/` if you need to move something.
- Always end with an audit. If it shows errors, surface them before declaring done.

## Args

`$ARGUMENTS` — optional target folder (defaults to cwd).
