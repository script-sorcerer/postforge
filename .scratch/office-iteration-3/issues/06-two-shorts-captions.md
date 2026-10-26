# 06: Two captions for a Short

**What to build:** A Shorts Publish package carries `caption_youtube` (the Post text, unchanged) and `caption_tiktok`: the Post text with only its first line replaced by the first alternative hook's caption line. The Packager writes both; `draft-length` and `hashtags` check both. The Owner publishes each caption on its platform and records metrics per platform (ticket 04's `platform` field), so the two hooks can be compared.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] `/package` on a Shorts Draft writes both captions; with no alternative hook it writes `caption_tiktok` equal to the YouTube one and tells the Owner
- [ ] `draft-length` and `hashtags` fixture Vaults gain a case where only `caption_tiktok` breaks the limit
- [ ] README documents the two captions and which platform gets which
