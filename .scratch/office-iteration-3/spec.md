# Spec: Office, iteration 3 (Content ahead, released on a schedule)

Status: ready-for-agent

## Problem Statement

Iterations 1 and 2 give the Office the whole path from Source material to a Publish package, including a rendered Short. What they do not give is a marketing operation. The Owner wants to produce content ahead of time and release it gradually, with a goal: followers and pre-registrations for the mobile release. Today a Publish package is either `ready` or `published`, with no date, no order and no cadence, so "ahead of time" means a pile of ready Posts and no plan for letting them out. Topics belong to Rubrics but not to a campaign: nothing plans the moment the game's name and store page go public, which is the one Post that turns viewers into pre-registrations. Published Posts record a link and nothing else, so the Scout ranks the next Digest blind and the borrowed best practices never become the Office's own. Every Topic carries its own Shot list, so the Owner, the only one who can capture footage, has no single list to work through in one sitting. And a Post has nowhere to send a viewer: the Voice guide rightly forbids begging for follows, but no rule says where the link lives.

## Solution

Five additions and one small one, all on the iteration 1 and 2 shape (notes in the Vault, Role prompts, the Vault check with fixture Vaults).

**Schedule.** A Schedule note per Project holds each Channel's cadence: how many Posts a week and on which weekdays. Every `ready` Publish package carries a `publish_on` date. The Packager picks the next free slot for the Channel when it writes the package. The Vault check fails a ready package whose date is not a cadence day of its Channel or collides with another package of that Channel on the same day. The Owner publishes on the date, by hand, as today.

**Campaign phases.** The Fact sheet gains a list of Phases: a name, a start date (or none yet) and what becomes public with it. Its "Not public yet" items name the Phase that lifts them. Every Topic names its Phase; a package cannot be scheduled before its Phase starts. The Scout spreads a Digest across the current and the next Phase and always proposes the reveal Topic for a Phase whose start date is set and has no Topic yet.

**Metrics on Posts.** A published Post records its numbers at two points, about two days and about seven days after publishing: views, likes, comments, shares and, where the platform shows it, retention and link clicks. The Owner enters them by hand (no platform API in this iteration). The Vault check reminds the Owner of a Post older than seven days with no seven-day entry. The Scout reads the metrics of every Post before it ranks a Digest and writes a short "What worked" section in the Digest: the Rubrics, Channels and hook levers that did best, and how that moved its ranking.

**Capture list.** A script builds one Capture list per Project from the Shot lists of every approved Topic, minus the files already in Attachments, grouped by what is captured together (the same level, the same junction, the same game clock). The Shorts Channel rules gain a capture specification (portrait capture window, hidden HUD, game clock, how to get 9:16 from a landscape game) so one recording session covers many Topics. The Owner captures from that list and reruns the script.

**Destination.** Each Channel rules note says where a Post sends a viewer (a pinned comment, the profile link, the description) and holds the template for it. The Fact sheet records the public links (store page, pre-registration, landing page) once they exist. The Packager writes the `pinned_comment` of a package from the template and the public links; while there are no public links, the pinned comment is the Channel's fallback text (for example "more clips on this channel"). The Vault check fails a ready package without a pinned comment on a Channel whose rules define a destination.

**Two captions for a Short.** A Shorts Publish package carries two captions: the YouTube one with the chosen hook and the TikTok one with the first alternative hook. The two platforms are published separately anyway, and their metrics are recorded per platform, so the Owner learns which hook held.

Out of scope: an Article Channel, a community (Discord, Telegram, a newsletter), reading metrics through platform APIs, uploading, replying to comments, any A/B beyond the two Shorts captions.

## User Stories

### Schedule

