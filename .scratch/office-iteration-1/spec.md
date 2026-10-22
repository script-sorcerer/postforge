# Spec: Office, iteration 1

Status: ready-for-agent

## Problem Statement

The Owner builds traffic_jam, a mobile traffic puzzle game, mostly with AI agents, and ships real progress every week: 344 commits, design docs, ADRs and closed issues. None of it reaches an audience. Writing posts by hand means re-reading the history, guessing which changes make a story, adapting one story to several Channels, and doing it again every week. It does not happen, so the game gains no followers and the Owner's portfolio does not grow.

## Solution

An Office: a small set of agent Roles run from Claude Code inside the postforge repository, with an Obsidian Vault in the same repository as their shared memory. On the Owner's command, the Scout reads what changed in traffic_jam since the last run, scans current trends, and delivers a Digest of Topics. The Owner approves, rejects or parks each Topic in Obsidian. On a second command, the Writer turns every approved Topic into one Draft per Channel through a fixed series of Passes, and an independent Editor checks each Draft. The Owner edits Drafts by hand or by prompt. On a third command, the Packager assembles a Publish package that the Owner publishes by hand. Iteration 1 covers X, Reddit and LinkedIn in English.

## User Stories

### Setup and Project

1. As the Owner, I want to register traffic_jam as a Project by giving its repository location, pitch and audience, so that the Office knows what it markets.
2. As the Owner, I want the Project described in config rather than in the Roles' prompts, so that a second Project can be added later without rewriting the Office.
3. As the Owner, I want the Scout to build a Fact sheet from the Project's glossary, design docs and ADRs on the first run, so that every Role shares one account of what the game is.
4. As the Owner, I want to review and approve the Fact sheet before the first Digest, so that no Topic rests on a wrong fact about the game.
5. As the Owner, I want the Fact sheet to hold a field for the game's public name, so that the Office uses the name once it exists and says "my traffic puzzle game" until then.
6. As the Owner, I want the Fact sheet to record what has already been shown publicly, so that the Office does not reveal unannounced work or repeat itself.
7. As the Owner, I want to open the postforge repository in Obsidian as its own Vault, so that I read and edit the Office's notes with a tool I already use.
8. As the Owner, I want the Office's notes kept apart from my personal Obsidian vault, so that my private notes never mix with Office state.

### Source material

9. As the Owner, I want the Scout to read the Project's git history, so that Topics come from real shipped work.
10. As the Owner, I want the Scout to read the Project's issues and their discussion through the GitHub CLI, so that it sees the reasoning and history behind a change.
11. As the Owner, I want the Scout to read design docs, ADRs, specs and other files in the Project's folder, so that Design decision and How-to Topics have substance.
12. As the Owner, I want to write Owner notes in the Vault, so that the Scout can use what exists nowhere in the code, such as a playtester's reaction.
13. As the Owner, I want the Office to only read the Project's material, so that it can never change or commit anything in traffic_jam.
14. As the Owner, I want the Scout to remember where it stopped reading, so that each Digest covers only what is new since the last one.
15. As the Owner, I want the first run to read the whole history once, so that the backlog of untold stories is not lost.

### Trend scan

16. As the Owner, I want the Scout to write a dated Trend scan before each Digest, so that Topics can ride current discussions and calendar hooks.
17. As the Owner, I want the Trend scan to cover hot threads in the gamedev subreddits, current meme formats, gaming and mobile news, and hooks such as #ScreenshotSaturday and #WIPWednesday, so that angles feel current.
18. As the Owner, I want a Trend scan older than two weeks treated as stale, so that the Office never builds on old trends.
19. As the Owner, I want the Scout to refresh the rules of the chosen subreddits during the Trend scan, so that Reddit Drafts follow each community's current rules.

### Digest and Topics

20. As the Owner, I want to start the Scout with one command, so that I decide when the Office works.
21. As the Owner, I want each Digest to hold 5 to 8 Topics ranked by strength, so that I can review one in a single sitting.
22. As the Owner, I want each Topic to state its title, angle, why now, the Source material it rests on, its Rubric and its target Channels, so that I can judge it without opening the code.
23. As the Owner, I want each Topic to carry a Shot list, so that I know what footage to capture before the Post goes out.
24. As the Owner, I want each Topic to say whether it needs media at all, so that I can tell at a glance which Topics I can ship without capturing anything.
25. As the Owner, I want Topics drawn from all eleven Rubrics, so that the feed stays varied.
26. As the Owner, I want at most two Topics of one Rubric in a Digest, so that no Digest is all Devlog.
27. As the Owner, I want promotional Topics to be at most a third of a Digest, so that the feed earns attention instead of asking for it, especially on Reddit.
28. As the Owner, I want to mark each Topic approved, rejected or parked in its note, so that I approve work with one edit.
29. As the Owner, I want to give a one-line reason when I reject a Topic, so that the Scout learns what I do not want.
30. As the Owner, I want parked Topics kept and offered again later, so that good ideas that are wrong for this week are not lost.
31. As the Owner, I want to change a Topic's Channels or angle before approving it, so that the Writer works from my version.
32. As the Owner, I want the Scout to read past rejected and parked Topics and the history of published Posts, so that it does not propose the same story twice.
33. As the Owner, I want to ask for a Russian Adaptation on a Topic, so that I control when Russian content is made.

