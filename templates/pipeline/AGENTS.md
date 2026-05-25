# Content Pipeline — Agent Contract

> **THIS IS AN EXAMPLE WORKSPACE.** It demonstrates a 3-stage content pipeline (research → script → production). Replace the project name, identity, references, and outputs with your own work. Keep the structure.

You are entering an ICM workspace. Before any work:

1. Read this file.
2. Read `CONTEXT.md` for the workspace overview.
3. Match the user's request to a row in the Routing table.
4. Go to the folder in `Go to`. Load only the files in `Read`.

If the `icm` skill is available, it has the full rule set. Otherwise, read `docs/CONVENTIONS.md` from the ICM plugin.

## Identity

A single-person content studio producing short-form educational videos. Voice is plain, direct, lightly opinionated. Audience is technical-curious non-engineers.

*(Replace this with your real identity.)*

## Folder structure

```
./
├── AGENTS.md                       # this file
├── CLAUDE.md, GEMINI.md, .cursorrules   # stubs → AGENTS.md
├── CONTEXT.md                      # workspace overview
├── _config/                        # Layer 3 — brand, naming
├── shared/                         # Layer 3 — voice, audience
├── skills/                         # workspace-scoped skills
└── stages/
    ├── 01-research/                # topic → structured research
    ├── 02-script/                  # research → polished script
    └── 03-production/              # script → animation specs + code
```

## Routing

| Task | Go to | Read | Skills |
|------|-------|------|--------|
| Research a topic | `stages/01-research/` | `CONTEXT.md`, `../../shared/audience.md` | — |
| Draft a script | `stages/02-script/` | `CONTEXT.md`, `../../shared/voice.md`, `../01-research/output/` | — |
| Build an animation | `stages/03-production/` | `CONTEXT.md`, `references/component-registry.md`, `../02-script/output/` | — |
| Methodology question | (here) | the ICM plugin's `docs/` | — |

## Naming conventions

- Research outputs: `YYYY-MM-DD_topic.md`
- Script drafts: `topic_draft.md`, `topic_v2.md`, `topic_final.md`
- Production builds: `topic_spec.md`, `topic_scenes.json`, `topic_render.mp4`

## Invariants

- A stage writes ONLY to its own `output/`.
- A stage NEVER edits another stage's folders.
- `_config/` and `shared/` are read-only during a run.
- Stubs are pointers. Don't put content in them.

## Maintenance

- Structure changed? `/icm:remap`
- Folder bloated? `/icm:debloat <path>`
- Need a tool? `/icm:new-tool`
- Question? `/icm:help`
