---
kind: channel-rules
channel: linkedin
status: proposed  # awaiting Owner approval
checked: 2026-10-22
text:
  max_length: 3000  # the feed cuts after about 210 characters on desktop, 140 on mobile
media:  # one Post holds ONE media type: images, or 1 video, or 1 document; never mixed
  image: {max_count: 20, formats: [jpg, png], max_size_mb: 5}
  video: {max_count: 1, formats: [mp4, mov], max_size_mb: 5120}
  document: {max_count: 1, formats: [pdf], max_size_mb: 100}
hashtags:
  max: 3  # house rule, not a platform limit
---

# Channel rules: LinkedIn

> [!warning] Proposal, awaiting Owner approval
> Drafted by an agent. The Owner confirms the limits and house rules before the Writer uses them.

## Limits

The frontmatter holds the limits the Vault check reads. Change them there.

| Limit | Value | Kind |
|---|---|---|
| Text | 3000 characters | Platform |
| Visible before "see more" | About 210 characters on desktop, 140 on mobile | Platform |
| Images | Up to 20, JPG / PNG, 5 MB each | Platform (size per third-party guides) |
| Video | 1, MP4 / MOV, up to 5 GB, 3 seconds to 15 minutes | Platform (third-party guides) |
| Document (carousel) | 1 PDF, up to 100 MB, 300 pages | Platform (third-party guides) |
| Mixing | One media type per Post | Platform |
| Hashtags | At most 3 | House rule |
| Alt text | Every image has alt text | House rule |

## Hashtags

- Up to 3, at the end of the Post, specific over broad (`#gamedev`, `#indiedev`, `#mobilegames`). No hashtags inside sentences.

## Etiquette

- Reflective, with a takeaway another developer or product person can use: what I tried, what happened, what I learned.
- The first two lines carry the hook; they are all most readers see before "see more".
- Short paragraphs, one to three sentences each. No bold-unicode text, no emoji bullet lists.
- No engagement bait ("Agree?", "Comment YES"). End with a real question only when I want the answers.
- Links in the body are fine but cost reach; prefer a link in the first comment.
- Never link to the private repository or its issues.

## Sources

- LinkedIn Help, sharing photos (up to 20 images): <https://www.linkedin.com/help/linkedin/answer/100983>
- Image, video and document sizes from third-party scheduler guides, unconfirmed by LinkedIn: <https://help.socialbu.com/article/155-technical-requirements-and-limitations>, <https://recurpost.com/blog/linkedin-post-size/>
