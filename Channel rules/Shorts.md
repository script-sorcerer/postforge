---
kind: channel-rules
channel: shorts
status: proposed  # the Owner sets approved after reading this note
checked: 2026-10-26
text:
  max_length: 2200        # caption; TikTok's limit, the stricter of the two (YouTube's description allows 5000)
  max_title_length: 100   # YouTube title; TikTok has none
mixed_attachments: false
attachments:  # one Post holds exactly ONE vertical video, the same file for both platforms
  video: {max_count: 1, formats: [mp4], max_size_mb: 1024, max_seconds: 60, aspect: "9:16"}
on_screen_text:
  max_chars_per_beat: 42  # house rule: one short line readable at phone size
hashtags:
  max: 3  # house rule, not a platform limit
---

# Channel rules: Shorts

One 9:16 video serves YouTube Shorts and TikTok. Its Draft is a Video script: the caption (the Post text), a `## Title` for YouTube and a `## Script` beat table the Producer renders.

## Limits

The frontmatter holds the limits the Vault check reads. Change them there. The video limits sit under `attachments.video` (count, format, size, `max_seconds`, `aspect`), so the Publish package checks read them like any other Attachment type.

| Limit | Value | Kind |
|---|---|---|
| Caption | 2,200 characters | Platform (TikTok; YouTube allows more) |
| Title | 100 characters | Platform (YouTube) |
| Video | 1, MP4, 1080x1920 (9:16), 1 GB | Platform (TikTok upload, the stricter) |
| Duration | At most 60 seconds | House rule (both platforms now allow longer) |
| On-screen text | At most 42 characters per beat | House rule |
| Hashtags | At most 3 | House rule |

## Safe bands

The platforms' own UI covers the top and the bottom of the frame: the top band holds the search and tabs, the bottom band the caption, the music line and the buttons; the right edge holds the like and share buttons.

- Top band: the top 15% of the frame (y from 0 to 0.15). No on-screen text there.
- Bottom band: the bottom 18% (y from 0.82 to 1). No on-screen text there.
- Keep on-screen text off the right 10% as well, where the buttons sit.

The Producer's check fails any caption inside the top or bottom band.

## Video

- Burned captions: most viewing starts with the sound off, so every beat's On-screen text is burned into the video, never left to the platform's auto-captions.
- The first beat carries the payoff: the viewer decides in about one second.
- Aim for 15 to 30 seconds; 60 is the ceiling. One mechanic per video.
- Before / after: a hard cut with the dramatic change first, never a fade.
- No end card, no fade to black, no logo outro. End on the payoff, or loop into the first beat so the replay feels seamless.
- The game's own sound is welcome. No narration is required, and a Video script never needs a recorded voice.
- Real footage only: the Owner's captured clips and screenshots, never generated video.

## Caption and hashtags

- The caption's first line repeats the hook in words; only its first 80 to 100 characters show before "more".
- The YouTube title is a searchable phrase that names the mechanic ("traffic puzzle game: lane change"), evergreen: Shorts keep surfacing for months, so no "Day N" or dated framing in it.
- At most three hashtags, at the end of the caption: one for the genre or platform (`#indiegame`, `#mobilegame`), one for the moment (`#gamedev`, `#screenshotsaturday` on Saturdays).
- Never link to the private repository or its issues.

## Sources

- TikTok caption 2,200 characters and upload size 1 GB: <https://dopost.featurebase.app/en/help/articles/4326822-tiktok>, <https://help.swat.io/en/articles/11726862-tiktok-post-format-specifications>
- YouTube Shorts 1080x1920, 9:16, up to 3 minutes since 2024-10-15; safe zones: <https://piktochart.com/blog/youtube-shorts-dimensions/>, <https://www.clipspeed.ai/blog/youtube-shorts-size.html>
- Clip length 15 to 30 s, hard-cut before/after, loop-friendly mechanics, no TikTok watermark on cross-posts: <https://presskit.gg/field-guides/tiktok-indie-game-marketing> (read 2026-10-27)
- Searchable evergreen Shorts titles, Shorts resurface for months while TikTok fades in 48 hours: <https://bugnet.io/blog/youtube-shorts-for-indie-game-marketing> (read 2026-10-27)
- YouTube title 100 characters: YouTube Studio upload form (not re-checked online on 2026-10-26).
