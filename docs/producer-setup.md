# Producer setup: HyperFrames on the Owner's machine

Checked 2026-10-26. What the Producer (ADR 0002) runs on, what costs what, and the rules that keep the Claude Code quota for the Posts themselves.

## What is installed

| Piece | State |
|---|---|
| HyperFrames desktop app | `/Applications/HyperFrames.app`, 0.1.0 (`dev.hyperframes.desktop`), signed in with a HeyGen account |
| HyperFrames CLI | `npx hyperframes` 0.8.204 (latest); not installed globally, `npx` fetches it |
| Node.js | v24.13.1 (needs 22+) |
| FFmpeg | 8.1 |
| `npx hyperframes doctor` | ok except two optional pieces: whisper-cpp (transcription) and Kokoro (local TTS). Neither is needed: Shorts carry no narration |
| CLI config | `~/.hyperframes/config.json`; `telemetryEnabled: true` by default. `npx hyperframes telemetry disable` turns it off; the Owner's call |

## What costs what

- **Local render is free.** `npx hyperframes render` runs headless Chrome and FFmpeg on this machine. No HeyGen credit, no account needed.
- **HeyGen credits** are spent only by `media-use` calls that the Producer never makes: avatars, HeyGen voices, catalog music, generated footage, cloud render (`npx hyperframes cloud render`). The free HeyGen plan is 3 videos a month with a watermark; irrelevant as long as nothing is rendered in the cloud.
- **The real quota is Claude Code.** The desktop app runs the Owner's own Claude Code beside its preview ("plan" billing in the app's settings), and `npx hyperframes usage --json` reads the remaining *Claude Code subscription* usage, not HeyGen credits. From this session it answers `{"status":"unknown","reason":"unsupported_auth"}`, so the Producer reports "unknown" and moves on. Every agent turn spent on a video is a turn not spent on Posts.

## Quota rules for the Producer

The Producer runs from Claude Code with the CLI, never through the desktop app's chat box: the box builds from a loose prompt and takes extra passes to get right. The Video script already decides every beat, so one build pass is the target.

1. **Build from a house template, not from scratch.** `docs/templates/shorts-composition/` holds a 1080x1920 `index.html` and one beat composition; the Producer copies it and fills footage paths, on-screen text and seconds from the beat table. Registry blocks only for captions and transitions (`npx hyperframes add <block>`), nothing exploratory from `catalog`.
2. **One check, one look, then stop.** `npx hyperframes check --json --caption-zone "x0=0;y0=.82;x1=1;y1=1;severity=error"` (the bottom safe band) and the same for the top band, fix the `Fix:` lines, then `npx hyperframes snapshot --at <start of each beat + 0.3> --no-end --json` and look at one frame per beat. Never `snapshot --review` (a full review set plus `REVIEW.md` to read), never `--describe` (Gemini key), never `compare`, `grade-compare`, `keyframes` or `benchmark`.
3. **The Owner reviews in the desktop app, which costs nothing.** `npx hyperframes open <dir>` then stop. The Owner edits by hand there or says "render". The Producer never renders before that word, and `npx hyperframes catch-up <dir> --json` at the start of the next run tells it what the Owner changed, so it rebuilds nothing by itself.
4. **Render once.** `npx hyperframes render <dir> --quality delivery --output "Attachments/<topic title> - shorts.mp4"`, then `ffprobe` for duration and 1080x1920. No `draft` render first: the snapshots already showed the frames.
5. **Never:** `cloud`, `lambda`, `cloudrun`, `publish`, `capture`, `tts`, `transcribe`, `remove-background`, `media-treatment`, `feedback`, `auth`, or anything from `media-use`. A beat with narration stops the run and says narration is out of scope.
6. **The Owner picks the model.** The skill sets no `model`; it runs on whatever the Owner chose for the session, or on the model named in the command (`/produce <draft> --model sonnet`). With the template and the beat table the work is filling, not designing, so a cheaper model is a fair default, but it is the Owner's call per Draft.
7. **Fixed checkpoints, no proposals.** The Producer stops and talks to the Owner at three points only: footage missing (lists the Shot list lines), composition ready for review (the app is open), render done (path, duration). It proposes no styles, music, transitions or extra scenes.

## Install (ticket 06, done 2026-10-26)

HyperFrames' own skills sit in the repository at project level, copied (not symlinked) so a fresh clone has them; `skills-lock.json` records their source and hash:

```sh
npx skills add heygen-com/hyperframes --skill hyperframes -a claude-code --copy -y
npx skills add heygen-com/hyperframes --skill hyperframes-cli -a claude-code --copy -y
npx skills add heygen-com/hyperframes --skill hyperframes-registry -a claude-code --copy -y
```

Not installed: `media-use`, `figma`, `slideshow`, `remotion-to-hyperframes`. Each `skills add` clones the whole HyperFrames repository. On 2026-10-26 the clone stalled twice for `hyperframes-cli` and `hyperframes-registry`, so those two were installed from a sparse clone of the same repository (`git clone --depth 1 --filter=blob:none --sparse`, commit `7d6c02f`, `git sparse-checkout set skills/...`, then `npx skills add <that folder> --skill ...`), and `skills-lock.json` was pointed back at `heygen-com/hyperframes`; the `hyperframes` skill from the regular install matched that clone file for file.

Checked on install: Node.js v24.13.1, FFmpeg 8.1, HyperFrames CLI 0.8.204 (`npx --yes hyperframes@0.8.204`).

`.gitignore` keeps out `Attachments/*.mp4` and, under `Attachments/video/**/`, `node_modules/`, `out/`, `renders/`, `.hyperframes/artifacts/` and `assets/footage/` (copies of the Owner's footage; the source stays in `Attachments/`). `.hyperframes/history` (undo) is committed.

The house template `docs/templates/shorts-composition/` (1080x1920 `index.html`, `compositions/beat-1.html`, `compositions/captions.html` adapted from the registry's `caption-highlight`, a placeholder still in `assets/`) passes `npx hyperframes check --json` with both caption zones (top `y1=.15`, bottom `y0=.82`, `severity=error`): no error, no warning. No sample render was run while installing: the render belongs to the Owner's word (rule 4), and the first one is the smoke run.