### Writer and Passes

34. As the Owner, I want one command to turn every approved Topic into Drafts, so that I do not start each one by hand.
35. As the Owner, I want one Draft per target Channel for each approved Topic, so that each Channel gets content written for it.
36. As the Owner, I want the Writer to work through the Angle, Hooks, Draft, Voice, Humanize and Channel fit Passes in that order, so that each Pass does one job well.
37. As the Owner, I want the Angle Pass to fix the one idea and the hook of the post first, so that the Draft has a point.
38. As the Owner, I want the Hooks Pass to produce three opening lines, so that the strongest opener wins.
39. As the Owner, I want the Writer to pick the best hook and keep the two alternatives under a collapsed section, so that I can switch hooks with one sentence.
40. As the Owner, I want the Voice Pass to check the Draft against the Voice guide, so that every Post sounds like me.
41. As the Owner, I want the Humanize Pass to remove the marks of machine-written text, so that readers judge the game and not the prose.
42. As the Owner, I want the Channel fit Pass to apply the Channel's length, format, hashtag and etiquette rules, so that a Post never breaks its Channel's limits.
43. As the Owner, I want Drafts written in the first person of a solo indie developer, honest and specific, without hype words, so that they build trust.
44. As the Owner, I want the X, Reddit and LinkedIn Drafts to differ in register (short on X, modest and not self-promotional on Reddit, reflective with takeaways on LinkedIn), so that each fits its audience.
45. As the Owner, I want AI-assisted development mentioned only when it is the story itself, never as a disclaimer, so that the focus stays on the product and its quality.
46. As the Owner, I want a Russian Adaptation rewritten for Russian readers rather than translated word for word, so that it reads naturally.

### Editor

47. As the Owner, I want the Editor to run as a separate agent with a fresh context, so that it judges the Draft as a reader would, without the Writer's reasoning.
48. As the Owner, I want the Editor to score each Draft against a checklist and give specific remarks, so that its verdict is concrete.
49. As the Owner, I want a Draft below the Editor's threshold sent back to the Writer, so that weak Drafts improve before I see them.
50. As the Owner, I want at most two Editor rounds per Draft, after which the Draft comes to me with the Editor's remarks, so that the loop always ends.

### Owner edits

51. As the Owner, I want to edit a Draft by hand in Obsidian, so that I can fix things directly.
52. As the Owner, I want to edit a Draft with a prompt from Claude Code, such as "shorter hook, no emoji", so that I can direct changes without rewriting.
53. As the Owner, I want my Owner edits to always win over the Editor's, so that the Office never undoes my choices.
54. As the Owner, I want the Editor to leave a comment instead of changing a part I edited, so that I see its objection and decide.
55. As the Owner, I want to mark a Draft ready myself, so that nothing becomes a Post without my say.

### Packager and Publish package

56. As the Owner, I want one command to build a Publish package from a ready Draft, so that publishing takes a minute.
57. As the Owner, I want the Publish package to hold the final text, the Attachments in order and alt text for each image, so that I can copy it straight to the Channel.
58. As the Owner, I want to add Attachments I captured myself to a Topic or Draft, so that the Post carries real footage.
59. As the Owner, I want the Packager to check each Attachment's existence, count, format and size against the Channel rules, so that an upload never fails at the last step.
60. As the Owner, I want a Publish package to list what is missing, such as a Shot list item not yet captured, so that I know what blocks it.
61. As the Owner, I want to record the published Post's link and mark it published, so that the history of published Posts stays complete.
62. As the Owner, I want the Publish package shaped so that a scheduler such as Postiz can take it later, so that automatic publishing needs no remodelling.

### Channel rules and Vault check

63. As the Owner, I want one note of rules per Channel in the Vault, so that limits and etiquette live in one place that I can edit.
64. As the Owner, I want a Vault check that I and the Roles can run, so that a broken note, a wrong status or a Channel-limit breach is caught before I publish.
65. As the Owner, I want the Packager and the Channel fit Pass to use the same Vault check, so that the rule that blocks publishing is the rule the Writer aimed at.
66. As the Owner, I want the Vault check to report each problem with the note and the rule it breaks, so that I can fix it at once.

### Models

67. As the Owner, I want the Scout, Writer and Editor to run on the strongest model, so that taste and quality come first.
68. As the Owner, I want the Packager to run on a cheaper model, so that mechanical work does not cost much.

## Implementation Decisions

