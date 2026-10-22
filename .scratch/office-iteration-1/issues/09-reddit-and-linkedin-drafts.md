# 09: Reddit and LinkedIn Drafts

**What to build:** `/write` produces one Draft per target Channel for each approved Topic: X, Reddit and LinkedIn. Each Draft uses its Channel's register and rules: modest and not self-promotional for the chosen subreddit on Reddit, reflective with takeaways on LinkedIn. The Vault check enforces one Draft per target Channel for every approved Topic.

**Blocked by:** 07 (`/write` for one Channel (X))

**Status:** ready-for-agent

- [x] An approved Topic targeting several Channels gets exactly one Draft per Channel
- [x] Reddit Drafts name their subreddit and follow its rules
- [x] LinkedIn Drafts follow the LinkedIn register
- [x] The Vault check fails an approved Topic missing a Draft for one of its Channels, or with two Drafts for one Channel
- [x] Fixtures cover both failure cases
