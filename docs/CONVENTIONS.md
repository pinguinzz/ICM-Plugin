# ICM Conventions — The Rules

Every agent that enters an ICM workspace MUST follow these rules. They are the load-bearing invariants. Breaking them turns the workspace into a normal messy folder.

## 1. One room, one job

A room does exactly one transformation. If a room does two things, split it.

## 2. Plain text is the only interface

rooms communicate via markdown and JSON files. No databases. No in-memory state. If it isn't on disk, it doesn't exist.

## 3. Numbered rooms encode execution order

`rooms/01-research/`, `rooms/02-script/`, `rooms/03-production/`. The number is part of the contract.
To reorder, rename. (Workspaces template uses named folders instead — see `docs/LAYERS.md`.)

## 4. Every room has a CONTEXT.md

The room contract: Inputs → Process → Outputs. No CONTEXT.md, no room. See `docs/ROOM-CONTRACT.md`.

## 5. Layer 3 (`references/`) is read-only during a run

Reference material is the HowtoWork. Don't edit it while working the product.
Edit between runs, not during.

## 6. Layer 4 (`output/`) is the only write target

A room writes to its own `output/` and nowhere else.
It never writes into another room's folders.

## 7. Handoffs happen via copy or pointer, not by mutation

room N+1 reads room N's `output/`. It does not modify it.
If it needs a different shape, it transforms on read.

## 8. Naming conventions replace databases

- Drafts: `topic_draft.md`
- Versions: `topic_v2.md`, `topic_v3.md`
- Dated artifacts: `YYYY-MM-DD_topic.md` or `YYYY-MM_topic.md`
- room prefixes: `01-`, `02-`, `03-` (zero-padded)

Pick the conventions for your project, document them in root `AGENTS.md`, and never deviate.

## 9. Root `AGENTS.md` carries the routing table

The routing table is a markdown table: `Task | Go to`.
Every agent reads this before doing anything. See`docs/ROUTING.md`.

## 10. Compatibility stubs are pointers, not content

`CLAUDE.md`, `GEMINI.md`, `.cursorrules` — each is a one-liner pointing to `AGENTS.md`.
Never duplicate content. One file, one fact.

## 11. AGENTS.md stays short

Root contract under 50 lines. If it grows, move detail down into workspace or room CONTEXT.md.

## 12. Context files describe the work, not the agent

80% about what the work is, who the audience is, what good looks like. 20% or less about the agent's personality.

## 13. Skills are wired in per workspace, not loaded globally

Skills (tools) belong in the workspace's `skills/` folder and are listed in that workspace's routing table. Never load every skill into every workspace.

## 14. Every output is editable by a human unless room contract says otherwise

No opaque binaries inside the workspace tree if avoidable. If a room emits a binary, also emit a markdown manifest describing what it is. Unless room contract explicitly says otherwise.

## 15. The structure documents itself

`/icm:remap` regenerates routing tables from the folder reality. If a folder isn't reachable from the routing table after a remap, it shouldn't be there. Use `/icm:debloat` to clean it up.

---

## When to break a rule

These rules exist to keep the system simple, transparent, and editable. If a rule blocks legitimate work, write a `DECISIONS.md` in the affected folder explaining the deviation. The deviation must be visible.
