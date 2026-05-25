"""Shared helpers for ICM scripts. Stdlib only."""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Iterable, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AGENT_FILES = ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".cursorrules")
STUB_FILES = ("CLAUDE.md", "GEMINI.md", ".cursorrules")
CANONICAL_AGENT_FILE = "AGENTS.md"

STAGE_PREFIX_RE = re.compile(r"^(\d{2})-(.+)$")
ROUTING_HEADER_RE = re.compile(r"^\s*##+\s+Routing\s*$", re.IGNORECASE | re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
ARCHIVE_DIRNAME = "_archive"

CHARS_PER_TOKEN = 4  # rough heuristic

# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------

@dataclass
class LayerSummary:
    layer: int
    files: list[str] = field(default_factory=list)


@dataclass
class StageInfo:
    folder: str            # POSIX path relative to root
    number: Optional[int]  # parsed from prefix, or None
    name: str
    has_context: bool
    has_references: bool
    has_output: bool
    context_tokens: int


@dataclass
class WorkspaceInfo:
    folder: str            # POSIX rel path
    name: str
    has_context: bool
    context_tokens: int
    has_stages: bool


@dataclass
class RoutingRow:
    task: str
    go_to: str
    read: str
    skills: str


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def to_posix(p: Path, root: Optional[Path] = None) -> str:
    if root is not None:
        try:
            p = p.relative_to(root)
        except ValueError:
            pass
    return p.as_posix()


def find_workspace_root(start: Path) -> Optional[Path]:
    """Walk up until we find an AGENTS.md (or CLAUDE.md). Return that folder, or None."""
    start = start.resolve()
    for candidate in (start, *start.parents):
        for name in AGENT_FILES:
            if (candidate / name).exists():
                return candidate
    return None


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def count_tokens(text: str) -> int:
    return max(1, len(text) // CHARS_PER_TOKEN) if text else 0


def is_hidden(p: Path) -> bool:
    return any(part.startswith(".") and part not in (".", "..") for part in p.parts)


# ---------------------------------------------------------------------------
# Layer detection
# ---------------------------------------------------------------------------

def detect_layers(root: Path) -> dict[int, list[str]]:
    """Walk the root and bucket files into layers."""
    layers: dict[int, list[str]] = {0: [], 1: [], 2: [], 3: [], 4: []}
    if not root.exists():
        return layers

    for dirpath, dirnames, filenames in os.walk(root):
        # skip dotfolders, archive, node_modules etc.
        dirnames[:] = [d for d in dirnames if d not in ("node_modules", ".git", ARCHIVE_DIRNAME)]
        d = Path(dirpath)
        rel = d.relative_to(root)
        rel_posix = rel.as_posix() if str(rel) != "." else ""

        for fn in filenames:
            full = d / fn
            rel_file = (rel / fn).as_posix()

            # Layer 0: agent contract at root
            if rel_posix == "" and fn in AGENT_FILES:
                layers[0].append(rel_file)
                continue

            # Layer 1: root CONTEXT.md
            if rel_posix == "" and fn == "CONTEXT.md":
                layers[1].append(rel_file)
                continue

            # Layer 2: stage / workspace CONTEXT.md (not at root)
            if rel_posix != "" and fn == "CONTEXT.md":
                layers[2].append(rel_file)
                continue

            # Layer 3: references / _config / shared / *_config* paths
            parts = rel.parts
            if any(p in ("references", "_config", "shared") for p in parts):
                layers[3].append(rel_file)
                continue

            # Layer 4: output / drafts / builds / final / output paths
            if any(p in ("output", "drafts", "builds", "final", "ideas",
                          "specs", "briefs", "platforms", "scheduling", "analytics") for p in parts):
                layers[4].append(rel_file)
                continue

    # sort each bucket
    for k in layers:
        layers[k].sort()
    return layers


# ---------------------------------------------------------------------------
# Stage / workspace detection
# ---------------------------------------------------------------------------

def find_stages(root: Path) -> list[StageInfo]:
    """Stages live under stages/ with numeric prefix folders."""
    stages_dir = root / "stages"
    out: list[StageInfo] = []
    if not stages_dir.is_dir():
        return out
    for child in sorted(stages_dir.iterdir()):
        if not child.is_dir():
            continue
        m = STAGE_PREFIX_RE.match(child.name)
        number = int(m.group(1)) if m else None
        name = m.group(2) if m else child.name
        ctx = child / "CONTEXT.md"
        ctx_text = read_text(ctx) if ctx.exists() else ""
        out.append(StageInfo(
            folder=to_posix(child, root),
            number=number,
            name=name,
            has_context=ctx.exists(),
            has_references=(child / "references").is_dir(),
            has_output=(child / "output").is_dir(),
            context_tokens=count_tokens(ctx_text),
        ))
    return out


def find_workspaces(root: Path) -> list[WorkspaceInfo]:
    """Named workspaces are top-level dirs with a CONTEXT.md that are NOT stages/, _config/, shared/, skills/."""
    out: list[WorkspaceInfo] = []
    if not root.is_dir():
        return out
    skip = {"stages", "_config", "shared", "skills", ARCHIVE_DIRNAME, ".git", "node_modules"}
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if child.name in skip:
            continue
        ctx = child / "CONTEXT.md"
        ctx_text = read_text(ctx) if ctx.exists() else ""
        out.append(WorkspaceInfo(
            folder=to_posix(child, root),
            name=child.name,
            has_context=ctx.exists(),
            context_tokens=count_tokens(ctx_text),
            has_stages=(child / "stages").is_dir(),
        ))
    return out


# ---------------------------------------------------------------------------
# Routing table parse / render
# ---------------------------------------------------------------------------

def parse_routing_table(text: str) -> list[RoutingRow]:
    """Find the first '## Routing' section and parse the markdown table beneath it."""
    rows: list[RoutingRow] = []
    if not text:
        return rows
    m = ROUTING_HEADER_RE.search(text)
    if not m:
        return rows
    rest = text[m.end():]
    # collect contiguous table lines
    lines = rest.splitlines()
    table_lines: list[str] = []
    in_table = False
    for line in lines:
        if line.strip().startswith("##"):
            break
        if TABLE_ROW_RE.match(line):
            in_table = True
            table_lines.append(line)
        elif in_table and not line.strip():
            break
    # skip header + separator
    data_lines = [l for l in table_lines if not re.match(r"^\s*\|[\s\-:|]+\|\s*$", l)]
    if len(data_lines) <= 1:
        return rows
    for line in data_lines[1:]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # pad to 4
        while len(cells) < 4:
            cells.append("")
        rows.append(RoutingRow(task=cells[0], go_to=cells[1], read=cells[2], skills=cells[3]))
    return rows


def render_routing_table(rows: list[RoutingRow]) -> str:
    """Render a list of RoutingRow back as a markdown table."""
    if not rows:
        rows = [RoutingRow("(no routes yet)", "—", "—", "—")]
    head = "| Task | Go to | Read | Skills |\n|------|-------|------|--------|\n"
    body = "\n".join(
        f"| {r.task} | {r.go_to} | {r.read} | {r.skills} |" for r in rows
    )
    return head + body


def replace_routing_section(text: str, new_table: str) -> str:
    """Replace the '## Routing' table in `text` with `new_table`. Append if missing."""
    m = ROUTING_HEADER_RE.search(text)
    if not m:
        if text and not text.endswith("\n"):
            text += "\n"
        return text + "\n## Routing\n\n" + new_table + "\n"
    # find end of the routing section (next ## or EOF)
    after = text[m.end():]
    next_section = re.search(r"^##\s+\S", after, re.MULTILINE)
    end = m.end() + (next_section.start() if next_section else len(after))
    before = text[:m.end()]
    tail = text[end:]
    return before + "\n\n" + new_table + "\n\n" + tail.lstrip("\n")


# ---------------------------------------------------------------------------
# Stub detection
# ---------------------------------------------------------------------------

STUB_BODY_RE = re.compile(r"^\s*(See\s+`?AGENTS\.md`?\.?|@AGENTS\.md)\s*$", re.IGNORECASE)
STUB_MAX_CHARS = 600  # multi-line cursorrules pointers are longer than a one-liner


def is_stub(p: Path) -> bool:
    """A stub file is small and points to AGENTS.md as the source of truth.

    Accepts:
      - one-liner like `See AGENTS.md.` or `@AGENTS.md`
      - multi-line pointer file (<600 chars) that explicitly mentions AGENTS.md as the source of truth
        (used for .cursorrules where Cursor reads the file as rules, not as a follow-the-pointer link)
    """
    txt = read_text(p).strip()
    if not txt:
        return False
    if STUB_BODY_RE.match(txt):
        return True
    if len(txt) <= STUB_MAX_CHARS and "AGENTS.md" in txt and (
        "source of truth" in txt.lower() or "canonical" in txt.lower() or "points you there" in txt.lower()
    ):
        return True
    return False


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def emit_json(obj) -> None:
    """Pretty-print JSON to stdout. Forces UTF-8 so em-dashes etc. survive Windows consoles."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass
    def default(o):
        if hasattr(o, "__dataclass_fields__"):
            return asdict(o)
        if isinstance(o, Path):
            return o.as_posix()
        raise TypeError(f"{type(o).__name__} not serializable")
    print(json.dumps(obj, indent=2, default=default, ensure_ascii=False))


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)
