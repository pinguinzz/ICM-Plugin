# Acknowledged exceptions — audit memory (append-only)

> Findings the human has marked OK / intentional. `audit` reads this FIRST and **suppresses** matches, so
> it never re-flags settled items. Append one block per acknowledgement.

## Format
- signature: <what + where — stable enough to match again>
- disposition: intentional | ok
- reason: <why it is fine>
- date: <YYYY-MM-DD>

## Acknowledged

### Same global Invariants referenced across parallel rooms
- signature: every room's `CONTEXT.md` Boundaries points to `../docs/CONVENTIONS.md`
- disposition: intentional
- reason: one-canonical-home is preserved (rooms POINT, never copy); parallel rooms legitimately share the same rules. Not drift.
- date: (seed)
