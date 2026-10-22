# 10: Owner edits and `/revise`

**What to build:** The Owner edits a Draft in two ways: by hand in Obsidian, or with `/revise` and a prompt such as "shorter hook, no emoji". Owner edits are marked in the Draft so that every Role and the Vault check can see them. The Editor never changes an Owner-edited part; when it disagrees it leaves a comment. Only the Owner marks a Draft ready.

**Blocked by:** 08 (Editor loop)

**Status:** resolved

- [x] `/revise` applies the Owner's prompt to the named Draft and marks the change as an Owner edit
- [x] A hand edit in Obsidian can be marked as an Owner edit
- [x] The Editor leaves a comment instead of changing an Owner-edited part
- [x] The Vault check fails a Draft where an Owner-edited part was changed by a Role
- [x] No Role sets a Draft to ready; only the Owner does
- [x] Fixtures cover the Owner-edit rule

## Comments

- 2026-10-22: Implemented on branch `office-iteration-1` (tip 574a8b2), reviewed (standards, spec, ponytail) and fixed. 57 tests pass; the Vault check passes on the real Vault. Acceptance on real traffic_jam data is ticket 12.
