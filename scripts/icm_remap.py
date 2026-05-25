"""Regenerate the routing table in root AGENTS.md from actual folder reality.

Usage:
    python icm_remap.py [PATH] [--write]

Behavior:
    - Default is dry-run: prints proposed routing table + diff, does not write.
    - With --write, replaces the '## Routing' section in AGENTS.md (creates one if missing).
    - Preserves existing rows' `Task` and `Skills` columns when the `Go to` still exists.

Exit codes:
    0 = ok
    1 = error
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    CANONICAL_AGENT_FILE, RoutingRow,
    emit_json, die, find_stages, find_workspace_root, find_workspaces,
    parse_routing_table, read_text, render_routing_table, replace_routing_section,
)


def humanize_stage(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").capitalize()


def build_rows(root: Path) -> list[RoutingRow]:
    stages = find_stages(root)
    workspaces = find_workspaces(root)
    rows: list[RoutingRow] = []

    for s in stages:
        num = f"{s.number:02d}" if s.number is not None else "??"
        rows.append(RoutingRow(
            task=f"Work on stage {num}: {humanize_stage(s.name)}",
            go_to=s.folder + "/",
            read="CONTEXT.md",
            skills="—",
        ))
    for w in workspaces:
        rows.append(RoutingRow(
            task=f"Work in {humanize_stage(w.name)}",
            go_to=w.folder + "/",
            read="CONTEXT.md",
            skills="—",
        ))

    if not stages and not workspaces:
        rows.append(RoutingRow(
            task="(no stages or workspaces yet — run /icm:set-up)",
            go_to="—",
            read="—",
            skills="—",
        ))
    return rows


META_GOTO_VALUES = {"(here)", "—", "-", ""}


def _norm_goto(s: str) -> str:
    """Normalize a Go-to cell so paths compare equal regardless of backticks / trailing slashes."""
    return s.strip().strip("`").strip("/").strip().lower()


def _is_meta_row(row: RoutingRow) -> bool:
    """Meta rows have a go_to like '(here)' or '—' — they describe the workspace, not a folder."""
    g = row.go_to.strip().strip("`")
    return g in META_GOTO_VALUES


def merge_rows(existing: list[RoutingRow], generated: list[RoutingRow]) -> list[RoutingRow]:
    """Merge existing routing rows with rows generated from current folder reality.

    Rules:
        1. For each generated row (one per real folder), keep the existing row's `Task`/`Read`/`Skills`
           if a matching `Go to` exists, else use the generated defaults.
        2. Preserve meta rows from `existing` (those with go_to like '(here)' or '—').
        3. Drop existing rows whose `Go to` points to a folder that no longer exists.
    """
    by_goto = {_norm_goto(r.go_to): r for r in existing}
    merged: list[RoutingRow] = []
    for g in generated:
        key = _norm_goto(g.go_to)
        if key in by_goto:
            prior = by_goto[key]
            merged.append(RoutingRow(
                task=prior.task or g.task,
                go_to=g.go_to,
                read=prior.read or g.read,
                skills=prior.skills or g.skills,
            ))
        else:
            merged.append(g)
    # Preserve meta rows (e.g. methodology / debugging) that the agent added
    for r in existing:
        if _is_meta_row(r):
            merged.append(r)
    return merged


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--write", action="store_true", help="Write changes back to AGENTS.md")
    args = ap.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        die(f"Path does not exist: {target}", code=1)

    root = find_workspace_root(target)
    if root is None:
        die(f"{target} is not inside an ICM workspace.", code=1)

    canonical = root / CANONICAL_AGENT_FILE
    existing_text = read_text(canonical) if canonical.exists() else ""
    existing_rows = parse_routing_table(existing_text) if existing_text else []
    generated = build_rows(root)
    merged = merge_rows(existing_rows, generated)
    new_table = render_routing_table(merged)

    if args.write:
        new_text = replace_routing_section(existing_text, new_table)
        canonical.write_text(new_text, encoding="utf-8")

    emit_json({
        "workspace_root": root.as_posix(),
        "agents_file": canonical.as_posix(),
        "existed": canonical.exists(),
        "wrote": args.write,
        "existing_row_count": len(existing_rows),
        "generated_row_count": len(generated),
        "merged_row_count": len(merged),
        "routing_table": new_table,
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
