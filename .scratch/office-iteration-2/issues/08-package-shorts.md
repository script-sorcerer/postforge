# 08: Package a Shorts Post

**What to build:** The Packager handles `channel: shorts`: copies the Draft's `title` into the Publish package (as it does Reddit's), carries the caption as the Post text, the one MP4 Attachment with its alt text, and lists `missing` as today. Vault check rules for a Shorts package: exactly one Attachment, an `mp4` within `video.max_size_mb`, `title` present and within the limit. `/package published` is unchanged. The Owner uploads to YouTube Shorts and TikTok by hand; one `published_url` is enough (the first platform), a second goes in the Post body as a line.

**Blocked by:** 02 (Shorts Channel rules), 07 (Producer)

**Status:** resolved

- [x] Shorts Publish package carries caption, title, one MP4, alt text
- [x] Vault check fails a Shorts package with no video, two Attachments, a non-mp4 or an oversized file, or no title
- [x] Fixtures cover each rule

## Comments

- 2026-10-26: Resolved in commit HASH08. The Packager copies a Shorts Draft's `title`, carries the caption as the Post text and takes only the Draft's MP4 (never the Topic's raw footage; an empty list becomes a `missing` line telling the Owner to run `/produce <draft> render`); a second platform link goes in the Post body as a line. Vault check: new rule `shorts-video` (a ready Shorts package with no Attachment); two Attachments, a non-MP4 and an oversized file are caught by the existing `attachment-count`, `attachment-format` and `attachment-size` reading `Channel rules/Shorts.md`, a missing title by `shorts-title` from ticket 03. Fixtures: `shorts-video`, `shorts-package-count`, `shorts-package-format`, `shorts-package-size` (its own tiny `max_size_mb`), `shorts-package-title`, and a passing package in `valid`. `.gitignore` now keeps the fixtures' few-byte `.mp4` and `.mov` files (`!tests/fixtures/**/*.mp4`). `/package published` is unchanged. Not run end to end with a real MP4 (ticket 09).
