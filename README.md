# Postforge

A content and marketing Office: agent Roles that turn a Project's work into ready-to-publish Posts. See `GLOSSARY.md` for the vocabulary.

## The Vault

Open this repository in Obsidian as its own Vault (ADR 0001). Its folders:

| Folder | Holds |
|---|---|
| `Projects/` | Project config, one note per Project (`traffic_jam.md`) |
| `Fact sheets/` | One Fact sheet per Project |
| `Voice guide/` | The Voice guide |
| `Channel rules/` | One note per Channel |
| `Trend scans/` | Dated Trend scans |
| `Digests/`, `Topics/` | Digests and their Topic notes |
| `Drafts/` | One Draft per Channel per approved Topic |
| `Publish packages/` | Posts ready to publish |
| `Posts/` | Published Posts |
| `Owner notes/` | The Owner's free-form notes |
| `Attachments/` | Images and videos (videos stay out of git) |

Topic, Draft and Post notes carry YAML frontmatter (`kind`, `status`, `project`, `language`, plus `rubric` and `channels` on a Topic, `topic` and `channel` on a Draft or Post, `published_url` on a published Post).

A Topic also carries `rank`, `needs_media`, `promotional`, a one-line `reason` once the Owner rejects it, and `previously_parked` (a link to the parked Topic it brings back, or empty); its `rubric` is one of the eleven Rubrics, its `channels` each one of `x`, `reddit`, `linkedin`, and its body has the sections `## Angle`, `## Why now`, `## Source material` and `## Shot list`. A Digest carries `kind: digest`, `project`, `date` and `topics`, the links to its Topic notes, best first (their `rank`s run 1 to N in that order), and `trend_scan`, the link to the Trend scan it built on (at most 14 days older than the Digest).

A Trend scan (`Trend scans/<YYYY-MM-DD> Trend scan.md`) carries `kind: trend-scan`, `date` (ISO) and `sources` (URLs).

The Project note holds `github` (the repository's `owner/name` slug, read with `gh`) and the Scout's reading position (`last_read_commit`, `last_read_date`); empty means the next Digest reads the whole git history.

A Fact sheet carries `kind: fact-sheet`, `status` (`proposed`, then `approved` by the Owner), `project`, `public_name` (empty until the name is public) and `shown_publicly` (a list).

A Draft also carries `passes`, the Writer's Passes in the order they ran (`angle`, `hooks`, `draft`, `voice`, `humanize`, `channel-fit`); all six once it leaves `drafting`. Its `topic` must link to an existing Topic note. Its body holds the Post text, then an `> [!note]- Alternative hooks` callout and `## Writer notes`. The Post text is the body up to the first line starting with `> [!` or `## `; the Vault check measures it against the Channel's `text.max_length` (URLs count as written, stricter than X's 23). After the Editor loop a Draft also carries `editor_rounds` (at most 2), `editor_score` and one `## Editor review N` section per round.

Each Channel rules note carries the Channel's limits in frontmatter (`channel`, `text.max_length`, `attachments.<type>` with `max_count`, `formats` and `max_size_mb`, `hashtags.max`); the Vault check reads limits from there and reports a note missing any of them under `channel-rules`.

## Commands

- `/scout`: the Scout (`.claude/skills/scout/`). On the first run it builds the Project's Fact sheet and stops for approval; it writes no Digest until the Fact sheet is approved. After that it first writes a Trend scan (hot subreddit threads, meme formats, gaming and mobile news, calendar hooks; a scan up to 14 days old is reused) and refreshes the subreddit rules in `Channel rules/Reddit.md`, then writes a Digest of 5 to 8 Topics from the git history since its reading position, the GitHub issues and their discussion (read-only `gh`), the Project's local docs and the Owner notes. It skips stories already rejected, published or in the pipeline, and may bring a parked Topic back as a new note marked `previously_parked`.
- `/write`: the Writer (`.claude/skills/write/`). Turns every approved Topic into one Draft per target Channel (X for now) through the six Passes, then runs the Vault check. Each Draft then goes through the Editor (`.claude/agents/editor.md`, a fresh subagent per review, which holds the checklist and pass threshold): below the threshold it goes back to the Writer, and after at most two rounds it comes to the Owner at `in-review` with the Editor's remarks. Say "use hook 2" on a Draft to swap in an alternative hook.

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
