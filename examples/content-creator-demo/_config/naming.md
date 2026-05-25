# Naming Conventions

> **EXAMPLE.** Keep what fits, change the rest.

## Stage outputs

- Research: `YYYY-MM-DD_topic.md` (dated; topics may recur)
- Script drafts: `topic_draft.md`, `topic_v2.md`, ..., `topic_final.md`
- Production: `topic_spec.md`, `topic_scenes.json`, `topic_render.mp4`

## Folder prefixes

- Stages always zero-padded numeric: `01-`, `02-`, ..., `10-`, `11-`
- Workspace-internal subfolders use unprefixed lowercase: `ideas/`, `drafts/`, `final/`

## File names

- All lowercase. Words separated by `_` (underscore) or `-` (hyphen) — pick one and stick to it. This project uses `_`.
- No spaces. No accented characters in filenames.

## Versioning

- Manual versions in filename suffix: `_v2`, `_v3`.
- `_final` is reserved for the artifact handed to the next stage.
- If a `_final` needs to change, bump to `_v<n+1>` first.
