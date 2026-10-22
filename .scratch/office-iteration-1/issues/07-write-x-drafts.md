# 07: `/write` for one Channel (X)

**What to build:** The Owner runs `/write` and every approved Topic that targets X gets an X Draft. The Writer works through the Angle, Hooks, Draft, Voice, Humanize and Channel fit Passes in order, keeps the best of three hooks in the body and the two alternatives in a collapsed section, and links the Draft to its Topic. The Draft enters the Draft lifecycle and the Vault check validates it.

**Blocked by:** 03 (First Digest from git history), 06 (Voice guide and Channel rules)

**Status:** ready-for-agent

- [x] `/write` picks up every approved Topic that targets X and leaves others alone
- [x] Each X Draft records that all six Passes ran, in order
- [x] The chosen hook is in the body; two alternatives sit in a collapsed section
- [x] The Draft follows the Voice guide and fits the X Channel rules
- [x] The Draft links to its Topic, and the Vault check fails a Draft without that link
- [x] The Owner can switch to an alternative hook with one sentence

Note: `/write` is a prompt (`.claude/skills/write/SKILL.md`); the Vault check enforces the Topic link, Pass order and X length. Voice and hook quality are checked only in the manual smoke run (ticket 12); `/write` was not run on real Topics.
