# ICM — Interpretable Context Methodology

> Folder-as-architecture for AI agents. Replaces multi-agent frameworks with a 5-layer filesystem contract any agent can read, navigate, and extend safely.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-15%20passing-brightgreen)](tests/)
[![Stdlib only](https://img.shields.io/badge/deps-python%20stdlib-lightgrey)](scripts/)

A Claude Code plugin that ships:

- 🗂️ **Two scaffold templates** — numbered pipeline (`01-research/` → `02-script/`...) or named workspaces (`script-lab/`, `production/`, ...).
- 🤖 **A skill** that auto-loads when an agent enters an ICM workspace, so it knows the rules.
- ⌨️ **Five slash commands** (`/ICM-set-up`, `/ICM-remap`, `/ICM-debloat`, `/ICM-new-tool`, `/ICM-help`).
- 🐍 **Six Python helper scripts** (stdlib only) that do the token-heavy structural work, returning JSON the agent reasons over.
- 📜 **Methodology docs** (LAYERS, CONVENTIONS, STAGE-CONTRACT, ROUTING) as the source of truth — no paraphrasing.
- 🧪 **15 tests** that exercise the scripts against a real example workspace.

Inspired by the [ICM paper](https://arxiv.org/abs/2603.16021) and the [original Interpreted-Context-Methodology repo](https://github.com/RinDig/Interpreted-Context-Methdology).

---

## What is ICM?

Most "AI agents" you see in production are not autonomous — they are prompts + orchestration code (Python, JS, whatever) that sequence a single model through a workflow. The AI is ~10% of the system; the rest is engineering scaffolding.

**ICM replaces that scaffolding with folders and markdown files.** The folder structure IS the orchestration. A single agent navigates it, loading only the context relevant to the current step. No frameworks. No agent classes. No DAGs to maintain.

### The five layers

| Layer | File | Job |
|---|---|---|
| 0 | `AGENTS.md` (+ stubs `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) | Global identity, routing |
| 1 | root `CONTEXT.md` | Workspace overview |
| 2 | stage `CONTEXT.md` | Inputs / Process / Outputs |
| 3 | `references/`, `_config/`, `shared/` | Stable rules — read-only during a run |
| 4 | `output/`, `drafts/`, `builds/` | Per-run artifacts — only write target |

Full detail in [`docs/LAYERS.md`](docs/LAYERS.md).

### Why this is agent-agnostic

`AGENTS.md` is the canonical file. `CLAUDE.md`, `GEMINI.md`, and `.cursorrules` are one-line stubs that just say "See AGENTS.md". Any agent's native loader picks up the pointer; the contract itself lives in one place.

---

## Install (Claude Code)

```bash
# In Claude Code:
/plugin install /path/to/ICM-skill
# or from a git repo:
/plugin install <your-github-url>
```

The plugin auto-registers:
- the `icm` skill
- the five `/ICM-*` slash commands

## Use it without Claude Code

The scripts and templates are plain files. Use them from any shell:

```bash
# Scaffold a new ICM workspace from the pipeline template
python ICM-skill/scripts/icm_scaffold.py --template pipeline --target ./my-workspace

# Detect / audit an existing workspace
python ICM-skill/scripts/icm_detect.py ./my-workspace
python ICM-skill/scripts/icm_audit.py ./my-workspace

# Regenerate the routing table from current folder reality
python ICM-skill/scripts/icm_remap.py ./my-workspace --write

# Propose archival of bloat (dry-run by default)
python ICM-skill/scripts/icm_debloat.py ./my-workspace

# Add a new skill (tool) and wire it into the routing table
python ICM-skill/scripts/icm_register_tool.py \
    --workspace ./my-workspace \
    --tool-name web-search \
    --tool-description "Search the web for sources" \
    --wire-into "research"
```

Any AGENTS.md-aware agent (Codex CLI, Cursor, others) can then enter the workspace and follow the contract.

---

## Slash commands

| Command | What it does |
|---|---|
| `/ICM-set-up` | Scaffolds a new workspace OR assimilates an existing folder into the 5-layer structure. Asks: blank vs assimilate; pipeline vs workspaces. |
| `/ICM-remap` | Walks the tree, regenerates the routing table in root `AGENTS.md`, validates pointer integrity. Dry-runs first; asks before writing. |
| `/ICM-debloat` | Flags oversized CONTEXTs, dead outputs, duplicate references, superseded drafts. Archives (never deletes) on confirmation. |
| `/ICM-new-tool` | Creates a new SKILL.md scoped to a workspace/stage and wires it into the relevant routing-table row. |
| `/ICM-help` | Answers methodology questions grounded in the plugin's `docs/`. No paraphrasing. |

---

## Repo layout

```
ICM-skill/
├── plugin.json                 Claude Code plugin manifest
├── AGENTS.md                   the plugin's own agent contract
├── skills/icm/SKILL.md         the skill that loads when entering an ICM workspace
├── commands/                   five /ICM-* slash commands
├── scripts/                    Python helpers (stdlib only)
│   ├── _lib.py                 shared helpers
│   ├── icm_detect.py
│   ├── icm_audit.py
│   ├── icm_scaffold.py
│   ├── icm_remap.py
│   ├── icm_debloat.py
│   └── icm_register_tool.py
├── templates/
│   ├── pipeline/               populated 3-stage content-creator example (numbered)
│   ├── workspaces/             populated 3-workspace content-creator example (named)
│   ├── parts/                  atomic templates (CONTEXT.md, AGENTS.md, tool-SKILL.md)
│   └── stubs/                  one-line CLAUDE.md / GEMINI.md / .cursorrules pointers
├── docs/                       methodology source of truth
│   ├── LAYERS.md
│   ├── CONVENTIONS.md
│   ├── STAGE-CONTRACT.md
│   └── ROUTING.md
├── examples/
│   └── content-creator-demo/   real scaffolded workspace used by tests
└── tests/
    └── test_scripts.py         15 tests, stdlib only
```

---

## Run the tests

```bash
python -m unittest discover tests
```

Expected: `Ran 15 tests in ~3s. OK`.

---

## Design principles

- **One stage, one job.**
- **Plain text is the only interface.**
- **Layer 3 (references) is read-only during a run; Layer 4 (output) is the only write target.**
- **Naming conventions replace databases.**
- **The structure documents itself** — `/ICM-remap` regenerates routing from folder reality.

Full list: [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) (15 rules).

---

## Comparison: ICM vs framework approach

| Task | Framework (CrewAI, LangChain) | ICM |
|---|---|---|
| Change stage order | Edit code, redeploy | Rename folders |
| Modify a prompt | Edit agent config | Edit markdown |
| Add/remove stage | Write class, update orchestrator | Add/delete folder |
| Inspect state | Add logging, build dashboard | Open folder |
| Hand off to teammate | Document setup, deps | Copy folder |
| Who can edit | Developer | Anyone with a text editor |

---

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

- ICM methodology: Jake Van Clief & David McDermott — original [paper](https://arxiv.org/abs/2603.16021) and [repo](https://github.com/RinDig/Interpreted-Context-Methdology).
- This plugin reorganizes their methodology into a Claude Code-installable artifact and adds tooling (audit, remap, debloat, tool registration, tests).
