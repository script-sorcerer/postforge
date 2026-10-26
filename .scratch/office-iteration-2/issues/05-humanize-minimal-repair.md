# 05: Humanize Pass as minimal repair

**What to build:** Rewrite the `humanize` Pass in `.claude/skills/write/SKILL.md` as a minimal-repair contract, after theclaymethod `unslop` (`references/core-contract.md`), no install. The Pass edits only a sentence with a confirmed banned word or pattern from the Voice guide, with the smallest repair; every other sentence is copied unchanged, in order. It adds no claim, advice, anecdote or conclusion; it deletes empty framing instead of replacing it with other filler; it keeps facts, numbers, names, code, units and every "never", "must" and "all"; a match inside a quote, a technical term or an Owner block is not a defect. It never stacks short sentences into staccato prose and stops at matters of taste. The same contract applies when the Writer revises from Editor remarks on item 7. The Voice guide's banned list stays the single source; the Pass gains categories to recognise paraphrased filler by function (formulaic framing, stock journey sentences, moralising recap, vague praise without a measure).

**Blocked by:** none

**Status:** resolved

- [x] `humanize` Pass states the minimal-repair rules above
- [x] Voice guide's Banned words and patterns gains the four categories as patterns, not only words
- [x] Owner blocks are named as untouchable in the Pass (already a ground rule; repeat it there)
- [x] One existing Draft run through the new Pass by hand as a check

## Comments

- 2026-10-26: Resolved in commit 6f2dca7. The `humanize` Pass in `.claude/skills/write/SKILL.md` is now the minimal-repair contract and also governs revisions from Editor item 7; the Voice guide gains a "Filler by function" block with the four categories (the Owner should reread it: the Voice guide is Owner-approved). Hand check on the fixture `tests/fixtures/valid/Drafts/Road capacity explained - x.md`: no confirmed match outside the Owner block, so the Post text is copied unchanged; "started to feel like a city" sits inside the Owner block and is not touched; alternative 2's "far more than any feature I shipped this month" is a matter of taste, not vague praise, and stays. Left out: no Vault check rule (the contract is judgement, scored by the Editor's item 7).