1. As the Owner, I want a Schedule note per Project with each Channel's cadence (Posts per week and weekdays), so that the Office releases at a rhythm I can keep in my worst week.
2. As the Owner, I want every ready Publish package to carry a `publish_on` date, so that a pile of ready Posts becomes a queue.
3. As the Owner, I want the Packager to pick the next free slot of the Channel when it writes a package, so that I do not plan dates by hand.
4. As the Owner, I want the Vault check to fail a ready package whose date is not one of the Channel's cadence days, so that the rhythm holds.
5. As the Owner, I want the Vault check to fail two ready packages of one Channel on the same day, so that Posts never crowd each other.
6. As the Owner, I want the Vault check to report a Channel whose next cadence day has no package while ready packages wait unscheduled, so that a gap is visible before it happens.
7. As the Owner, I want to move a package to another date by editing `publish_on`, so that a date change is one line.
8. As the Owner, I want `/package published` to keep `publish_on` on the Post next to `published_on`, so that I can see later whether I held the schedule.
9. As the Owner, I want a Shorts package scheduled on a weekday the Shorts cadence names, and X, Reddit and LinkedIn each on their own days, so that one Topic's Posts spread over the week instead of landing together.

### Campaign phases

10. As the Owner, I want the Fact sheet to hold the campaign Phases (name, start date or none, what becomes public), so that the reveal is planned, not improvised.
11. As the Owner, I want each "Not public yet" item in the Fact sheet to name the Phase that lifts it, so that the Scout knows when a story becomes allowed.
12. As the Owner, I want every Topic to name its Phase, so that a story written ahead waits for its date.
13. As the Owner, I want the Vault check to fail a package whose `publish_on` is before its Topic's Phase start, so that nothing leaks early.
14. As the Owner, I want the Vault check to fail a Topic that names a Phase the Fact sheet does not list, so that Phase names stay consistent.
15. As the Owner, I want the Scout to spread a Digest across the current Phase and the next one, so that content for the next Phase is ready before it starts.
16. As the Owner, I want the Scout to propose the reveal Topic (the name, the store page, the pre-registration link) for a Phase whose start date is set and has no Topic yet, so that the one Post that converts is never forgotten.
17. As the Owner, I want the Scout to refuse a Topic whose Source material sits in a later Phase than the one the Topic names, so that an early Phase never shows later secrets.
18. As the Owner, I want a Phase with no start date to still accept Topics and Drafts, so that I can write ahead before I know the launch date.

### Metrics

19. As the Owner, I want to record a Post's views, likes, comments, shares and, where shown, retention and link clicks at about two and about seven days, so that every Post teaches the next one.
20. As the Owner, I want the Vault check to remind me of a published Post older than seven days with no seven-day entry, so that the record stays complete.
21. As the Owner, I want to mark a Post's metrics as skipped with one line, so that a Post I chose not to measure stops the reminder.
22. As the Owner, I want the Scout to read every Post's metrics before ranking a Digest, so that Rubrics, Channels and hooks that worked rank higher.
23. As the Owner, I want the Digest to carry a short "What worked" section with the numbers it drew on, so that I can see why the ranking moved.
24. As the Owner, I want the Shorts metrics recorded per platform (YouTube and TikTok), so that the two captions can be compared.
25. As the Owner, I want the metric entries to name the hook lever the Post used, so that the Scout can rank levers, not only Rubrics.

### Capture list

26. As the Owner, I want one Capture list per Project built from the Shot lists of every approved Topic, so that I record in one sitting instead of per Topic.
27. As the Owner, I want the Capture list to leave out footage already in Attachments, so that it shows only what is left.
28. As the Owner, I want the Capture list grouped by what is captured together (same level, same junction, same game clock), so that I set up a scene once.
29. As the Owner, I want each Capture list line to name the Topic it serves and the file name the Video script expects, so that the Producer finds the file without renaming.
30. As the Owner, I want the Shorts Channel rules to hold a capture specification (portrait capture window or crop, hidden HUD, resolution, game clock), so that every capture is usable in 9:16.
31. As the Owner, I want to rerun the Capture list after a recording session and see it shrink, so that I know when a Topic is ready for `/produce`.
32. As the Owner, I want the Producer's "footage missing" refusal to point me to the Capture list, so that one note is the place to look.

### Destination

33. As the Owner, I want each Channel rules note to say where a Post sends a viewer and to hold the template for it, so that every Post has a destination without a call to action in its text.
34. As the Owner, I want the Fact sheet to hold the public links (store page, pre-registration, landing page) once they exist, so that the Packager fills them in.
35. As the Owner, I want the Packager to write a `pinned_comment` in every package from the template and the public links, so that I paste it right after publishing.
36. As the Owner, I want the pinned comment to fall back to the Channel's fallback text while no public link exists, so that early Posts still point somewhere.
37. As the Owner, I want the Vault check to fail a ready package without a pinned comment on a Channel whose rules define a destination, so that no Post goes out without one.
38. As the Owner, I want the Vault check to fail a pinned comment that links to the private repository, so that the existing rule covers it.
39. As the Owner, I want the Voice guide's ban on calls to action to stay as it is, so that the destination lives in the pinned comment and the profile, never in the Post.

