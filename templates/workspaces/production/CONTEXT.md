# Production

## Purpose

Turn a finished script into produced output (video, audio, visual asset).

## Inputs

| From | File / Folder | What to load |
|------|---------------|--------------|
| `../script-lab/final/<topic>_final.md` | full file | the script |
| `../_config/brand.md` | full file | visual rules |

## Process

1. Read the script.
2. Write a production brief in `briefs/<topic>_brief.md`.
3. Write a per-scene spec in `specs/<topic>_spec.md`.
4. Build assets in `builds/<topic>/` (raw working files).
5. Export finished asset to `output/<topic>.<ext>`.

## Outputs

| To | File | Format |
|----|------|--------|
| `./briefs/` | `<topic>_brief.md` | markdown |
| `./specs/` | `<topic>_spec.md` | markdown per-scene |
| `./builds/` | `<topic>/*` | working files |
| `./output/` | `<topic>.<ext>` | finished asset |

## Done when

- Brief matches the script.
- Spec covers every scene.
- Output is in `output/`.

## Hand-off

Distribution reads from `./output/`. See `../distribution/CONTEXT.md`.
