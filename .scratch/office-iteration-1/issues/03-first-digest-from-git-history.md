# 03: First Digest from git history

**What to build:** With an approved Fact sheet, the Owner runs `/scout` and gets a Digest of 5 to 8 ranked Topics drawn from traffic_jam's git history since the saved reading position (the whole history on the first run). Each Topic states its title, angle, why now, Source material, Rubric, target Channels, Shot list and whether it needs media. The Owner marks each Topic approved, rejected (with a one-line reason) or parked, and may change its Channels or angle first. The Vault check enforces the Digest rules.

**Blocked by:** 02 (Fact sheet)

**Status:** resolved

- [x] `/scout` reads git history only after the saved reading position and then moves the position forward
- [x] With no saved position it reads the whole history
- [x] The Digest holds 5 to 8 Topics, ranked, each with every field listed above
- [x] The Owner can set approved, rejected with reason, or parked on each Topic in Obsidian
- [x] The Vault check fails a Digest with fewer than 5 or more than 8 Topics, more than two Topics of one Rubric, or promotional Topics above a third
- [x] Fixtures cover each Digest rule

## Comments

- 2026-10-22: Implemented on branch `office-iteration-1` (tip 574a8b2), reviewed (standards, spec, ponytail) and fixed. 57 tests pass; the Vault check passes on the real Vault. Acceptance on real traffic_jam data is ticket 12.
