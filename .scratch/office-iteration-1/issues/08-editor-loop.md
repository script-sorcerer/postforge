# 08: Editor loop

**What to build:** After the Writer finishes a Draft, the Editor reviews it as a separate agent with a fresh context that does not see the Writer's reasoning. It scores the Draft against a fixed checklist and writes specific remarks. Below the pass threshold the Draft goes back to the Writer. After two rounds the Draft goes to the Owner with the Editor's remarks, whatever the score.

**Blocked by:** 07 (`/write` for one Channel (X))

**Status:** ready-for-agent

- [ ] The Editor runs in a fresh context on every review
- [ ] Each review records a checklist score and specific remarks in the Draft
- [ ] A Draft below the threshold returns to the Writer
- [ ] No Draft gets more than two Editor rounds; after the second it goes to the Owner with remarks
- [ ] The Draft's status moves through in-review and revising as the loop runs
