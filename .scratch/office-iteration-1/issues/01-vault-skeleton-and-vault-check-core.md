# 01: Vault skeleton and Vault check core

**What to build:** The Owner opens the postforge repository in Obsidian as its own Vault and finds a home for every kind of Office note, plus the traffic_jam Project registered in config (repository location, pitch, audience, read-only access). The Owner runs the Vault check from the command line: it reads every note, checks required frontmatter and valid statuses for Topics, Drafts and Posts, and reports each violation with the note and the rule broken, exiting non-zero on any violation. Fixture Vaults prove it: valid ones pass, each broken one fails naming its rule.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] The repository opens in Obsidian as a Vault with a place for Project config, Fact sheet, Voice guide, Channel rules, Trend scans, Digests and Topics, Drafts, Publish packages, Owner notes, published Posts and Attachments
- [ ] traffic_jam is registered as a Project in config, not in any Role prompt
- [ ] The Vault check runs from the command line over the whole Vault
- [ ] It rejects a Topic, Draft or Post note with missing required frontmatter or a status outside its lifecycle
- [ ] Each reported violation names the note and the rule broken; any violation gives a non-zero exit
- [ ] Fixture Vaults cover one valid case and one broken case per rule, and a test run passes
- [ ] The real Vault passes the check
