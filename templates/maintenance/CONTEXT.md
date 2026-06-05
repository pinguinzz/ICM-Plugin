# maintenance — workspace source-of-truth + structural authority

> The dept that owns **how this workspace works and how to change anything**. Any agent told to **build**
> or **change** structure comes **here first**, is routed to the right room, then acts. Parallel pipeline
> (capability rooms, no fixed order). Everyday productive agents never enter here.
>
> Scaffolded by `/icm:new`. The generic canon (CONVENTIONS · LAYERS · ROOM-CONTRACT · ROUTING) is vendored
> into `docs/` here as the C5 fallback copy — used only when the `icm` skill isn't loaded. If the skill is
> loaded, do not re-read the vendored copy.

## Intent router
| You want to… | Go to |
|---|---|
| Understand how the structure works / the 5 layers / how it grows | `docs/LAYERS.md` |
| Know the rules (Invariants vs Guidelines) + the tooling model | `docs/CONVENTIONS.md` |
| Know which model a room runs on | `docs/model-tiers.md` |
| Understand state / markers / the reconciler | `docs/CONVENTIONS.md` (Invariant 5) |
| **Create** a room / sub-room / dept, or make a **structural / major** change | `modify-workspace/` (= /new; heavy, gated) |
| **Evolve a room's own process** in convention (cheap) | `modify-room/` |
| Split oversized files · re-point · organize · rewire drifted pointers | `janitor/` |
| **Audit** conformance / find drift (read-only) | `audit/` (= /assimilate) |
| Propose a structural change (CR) | `docs/pipeline-change-requests.md` |

## Map
```
maintenance/
├── CONTEXT.md          this router (L2)
├── docs/               KNOWLEDGE: LAYERS · CONVENTIONS (Invariants + tooling + state/markers) ·
│                       model-tiers · changelog · pipeline-change-requests
├── modify-workspace/   ROOM — create new + structural/major change (heavy, gated). = /new
├── modify-room/        ROOM — cheap in-convention room-local edits
├── janitor/            ROOM — hygiene: split oversized files, re-point, organize, rewire pointers
└── audit/              ROOM — read-only conformance audit + dedupe (has memory). = /assimilate
```

## How change is gated (Invariant 6 → `docs/CONVENTIONS.md`)
- **Create new (additive):** `modify-workspace` drafts in `workbench-<target>/` → human gate → promote.
- **Evolve a room (in-convention):** `modify-room` — double-check it's room-local + in-convention → apply → log.
- **Hygiene (split / organize / re-point):** `janitor` — mechanical, within invariants → log. No CR.
- **Major** (contract I/O, routing, names, another room, an invariant): **CR required** → `docs/pipeline-change-requests.md` → human disposes → `modify-workspace` applies.
- **Audit** is read-only: reports + a plan; fixes are routed to the rooms above.
- **Every applied change** is logged in `docs/changelog.md`.

## Boundaries
Acts on structure only through the gates above. Never edits `projects/` runs. Self-contained — the `icm`
skill/plugin is an optional accelerator, never a runtime dependency (C5).
