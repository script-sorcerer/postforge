# Spec: Office, iteration 2 (Shorts and Owner Topics)

Status: needs-triage

## Problem Statement

Iteration 1 turns the Project's git history into X, Reddit and LinkedIn Posts, with the Scout as the only source of Topics. Two things stay outside the Office. First, short vertical video: the Glossary names Shorts and TikTok as Channels and the Topic carries a Shot list, but no Role writes a Video script and nobody makes the video, so the Channel with the most reach for a game is empty. Second, the Owner's own ideas: a story the Owner already has in mind must wait for a Digest and compete with the Scout's Topics, or be written by hand outside the Office.

## Solution

Two additions, both reusing the iteration 1 shape (Topic, Draft with six Passes, Editor loop, Publish package, Vault check).

**Owner Topics.** The Owner writes a Topic note by hand from a template, already `approved`, with `origin: owner`. It needs no Digest, no rank and no Trend scan. From there the Writer, Editor, Producer and Packager treat it like any Scout Topic. The Scout reads it like any other Topic so it never proposes the same story.

**Shorts Channel.** A fourth Channel, `shorts`, for YouTube Shorts and TikTok with one 9:16 Draft for both. The Writer's Draft for this Channel is a Video script: a caption (the Post text) plus a Script section with a beat table (footage file, on-screen text, narration, seconds), written through the same six Passes with Shorts-specific rules in the `hooks` and `channel-fit` Passes. The Editor scores it with two Shorts-specific items. A new Role, the Producer (`/produce`), builds a HyperFrames composition from a ready Shorts Draft and the Owner's captured footage, renders the MP4 and attaches it to the Draft (ADR 0002). The Packager then packages it like any Post.

**Better hooks and humanizing.** Two external practices folded into the Writer and Editor as text, no install: the five hook levers with a diversification rule and an anti-pattern list (from samber/cc-skills `copywriting-hooks`), and the minimal-repair contract for the Humanize Pass (from theclaymethod `unslop`). These apply to every Channel.

Out of scope: generated footage, avatars or voiceover (the Producer uses only real Attachments and text; `media-use` is not installed), Russian Adaptations of Shorts, a Shorts-specific Trend scan, uploading anything.

## User Stories

### Owner Topics

1. As the Owner, I want to write a Topic by hand from a template and mark it approved at once, so that an idea of mine goes to the Writer without a Digest.
2. As the Owner, I want the Vault check to accept my Topic without a rank or a Digest, so that the template stays short.
3. As the Owner, I want the Scout to see my Topics as it sees its own, so that it never proposes a story I already told.
4. As the Owner, I want my Topic to carry the same Angle, Source material and Shot list sections, so that the Writer and the Producer work from the same shape.

### Shorts Channel and Video script

5. As the Owner, I want a `shorts` Channel with its rules note (9:16, duration, caption length, hashtags, video format and size, the top and bottom safe bands), so that one Draft serves YouTube Shorts and TikTok.
6. As the Owner, I want the Writer to produce a Video script for a Shorts Draft: a caption and a beat table where each beat names its footage file or screenshot, on-screen text, narration and seconds, so that the Producer can build it without guessing.
7. As the Owner, I want the Hooks Pass for Shorts to put the payoff in the first two seconds and to end on the payoff or a loop into the opening, so that the clip holds viewers who decide in one second.
8. As the Owner, I want the Vault check to fail a Shorts Draft whose beats add up to more than the Channel's maximum seconds, whose on-screen text is longer than the Channel's limit, or that lacks a Script section, so that no script reaches the Producer broken.
9. As the Owner, I want the Editor to score a Shorts Draft on two added items (hook in the first two seconds, one idea with no setup, captions readable at phone size), so that weak scripts go back before I see them.
10. As the Owner, I want a Shorts Draft to work with no narration (on-screen text and the game's own sound only), so that I never have to record a voice.

### Producer

11. As the Owner, I want to run `/produce <draft>` on a ready Shorts Draft and get an MP4, so that the video gets made.
12. As the Owner, I want the Producer to use only my captured footage and screenshots from `Attachments/`, text, and HyperFrames registry blocks, so that nothing in the video is invented.
13. As the Owner, I want the Producer to refuse a Draft that is not ready or whose footage files are missing, listing the missing Shot list lines, so that I know what to capture.
14. As the Owner, I want the composition source kept under `Attachments/video/<topic title>/` and committed, and the MP4 kept out of git, so that I can re-render and the repository stays small.
15. As the Owner, I want the Producer to preview or re-render after I edit the composition by hand, so that a small fix needs no new script.
16. As the Owner, I want the Producer to set the MP4 as the Draft's Attachment, so that `/package` works unchanged.
17. As the Owner, I want the Packager to carry the caption as the Post text and the MP4 as the one Attachment, with a title for YouTube, so that I publish by hand from one note.

### Hooks and Humanize

18. As the Owner, I want the Hooks Pass to write its three hooks from different levers (open a gap, break a prediction, drop into a scene, promise a payoff, borrow weight), at least one sensory and one reader-direct, so that the alternatives are real choices.
19. As the Owner, I want a hook anti-pattern list (rhetorical questions, "Hot take", unsourced statistics, "it's not just X, it's Y") checked in the Hooks Pass and by the Editor, so that clichés never reach me.
20. As the Owner, I want the Humanize Pass to edit only the sentences with a confirmed banned word or pattern and copy every other sentence unchanged, so that it never rewrites my meaning or my Owner edits.

### Tooling

21. As the Owner, I want HyperFrames' own skills installed inside this repository and the Node and FFmpeg requirements checked once, so that the Producer works on a fresh clone.
22. As the Owner, I want the Producer to spend as little Claude Code usage as a video allows: a house template, one check, one frame per beat, review in the desktop app, one render on my word, and no proposals, so that videos do not eat the quota the Posts need.

## Tickets

See `issues/`. Order: 01 Owner Topic, 02 Shorts Channel rules, 03 Video script Draft, 04 Hooks Pass, 05 Humanize Pass, 06 HyperFrames install, 07 Producer, 08 Package Shorts, 09 Smoke run.
