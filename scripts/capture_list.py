#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Capture list: writes `Capture list/<project>.md` for every Project in `Projects/`, one
checkbox line per Shot list file of an approved Topic not captured yet (naming every Topic that
needs it), grouped by the line's `scene:` tag. A Topic with a published Post on each of its Channels is done. The note is regenerated on every run; never edit it.

A Shot list line names its file in backticks and may end in a scene tag:
    - `Attachments/<file>`: what to capture, <seconds> s; scene: <what is captured together>

Usage: scripts/capture_list.py [VAULT]   (default: this repository; needs uv)
"""

import re
import sys
from pathlib import Path

from vault_check import link_name, project_name, read_note

SHOT_LINE = re.compile(r"^- `([^`]+)`:?\s*(.*)$")
SCENE_TAG = re.compile(r";\s*scene:\s*(.+)$", re.IGNORECASE)
NO_SCENE = "No scene"


def shot_list(text):
    """The lines under a note's `## Shot list` heading, up to the next `#` or `##` heading."""
    match = re.search(r"^## Shot list[ \t]*\n(.*?)(?=^#{1,2}\s|\Z)", text, re.MULTILINE | re.DOTALL)
    return [line.strip() for line in match.group(1).splitlines()] if match else []


def published_channels(vault):
    """{(Topic name, channel)} of every published Post."""
    notes = (read_note(p)["fm"] or {} for p in (vault / "Posts").rglob("*.md"))
    return {(link_name(fm.get("topic") or ""), fm.get("channel")) for fm in notes
            if fm.get("kind") == "post" and fm.get("status") == "published" and isinstance(fm.get("channel"), str)}


def missing_shots(vault):
    """Return ({project: {file: {"scene", "topics", "what"}}}, [lines naming no file]) for the Shot list files
    of approved Topics not captured yet. A Topic with a published Post on each of its Channels is done."""
    published = published_channels(vault)
    lists, unnamed = {}, []
    for path in sorted((vault / "Topics").rglob("*.md")):
        note = read_note(path)
        fm = note["fm"] or {}
        project, channels = project_name(fm), fm.get("channels")
        if fm.get("kind") != "topic" or fm.get("status") != "approved" or not project:
            continue  # a malformed project is reported by the Vault check
        if isinstance(channels, list) and channels and all(isinstance(c, str) and (path.stem, c) in published for c in channels):
            continue
        for line in shot_list(note["text"]):
            shot = SHOT_LINE.match(line)
            if not shot:
                if line.startswith("- "):
                    unnamed.append(f"{path.relative_to(vault)}: {line}")
                continue
            file, what = shot.groups()
            if (vault / file).is_file():
                continue
            scene = SCENE_TAG.search(what)
            # shortcut: a file two Topics name keeps the scene of the first Topic by path.
            entry = lists.setdefault(project, {}).setdefault(
                file, {"scene": scene.group(1).strip() if scene else NO_SCENE, "topics": [], "what": []})
            entry["topics"].append(path.stem)
            if what := (what[: scene.start()] if scene else what).strip():
                entry["what"].append(what)
    return lists, unnamed


def render(project, files):
    scenes = {}
    for file, entry in files.items():
        topics = ", ".join(f"[[{t}]]" for t in entry["topics"])
        what = "; ".join(entry["what"])
        scenes.setdefault(entry["scene"], []).append(f"- [ ] `{file}` for {topics}" + (f": {what}" if what else ""))
    body = []
    for scene in sorted(scenes, key=lambda s: (s == NO_SCENE, s)):
        body += ["", f"## {scene}", *scenes[scene]]
    return "\n".join([
        "---",
        "kind: capture-list",
        f'project: "[[{project}]]"',
        "---",
        "",
        f"# Capture list: {project}",
        "",
        "Built by `scripts/capture_list.py` from the Shot lists of approved Topics, minus the Attachments already captured. "
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
        files = lists.get(project, {})
        (vault / "Capture list" / f"{project}.md").write_text(render(project, files), encoding="utf-8")
        print(f"Capture list/{project}.md: {len(files)} file(s) to capture.")
    for line in unnamed:
        print(f"warning: {line} (Shot list line names no file in backticks)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
