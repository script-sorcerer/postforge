# Postforge

A content and marketing Office: agent Roles that turn a Project's work into ready-to-publish Posts. See `GLOSSARY.md` for the vocabulary.

## The Vault

Open this repository in Obsidian as its own Vault (ADR 0001). Its folders:

| Folder | Holds |
|---|---|
| `Projects/` | Project config, one note per Project (`traffic_jam.md`) |
| `Fact sheets/` | One Fact sheet per Project |
| `Voice guide/` | The Voice guide |
| `Channel rules/` | One note per Channel: `X.md`, `Reddit.md`, `LinkedIn.md`, `Shorts.md` (one 9:16 video for YouTube Shorts and TikTok) |
| `Schedule/` | One Schedule note per Project: each Channel's cadence |
| `Trend scans/` | Dated Trend scans |
| `Digests/`, `Topics/` | Digests and their Topic notes |
| `Drafts/` | One Draft per Channel per approved Topic |
| `Publish packages/` | Posts ready to publish |
| `Posts/` | Published Posts |
| `Owner notes/` | The Owner's free-form notes |
| `Capture list/` | One Capture list per Project, built by `scripts/capture_list.py`; never edited by hand |
| `Attachments/` | Images and videos (videos stay out of git) |

Topic, Draft and Post notes carry YAML frontmatter (`kind`, `status`, `project`, `language`, plus `rubric` and `channels` on a Topic, `topic` and `channel` on a Draft or Post, `published_url` on a published Post).

A Topic also carries `origin` (`scout`, the default when absent, or `owner`), `rank` (not on an Owner Topic), `needs_media`, `promotional`, a one-line `reason` once the Owner rejects it, and `previously_parked` (a link to the parked Topic it brings back, or empty); its `rubric` is one of the eleven Rubrics, its `channels` each one of `x`, `reddit`, `linkedin`, `shorts`, and its body has the sections `## Angle`, `## Why now`, `## Source material` and `## Shot list`. A Digest carries `kind: digest`, `project`, `date` and `topics`, the links to its Topic notes, best first (their `rank`s run 1 to N in that order), and `trend_scan`, the link to the Trend scan it built on (at most 14 days older than the Digest).

A Trend scan (`Trend scans/<YYYY-MM-DD> Trend scan.md`) carries `kind: trend-scan`, `date` (ISO) and `sources` (URLs).

