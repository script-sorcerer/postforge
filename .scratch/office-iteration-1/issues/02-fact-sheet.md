# 02: Fact sheet

**What to build:** The Owner runs `/scout` for the first time. Because no approved Fact sheet exists, the Scout builds one from traffic_jam's glossary, design docs and ADRs: what the game is, who it is for, the public-name field (empty until a name exists), and what has already been shown publicly. The Scout stops and asks the Owner to approve it. Until the Owner approves, `/scout` produces no Digest.

**Blocked by:** 01 (Vault skeleton and Vault check core)

**Status:** ready-for-agent

- [x] The first `/scout` run writes a Fact sheet note drawn from the Project's own material and asks for approval
- [x] The Fact sheet holds a public-name field and a record of what has been shown publicly
- [x] `/scout` refuses to write a Digest while the Fact sheet is not approved
- [x] The Scout only reads the Project folder; nothing in traffic_jam changes
- [x] The Vault check validates the Fact sheet note
