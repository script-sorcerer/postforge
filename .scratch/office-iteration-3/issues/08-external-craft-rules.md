# 08: External craft rules from agency-agents

**What to build:** Carry the rules the Owner ticks below into the Channel rules notes and `docs/producer-setup.md`, each marked `External` in its Kind column (or as a `Source:` line) with the file it came from and the date it was read. Nothing else from the repository comes in: no personas, no invented metrics, no agents installed.

**Source:** <https://github.com/msitarzewski/agency-agents> (MIT), commit `b37b5bb` of 2026-10-25, read 2026-10-27. Files under `marketing/`: `marketing-twitter-engager.md`, `marketing-reddit-community-builder.md`, `marketing-linkedin-content-creator.md`, `marketing-tiktok-strategist.md`, `marketing-video-optimization-specialist.md`, `marketing-short-video-editing-coach.md`, `marketing-content-creator.md`. The repository dates none of its platform claims; every rule below is "as the repository says", not verified against the platform.

**Blocked by:** none

**Status:** ready-for-human

How to read a line: the rule as it would stand in our note, then where it goes, the source file, and a note on fit. The Owner ticks a box to accept, strikes a line to reject, and edits the wording in place. A ticked rule goes into the named note with `status: proposed` until the Owner re-approves that note.

## X (`Channel rules/X.md`)

Nothing new. `marketing-twitter-engager.md` is about live engagement, Spaces, crisis response and ads. Its content rules (one idea, value first, reply to mentions, link in a reply) are already in the Etiquette section.

- [ ] Promotion share: at most one Post in ten is a store or pre-registration pitch; the rest show the game or a lesson. Goes to Etiquette, House rule adapted from the repository's 10% promotional share. Source: `marketing-twitter-engager.md` ("Tweet Mix Strategy"). Fit: the Schedule note decides cadence, so this may belong there instead.

## Reddit (`Channel rules/Reddit.md`)

The 90/10 rule, subreddit rules first, no cross-posting the same text, and replying early are already in the note.

- [ ] Say I am the developer in the title, flair or first line; never let a reader find out from the comments. Goes to Etiquette, House rule. Source: `marketing-reddit-community-builder.md` ("Transparent Honesty: Open about affiliations"). Fit: matches the Voice guide's first person and the subreddits' self-promotion rules.
- [ ] A post gives the lesson or the clip in full; it never ends on "link in comments" or "DM me". Goes to Etiquette, House rule. Source: same file ("Value-First Engagement"). Fit: the destination is already the profile link, so this closes the loophole.

## LinkedIn (`Channel rules/LinkedIn.md`)

- [ ] Links: never in the body; the one link goes in the first comment (today: "fine but cost reach; prefer the first comment"). Goes to Etiquette and the Limits table as `External`. Source: `marketing-linkedin-content-creator.md` ("No Links in the Post Body"). Fit: the `destination` block already does this; the wording in Etiquette just gets strict.
- [ ] Reply to every comment within the first hour after publishing. Goes to Etiquette, `External`. Source: same file ("Never Post and Ghost"; "Early velocity: first-hour engagement determines distribution"). Fit: Reddit has the same line; the Schedule should then not place a LinkedIn Post at an hour the Owner is away.
- [ ] Carousel (PDF document) shape: slide 1 stands alone as a Post, one idea and at most 15 words per interior slide, the payoff on the second-to-last slide, the last slide one plain line (no "follow for more"). Goes to a new "Carousel" section, `External`, adapted: the repository's CTA slide is dropped for the Voice guide's ban on generic calls to action. Source: same file ("Carousel Deep Architecture"). Fit: our Attachment rules allow one PDF but say nothing about its content.
- [ ] Post shapes the Writer may pick for the Angle Pass: story (one moment, the tension, what happened, the takeaway), lesson (what most people get wrong, the correct model, the proof), number (the surprising number first, why it matters, one implication). Goes to Etiquette as "Shapes", `External`. Source: same file ("Post Construction by Type"). Fit: the "opinion" shape (state the take, defend it) is left out, it pulls toward the hype register the Voice guide bans.
- [ ] Posting window: Tuesday to Thursday, 07:00 to 09:00 or 12:00 to 13:00 in the audience's timezone. Goes to `Schedule/`, not Channel rules, `External (unverified)`. Source: same file ("Phase 6"). Fit: a claim with no source in the repository; take it as a tie-breaker between free slots, not a rule.
- [ ] Rejected candidate, recorded so it is not re-proposed: "break the text at a tension point so the insight sits after `see more`". Conflicts with the Voice guide ("lead with the thing itself"). Source: same file ("Phase 4").

## Shorts (`Channel rules/Shorts.md`)

