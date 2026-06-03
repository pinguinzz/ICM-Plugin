# ICM Conventions — The Rules

Two tiers. **Invariants** are hard — never break them; a checker enforces them; change one only through a
Change Request (CR). **Guidelines** are soft — a node may adapt one with a deliberate double-check.
Breaking the invariants turns the workspace back into a normal messy folder.

## Invariants (hard — never break)

1. **Five layers, fixed roles.** L0 `AGENTS.md` (what this place is + how to enter + base rules) · L1 root
   `CONTEXT.md` (maps + routing — where to go) · L2 every dept/room/sub-room `CONTEXT.md` · L3 every
   `docs/` · L4 the product folder (`projects/` or a room-local `workbench-<id>/`). Don't mix layers. The
   **routing table lives in root `CONTEXT.md`** (departments carry their own in their `CONTEXT.md`).
2. **Routing resolves.** Every routing target and every Inputs pointer points to a file/folder that exists.
3. **`docs/` per node — NOT `docs-<name>/`.** Self-containment by nesting. (This overrides the flat-MWP
   `references/` convention.)
4. **The product layer is the only write target during a run.** A room writes to its run folder under
   `projects/<...>/<this-room>/` (or its own `workbench-<id>/`) and to its own `docs/memory/`. Never into
   another room's or another run's folder.
5. **Agents drop markers; a script owns machine state.** Agents emit marker files
   (`_handoff` / `_awaiting-human` / `_done` / `_rejected` or the workspace's declared set); a reconciler
   script writes any `_state.json`/dashboard. Never hand-edit state.
6. **No structure mutation without a CR.** Moving / renaming / adding rooms, or changing a contract or
   routing, goes through the workspace's change-request inbox; a human disposes. (Carve-outs: additive
   greenfield builds are human-gated in a workbench; minor non-disruptive housekeeping is double-checked
   and logged.)
7. **One-way cross-references.** If A points to B, B does not point back to A. Prevents N² reference growth.
8. **One canonical home per fact.** Every rule lives in exactly one file; others point to it. The moment
   the same rule exists in two files, they drift.
9. **Compatibility stubs are pointers, not content.** `CLAUDE.md` / `GEMINI.md` / `.cursorrules` are
   one-liners pointing to `AGENTS.md`. One file, one fact.
10. **Naming / hygiene.** `lowercase-with-hyphens`; stage folders zero-padded (`01-`, `02.1-`); no emoji
    in names (they break shell tools / grep / git normalization).

## Guidelines (soft — adapt with a double-check)

- **Line caps:** `CONTEXT.md` < 80 lines; reference files < 200 (split if longer). Keeps L0/L2 routing,
  not content.
- **Selective Inputs.** An Inputs table names the *section/scope* to load, not just the file — accuracy
  (avoid "lost in the middle") and cost.
- **`NN.0` = QA / auto-review (runs last); `NN.1+` = productive.**
- **Uniform decomposition, recursive by need.** Sub-rooms named by *process*, tool-agnostic (swappability).
- **Checkpoints + Audit on creative rooms.** Pause mid-process for human steering; run an end-of-process
  audit (incl. an upstream-brief trace) before writing output.
- **Docs over outputs.** Learn from `docs/` + correction notes — never copy a prior run's deliverable to
  imitate it. Early outputs are the worst outputs.
- **Gate tiering.** Start human-gated; loosen a gate to auto per node as it earns trust (middle stages
  first).

## Work patterns (each department declares one)

- **Sequential pipeline** — centralized `projects/<run>/<NN-room>/`; rooms hand off in order.
- **Parallel pipeline** — room-local `workbench-<id>/`; capability rooms run independently, no fixed order.

## When to break a rule

Invariants: don't — file a CR. Guidelines: if one blocks legitimate work, write a short `DECISIONS.md` in
the affected folder explaining the deviation. The deviation must be visible.
