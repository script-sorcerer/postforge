# 06: Install HyperFrames skills and tooling

**What to build:** Install HyperFrames' own skills into this repository so the Producer has them on a fresh clone: `npx skills add heygen-com/hyperframes --skill hyperframes`, then `hyperframes-cli` and `hyperframes-registry`, at project level (`.claude/skills/`), not global. Not `media-use`, `figma`, `slideshow` or `remotion-to-hyperframes`. Check Node.js 22+ and FFmpeg; record the versions and the install commands in `docs/producer-setup.md`. Add to `.gitignore`: `Attachments/video/**/node_modules/`, `Attachments/video/**/out/`, `Attachments/*.mp4` (videos already stay out of git, ADR 0001). Run `npx hyperframes init` once in a scratch folder to confirm the toolchain renders a sample, then delete it. Answered 2026-10-26, see `docs/producer-setup.md`: `npx hyperframes usage` reads the Claude Code subscription, not HeyGen credits; local render is free; the desktop app is installed and signed in; Node 24 and FFmpeg 8.1 present; `doctor` ok. Also build `docs/templates/shorts-composition/` (1080x1920 `index.html`, one beat composition, a caption block from the registry) so the Producer fills a template instead of designing.

**Blocked by:** none

**Status:** ready-for-agent

- [ ] Three HyperFrames skills under `.claude/skills/`
- [x] `docs/producer-setup.md` with versions, commands and the usage/plan answer
- [ ] `docs/templates/shorts-composition/` passes `npx hyperframes check` with placeholder footage
- [ ] `.gitignore` covers renders and `node_modules`
- [ ] A sample render completes locally

## Comments

- 2026-10-26: Pipeline studied on the Owner's machine; findings and quota rules in `docs/producer-setup.md`. Ready to install.
