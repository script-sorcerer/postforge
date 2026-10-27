# 02: Campaign Phases

**What to build:** The Fact sheet lists the Project's Phases in order (`name`, `starts` as an ISO date or empty, `makes_public`), and each "Not public yet" item names in brackets the Phase that lifts it. Every Topic names its `phase`; the Owner Topic template has the field. The Vault check fails a Topic whose Phase is not in its Project's Fact sheet (`topic-phase`) and a package whose `publish_on` is before its Topic's Phase `starts` (`phase-date`; an empty `starts` blocks scheduling, not drafting). The Scout proposes Topics for the current Phase and the next one only, checks each Topic's Source material against the Phase order and the "Not public yet" list, and proposes the reveal Topic (name, store page, pre-registration) whenever the next Phase has a `starts` date and no Topic names it yet. The Glossary defines Phase.

**Blocked by:** 01 Schedule and `publish_on`

**Status:** resolved

- [x] Fact sheet template and the existing Fact sheet carry `phases`; "Not public yet" items start with `[<Phase>]`
- [x] Topic and Owner Topic template carry `phase`; `topic-phase` and `phase-date` have fixture Vaults; the valid fixture passes with Phases
- [x] Scout prompt: current and next Phase only, reveal Topic rule, Source material checked against Phase order
- [x] A package for a Topic in a Phase with empty `starts` fails `phase-date` with a message that says the Phase has no date
- [x] Glossary entry "Phase"; README documents Phases

## Comments

- 2026-10-27: Resolved in commit 1831227; review fixes in b79f48e, 915b9c6 and 14032db (no crash on a list `phase`, Phase date order, strict `starts`). Fact sheet Phases (Pre-reveal 2026-10-27, Reveal and Launch undated) and the `[never]` tag are proposals for the Owner (Open question 9). The Packager refuses to schedule before a Phase starts.
