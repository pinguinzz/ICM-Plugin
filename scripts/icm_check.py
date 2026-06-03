#!/usr/bin/env python3
"""icm_check.py - check an ICM workspace (or a builder workbench) against the Invariants.

The single mechanical checker for ICM (replaces the old detect/audit/remap/debloat/scaffold/register
toolchain). Stdlib only. Spec: docs/CONVENTIONS.md ("Invariants").

ERRORS are invariant violations (exit 1). WARNINGS are guideline items (exit 0 unless --strict).
Checks mechanically: emoji in names, `docs-<name>` antipattern, naming, line caps, and routing-pointer
integrity (every `Go to` in a `## Routing` table resolves). Deeper checks (one-way DAG, contract purity,
stale prose paths) are for `/assimilate` to grill, not this script.

Usage:
  python icm_check.py [path]        default path = current dir
  python icm_check.py --json        machine-readable output
  python icm_check.py --strict      treat warnings as failures
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Emoji blocks only (NOT accents — "ç/ã" are fine; emoji break tooling). Invariant 10.
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\U00002B00-\U00002BFF️✨✅❌]"
)
ROOM_DIR = re.compile(r"^\d{2}(\.\d+)*-")              # 01-name, 02.1-name, 03.2.1-name
ROOM_OK = re.compile(r"^[\d.]+-[a-z0-9-]+$")
DOCS_BAD = re.compile(r"^docs-[a-z]")                  # Invariant 3 (use docs/)
EXCLUDE_PART = {".git", "node_modules", "__pycache__", ".claude", ".codex", ".gemini",
                "archive", "_archive", ".example"}
META_MARKER = re.compile(r"^\(.*\)$")                  # (here), (aqui), (ici)... — not a path
ROUTING_HEADER = re.compile(r"^\s*##+\s+Routing\s*$", re.IGNORECASE)
TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
SEP_ROW = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")
CONTEXT_MAX = 80
REFERENCE_MAX = 200


def _walk(root: Path):
    for p in root.rglob("*"):
        if any(part in EXCLUDE_PART for part in p.parts):
            continue
        yield p, p.relative_to(root).as_posix()


def _go_to_targets(text: str):
    """Yield the 'Go to' cell of every data row under a '## Routing' header."""
    lines = text.splitlines()
    in_routing = False
    in_table = False
    for line in lines:
        if line.strip().startswith("#"):
            in_routing = bool(ROUTING_HEADER.match(line))
            in_table = False
            continue
        if not in_routing:
            continue
        if TABLE_ROW.match(line) and not SEP_ROW.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not in_table:           # first row is the header
                in_table = True
                continue
            if len(cells) >= 2:
                yield cells[1]
        elif in_table and not line.strip():
            in_table = False


def _check_routing(root: Path, errors: list):
    """Every `Go to` target in a CONTEXT.md / AGENTS.md routing table must resolve."""
    for p, rel in _walk(root):
        if p.name not in ("AGENTS.md", "CONTEXT.md"):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        base = p.parent
        for cell in _go_to_targets(text):
            target = cell.strip().strip("`").strip()
            if not target or META_MARKER.match(target) or target in ("—", "-"):
                continue
            target = target.rstrip("/")
            if not (base / target).exists():
                errors.append(f"routing pointer does not resolve: {rel} -> '{cell.strip()}'")


def check(root: Path):
    root = Path(root).resolve()
    errors: list[str] = []
    warns: list[str] = []
    for p, rel in _walk(root):
        name = p.name
        if EMOJI.search(name):
            errors.append(f"emoji in name: {rel}")
        if p.is_dir():
            if DOCS_BAD.match(name):
                errors.append(f"docs-<name> antipattern (use docs/): {rel}")
            if ROOM_DIR.match(name) and not ROOM_OK.match(name):
                warns.append(f"room dir not lowercase-with-hyphens: {rel}")
        elif name.endswith(".md"):
            try:
                n = sum(1 for _ in p.open(encoding="utf-8", errors="ignore"))
            except OSError:
                continue
            if name == "CONTEXT.md" and n > CONTEXT_MAX:
                warns.append(f"CONTEXT.md > {CONTEXT_MAX} lines ({n}): {rel}")
            elif name != "CONTEXT.md" and n > REFERENCE_MAX:
                warns.append(f"reference > {REFERENCE_MAX} lines ({n}): {rel}")
    _check_routing(root, errors)
    return errors, warns


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate an ICM workspace/workbench against the Invariants.")
    ap.add_argument("path", nargs="?", default=".", help="dir to validate (default: cwd)")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on warnings too")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args(argv)
    root = Path(a.path)
    if not root.exists():
        print(f"path does not exist: {root}", file=sys.stderr)
        return 1
    errors, warns = check(root)
    if a.json:
        try:
            sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except (AttributeError, OSError):
            pass
        print(json.dumps({"root": str(Path(a.path).resolve()), "errors": errors,
                          "warnings": warns}, indent=2, ensure_ascii=False))
    else:
        for w in warns:
            print(f"WARN  {w}")
        for e in errors:
            print(f"ERROR {e}")
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s) under {Path(a.path).resolve()}")
    return 1 if (errors or (a.strict and warns)) else 0


if __name__ == "__main__":
    raise SystemExit(main())
