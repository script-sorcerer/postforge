"""Run the Capture list script on a fixture Vault and compare the note it writes."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "capture_list.py"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "capture-list"

HEADER = """---
kind: capture-list
project: "[[traffic_jam]]"
---

# Capture list: traffic_jam

Built by `scripts/capture_list.py` from the Shot lists of approved Topics, minus the Attachments already captured. Do not edit: capture per `Channel rules/Shorts.md` (Capture), then rerun the script.
"""


def run(vault):
    result = subprocess.run([sys.executable, str(SCRIPT), str(vault)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return (vault / "Capture list" / "traffic_jam.md").read_text(encoding="utf-8")


def test_capture_list_lists_missing_files_of_approved_topics_by_scene_and_shrinks(tmp_path):
    """One line per file, naming every Topic that needs it; a `###` subheading stays in the Shot list; the
    scene tag ignores case; a published Topic (Old clip) and a malformed project (List project) are skipped."""
    vault = tmp_path / "vault"
    shutil.copytree(FIXTURE, vault)
    assert run(vault) == HEADER + """
## District 2 at 17:00
- [ ] `Attachments/rush-hour-wide.mp4` for [[Rush hour in one tap]]: the whole district at 17:00, 4 s

## Junction 4 at 08:00
- [ ] `Attachments/queue-after.mp4` for [[Queue at the junction]], [[Rush hour in one tap]]: the same junction queueing, 4 s; the queue from above, 4 s

## No scene
- [ ] `Attachments/rush-hour-tap.mp4` for [[Rush hour in one tap]]: one tap releases rush hour, 5 s
- [ ] `Attachments/rush-hour-sound.wav` for [[Rush hour in one tap]]
"""
    for name in ("queue-after.mp4", "rush-hour-wide.mp4", "rush-hour-tap.mp4", "rush-hour-sound.wav"):
        (vault / "Attachments" / name).write_bytes(b"clip")
    assert run(vault) == HEADER + "\nNothing to capture.\n"
