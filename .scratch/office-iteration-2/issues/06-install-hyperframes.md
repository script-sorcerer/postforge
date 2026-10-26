# 06: Install HyperFrames skills and tooling

**What to build:** Install HyperFrames' own skills into this repository so the Producer has them on a fresh clone: `npx skills add heygen-com/hyperframes --skill hyperframes`, then `hyperframes-cli` and `hyperframes-registry`, at project level (`.claude/skills/`), not global. Not `media-use`, `figma`, `slideshow` or `remotion-to-hyperframes`. Check Node.js 22+ and FFmpeg; record the versions and the install commands in `docs/producer-setup.md`. Add to `.gitignore`: `Attachments/video/**/node_modules/`, `Attachments/video/**/out/`, `Attachments/*.mp4` (videos already stay out of git, ADR 0001). Run `npx hyperframes init` once in a scratch folder to confirm the toolchain renders a sample, then delete it. Answered 2026-10-26, see `docs/producer-setup.md`: `npx hyperframes usage` reads the Claude Code subscription, not HeyGen credits; local render is free; the desktop app is installed and signed in; Node 24 and FFmpeg 8.1 present; `doctor` ok. Also build `docs/templates/shorts-composition/` (1080x1920 `index.html`, one beat composition, a caption block from the registry) so the Producer fills a template instead of designing.

**Blocked by:** none

**Status:** resolved

- [x] Three HyperFrames skills under `.claude/skills/`
- [x] `docs/producer-setup.md` with versions, commands and the usage/plan answer
- [x] `docs/templates/shorts-composition/` passes `npx hyperframes check` with placeholder footage
- [x] `.gitignore` covers renders and `node_modules`
- [ ] A sample render completes locally

## Comments

- 2026-10-26: Pipeline studied on the Owner's machine; findings and quota rules in `docs/producer-setup.md`. Ready to install.
- 2026-10-26: Resolved in commit HASH06. Skills `hyperframes`, `hyperframes-cli`, `hyperframes-registry` copied into `.claude/skills/` with `skills-lock.json` (two of them from a sparse clone after the regular clone stalled; see `docs/producer-setup.md`). `.gitignore` covers `Attachments/*.mp4` and, under `Attachments/video/**/`, `node_modules/`, `out/`, `renders/`, `.hyperframes/artifacts/`, `assets/footage/` (verified with `git status`; `.hyperframes/history` stays tracked). `docs/templates/shorts-composition/` (1080x1920 `index.html`, `compositions/beat-1.html`, `compositions/captions.html`, placeholder still) passes `npx hyperframes check --json` with the top and bottom caption zones at `severity=error`: 0 errors, 0 warnings; one `snapshot --at 0.3` frame looked right. The caption block is adapted by hand from the registry's `caption-highlight` component (installed with `npx hyperframes add caption-highlight` in a scratch project, then cut to one line per beat at 1080x1920), not added to the template with `add`. `npx hyperframes init` ran once in a scratch folder and was deleted. Left out: the sample render (box unticked), because this run was told not to run `npx hyperframes render`; the first render is the Owner's, in ticket 09.
