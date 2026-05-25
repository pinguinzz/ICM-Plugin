# {{PROJECT_NAME}} — Agent Contract

You are entering an ICM workspace. Before doing any work here:

1. Read this entire file.
2. Read the workspace overview in `CONTEXT.md`.
3. Match the user's request to a row in the Routing table below.
4. Go to the folder named in `Go to`. Read only the files in `Read`.

If you have the `icm` skill loaded, you already know the rules. If not, read `docs/CONVENTIONS.md` (or the ICM plugin's `docs/CONVENTIONS.md` if installed).

## Identity

{{PROJECT_DESCRIPTION}}

## Folder structure

```
{{FOLDER_TREE}}
```

## Routing

| Task | Go to | Read | Skills |
|------|-------|------|--------|
{{ROUTING_ROWS}}

## Naming conventions

{{NAMING_CONVENTIONS}}

## Invariants you must not break

- A stage writes ONLY to its own `output/`.
- A stage NEVER edits another stage's folders.
- A stage NEVER edits `references/`, `_config/`, or `shared/` during a run.
- `CLAUDE.md`, `GEMINI.md`, `.cursorrules` are stubs pointing to this file. Do not put content in them.

## Maintenance

- Structure changed? Run `/icm:remap`.
- Folder feels heavy? Run `/icm:debloat <path>`.
- Need a new tool? Run `/icm:new-tool`.
- Have a question? Run `/icm:help`.
