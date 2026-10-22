# 02: Fact sheet

**What to build:** The Owner runs `/scout` for the first time. Because no approved Fact sheet exists, the Scout builds one from traffic_jam's glossary, design docs and ADRs: what the game is, who it is for, the public-name field (empty until a name exists), and what has already been shown publicly. The Scout stops and asks the Owner to approve it. Until the Owner approves, `/scout` produces no Digest.

**Blocked by:** 01 (Vault skeleton and Vault check core)

**Status:** resolved

- [x] The first `/scout` run writes a Fact sheet note drawn from the Project's own material and asks for approval
- [x] The Fact sheet holds a public-name field and a record of what has been shown publicly
- [x] `/scout` refuses to write a Digest while the Fact sheet is not approved
- [x] The Scout only reads the Project folder; nothing in traffic_jam changes
- [x] The Vault check validates the Fact sheet note

## Comments

- 2026-10-22: Implemented on branch `office-iteration-1` (tip 574a8b2), reviewed (standards, spec, ponytail) and fixed. 57 tests pass; the Vault check passes on the real Vault. Acceptance on real traffic_jam data is ticket 12.
