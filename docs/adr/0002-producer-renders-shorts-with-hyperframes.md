# The Producer renders Shorts videos with HyperFrames

Iteration 1 stopped at the Video script: the Office wrote it and the Owner was to make the video by hand. That video never got made, for the same reason the posts never got written. So a new Role, the Producer, turns a ready Shorts Draft into an MP4. It builds a HyperFrames composition (an HTML project: `index.html`, `compositions/`, `assets/`) from the Draft's Script beats, places the Owner's captured footage as video layers, adds on-screen text and burned captions from the HyperFrames registry, and renders it locally with `npx hyperframes render`. The MP4 becomes the Draft's Attachment and goes through the Packager like any other.

HyperFrames was chosen because it is plain HTML, CSS and GSAP, which the Roles already write well, it renders deterministically (headless Chrome seeks each frame, FFmpeg encodes), it ships agent skills and a registry of caption, transition and chart blocks, and its license is Apache 2.0 with no per-render fee.

## Considered Options

- Remotion: React compositions and a custom license with paid tiers above a small-team threshold. Rejected: more code per video and a license to track.
- Generated footage (Veo, Sora, Kling, HeyGen avatars): rejected for the Project's content. A Shorts Post shows the real game; invented footage would break the Voice guide's honesty rule. The Producer uses only the Owner's captured Attachments, screenshots and text.
- The Owner edits the video by hand in CapCut or similar: rejected, it is the step that never happens.

## Consequences

- The Producer needs Node.js 22+ and FFmpeg on the Owner's machine. HyperFrames' own skills (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`) are installed into `.claude/skills/` so the repository carries them; `media-use` (voiceover, music) is not installed until a Topic needs narration.
- Composition sources live under `Attachments/video/<topic title>/` and are committed; rendered MP4s and `node_modules` stay out of git, as ADR 0001 already requires for videos.
- The Writer's Video script gains a fixed beat table so the Producer can build from it without guessing: each beat names its footage file, on-screen text, narration and seconds.
- The cost of a video is Claude Code usage, not HeyGen credits: local rendering is free and the Producer never calls HeyGen media. So the Producer fills a house template from the beat table, looks at one frame per beat, hands review to the desktop app (free) and renders once on the Owner's word; the rules are in `docs/producer-setup.md`.
- The Office now has a Role that runs a build tool. Its ground rules keep it to `Attachments/video/` and the `attachments` field of its own Draft.
