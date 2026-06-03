# ICM — Interpretable Context Methodology

> Folder-as-architecture for AI agents. Replaces multi-agent frameworks with a 5-layer filesystem contract
> any agent can read, navigate, and extend safely.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Stdlib only](https://img.shields.io/badge/deps-python%20stdlib-lightgrey)](scripts/)

A deliberately **thin** Claude Code plugin:

- 🛡️ **One guardrail skill** (`icm`) — auto-loads on entering an ICM workspace; carries the 5 layers, the
  base rules, and the invariants.
- 🤝 **One primitive** (`dispatch-subagent`) — spawn a subagent that enters as a generic ICM agent and
  self-routes to a room (worker mode) or runs an auto-review pre-pass (reviewer mode).
- ⌨️ **Two commands** — `/icm:new` (create a workspace / department / room / sub-room) and
  `/icm:assimilate` (convert a folder to ICM, or read-only integrity-check an existing one).
- 🐍 **One stdlib checker** (`scripts/icm_check.py`) — enforces the Invariants; `/icm:assimilate` runs it.
- 📜 **Methodology docs** (`docs/`: LAYERS, CONVENTIONS, ROOM-CONTRACT, ROUTING) as the source of truth.
- 🧪 **Tests** that run the checker against a demo workspace + temp fixtures.

Inspired by the [ICM paper](https://arxiv.org/abs/2603.16021) and the
[original Interpreted-Context-Methodology repo](https://github.com/RinDig/Interpreted-Context-Methdology).

## What is ICM?

Most "AI agents" are prompts + orchestration code that sequence a single model through a workflow. ICM
replaces that scaffolding with **folders and markdown**. The folder structure IS the orchestration: one
agent navigates it, loading only the context relevant to the current step. No frameworks, no DAGs.

### The five layers

| Layer | File | Job |
|---|---|---|
| 0 | `AGENTS.md` (+ stubs `CLAUDE.md`/`GEMINI.md`/`.cursorrules`) | Identity, routing, base rules |
| 1 | root `CONTEXT.md` | Workspace overview |
| 2 | each dept/room/sub-room `CONTEXT.md` | The contract |
| 3 | each `docs/` | Stable rules + memory — read-only during a run |
| 4 | `projects/<run>/...` or room-local `workbench-<id>/` | Per-run artifacts — the only write target |

Full detail: [`docs/LAYERS.md`](docs/LAYERS.md). A workspace can be flat or clustered into **departments**,
and a room can nest **sub-rooms** (recursion by need).

## Install (Claude Code)

```
/plugin install https://github.com/pinguinzz/ICM-Plugin
```

Registers two skills (`icm`, `dispatch-subagent`) and two commands (`/icm:new`, `/icm:assimilate`).

## Skills

| Skill | Purpose |
|---|---|
| `icm` | Guardrail meta-skill — auto-loads on entering an ICM workspace. The 5 layers, base rules, invariants, nested-ICM detection, and the two commands. |
| `dispatch-subagent` | Spawn a subagent that enters as a generic ICM agent and self-routes. **Worker** (do real work in a room, e.g. a gated edit via the maintenance room) or **reviewer** (transitory auto-review pre-pass). Model scales to the work's value. |

## Commands

| Command | What it does |
|---|---|
| `/icm:new` | Create new structure — workspace, department, room, or sub-room. Backbone-locked intake; scaffolds from `templates/parts/` into the fixed skeleton. Additive only. |
| `/icm:assimilate` | Read-only, plan-mode. Convert a non-ICM folder (emits a conversion plan) or integrity-check an ICM one (grills the structure, runs `icm_check.py`, reports, emits a fix plan). Never mutates. |

## Use it without Claude Code

```
# Check any workspace against the Invariants
python scripts/icm_check.py /path/to/workspace            # human-readable
python scripts/icm_check.py /path/to/workspace --json     # machine-readable
python scripts/icm_check.py /path/to/workspace --strict   # warnings fail too
```

The templates and docs are plain files any AGENTS.md-aware agent can use.

## Repo layout

```
icm-marketplace/
├── .claude-plugin/plugin.json
├── AGENTS.md                      the plugin's own agent contract
├── skills/{icm,dispatch-subagent}/SKILL.md
├── commands/{new,assimilate}.md
├── scripts/icm_check.py           single stdlib checker
├── templates/parts/               root-AGENTS · workspace-CONTEXT · dept-CONTEXT · room-CONTEXT · tool-SKILL
├── templates/stubs/               one-line CLAUDE/GEMINI/.cursorrules pointers
├── docs/                          LAYERS · CONVENTIONS · ROOM-CONTRACT · ROUTING
├── examples/content-creator-demo/ checker fixture
└── tests/test_scripts.py
```

## Run the tests

```
python -m unittest discover tests
```

## Design principles

- **One room, one job. Plain text is the only interface.**
- **Layer 3 is read-only during a run; the product layer is the only write target.**
- **Agents drop markers; a script owns machine state. No structure mutation without a CR.**
- **One canonical home per fact. Naming conventions replace databases.**

Full list: [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md).

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

- ICM methodology: Jake Van Clief & David McDermott — [paper](https://arxiv.org/abs/2603.16021) and
  [repo](https://github.com/RinDig/Interpreted-Context-Methdology).
- This plugin distills their methodology into a thin, installable Claude Code artifact.
