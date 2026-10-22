---
kind: channel-rules
channel: reddit
status: proposed  # awaiting Owner approval; subreddits need Owner confirmation
checked: 2026-10-22
text:
  max_length: 40000  # self-post body
  max_title_length: 300
mixed_media: false
media:  # one Post holds ONE media type: an image gallery, or 1 GIF, or 1 video; never mixed
  image: {max_count: 20, formats: [jpg, png], max_size_mb: 20}
  gif: {max_count: 1, formats: [gif], max_size_mb: 100}
  video: {max_count: 1, formats: [mp4, mov], max_size_mb: 1024}
hashtags:
  max: 0  # Reddit has no hashtags; they read as spam
subreddits: [IndieDev, indiegames, gamedev, unrealengine, MobileGaming, AndroidGaming, iosgaming]
---

# Channel rules: Reddit

> [!warning] Proposal, awaiting Owner approval
> Drafted by an agent. The Owner confirms the limits, the subreddit list and each subreddit's rules before the Writer uses them. Subreddit rules change often: read the sidebar and pinned posts before every first post in a subreddit.

## Limits

The frontmatter holds the limits the Vault check reads. Change them there. A subreddit can be stricter: some forbid images, galleries, video or links.

| Limit | Value | Kind |
|---|---|---|
| Title | 300 characters | Platform (third-party sources) |
| Body | 40,000 characters (self post) | Platform (third-party sources) |
| Images | Gallery of up to 20, JPG / PNG, 20 MB each | Platform (unverified) |
| GIF | 1, 100 MB | Platform |
| Video | 1, MP4 / MOV, 1 GB | Platform (third-party sources) |
| Hashtags | None | House rule |
| Alt text | Every image has a caption that describes it | House rule |

## Chosen subreddits (to confirm)

| Subreddit | Fit | Self-promotion rule (verify in the sidebar) |
|---|---|---|
| r/IndieDev | Devlogs, gifs, lessons from solo development | Own work welcome; use the right flair |
| r/indiegames | Showing the game to players | Own games allowed with flair; posts must show the game |
| r/gamedev | Technical and design lessons, written as discussion | Strict: no self-promotion in normal posts; the game may appear only in the designated weekly threads. Lessons with no link are fine |
| r/unrealengine | How a thing was built in Unreal | Showcase posts need the showcase flair; questions and tips welcome |
| r/MobileGaming | Players of mobile games | Developers may post their own games under limits; verify frequency and flair rules |
| r/AndroidGaming | Android players, once there is a store page | Developer posts restricted (dev flair, frequency limits); verify before posting |
| r/iosgaming | iOS players, once there is a store page | Developer self-promotion restricted; verify before posting |

Hold the store-player subreddits (MobileGaming, AndroidGaming, iosgaming) until the game's name is public and a pre-registration page exists.

## Etiquette

- Modest, not self-promotional. Write as a developer sharing a lesson or a moment, not as a marketer.
- The title states what the post shows or teaches. No clickbait, no "my game" in every title.
- Give value in the post itself; a link, if any, comes last and only where the subreddit allows it.
- Follow the 9:1 spirit: the account takes part in discussions, not only posts its own work.
- Reply to comments in the first hours. Take criticism without arguing.
- Never post the same text to several subreddits at once; adapt it to each.
- Never link to the private repository or its issues.

## Sources

- Title and body limits (third-party, no official Reddit page found): <https://typecount.com/blog/reddit-post-character-limit>
- Image 20 MB and GIF 100 MB from Reddit's native image hosting launch: <https://searchenginejournal.com/reddit-breaks-imgur-releases-image-uploading-tool/164888>
- Video 1 GB: <https://help.postpone.app/en/scheduling-posts/submitting-image-video-posts-to-reddit>
- Media types per subreddit vary: <https://info.bundle.social/api-reference/limits>
