# Distribution

## Purpose

Publish, schedule, and track finished assets across platforms.

## Inputs

| From | File / Folder | What to load |
|------|---------------|--------------|
| `../production/output/` | most recent asset | what to publish |

## Process

1. For each platform, create a platform-formatted version in `platforms/<platform>/<topic>.md` (caption, hashtags, dimensions).
2. Add scheduling info in `scheduling/<YYYY-MM>.md`.
3. After publishing, log analytics in `analytics/<YYYY-MM>.md`.

## Outputs

| To | File | Format |
|----|------|--------|
| `./platforms/<platform>/` | `<topic>.md` | platform-specific text |
| `./scheduling/` | `YYYY-MM.md` | calendar list |
| `./analytics/` | `YYYY-MM.md` | numbers + notes |

## Done when

- Each target platform has a formatted version.
- Scheduling entry exists.

## Hand-off

External: human publishes. Analytics fed back into next research cycle.
