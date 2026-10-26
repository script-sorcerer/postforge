---
kind: channel-rules
channel: x
status: approved
checked: 2026-10-22
text:
  max_length: 280  # non-Premium account; Premium allows far more, but we write for 280
mixed_attachments: false
attachments:  # one Post holds ONE Attachment type: up to 4 images, or 1 GIF, or 1 video; never mixed
  image: {max_count: 4, formats: [jpg, png, webp], max_size_mb: 5}
  gif: {max_count: 1, formats: [gif], max_size_mb: 15}
  video: {max_count: 1, formats: [mp4, mov], max_size_mb: 512}
hashtags:
  max: 1  # house rule, not a platform limit
---

# Channel rules: X

## Limits

The frontmatter holds the limits the Vault check reads. Change them there.

| Limit | Value | Kind |
|---|---|---|
| Text | 280 characters | Platform (non-Premium) |
| Links | Every URL counts as 23 characters, whatever its length | Platform |
| Images | Up to 4, JPG / PNG / WEBP, 5 MB each | Platform |
| GIF | 1, 15 MB; stay under 1280x1080 and 350 frames or it may fail at posting | Platform |
| Video | 1, MP4 / MOV, 512 MB | Platform |
| Mixing | One Attachment type per Post | Platform |
| Hashtags | At most 1 | House rule |
| Alt text | Every image has alt text | House rule |

## Hashtags

- At most one hashtag, and only when it joins a live conversation (`#screenshotsaturday` on Saturdays, `#indiedev`, `#gamedev`, `#madewithunreal`).
- Never a string of hashtags at the end. Never hashtag a word mid-sentence just to tag it.

## Etiquette

- One idea per Post. Lead with the thing itself (the clip, the number, the bug), not with a preamble.
- Short, plain sentences. No threads unless the Topic truly needs more than one Post; then at most 4 Posts.
- The Attachment carries the Post: a short clip or a GIF beats a screenshot, a screenshot beats text only.
- Put a link, if any, in a reply rather than the first Post: X shows linked Posts less.
- Reply to replies. Do not @-mention people or studios to get their attention.
- Never link to the private repository or its issues.

## Sources

- X API, media upload best practices: <https://docs.x.com/x-api/media/quickstart/best-practices> (image 5 MB, GIF 15 MB, video 512 MB; up to 4 photos, 1 GIF or 1 video per Post).
- X counting characters (URLs count as 23): <https://docs.x.com/fundamentals/counting-characters>
