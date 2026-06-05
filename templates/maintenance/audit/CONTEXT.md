# audit — workspace conformance auditor (room; = /assimilate)

> Parallel capability. **Read-only**: relentlessly audits structure + context against the Invariants,
> reports findings + a plan, and remembers what the human already OK'd. Never mutates — fixes are routed
> to `../janitor/` / `../modify-workspace/`. Model tier: `../docs/model-tiers.md` (mid / sonnet, clean context).

## Inputs
| Source | File/Location | Section/Scope | Why |
|--------|--------------|---------------|-----|
| Tools | `tools.json` | Full file | what this room may call (read FIRST) |
| Canon | `../docs/conventions.md` | "Invariants" | the rules to check against |
| Skeleton | `../docs/architecture.md` | Full file | the fixed structure |
| Memory | `docs/memory/acknowledged-exceptions.md` | Full file | what the human already flagged OK (suppress these) |
| Target | `<path being audited>` | Full subtree | what to inspect |

## Process
1. Read `tools.json`; resolve the conformance checker via its `how-to-use`.
2. Read the acknowledged-exceptions memory.
3. Run the checker + walk the tree: Invariant violations · Layer-3/4 misclassification · unresolved routing/Inputs pointers · duplicated authoritative rules (drift) · oversize files (>~200) · stale pointers.
4. **Suppress** findings already in memory (esp. intentional parallel duplication). Report only NEW findings.
5. Write `audit-report-<date>.md` (each finding + proposed owner: janitor / modify-workspace / modify-room). Drop `_handoff.md`.
6. On human disposition: append OK'd items to `docs/memory/acknowledged-exceptions.md` (signature · why-ok · date).

## Outputs
| Artifact | Location | Format |
|----------|----------|--------|
| Audit report | `audit/workbench-<id>/audit-report-<date>.md` | findings + owner + plan |
| Acknowledged exceptions | `docs/memory/acknowledged-exceptions.md` | append-only ledger |

## Done-when
A report listing only NEW non-conformances (acknowledged ones suppressed), each with a proposed owner. Nothing mutated.

## Hand-off
Findings → `../modify-workspace/` (structural) · `../janitor/` (hygiene) · `../modify-room/` (in-convention). Drops `_handoff.md`.

## Boundaries
**READ-ONLY** — never moves/renames/edits/deletes; never writes `_state.json`; writes only its `workbench-<id>/` + `docs/memory/`. **NEVER modify** structure. Base rules: the `icm` skill · invariants: `../docs/conventions.md`.

## Tools
Read `tools.json` first. (Relentless grilling: the `grill-me` skill, when available.)
