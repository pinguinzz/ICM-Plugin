# Content Creator Workspace — Agent Contract

> **THIS IS AN EXAMPLE WORKSPACE.** Three named workspaces (no numbered pipeline). Best when work is not strictly sequential — e.g. content creators, consultants, devs with parallel concerns. Replace identity, references, and content with your own.

You are entering an ICM workspace. Before any work:

1. Read this file.
2. Read `CONTEXT.md` for the workspace overview.
3. Match the user's request to a row in the Routing table.
4. Go to the folder. Load only the files in `Read`.

## Identity

A solo content creator producing short-form educational content across YouTube, Instagram, and a newsletter. Voice is plain, direct, and earned.

*(Replace with your real identity.)*

## Folder structure

```
./
├── AGENTS.md                       # this file
├── CLAUDE.md, GEMINI.md, .cursorrules   # stubs
├── CONTEXT.md                      # workspace overview
├── _config/                        # Layer 3 — brand, naming
├── shared/                         # Layer 3 — voice, audience
├── skills/                         # workspace-scoped skills
├── script-lab/                     # ideation → drafts → final
├── production/                     # briefs → specs → builds → output
└── distribution/                   # platforms, scheduling, analytics
```

## Routing

| Task | Go to | Read | Skills |
|------|-------|------|--------|
| Write or brainstorm | `script-lab/` | `CONTEXT.md`, `../shared/voice.md`, `../shared/audience.md` | — |
| Build or produce | `production/` | `CONTEXT.md`, `../_config/brand.md` | — |
| Publish or repurpose | `distribution/` | `CONTEXT.md` | — |
| Methodology question | (here) | the ICM plugin's `docs/` | — |

## Naming conventions

- Drafts: `topic_draft.md`, `topic_v2.md`, `topic_final.md`
- Production specs: `topic_spec.md`
- Published artifacts: `YYYY-MM_platform_topic.md`

## Invariants

- Workspaces write only to their own subfolders.
- `_config/` and `shared/` are read-only during a run.
- Stubs are pointers. Don't put content in them.

## Maintenance

`/ICM-remap` · `/ICM-debloat` · `/ICM-new-tool` · `/ICM-help`
