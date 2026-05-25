# Content Pipeline — Workspace Overview

> **EXAMPLE.** Adapt to your own project.

## What this workspace does

Takes a topic and produces a finished short-form video. Three stages, human review between each.

## Stages

| # | Stage | Transforms | Output |
|---|-------|------------|--------|
| 01 | research | topic → structured research | `01-research/output/<topic>.md` |
| 02 | script | research → polished script | `02-script/output/<topic>_final.md` |
| 03 | production | script → animation specs + Remotion code | `03-production/output/<topic>_*` |

## When in doubt

- Where do I write? → Your stage's `output/`. Nowhere else.
- Where's the voice guide? → `shared/voice.md`.
- Where's the brand? → `_config/brand.md`.
- What's a stage contract? → Open the stage's `CONTEXT.md`.

## Skills wired in

(None yet. Add via `/ICM-new-tool`.)
