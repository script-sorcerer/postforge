---
kind: topic
status: approved         # an Owner Topic is approved the moment the Owner writes it
origin: owner            # no Digest and no rank; every Role after the Scout treats it like a Scout Topic
project: "[[traffic_jam]]"
rubric: Gameplay moment  # one of the eleven Rubrics in README.md
channels: [x, reddit, linkedin]  # any of x, reddit, linkedin, shorts
language: en
needs_media: true        # false when the Post can ship with no image or video
promotional: false
phase: Pre-reveal        # one Phase name from the Fact sheet's phases; a Phase with no starts date is drafted, not scheduled
attachments: []
---

# <title>

Copy this file to `Topics/<title>.md` (a valid file name, unique in `Topics/`), fill each section, then run `/write`. Delete this paragraph.

## Angle
The one point the Post makes and for whom.

## Why now
Why tell it now: the change that just landed, a date, a reaction you saw.

## Source material
- `<commit hash>` what it changed, or a path to a doc, an issue number, an Owner note

## Shot list
- `Attachments/<file>`: what to capture, <seconds> s; scene: <what is captured together>
<!-- One line per file, its name in backticks: the Video script links that exact file. End with the duration. "; scene: ..." is optional: lines with the same scene (same level, junction, game clock) are grouped in the Capture list. Write "None" instead of lines when the Post needs no image or video. -->

