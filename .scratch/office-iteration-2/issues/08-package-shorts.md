# 08: Package a Shorts Post

**What to build:** The Packager handles `channel: shorts`: copies the Draft's `title` into the Publish package (as it does Reddit's), carries the caption as the Post text, the one MP4 Attachment with its alt text, and lists `missing` as today. Vault check rules for a Shorts package: exactly one Attachment, an `mp4` within `video.max_size_mb`, `title` present and within the limit. `/package published` is unchanged. The Owner uploads to YouTube Shorts and TikTok by hand; one `published_url` is enough (the first platform), a second goes in the Post body as a line.

**Blocked by:** 02 (Shorts Channel rules), 07 (Producer)

**Status:** ready-for-agent

- [ ] Shorts Publish package carries caption, title, one MP4, alt text
- [ ] Vault check fails a Shorts package with no video, two Attachments, a non-mp4 or an oversized file, or no title
- [ ] Fixtures cover each rule

## Comments
