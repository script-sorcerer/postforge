#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Capture list: writes `Capture list/<project>.md` for every Project in `Projects/`, one
checkbox line per Shot list file of an approved Topic that is not in Attachments yet,
grouped by the line's `scene:` tag. The note is regenerated on every run; never edit it.

A Shot list line names its file in backticks and may end in a scene tag:
    - `Attachments/<file>`: what to capture, <seconds> s; scene: <what is captured together>

Usage: scripts/capture_list.py [VAULT]   (default: this repository; needs uv)
"""

import re
import sys
from pathlib import Path

import vault_check
from vault_check import attachment_path, link_name, read_note

SHOT_LINE = re.compile(r"^- `([^`]+)`:?\s*(.*)$")
SCENE_TAG = re.compile(r";\s*scene:\s*(.+)$")
NO_SCENE = "No scene"


def shot_list(text):
    """The lines under a note's `## Shot list` heading, up to the next heading."""
    match = re.search(r"^## Shot list[ \t]*\n(.*?)(?=^#|\Z)", text, re.MULTILINE | re.DOTALL)
    return [line.strip() for line in match.group(1).splitlines()] if match else []


def missing_shots(vault):
    """Return ({project: {scene: [checkbox line]}}, [lines naming no file])."""
    vault_check.VAULT_ROOT[:] = [vault]
    lists, unnamed = {}, []
    for path in sorted((vault / "Topics").rglob("*.md")):
        note = read_note(path)
        fm = note["fm"] or {}
        project = link_name(fm.get("project") or "")
        if fm.get("kind") != "topic" or fm.get("status") != "approved" or not project:
            continue
        for line in shot_list(note["text"]):
            shot = SHOT_LINE.match(line)
            if not shot:
                if line.startswith("- "):
                    unnamed.append(f"{path.relative_to(vault)}: {line}")
                continue
            file, what = shot.groups()
            scene = SCENE_TAG.search(what)
            if scene:
                what = what[: scene.start()].rstrip()
            if attachment_path({"file": file}).is_file():
                continue
            group = scene.group(1).strip() if scene else NO_SCENE
            entry = f"- [ ] `{file}` for [[{path.stem}]]: {what}"
            lists.setdefault(project, {}).setdefault(group, []).append(entry)
    return lists, unnamed


def render(project, groups):
    body = []
    for scene in sorted(groups, key=lambda s: (s == NO_SCENE, s)):
        body += ["", f"## {scene}", *groups[scene]]
    return "\n".join([
        "---",
        "kind: capture-list",
        f'project: "[[{project}]]"',
        "---",
        "",
        f"# Capture list: {project}",
        "",
        "Built by `scripts/capture_list.py` from the Shot lists of approved Topics, minus the files already in Attachments. "
        "Do not edit: capture per `Channel rules/Shorts.md` (Capture), then rerun the script.",
        *(body or ["", "Nothing to capture."]),
        "",
    ])


def main(argv):
    vault = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    if not vault.is_dir():
        print(f"Vault not found: {vault}", file=sys.stderr)
        return 2
    lists, unnamed = missing_shots(vault)
    projects = sorted({p.stem for p in (vault / "Projects").glob("*.md")} | set(lists))
    (vault / "Capture list").mkdir(exist_ok=True)
    for project in projects:
        groups = lists.get(project, {})
        (vault / "Capture list" / f"{project}.md").write_text(render(project, groups), encoding="utf-8")
        print(f"Capture list/{project}.md: {sum(map(len, groups.values()))} file(s) to capture.")
    for line in unnamed:
        print(f"warning: {line} (Shot list line names no file in backticks)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