### Two captions for a Short

40. As the Owner, I want a Shorts package to carry a YouTube caption with the chosen hook and a TikTok caption with the first alternative hook, so that the two platforms test two hooks.
41. As the Owner, I want both captions checked against the caption length and hashtag limits, so that neither fails at upload.
42. As the Owner, I want the TikTok caption to be the YouTube caption with only the hook line swapped, so that the two stay comparable.

### Vocabulary and docs

43. As the Owner, I want the Glossary to define Schedule, Phase, Metrics, Capture list and Destination, so that every Role uses the same words.
44. As the Owner, I want the README to document the new fields, folders and rules, so that a fresh reader can run the pipeline.

## Implementation Decisions

- **Vocabulary.** The Glossary gains: Schedule (a Project's cadence per Channel and the dates its Publish packages go out), Phase (one stage of a Project's campaign, with a start date and what it makes public), Metrics (the numbers a Post records at about two and about seven days), Capture list (the footage still to capture for every approved Topic, built from their Shot lists) and Destination (where a Channel sends a viewer after a Post: the pinned comment, the profile link or the description). A Post "goes out" on its `publish_on`; it "is published" when the Owner records the link.
- **Schedule note.** One note per Project in a new `Schedule/` folder, `kind: schedule`, with `project` and a `cadence` map: per Channel, `per_week` and `weekdays` (ISO weekday names). The Vault check treats it like a Channel rules note: it is read, not lifecycle-checked, and a missing or malformed one is reported under one rule. The Packager reads it to pick a slot: the first cadence weekday on or after today with no other ready or published package of that Channel on that date.
- **`publish_on`.** An ISO date on a Publish package, required when `status: ready`. It stays on the Post after `/package published`, next to `published_on`. Three Vault check rules: the date is a cadence weekday of the Channel (`schedule-slot`), no other ready package of the Channel has the same date (`schedule-collision`), and a Channel with an unscheduled ready package and an empty next cadence day is reported (`schedule-gap`). All three read the Schedule note; without one, only `publish_on`'s presence and format are checked.
- **Phases.** The Fact sheet gains `phases`, a list of `name`, `starts` (ISO date or empty) and `makes_public` (free text), in order. The "Not public yet" section becomes a list whose items start with the Phase name in brackets. A Topic gains `phase`, the name of one listed Phase; the Owner Topic template gets it too. Rules: `topic-phase` (the Phase exists in the Project's Fact sheet) and `phase-date` (a package's `publish_on` is on or after its Topic's Phase `starts`; an empty `starts` blocks scheduling, not drafting). The Scout's Digest step reads the Phases: it proposes Topics for the current Phase and the next, never for a later one, and proposes the reveal Topic when the next Phase has a `starts` date and no Topic in `Topics/` names it. The Scout checks every Topic's Source material against the "Not public yet" list and the Phase order.
- **Metrics.** A list field `metrics` on a published Post, each entry with `at` (`2d` or `7d`), `platform` (for Shorts: `youtube` or `tiktok`; otherwise the Channel), `views`, `likes`, `comments`, `shares`, optional `retention` (percent) and `link_clicks`, and `hook` (the lever of the hook that went out, copied from the Draft's Writer notes by the Packager into the package as `hook_lever`, so the Owner does not look it up). `metrics: skipped` is accepted. Rule `post-metrics`: a published Post whose `published_on` is more than seven days ago has a `7d` entry or `skipped`. The Scout's Digest step reads the Posts' metrics, ranks Rubrics, Channels and levers by views and comments per Post with at least two Posts of that kind, and writes a "What worked" section in the Digest; the Vault check does not check the section's content.
- **Capture list.** A new script next to the Vault check, run by the Owner or by the Writer at the end of `/write` and by the Producer before it refuses a Draft. It reads every approved Topic's Shot list, lists the lines whose file is not in Attachments (a Shot list line names its expected file in backticks, which the Scout and the Owner Topic template now require), groups lines by a `scene:` tag the Shot list line may carry (same level, same junction, same clock), and writes `Capture list/<project>.md`, `kind: capture-list`, with one checkbox line per file: Topic, file name, what to capture, duration. The note is regenerated, never edited by hand; the Vault check does not check it. The Shorts Channel rules gain a "Capture" section: 1080x1920 portrait capture window or a crop around one junction from a landscape capture, HUD hidden unless the beat shows it, game clock visible in the file name, 60 fps where the engine allows, no overlays.
- **Destination.** Each Channel rules note gains `destination` in frontmatter: `kind` (`pinned_comment`, `profile_link` or `description`), `template` (text with placeholders for the public links) and `fallback` (text used while a placeholder's link is empty). The Fact sheet gains `public_links`: `store`, `pre_registration` and `landing`, each empty until public. A Publish package gains `pinned_comment`, written by the Packager from the template; rule `pinned-comment` requires it on a Channel with a `destination`, and `private-repo-link` already covers its text. The Voice guide is unchanged.
- **Two captions for a Short.** A Shorts package carries `caption_youtube` (the Post text, unchanged) and `caption_tiktok`: the Post text with the first line replaced by the first alternative hook's caption line. The Packager writes it; `draft-length` and `hashtags` apply to both. The Post records one `metrics` entry per platform.
- **Roles touched.** Scout (Phases, What worked, Shot list file names), Writer (runs the Capture list script at the end), Producer (points to the Capture list), Packager (slot, pinned comment, hook lever, second caption). No new Role. Prompts change as text; the Vault check and the Capture list script change as code.
- **Order of tickets.** Schedule and `publish_on`; Phases; Destination and pinned comment; Metrics and What worked; Capture list and capture specification; two captions; Glossary and README; a smoke run with the five Shorts candidates once the Fact sheet is approved.

## Testing Decisions

- **One seam, the existing one: the Vault check against fixture Vaults.** Every new rule gets one fixture folder under the tests' fixtures with the smallest Vault that breaks exactly that rule, and the valid fixture Vault grows a Schedule note, Phases, a scheduled package with a pinned comment and a Post with metrics so it still passes. A test asserts the rule name and the note in the output, as the existing rule tests do.
- **The Capture list script is tested through the same seam shape:** a fixture Vault with two approved Topics, one captured file, and the expected note text; the test runs the script and compares the note.
- **Good tests check external behaviour only:** the violation line a note produces, the note the script writes. Never the parsing helpers.
- **Role prompts are not unit tested.** The smoke run ticket runs `/scout`, `/write`, `/package` once on the real Project and records what each Role did with Phases, slots, pinned comments and the Capture list.
- **Prior art:** the existing Vault check test module with one fixture folder per rule, and iteration 2's smoke run ticket.

## Out of Scope

- An Article Channel (dev.to, Habr) as the long-form anchor Shorts point to.
- Community channels (Discord, Telegram, a newsletter) and replying to comments.
- Reading metrics from platform APIs or dashboards; uploading or scheduling on the platforms themselves.
- A/B testing beyond the two Shorts captions; per-platform hooks for X, Reddit or LinkedIn.
- Paid promotion.
- Changing the Voice guide's stance on calls to action.

## Further Notes

- Best practices behind these decisions, read on 2026-10-27 and cited in the Shorts Channel rules: hold a cadence you can keep in your worst week; Shorts resurface for months while TikTok fades in about two days, so titles are evergreen searchable phrases; a viral clip with no store page is wasted, so plan the reveal; lead with the most interesting true thing, never with the ask; put the link in the pinned comment because descriptions are nearly invisible on mobile.
- The Project's name and store page are expected soon. Until the Fact sheet's `public_links` are filled, every pinned comment uses the fallback text; the reveal Topic is written ahead and waits for its Phase date.
- The five Shorts candidates from 2026-10-27 (in the session scratchpad, not in the Vault) are the smoke run's input once the Fact sheet is approved: each gets a Phase and a scene tag on its Shot list lines.
- Iteration 2's rule that only the Owner sets `ready`, `approved` and `published` stays; `publish_on` is set by the Packager and moved by the Owner.
