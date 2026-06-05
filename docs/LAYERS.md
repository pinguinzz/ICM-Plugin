# The 5 Layers

ICM organizes context as a hierarchy. Each layer answers one question, lives in its own file, and is
loaded only when the task needs it. Less irrelevant context = sharper model output 
Key is selected information, not compression of information. Keep L3 files atomical and referenced to be loaded when needed only.

| Layer | Name | Question it answers | File / Folder | Typical size | Changes |
|---|---|---|---|---|---|
| 0 | Frontdoor | What is this place + how do I enter it? (identity + base rules) | `AGENTS.md` at workspace root (+ stubs `CLAUDE.md`, `GEMINI.md`, `.cursorrules`) | ~800 tokens | Never (after setup) |
| 1 | Reception | Where do I go? (maps + routing + overview) | `CONTEXT.md` at workspace root | ~300 tokens | Setup only |
| 2 | Rooms | What work do I do? (the contract) | `CONTEXT.md` in each department / room / sub-room | 200–500 tokens | Per node |
| 3 | HowtoWork | What rules apply? (references + memory) | each `docs/` folder | 500–2k tokens | Between runs |
| 4 | Product | What am I working on? (per-run artifacts) | `projects/` (or a room-local `workbench-<id>/`) | Variable | Every run |

## Why layers

If an agent loads everything in the project, it spends tokens on irrelevant context and the relevant
context gets buried ("lost in the middle"). Agents retain better the information the get at the start of the session, and the latest informations they got.
If it loads only the right layers for the current job as it needs it, it stays sharp. Each navigation step mid work resharp the context window.

## The split that matters most: Layer 3 vs Layer 4

- **Layer 3 is the factory.** Stable rules, voice guides, conventions, memory. Read-only *during* a run;
  edit it *between* runs.
- **Layer 4 is the product.** The artifact each run produces. Write as needed and prefer versionating than discard.
Mixing them is the most common ICM mistake.

## Departments, rooms, sub-rooms

A workspace can be flat (rooms directly under root) or clustered into **departments** (top-level numbered
folders that group related rooms). A **room** is one specialized capability; a room may nest
**sub-rooms** (`NN.n-<name>`) when a subprocess genuinely ramifies — recursion is allowed *by need*, with
no fixed depth cap. Every department / room / sub-room is a Layer-2 node with its own `CONTEXT.md` + `docs/`.

The numbering carries the nesting, so depth is readable from the name alone:

```
dept-content/                 (department)
  02-script/                  (room)
    02.1-concept/             (sub-room)
    02.2-copy/                (sub-room)
      02.2.1-hooks/           (sub-sub-room — same rules, deeper)
    02.0-review/              (the NN.0 review sub-room)
```

Nest only when a subprocess earns its own contract; a room that is one clean recipe stays a leaf. By
convention `NN.0` is the QA / auto-review sub-room (it runs every checkpoint, despite the number); `NN.1+`
are productive sub-rooms. The same rules apply identically at every depth — there is no special "sub-room
contract," just a `CONTEXT.md` deeper in the tree.

## How agents enter

```
AGENTS.md (L0) — identity + base rules
  └─> CONTEXT.md (L1) — routing table picks one target
       └─> <dept>/CONTEXT.md (L2) — if a department, sub-routes to a room
            └─> <dept>/<NN-room>/CONTEXT.md (L2) — the room contract
                 └─> <room>/docs/* (L3) — load only the Inputs the contract names
                      └─> projects/... (L4) — write the run output here
```

## Token budget

A well-built ICM workspace lets one agent specialize per room by reading ~5k tokens instead of ~40k. The model is the same; only the context changes.
A well structured pipeline loads context when it is needed, not before. Atomical context files (L3), and structured descriptions an map trees (L2) is how we do this. 
