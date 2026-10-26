# 04: Metrics and "What worked"

**What to build:** A published Post records `metrics`: entries with `at` (`2d` or `7d`), `platform` (the Channel, or `youtube` / `tiktok` for Shorts), `views`, `likes`, `comments`, `shares`, optional `retention` and `link_clicks`, and `hook` (the lever that went out). The Packager copies the lever from the Draft's Writer notes into the package as `hook_lever` so the Owner never looks it up. `metrics: skipped` is accepted. The Vault check reports a published Post more than seven days old with no `7d` entry and not skipped (`post-metrics`). Before ranking a Digest the Scout reads every Post's metrics, ranks Rubrics, Channels and levers by views and comments where at least two Posts of that kind exist, and writes a "What worked" section in the Digest with the numbers it drew on. The Glossary defines Metrics.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] `metrics` schema validated: `at`, `platform`, integer counts, optional fields; a malformed entry is reported
- [ ] `post-metrics` fixture Vault (old Post without `7d`), and a skipped Post passes
- [ ] `/package` writes `hook_lever`; `/package published` keeps it on the Post
- [ ] Scout prompt: read metrics, "What worked" section, ranking rule with the two-Post minimum
- [ ] Glossary entry "Metrics"; README documents how the Owner records numbers
