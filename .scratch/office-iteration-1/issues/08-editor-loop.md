# 08: Editor loop

**What to build:** After the Writer finishes a Draft, the Editor reviews it as a separate agent with a fresh context that does not see the Writer's reasoning. It scores the Draft against a fixed checklist and writes specific remarks. Below the pass threshold the Draft goes back to the Writer. After two rounds the Draft goes to the Owner with the Editor's remarks, whatever the score.

**Blocked by:** 07 (`/write` for one Channel (X))

**Status:** resolved

- [x] The Editor runs in a fresh context on every review
- [x] Each review records a checklist score and specific remarks in the Draft
- [x] A Draft below the threshold returns to the Writer
- [x] No Draft gets more than two Editor rounds; after the second it goes to the Owner with remarks
- [x] The Draft's status moves through in-review and revising as the loop runs

## Comments

- 2026-10-22: Implemented on branch `office-iteration-1` (tip 574a8b2), reviewed (standards, spec, ponytail) and fixed. 57 tests pass; the Vault check passes on the real Vault. Acceptance on real traffic_jam data is ticket 12.
