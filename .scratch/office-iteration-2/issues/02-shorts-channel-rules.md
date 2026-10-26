# 02: Shorts Channel rules

**What to build:** A fourth Channel, `shorts`, serving YouTube Shorts and TikTok with one Draft. `Channel rules/Shorts.md` follows the shape of `X.md`: frontmatter the Vault check reads, then the prose rules. Frontmatter: `text.max_length` for the caption (TikTok's limit, the stricter of the two), `text.max_title_length` for the YouTube title, `video.max_seconds: 60`, `video.aspect: 9:16`, `video.max_size_mb`, `video.formats: [mp4]`, `on_screen_text.max_chars_per_beat`, `hashtags.max`. Prose: the top and bottom safe bands the platforms' UI covers, burned captions because most viewing starts with sound off, no end card and no fade (end on the payoff or loop), game sound allowed, no narration required. Add `shorts` to `CHANNELS` in the Vault check and to the Topic template's allowed `channels`. Note `checked:` with the date the limits were verified, as the other Channel rules do.

**Blocked by:** none

**Status:** ready-for-agent

- [ ] `Channel rules/Shorts.md` exists, `status: approved` only after the Owner reads it
- [ ] A Topic may list `shorts` in `channels`
- [ ] The Vault check reads the Shorts limits from the note's frontmatter like the other Channels
- [ ] README's Channel list names Shorts

## Comments
