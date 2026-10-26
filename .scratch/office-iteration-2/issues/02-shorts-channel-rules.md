# 02: Shorts Channel rules

**What to build:** A fourth Channel, `shorts`, serving YouTube Shorts and TikTok with one Draft. `Channel rules/Shorts.md` follows the shape of `X.md`: frontmatter the Vault check reads, then the prose rules. Frontmatter: `text.max_length` for the caption (TikTok's limit, the stricter of the two), `text.max_title_length` for the YouTube title, `video.max_seconds: 60`, `video.aspect: 9:16`, `video.max_size_mb`, `video.formats: [mp4]`, `on_screen_text.max_chars_per_beat`, `hashtags.max`. Prose: the top and bottom safe bands the platforms' UI covers, burned captions because most viewing starts with sound off, no end card and no fade (end on the payoff or loop), game sound allowed, no narration required. Add `shorts` to `CHANNELS` in the Vault check and to the Topic template's allowed `channels`. Note `checked:` with the date the limits were verified, as the other Channel rules do.

**Blocked by:** none

**Status:** resolved

- [x] `Channel rules/Shorts.md` exists, `status: approved` only after the Owner reads it
- [x] A Topic may list `shorts` in `channels`
- [x] The Vault check reads the Shorts limits from the note's frontmatter like the other Channels
- [x] README's Channel list names Shorts

## Comments

- 2026-10-26: Resolved in commit a4b7390. `Channel rules/Shorts.md` is `status: proposed` until the Owner reads it and sets `approved`; the Writer skips a Channel whose rules are not approved. The video limits sit under `attachments.video` (`max_count`, `formats`, `max_size_mb`, `max_seconds`, `aspect`) instead of a separate `video:` key, so the existing Attachment checks read them unchanged. Caption 2,200 (TikTok) and upload 1 GB (TikTok) checked online; the YouTube title limit of 100 was not re-checked online. New rule branch in `channel-rules` for Shorts, fixture `channel-rules-shorts`. The checkbox for approval stays the Owner's to act on.
- 2026-10-26: Review fix in commit 23b57bd: `topic-drafts` no longer reports a missing Draft for a Channel whose rules note exists but is not `approved` (Shorts is `proposed`), and the Writer creates `drafting` stubs only for Channels whose rules are approved; test `test_missing_draft_for_channel_with_unapproved_rules_passes_until_approved`, fixture `topic-drafts-unapproved-rules`.
