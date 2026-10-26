# 01: Schedule and `publish_on`

**What to build:** The Owner keeps a Schedule note per Project with each Channel's cadence (Posts per week, weekdays). Every `ready` Publish package carries a `publish_on` date; the Packager picks the first cadence weekday on or after today with no other ready or published package of that Channel on it. The Vault check fails a ready package whose date is not a cadence weekday of its Channel (`schedule-slot`), two ready packages of one Channel on one date (`schedule-collision`), and reports a Channel whose next cadence day is empty while an unscheduled ready package waits (`schedule-gap`). Without a Schedule note only `publish_on`'s presence and ISO format are checked. `/package published` keeps `publish_on` on the Post next to `published_on`. The Glossary defines Schedule; the README documents the note, the field and the rules.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] A Schedule note (`kind: schedule`, `project`, `cadence` per Channel with `per_week` and `weekdays`) is read by the Vault check; a malformed one is reported under one rule
- [ ] A ready package without `publish_on`, or with a non-ISO value, fails
- [ ] `schedule-slot`, `schedule-collision` and `schedule-gap` each have a fixture Vault that breaks only that rule, and the valid fixture Vault gains a Schedule note and a scheduled package
- [ ] `/package` writes `publish_on` from the next free slot and tells the Owner the date
- [ ] `/package published` carries `publish_on` onto the Post
- [ ] Glossary entry "Schedule"; README paragraph on scheduling
