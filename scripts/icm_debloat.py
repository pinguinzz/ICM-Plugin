"""Propose what to archive in a workspace or sub-folder.

Usage:
    python icm_debloat.py PATH [--apply]

Default is dry-run (JSON report of what WOULD be archived).
With --apply, moves flagged items to <workspace-root>/_archive/<timestamp>/
along with a manifest.json describing what was moved and why.

Flags:
    - empty output files older than 30 days (likely abandoned)
    - duplicate references (same filename in multiple references/)
    - oversized CONTEXT.md files (suggest extraction, do not auto-archive)
    - draft files with no recent edits and a _final exists

Exit codes:
    0 = ok
    1 = error
    2 = bloat found (non-fatal)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import (
    ARCHIVE_DIRNAME, count_tokens, emit_json, die,
    find_workspace_root, read_text,
)


STALE_DAYS = 30


def file_age_days(p: Path) -> float:
    try:
        mtime = p.stat().st_mtime
    except OSError:
        return 0.0
    return (dt.datetime.now().timestamp() - mtime) / 86400.0


def collect_proposals(root: Path, target: Path) -> list[dict]:
    proposals: list[dict] = []

    # 1. Empty / tiny output files
    for output_dir_name in ("output", "drafts", "builds"):
        for d in target.rglob(output_dir_name):
            if not d.is_dir() or ARCHIVE_DIRNAME in d.parts:
                continue
            for f in d.iterdir():
                if not f.is_file() or f.name == ".gitkeep":
                    continue
                size = f.stat().st_size
                age = file_age_days(f)
                if size < 50 and age > STALE_DAYS:
                    proposals.append({
                        "action": "archive",
                        "path": f.relative_to(root).as_posix(),
                        "reason": f"empty/tiny ({size}b) and stale ({age:.0f}d old)",
                        "category": "abandoned_output",
                    })

    # 2. Duplicate reference filenames across multiple references/ folders
    seen: dict[str, list[Path]] = defaultdict(list)
    for d in target.rglob("references"):
        if not d.is_dir() or ARCHIVE_DIRNAME in d.parts:
            continue
        for f in d.iterdir():
            if f.is_file():
                seen[f.name].append(f)
    for name, paths in seen.items():
        if len(paths) > 1:
            for p in paths[1:]:
                proposals.append({
                    "action": "archive",
                    "path": p.relative_to(root).as_posix(),
                    "reason": f"duplicate of {paths[0].relative_to(root).as_posix()} — consolidate into shared/",
                    "category": "duplicate_reference",
                })

    # 3. Oversized CONTEXT.md (warn-only, do not auto-archive)
    for ctx in target.rglob("CONTEXT.md"):
        if ARCHIVE_DIRNAME in ctx.parts:
            continue
        toks = count_tokens(read_text(ctx))
        if toks > 600:
            proposals.append({
                "action": "review",
                "path": ctx.relative_to(root).as_posix(),
                "reason": f"oversized CONTEXT.md (~{toks} tokens) — extract reference material to references/",
                "category": "oversized_context",
            })

    # 4. Draft files when a _final exists
    drafts: dict[str, list[Path]] = defaultdict(list)
    finals: set[str] = set()
    for f in target.rglob("*_draft.md"):
        if ARCHIVE_DIRNAME in f.parts:
            continue
        stem = f.name[:-len("_draft.md")]
        drafts[stem].append(f)
    for f in target.rglob("*_final.md"):
        if ARCHIVE_DIRNAME in f.parts:
            continue
        stem = f.name[:-len("_final.md")]
        finals.add(stem)
    for stem, paths in drafts.items():
        if stem in finals:
            for p in paths:
                age = file_age_days(p)
                if age > STALE_DAYS:
                    proposals.append({
                        "action": "archive",
                        "path": p.relative_to(root).as_posix(),
                        "reason": f"a _final.md exists for '{stem}' and this draft is {age:.0f}d old",
                        "category": "superseded_draft",
                    })

    return proposals


def apply_archive(root: Path, proposals: list[dict]) -> dict:
    if not proposals:
        return {"archived": [], "archive_dir": None}
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_dir = root / ARCHIVE_DIRNAME / ts
    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = []
    for prop in proposals:
        if prop["action"] != "archive":
            continue
        src = root / prop["path"]
        if not src.exists():
            continue
        dst = archive_dir / prop["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        archived.append(prop)
    manifest = archive_dir / "manifest.json"
    manifest.write_text(json.dumps({
        "timestamp": ts,
        "items": archived,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"archived": archived, "archive_dir": archive_dir.relative_to(root).as_posix()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", help="Folder to debloat (must be inside an ICM workspace)")
    ap.add_argument("--apply", action="store_true", help="Actually archive (default: dry-run)")
    args = ap.parse_args()

    target = Path(args.path).resolve()
    if not target.exists():
        die(f"Path does not exist: {target}", code=1)

    root = find_workspace_root(target)
    if root is None:
        die(f"{target} is not inside an ICM workspace.", code=1)

    proposals = collect_proposals(root, target)
    summary = {
        "to_archive": sum(1 for p in proposals if p["action"] == "archive"),
        "to_review": sum(1 for p in proposals if p["action"] == "review"),
    }

    result = {
        "workspace_root": root.as_posix(),
        "target": target.as_posix(),
        "dry_run": not args.apply,
        "summary": summary,
        "proposals": proposals,
    }

    if args.apply:
        result["apply_result"] = apply_archive(root, proposals)

    emit_json(result)
    return 0 if summary["to_archive"] == 0 and summary["to_review"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
