# Stage 03 — Production

## Purpose

Turn a final script into animation specs and Remotion-ready React components.

## Inputs

| From | File / Folder | What to load |
|------|---------------|--------------|
| `../02-script/output/<topic>_final.md` | full file | the script |
| `references/component-registry.md` | full file | reusable Remotion components |
| `../../_config/brand.md` | full file | visual rules |

## Process

1. Break the script into scenes (one per script section).
2. For each scene, write a spec: visual, timing, component(s) used, audio cue.
3. Save spec as `output/<topic>_spec.md`.
4. Generate scene JSON: `output/<topic>_scenes.json` (array of `{id, start, duration, component, props}`).
5. (Optional) Scaffold Remotion component files in `output/<topic>_components/`.

## Outputs

| To | File | Format |
|----|------|--------|
| `./output/` | `<topic>_spec.md` | markdown per-scene spec |
| `./output/` | `<topic>_scenes.json` | JSON array of scenes |
| `./output/` | `<topic>_components/` | React/Remotion components (optional) |

## Done when

- Every script section has a scene spec.
- Every scene names a component from the registry (or flags a new one needed).
- Total run time matches the script (±10%).

## Hand-off

External: Remotion renders `output/<topic>_scenes.json` to a video file. The video lives outside the ICM workspace.