Already covered and skipped: hook in the first seconds (ours is stricter), 15% safe bands, burned captions, hard cut before/after, no end card, loops, no cross-post watermark, 60 fps capture, file naming.

- [ ] Every on-screen label stays readable: at least one of a backdrop bar, a stroke or a drop shadow, and the label colour contrasts with the footage behind it. Goes to "Video", `External`. Source: `marketing-short-video-editing-coach.md` ("Subtitle typography aesthetics"). Fit: checkable on the Producer's one snapshot per beat.
- [ ] Label animation lasts 0.3 to 0.5 seconds; a label is on screen for at least 1 second. Goes to "Video", `External`. Source: same file ("Text animation"; "Subtitle timing", adapted from narration subtitles to labels). Fit: the house template's `captions.html` carries the timing, so this is a template rule as much as a Channel rule.
- [ ] Label size: body labels 30 to 36 px, a title label 48 to 64 px, at 1080x1920. Goes to "Video", `External (unit unclear)`. Source: same file ("Font size guidelines"). Fit: the repository does not say which resolution its px refer to; verify on one snapshot at phone size before adopting the numbers.
- [ ] Transitions: hard cuts between beats; one dissolve at most, only where the beat table asks for it. Goes to "Video", `External`. Source: same file ("Transition design": "if a hard cut works, don't add a fancy transition"). Fit: Producer rule 7 already forbids proposed transitions; this states the default.
- [ ] Sound: the game's own audio or none; no third-party music burned into the file. A trending sound, if ever, is added at upload from the platform's own library, and only on that platform's copy. Goes to "Video", `External`. Source: same file ("Platform Rules & Copyright Red Lines"; "BGM selection principles"). Fit: extends the existing "game's own sound is welcome" line with the copyright side.
- [ ] Fonts in the house template: only fonts licensed for commercial use, named in the template. Goes to "Video" or to `docs/templates/shorts-composition/`, `External`. Source: same file ("Font copyright"). Fit: a one-time check of `index.html` and `captions.html`.
- [ ] Thumbnail (YouTube picks a frame for a Short): choose the frame from the first beat that shows the payoff with its label, high contrast, at most three words of text. Goes to "Caption and hashtags" or the Publish package, `External (adapted from long-form YouTube)`. Source: `marketing-video-optimization-specialist.md` ("Clickability Without Clickbait"). Fit: the Packager would need a `thumbnail_at` seconds field; small, but a new field.
- [ ] Rejected candidate: TikTok hashtags 5 to 8 (`marketing-tiktok-strategist.md`). Our house rule is 3; keep it.
- [ ] Rejected candidate: three hook variants per post, "curiosity gap, bold claim, specific story" (`marketing-linkedin-content-creator.md`, `marketing-video-optimization-specialist.md`). The Writer already produces two Alternative hooks from the five levers in the Glossary; "bold claim" is the hype register.

## Producer (`docs/producer-setup.md`, render check)

These are technical and checkable with `ffprobe` and `ffmpeg`; none changes a Role's behaviour beyond the render check in rule 4.

- [ ] Render target: 1080x1920, 60 fps (gaming footage), H.264, 8 to 15 Mbps, AAC 256 kbps stereo. Goes to rule 4 as the expected output, `External`. Source: `marketing-short-video-editing-coach.md` ("Multi-Platform Export Optimization"; "Encoding & export settings"). Fit: unknown what `render --quality delivery` produces; the first render tells, then the numbers either stand or get corrected.
- [ ] After the render, `ffprobe` checks frame rate and that an audio stream exists, beside the duration and size it checks today. Goes to rule 4, `External`. Source: same file ("Pre-export checklist"). Fit: two more fields in one command.
- [ ] Loudness: integrated loudness about -14 LUFS, true peak at or below -1 dBFS (`ffmpeg -af loudnorm=print_format=json` to measure). Goes to rule 4, `External`. Source: same file ("Mix balance"). Fit: only matters when the game's audio is in the file; a silent render skips it.
- [ ] Rejected candidates: colour grading, LUTs, speed ramps, particle effects, AI cutout, avatars, proxy editing, team workflow. Game capture does not need them and Producer rule 7 forbids proposing them.

## Not taken from the repository, on purpose

- Every "Success Metrics" block (engagement 25%, 300% leads, 8% CTR, 10,000 karma): invented targets with no source.
- Every persona ("Identity & Memory", "Communication Style", "vibe"): the Glossary avoids "agency" and "agent" for a Role, and the Roles already have their own contracts.
- Engagement tactics (priming the feed with comments before posting, Spaces, AMAs, influencer tiers, ads, crisis protocols): outside the Office's job, which ends at the Publish package.

## Comments

- 2026-10-27: Opened after reading the repository on 2026-10-27. Nothing applied yet; the Owner ticks, then the ticked lines go into the notes in one commit.
