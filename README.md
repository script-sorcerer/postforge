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

A Fact sheet carries `kind: fact-sheet`, `status` (`proposed`, then `approved` by the Owner), `project`, `public_name` (empty until the name is public) and `shown_publicly` (a list).

Each Channel rules note carries the Channel's limits in frontmatter (`channel`, `text.max_length`, `media.<type>` with `max_count`, `formats` and `max_size_mb`, `hashtags.max`); the Vault check reads limits from there and reports a note missing any of them under `channel-rules`.

## Commands

- `/scout`: the Scout (`.claude/skills/scout/`). On the first run it builds the Project's Fact sheet and stops for approval; it writes no Digest until the Fact sheet is approved.

## Vault check

Needs [uv](https://docs.astral.sh/uv/). Check the whole Vault, or a Vault at another path:

```sh
uv run scripts/vault_check.py
uv run scripts/vault_check.py path/to/vault
```

It prints each violation as `note: [rule] message` and exits non-zero on any violation.

Run the tests (fixture Vaults live in `tests/fixtures/`, one folder per broken rule):

```sh
uv run --with pytest --with pyyaml pytest
```
