# 04: Full Source material

**What to build:** The Scout's Topics draw on everything the Owner agreed the Office may read: traffic_jam's GitHub issues and their discussion (read through the GitHub CLI), its docs, ADRs, specs and other local files, and the Owner notes in the Vault. The Scout also reads past rejected and parked Topics and the history of published Posts, offers parked Topics again when they fit, and never proposes a story already rejected or published.

**Blocked by:** 03 (First Digest from git history)

**Status:** resolved

- [x] Topics can cite issues and their discussion, local files and Owner notes as Source material
- [x] All access to traffic_jam and its GitHub repository is read-only
- [x] A rejected or published story does not reappear in a later Digest
- [x] A parked Topic can reappear, marked as previously parked
- [x] Topics never link to the private repository or its issues

## Comments

- 2026-10-22: Implemented on branch `office-iteration-1` (tip 574a8b2), reviewed (standards, spec, ponytail) and fixed. 57 tests pass; the Vault check passes on the real Vault. Acceptance on real traffic_jam data is ticket 12.
