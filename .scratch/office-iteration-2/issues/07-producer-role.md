# 07: Producer Role (`/produce`)

**What to build:** A new skill `.claude/skills/produce/SKILL.md` (no fixed `model` in its frontmatter: the Owner chooses the model per session or with `--model`; the quota rules in `docs/producer-setup.md` are part of this ticket) and the Producer entry in the Glossary (done in ADR 0002). `/produce <draft>` takes a Shorts Draft. Ground rules: write only under `Attachments/video/<topic title>/` and the `attachments` field of this Draft; never change the Post text, the Script or any other note; never invent footage. Steps: gate (`status: ready`, `channel: shorts`, else stop and say why); read the Draft's Script, Title and the Channel rules; check every `Footage` link exists on disk, else stop and list the missing Shot list lines; copy `docs/templates/shorts-composition/` to `Attachments/video/<topic title>/` and fill it from the beat table: one sub-composition per beat, each beat's footage as a video or image layer trimmed to its `Seconds`, its On-screen text in the template's caption block kept out of the safe bands; a beat with narration stops the run (narration is out of scope). Then the fixed sequence from `docs/producer-setup.md`: `check --json` with both caption zones, fix the `Fix:` lines, one `snapshot --at` frame per beat and look, `open` in the desktop app, stop and tell the Owner it is ready to review there. `/produce <draft> render` is a second command: `catch-up --json` first (never undo the Owner's app edits), `render --quality delivery` once to `Attachments/<topic title> - shorts.mp4`, ffprobe for duration within `video.max_seconds` and 1080x1920, set the Draft's `attachments` to that one file with alt text from the caption, Vault check, hand over path and duration. `/produce <draft> --fresh` throws the composition away and rebuilds from the Script; only on the Owner's word. The forbidden command list and the three checkpoints from the setup doc go into the skill verbatim; the Producer proposes nothing.

**Blocked by:** 03 (Video script Draft), 06 (Install HyperFrames)

**Status:** ready-for-agent

- [ ] `/produce` refuses a Draft that is not ready or not Shorts
- [ ] Missing footage stops the run with the Shot list lines named
- [ ] Composition under `Attachments/video/<topic title>/`, committed; MP4 ignored by git
- [ ] Rendered MP4 is 9:16, within the Channel's seconds, text out of the safe bands (checked by eye on one frame per beat)
- [ ] Draft `attachments` set to the MP4; Vault check passes
- [ ] `/produce <draft>` stops after `open`; `/produce <draft> render` renders once; `--fresh` rebuilds
- [ ] Skill lists the forbidden commands and the three checkpoints; no `snapshot --review`, no `draft` render
- [ ] Skill frontmatter has no `model`; `--model` argument is honoured

## Comments