The Project note holds `github` (the repository's `owner/name` slug, read with `gh`) and the Scout's reading position (`last_read_commit`, `last_read_date`); empty means the next Digest reads the whole git history.

A Fact sheet carries `kind: fact-sheet`, `status` (`proposed`, then `approved` by the Owner), `project`, `public_name` (empty until the name is public) and `shown_publicly` (a list).

A Draft also carries `passes`, the Writer's Passes in the order they ran (`angle`, `hooks`, `draft`, `voice`, `humanize`, `channel-fit`); all six once it leaves `drafting`. Its `topic` must link to an existing Topic note. Its body holds the Post text, then an `> [!note]- Alternative hooks` callout and `## Writer notes`. The Post text is the body up to the first line starting with `> [!` or `## `; the Vault check measures it against the Channel's `text.max_length` (URLs count as written, stricter than X's 23; `draft-length`) and counts its `#hashtags` against `hashtags.max` (`hashtags`). A Reddit Draft also carries `subreddit`, one of the Channel rules' `subreddits` (`reddit-subreddit`), and `title`, at most `text.max_title_length` characters (`reddit-title`). A Shorts Draft is a Video script: its Post text is the caption, and it also carries `title` (the YouTube title, within `text.max_title_length`; `shorts-title`), `duration_s`, a `## Title` section and a `## Script` beat table with the columns `#`, `Footage`, `On-screen text`, `Narration`, `Seconds` (`shorts-script`: at least two beats, each with Footage and Seconds; `shorts-duration`: `duration_s` is the beats' sum and within `attachments.video.max_seconds`; `shorts-on-screen-text`: each within `on_screen_text.max_chars_per_beat`). An approved Topic has exactly one Draft per Channel in its `channels` and none for a Channel it does not list; a Publish package or Post for that Channel stands in for a packaged Draft (`topic-drafts`). A missing Draft is reported only once the Topic has a Draft and none is `drafting`, and never for a Channel whose rules note is not `approved` (the Writer skips it): `/write` first creates one `drafting` Draft per Channel. After the Editor loop a Draft also carries `editor_rounds` (at most 2), `editor_score` and one `## Editor review N` section per round. A Draft with Owner edits carries `owner_edits`, one fingerprint per Owner block (see below).

Only the Owner sets a Draft to `ready`. The Vault check cannot see who wrote a status, so every Role's prompt forbids it.

### Owner edits

An Owner edit is text between `%% owner %%` and `%% /owner %%` in a Draft (Obsidian hides these comments in reading view; they are never posted). No Role changes it; the Editor remarks on it with `Owner edit:` instead. To mark a hand edit in Obsidian:

1. Wrap the text you changed: `%% owner %%your words%% /owner %%`.
2. Run `scripts/vault_check.py --seal "Drafts/<name>.md"`; it records each block's fingerprint in `owner_edits`.
3. Edit a block again later? Seal again. The Vault check fails a Draft whose blocks no longer match `owner_edits` (`owner-edits`), so a Role's change to your words shows up.

Each Channel rules note carries the Channel's limits in frontmatter (`channel`, `text.max_length`, `attachments.<type>` with `max_count`, `formats` and `max_size_mb`, `hashtags.max`; for Reddit also `subreddits` and `text.max_title_length`; for Shorts also `text.max_title_length`, `attachments.video.max_seconds` and `on_screen_text.max_chars_per_beat`); the Vault check reads limits from there and reports a note missing any of them under `channel-rules`.

**Attachments.** Put captured files in `Attachments/` and list them, in upload order, in the Topic's `attachments` (or the Draft's, once it exists; the Draft's list wins when not empty), one entry each:

```yaml
attachments:
  - file: "[[Attachments/lane-change.png]]"   # path from the Vault root; a bare "![[lane-change.png]]" is found under Attachments/
    alt: ""                                    # the Packager fills empty alt text
```

A Publish package (`Publish packages/<topic title> - <channel>.md`, `kind: post`, `status: ready`) holds the Post text as its body, `draft` (link), for Reddit the Draft's `subreddit` and `title`, `attachments` (the same entries, with alt text) and `missing` (one line per blocker, such as an uncaptured Shot list item). The Vault check checks each `ready` package's Post text like a Draft's (`draft-length`, `hashtags`, `reddit-subreddit`, `reddit-title`) and its Attachments against its Channel rules: file on disk (`attachment-files`), format (`attachment-format`), count per type (`attachment-count`), size (`attachment-size`), alt text on images and GIFs (`alt-text`), and one type per Post when `mixed_attachments: false` (`mixed-attachments`). A ready Shorts package also carries `title`, within its limit (`shorts-title`), and exactly one MP4, the video the Producer rendered (`shorts-video` fails one with none). Instead of a body it carries two captions, so the two sites test two hooks: `caption_youtube`, the Post text unchanged, goes to YouTube Shorts; `caption_tiktok`, the same text opening with the first alternative hook's caption line, goes to TikTok (equal to the YouTube one when the Draft has no alternative hook; `/package` tells you). `draft-length` and `hashtags` check each caption and fail a ready Shorts package missing one. The Owner uploads the one video by hand to both sites, each with its caption; `published_url` holds the first link and the second goes in the Post body as a line. Published Posts are not checked against disk: video files stay out of git. Once published, the Post sets `status: published`, `published_url` and `published_on` and moves to `Posts/`, the history of published Posts (`post-folder` fails a published Post left in `Publish packages/` or a ready one in `Posts/`).

### Schedule

A Schedule note (`Schedule/<project>.md`, `kind: schedule`, `project` link) holds the Project's `cadence`: per Channel, `per_week` and `weekdays` (weekday names, `Monday` to `Sunday`). Give each Channel its own days, so one Topic's Posts spread over the week. Every `ready` Publish package carries `publish_on`, the ISO date it goes out on (`publish-on` fails one without it or with another format). `/package` picks it: the first cadence weekday of the Channel on or after today with no other ready or published package of that Channel on it, and tells you the date; move a package by editing `publish_on`. With a Schedule note the Vault check also fails a package whose date is not a cadence weekday of its Channel, or whose Channel has no cadence (`schedule-slot`), a second ready package of one Channel on one date (`schedule-collision`, reported on the later note by path), and a malformed Schedule note or a second one for the same Project (`schedule`). It warns, without failing, about a `ready` Draft with no Publish package while its Channel's next cadence day has nothing on it (`schedule-gap`: run `/package`). Without a Schedule note only `publish_on`'s presence and format are checked. `per_week` is read but not enforced: the `weekdays` set the cadence days. A published Post keeps `publish_on` next to `published_on`, so you can see whether the schedule held.

### Phases

The Fact sheet lists the Project's Phases in order under `phases`: each has a `name`, `starts` (an ISO date, or empty until you set it) and `makes_public` (what the Phase lets Posts show). Each item under "Not public yet" starts with the Phase that lifts it in brackets (`- [Reveal] The working name`), or `[never]`. Every Topic names its `phase`. The Scout proposes Topics for the current Phase (the last one that has started) and the next one only, checks each Topic's Source material against the "Not public yet" list and the Phase order, and proposes the reveal Topic (the name, the store page, the pre-registration link) once the next Phase has a `starts` date and no Topic names it. The Vault check fails a Topic whose `phase` its Project's Fact sheet does not list (`topic-phase`) and a ready Publish package whose `publish_on` is before its Topic's Phase starts, or whose Phase has no date yet (`phase-date`). A Phase with no date still takes Topics and Drafts: write ahead, schedule once you date the Phase. Both rules apply only to a Project whose Fact sheet has well-formed `phases`; a malformed list fails `fact-sheet`.

### Destination and pinned comment

Each Channel rules note may carry a `destination`: `kind` (`pinned_comment`, `profile_link` or `description`), `template` (text with `{store}`, `{pre_registration}` and `{landing}` placeholders) and `fallback` (text used when no template line has all its links, for example "more clips on this channel"); write the template one line per link. The Fact sheet holds `public_links` (`store`, `pre_registration`, `landing`), each empty until it is public; fill them as they go live. The package field `pinned_comment` holds the destination text for both kinds that carry one (`pinned_comment`, `description`). `/package` writes it from the template and those links: it keeps each template line whose links are all filled and drops each line with an empty link, uses the fallback only when no line is left, and tells you which. Paste it right after you publish, by the destination's `kind`: `pinned_comment` as your own first comment, pinned (X: your first reply; YouTube and TikTok: pin it), `description` into the post's description. A `profile_link` Channel (Reddit, where subreddits ban self-promotion) gets no `pinned_comment`: set the Channel profile's link once from its template (or its fallback while the link is empty), and update it when `public_links` change. The Vault check fails a ready package without `pinned_comment` on a Channel whose destination is `pinned_comment` or `description` (`pinned-comment`), a malformed `destination` (`channel-rules`) or `public_links` (`fact-sheet`), and a pinned comment that links the private repository (`private-repo-link`). The Voice guide still bans calls to action in the Post text: the destination lives only in the pinned comment, the description and the profile link.

### Metrics

Record a published Post's numbers by hand in its `metrics` list in `Posts/`, about two days and about seven days after it went out: one entry per point (`at: 2d` or `7d`) and `platform` (the Channel, or `youtube` and `tiktok` for a Short, one entry each). `views`, `likes`, `comments` and `shares` are whole numbers; add `retention` (percent) and `link_clicks` where the site shows them. `hook` is the lever of the hook that went out: copy it from the Post's `hook_lever`, which `/package` fills from the Draft's Writer notes; for a Short's `tiktok` entry, from `hook_lever_tiktok`, the lever of the TikTok caption's hook.

```yaml
hook_lever: scene
hook_lever_tiktok: gap
metrics:
  - at: 2d
    platform: youtube
    views: 3200
    likes: 140
    comments: 11
    shares: 6
    retention: 68
    hook: scene
  - at: 2d
    platform: tiktok
    views: 900
    likes: 40
    comments: 3
    shares: 1
    hook: gap      # hook_lever_tiktok: caption_tiktok opens with the first alternative hook
```

Write `metrics: skipped` on a Post you chose not to measure. The Vault check fails a malformed entry (`metrics`) and warns, without failing, about a published Post more than seven days old with no `7d` entry and not skipped (`post-metrics`). The Scout reads every Post's metrics before ranking a Digest and writes a "What worked" section: Rubrics, Channels and hook levers ranked by views and comments per Post, each only once it has at least two Posts.

### Capture list

Each line of a Topic's `## Shot list` names one file in backticks, the name the Video script links, then what to capture and the duration, with an optional scene tag:

```markdown
- `Attachments/junction-4-0800.mp4`: cars queueing at junction 4, 4 s; scene: Junction 4 at 08:00
```

`scripts/capture_list.py` (needs uv; default: this repository, or pass a Vault path) reads the Shot lists of every approved Topic and writes `Capture list/<project>.md` (`kind: capture-list`) for each Project: one checkbox line per file not in `Attachments/` yet, with the Topic, the file name, what to capture and the duration, grouped by scene (untagged lines last). Capture per the "Capture" section of `Channel rules/Shorts.md`, save each file under its exact name, and rerun the script: the list shrinks. `/write` runs it at the end and `/produce` before it stops on missing footage. The note is regenerated on every run, so never edit it; the Vault check does not check it.

```sh
scripts/capture_list.py
scripts/capture_list.py path/to/vault
```

### Bring your own Topic

To have the Office write a story you already have in mind, copy `docs/templates/Owner Topic.md` to `Topics/<title>.md` and fill it in. It is an Owner Topic: `status: approved` and `origin: owner` from the start, with no Digest and no `rank`. Run `/write` and it is drafted like any approved Topic; the Scout reads it too, so it never proposes the same story.

## Commands

The Scout, the Writer, `/revise` and the Editor run on Opus at `effort: medium` (set in each skill's or agent's frontmatter; `opus` resolves to the current Opus, 5.5 today). The Packager runs on Sonnet; the Producer runs on the session's model.

- `/scout`: the Scout (`.claude/skills/scout/`). On the first run it builds the Project's Fact sheet and stops for approval; it writes no Digest until the Fact sheet is approved. After that it first writes a Trend scan (hot subreddit threads, meme formats, gaming and mobile news, calendar hooks; a scan up to 14 days old is reused) and refreshes the subreddit rules in `Channel rules/Reddit.md`, then writes a Digest of 5 to 8 Topics from the git history since its reading position, the GitHub issues and their discussion (read-only `gh`), the Project's local docs and the Owner notes. It skips stories already rejected, published, approved or proposed, and may bring a parked Topic back as a new note marked `previously_parked`.
- `/write`: the Writer (`.claude/skills/write/`). Turns every approved Topic into one Draft per target Channel (X, Reddit, LinkedIn, each in its register, and a Video script for Shorts) through the six Passes, then runs the Vault check. Each Draft then goes through the Editor (`.claude/agents/editor.md`, a fresh subagent per review, which holds the checklist and pass threshold): below the threshold it goes back to the Writer, and after at most two rounds it comes to the Owner at `in-review` with the Editor's remarks. Say "use hook 2" on a Draft to swap in an alternative hook (it becomes an Owner edit).
- `/revise <draft> <prompt>`: applies your prompt, such as "shorter hook, no emoji", to one Draft (`.claude/skills/revise/`), marks the change as an Owner edit and seals it. It never changes `status`.
- `/produce <draft>`: the Producer (`.claude/skills/produce/`, ADR 0002; no fixed model, add `--model <model>` to pick one). Takes a `ready` Shorts Draft, stops and lists the Shot list lines whose footage is not in `Attachments/` yet and points to the Capture list, else builds a HyperFrames Composition under `Attachments/video/<topic title>/` from the house template `docs/templates/shorts-composition/` and the beat table, checks it, looks at one frame per beat and opens it in the HyperFrames desktop app for your review. Edit it there by hand if you like, then `/produce <draft> render` renders it once (locally, free) to `Attachments/<topic title> - shorts.mp4` and sets it as the Draft's Attachment. `/produce <draft> --fresh` rebuilds the Composition from the Script, discarding your app edits. The Composition is committed; the MP4 is not. Setup and quota rules: `docs/producer-setup.md`.
- `/package <draft>`: the Packager (`.claude/skills/package/`, on Sonnet). Refuses a Draft that is not `ready`; writes its Publish package with the Attachments in order, alt text, the `missing` list and `publish_on` (the next free cadence day of the Channel's Schedule; it tells you the date) and `pinned_comment` (the Channel's destination text, which you paste after publishing; none on a `profile_link` Channel), then runs the Vault check. After you publish by hand, `/package published <publish package> <link>` records the link and moves the Post to `Posts/`, keeping `hook_lever` (the opening hook's lever; a Short also keeps `hook_lever_tiktok`) for your `metrics` entries. A Shorts package carries `caption_youtube` and `caption_tiktok`, one per site.

## Vault check

Needs [uv](https://docs.astral.sh/uv/). Check the whole Vault, or a Vault at another path:

```sh
scripts/vault_check.py
scripts/vault_check.py path/to/vault
```

It fails any Topic, Draft or Post that links to a Project's `github` repository (`private-repo-link`): that repository is private. It prints each violation as `note: [rule] message` and exits non-zero on any violation. A warning (`schedule-gap`, `post-metrics`) prints as `warning: note: [rule] message` and does not fail the check.

Run the tests (fixture Vaults live in `tests/fixtures/`, one folder per broken rule):

```sh
uv run --with pytest --with pyyaml pytest
```
