# 01: Owner Topic

**What to build:** The Owner writes a Topic note by hand and approves it at once, with no Digest. A template at `docs/templates/Owner Topic.md` (outside the Vault folders the Vault check reads) holds the frontmatter and the four body sections of a Scout Topic, with `status: approved`, `origin: owner`, no `rank` and no `previously_parked`. The Vault check learns `origin` (`scout` by default when absent, or `owner`) and stops requiring `rank` on an `owner` Topic; a Scout Topic is unchanged. The Scout's "what not to propose again" reading already covers every note in `Topics/`, so it only needs its prompt to say Owner Topics count. The README gets a short "Bring your own Topic" paragraph.

**Blocked by:** none

**Status:** resolved

- [x] `docs/templates/Owner Topic.md` exists with the four sections and `origin: owner`
- [x] The Vault check accepts an `owner` Topic without `rank` and still fails a `scout` Topic without one
- [x] The Vault check fails `origin` outside `scout`/`owner`
- [x] `/write` picks up an approved Owner Topic like any other
- [x] Scout prompt names Owner Topics among the Topics it must not repeat
- [x] Fixtures: an Owner Topic that passes, a Scout Topic without rank that fails

## Comments

- 2026-10-26: Resolved in commit 343100a. Rank is required only when `origin` is not `owner`; new rule `topic-origin`; fixtures `valid/Topics/Rush hour in one tap.md`, `required-fields-scout-rank`, `topic-origin`. `/write` needed only one prompt line: its work selection already reads every approved Topic. Not checked end to end with a real `/write` run (ticket 09).
