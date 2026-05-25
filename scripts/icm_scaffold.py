"""Scaffold a new ICM workspace by copying a template.

Usage:
    python icm_scaffold.py --template {pipeline,workspaces} --target PATH [--force]

Behavior:
    - Refuses to overwrite a non-empty target unless --force.
    - Preserves empty `.gitkeep` files (lets folders survive git).
    - Emits JSON describing what was copied.

Exit codes:
    0 = ok
    1 = invalid args / template not found
    2 = target not empty and --force not passed
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib import emit_json, die


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = {
    "pipeline": PLUGIN_ROOT / "templates" / "pipeline",
    "workspaces": PLUGIN_ROOT / "templates" / "workspaces",
}


def is_dir_effectively_empty(p: Path) -> bool:
    if not p.exists():
        return True
    if not p.is_dir():
        return False
    for child in p.iterdir():
        return False
    return True


def copy_tree(src: Path, dst: Path) -> list[str]:
    copied: list[str] = []
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            copied.append(rel.as_posix())
    return copied


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--template", required=True, choices=list(TEMPLATES.keys()))
    ap.add_argument("--target", required=True, help="Target directory (created if missing)")
    ap.add_argument("--force", action="store_true", help="Overwrite even if target not empty")
    args = ap.parse_args()

    src = TEMPLATES[args.template]
    if not src.exists():
        die(f"Template not found: {src}", code=1)

    dst = Path(args.target).resolve()

    if dst.exists() and not is_dir_effectively_empty(dst) and not args.force:
        die(
            f"Target {dst} is not empty. Re-run with --force to overwrite.",
            code=2,
        )

    dst.mkdir(parents=True, exist_ok=True)
    copied = copy_tree(src, dst)

    emit_json({
        "template": args.template,
        "source": src.as_posix(),
        "target": dst.as_posix(),
        "files_copied": copied,
        "count": len(copied),
        "next_steps": [
            f"Edit {dst.as_posix()}/AGENTS.md and replace identity / project name.",
            f"Edit {dst.as_posix()}/_config/ and {dst.as_posix()}/shared/ to match your domain.",
            f"Run `python {PLUGIN_ROOT.as_posix()}/scripts/icm_remap.py {dst.as_posix()}` to rebuild routing table from actual folders.",
        ],
    })
    return 0


if __name__ == "__main__":
    sys.exit(main())
