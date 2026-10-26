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
| `Trend scans/` | Dated Trend scans |
| `Digests/`, `Topics/` | Digests and their Topic notes |
| `Drafts/` | One Draft per Channel per approved Topic |
| `Publish packages/` | Posts ready to publish |
| `Posts/` | Published Posts |
| `Owner notes/` | The Owner's free-form notes |
| `Attachments/` | Images and videos (videos stay out of git) |

Topic, Draft and Post notes carry YAML frontmatter (`kind`, `status`, `project`, `language`, plus `rubric` and `channels` on a Topic, `topic` and `channel` on a Draft or Post, `published_url` on a published Post).

A Topic also carries `origin` (`scout`, the default when absent, or `owner`), `rank` (not on an Owner Topic), `needs_media`, `promotional`, a one-line `reason` once the Owner rejects it, and `previously_parked` (a link to the parked Topic it brings back, or empty); its `rubric` is one of the eleven Rubrics, its `channels` each one of `x`, `reddit`, `linkedin`, `shorts`, and its body has the sections `## Angle`, `## Why now`, `## Source material` and `## Shot list`. A Digest carries `kind: digest`, `project`, `date` and `topics`, the links to its Topic notes, best first (their `rank`s run 1 to N in that order), and `trend_scan`, the link to the Trend scan it built on (at most 14 days older than the Digest).

A Trend scan (`Trend scans/<YYYY-MM-DD> Trend scan.md`) carries `kind: trend-scan`, `date` (ISO) and `sources` (URLs).

The Project note holds `github` (the repository's `owner/name` slug, read with `gh`) and the Scout's reading position (`last_read_commit`, `last_read_date`); empty means the next Digest reads the whole git history.

A Fact sheet carries `kind: fact-sheet`, `status` (`proposed`, then `approved` by the Owner), `project`, `public_name` (empty until the name is public) and `shown_publicly` (a list).

A Draft also carries `passes`, the Writer's Passes in the order they ran (`angle`, `hooks`, `draft`, `voice`, `humanize`, `channel-fit`); all six once it leaves `drafting`. Its `topic` must link to an existing Topic note. Its body holds the Post text, then an `> [!note]- Alternative hooks` callout and `## Writer notes`. The Post text is the body up to the first line starting with `> [!` or `## `; the Vault check measures it against the Channel's `text.max_length` (URLs count as written, stricter than X's 23; `draft-length`) and counts its `#hashtags` against `hashtags.max` (`hashtags`). A Reddit Draft also carries `subreddit`, one of the Channel rules' `subreddits` (`reddit-subreddit`), and `title`, at most `text.max_title_length` characters (`reddit-title`). An approved Topic has exactly one Draft per Channel in its `channels` and none for a Channel it does not list; a Publish package or Post for that Channel stands in for a packaged Draft (`topic-drafts`). A missing Draft is reported only once the Topic has a Draft and none is `drafting`: `/write` first creates one `drafting` Draft per Channel. After the Editor loop a Draft also carries `editor_rounds` (at most 2), `editor_score` and one `## Editor review N` section per round. A Draft with Owner edits carries `owner_edits`, one fingerprint per Owner block (see below).

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

A Publish package (`Publish packages/<topic title> - <channel>.md`, `kind: post`, `status: ready`) holds the Post text as its body, `draft` (link), for Reddit the Draft's `subreddit` and `title`, `attachments` (the same entries, with alt text) and `missing` (one line per blocker, such as an uncaptured Shot list item). The Vault check checks each `ready` package's Post text like a Draft's (`draft-length`, `hashtags`, `reddit-subreddit`, `reddit-title`) and its Attachments against its Channel rules: file on disk (`attachment-files`), format (`attachment-format`), count per type (`attachment-count`), size (`attachment-size`), alt text on images and GIFs (`alt-text`), and one type per Post when `mixed_attachments: false` (`mixed-attachments`). Published Posts are not checked against disk: video files stay out of git. Once published, the Post sets `status: published`, `published_url` and `published_on` and moves to `Posts/`, the history of published Posts (`post-folder` fails a published Post left in `Publish packages/` or a ready one in `Posts/`).

### Bring your own Topic

To have the Office write a story you already have in mind, copy `docs/templates/Owner Topic.md` to `Topics/<title>.md` and fill it in. It is an Owner Topic: `status: approved` and `origin: owner` from the start, with no Digest and no `rank`. Run `/write` and it is drafted like any approved Topic; the Scout reads it too, so it never proposes the same story.

## Commands

- `/scout`: the Scout (`.claude/skills/scout/`). On the first run it builds the Project's Fact sheet and stops for approval; it writes no Digest until the Fact sheet is approved. After that it first writes a Trend scan (hot subreddit threads, meme formats, gaming and mobile news, calendar hooks; a scan up to 14 days old is reused) and refreshes the subreddit rules in `Channel rules/Reddit.md`, then writes a Digest of 5 to 8 Topics from the git history since its reading position, the GitHub issues and their discussion (read-only `gh`), the Project's local docs and the Owner notes. It skips stories already rejected, published, approved or proposed, and may bring a parked Topic back as a new note marked `previously_parked`.
- `/write`: the Writer (`.claude/skills/write/`). Turns every approved Topic into one Draft per target Channel (X, Reddit, LinkedIn, each in its register) through the six Passes, then runs the Vault check. Each Draft then goes through the Editor (`.claude/agents/editor.md`, a fresh subagent per review, which holds the checklist and pass threshold): below the threshold it goes back to the Writer, and after at most two rounds it comes to the Owner at `in-review` with the Editor's remarks. Say "use hook 2" on a Draft to swap in an alternative hook (it becomes an Owner edit).
- `/revise <draft> <prompt>`: applies your prompt, such as "shorter hook, no emoji", to one Draft (`.claude/skills/revise/`), marks the change as an Owner edit and seals it. It never changes `status`.
- `/package <draft>`: the Packager (`.claude/skills/package/`, on Sonnet). Refuses a Draft that is not `ready`; writes its Publish package with the Attachments in order, alt text and the `missing` list, then runs the Vault check. After you publish by hand, `/package published <publish package> <link>` records the link and moves the Post to `Posts/`.

## Vault check

Needs [uv](https://docs.astral.sh/uv/). Check the whole Vault, or a Vault at another path:

```sh
scripts/vault_check.py
scripts/vault_check.py path/to/vault
```

It fails any Topic, Draft or Post that links to a Project's `github` repository (`private-repo-link`): that repository is private. It prints each violation as `note: [rule] message` and exits non-zero on any violation.

Run the tests (fixture Vaults live in `tests/fixtures/`, one folder per broken rule):

```sh
uv run --with pytest --with pyyaml pytest
```