- **Office shape.** Each Role is a Claude Code skill in the postforge repository. The Editor runs as a subagent with a fresh context. No server, no UI and no agent framework. The Roles' state lives only in Vault notes.
- **Commands.** Four slash commands are the Owner's interface: scout (Trend scan, then Digest; on the first run, Fact sheet first), write (all approved Topics to Drafts, with the Editor loop), revise (one Draft plus the Owner's prompt) and package (one ready Draft to a Publish package). Free-form prompts in the chat cover everything else.
- **Vault.** The Vault lives inside the postforge repository (ADR 0001). It holds the Project config and Fact sheet, the Voice guide, Channel rules, Trend scans, Digests and Topics, Drafts, Publish packages, Owner notes, the history of published Posts, and Attachments. Video Attachments stay on disk and out of git.
- **Notes are the contract.** Every Topic, Draft and Publish package is one markdown note with YAML frontmatter. The frontmatter carries at least: kind, status, Project, Rubric (Topic), Channels (Topic) or Channel (Draft and Publish package), language, a link from each Draft to its Topic, and Attachment links. Obsidian links tie the notes together.
- **Lifecycles.** Topic: proposed, then approved, rejected or parked. Draft: drafting, in-review, revising, ready. Post: ready, then published, with the published link recorded. Only the Owner moves a Topic out of proposed and a Draft to ready.
- **Reading position.** The Project's state note records the last commit and date the Scout read. The first run has no position and reads the whole history.
- **Source material access.** The Scout reads the Project folder, its git history and its GitHub issues with read-only commands. The Office never writes to the Project.
- **Digest rules.** 5 to 8 Topics, ranked. At most two per Rubric. Promotional Topics at most a third. Each Topic states its title, angle, why now, Source material, Rubric, Channels, Shot list and whether it needs media.
- **Rubrics.** Devlog, Design decision, Gameplay moment, Building with AI agents, Ask the audience, How-to, Humor / Meme, Bug of the week, Before / After, By the numbers, Player challenge. Iteration 1 may propose Topics of every Rubric, but Humor / Meme and Player challenge have only the handling iteration 1 gives every other Topic (see Out of Scope).
- **Writer Passes.** Angle, Hooks (three opening lines), Draft, Voice, Humanize, Channel fit, always in that order. The Writer keeps the chosen hook in the body and the two alternatives in a collapsed section.
- **Editor loop.** The Editor scores against a fixed checklist with a pass threshold. Below the threshold the Draft goes back to the Writer. After two rounds the Draft goes to the Owner with the Editor's remarks, whatever the score.
- **Owner edits.** Owner edits take precedence. The Editor never changes a part the Owner edited and comments instead. How an Owner edit is marked in the note is left to the implementation, but it must be visible to the Vault check.
- **Voice guide.** One Vault note holds tone, banned words and patterns, the per-Channel register, the stance on mentioning AI, and what must never be published: code beyond short snippets, unannounced mechanics, and the game's name until it is public.
- **Channel rules.** One Vault note per Channel (X, Reddit, LinkedIn in iteration 1) with length limits, Attachment count, format and size limits, hashtag rules and etiquette. The Reddit note also lists the chosen subreddits and their rules.
- **Vault check.** A deterministic script, run from the command line by the Owner, by the Packager and by the Channel fit Pass. It reports each violation with the note and the rule broken, and exits non-zero on any violation. It checks: required frontmatter and valid statuses; Digest size and Rubric balance; one Draft per Channel for each approved Topic; Publish packages against Channel rules (text length, Attachment count, format and size, Attachments present on disk, alt text present); Owner-edited parts untouched by the Editor. The script is the only code in iteration 1 that is not a prompt.
- **Models.** Scout, Writer and Editor use Opus. The Packager uses a cheaper model.
- **Local models.** No adapter layer for local models. Roles stay plain prompts so that they can be ported to a local server later.

## Testing Decisions

- **One automated seam: the Vault check.** Tests feed fixture Vaults to the Vault check and assert its verdicts: valid fixtures pass; each broken fixture fails with the expected rule named. Fixtures cover each check listed above, one rule per broken fixture.
- **Good tests check external behavior only:** given these notes, the check reports these violations. They do not test the script's internals, and they do not test model output.
- **No tests on Role prompts.** Assertions on model text are brittle and catch nothing real. Voice and quality are judged by the Editor and the Owner.
- **Manual smoke run.** Run scout, write and package against the real traffic_jam, with the Vault check passing after each step. This is the acceptance check for iteration 1.
- **Prior art:** none in postforge. The repository has no code yet.

## Out of Scope

- Video scripts for YouTube Shorts and TikTok, and generating video of any kind.
- The Article Channel (dev.to, Habr) and its outline approval step.
- Meme concepts and trend-aware humor beyond the Trend scan itself.
- Russian Adaptations in practice. The language field exists, but only English is written in iteration 1.
- Player challenge as a linked pair of Posts with a delayed follow-up.
- Learning from Owner edits and proposing new Voice guide rules.
- Automatic publishing (Postiz or any API), Telegram review, scheduled runs.
- Local models (llama.cpp, oMLX).
- Image generation.
- A second Project.
- Results logging (likes, comments) beyond an optional manual note.

## Further Notes

- traffic_jam is a mobile game (iOS and Android), so the goal is followers and pre-registration, not Steam wishlists.
- traffic_jam's GitHub repository is private. Posts must never link to it or to its issues.
- traffic_jam has almost no media yet, so the Shot list is what makes Gameplay moment and Before / After Topics publishable.
- The Owner publishes from personal accounts as a solo indie developer.
