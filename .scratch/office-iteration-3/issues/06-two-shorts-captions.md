# 06: Two captions for a Short

**What to build:** A Shorts Publish package carries `caption_youtube` (the Post text, unchanged) and `caption_tiktok`: the Post text with only its first line replaced by the first alternative hook's caption line. The Packager writes both; `draft-length` and `hashtags` check both. The Owner publishes each caption on its platform and records metrics per platform (ticket 04's `platform` field), so the two hooks can be compared.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] `/package` on a Shorts Draft writes both captions; with no alternative hook it writes `caption_tiktok` equal to the YouTube one and tells the Owner
- [x] `draft-length` and `hashtags` fixture Vaults gain a case where only `caption_tiktok` breaks the limit
- [x] README documents the two captions and which platform gets which

## Comments

- 2026-10-27: Resolved in commits fdb3067 and 02f4387; review fixes in 14032db and 165d528. A Shorts package carries both captions in frontmatter (no body), plus `hook_lever_tiktok`; a missing caption fails the new rule `shorts-captions`. The second site's link goes in `published_url_tiktok` / `published_url_youtube`; `published_on` stays the first site's date.
