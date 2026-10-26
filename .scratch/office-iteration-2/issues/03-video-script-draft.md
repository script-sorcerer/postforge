# 03: Video script Draft for Shorts

**What to build:** `/write` writes a Shorts Draft as a Video script through the same six Passes. The Post text (body up to the first callout or heading) is the caption, measured against `text.max_length`. A `## Script` section follows the Writer notes with a beat table, one row per beat: `#`, `Footage` (an `[[Attachments/<file>]]` link from the Topic's Shot list, or `text` for a text-only beat), `On-screen text`, `Narration` (empty when none), `Seconds`. A `## Title` line holds the YouTube title. Shorts rules per Pass: `hooks` writes three openings as the first beat's on-screen text plus caption first line, payoff first, no setup; `draft` keeps one idea and ends on the payoff or a loop into beat 1; `channel-fit` keeps text out of the safe bands (prose rule), sums `Seconds` against `video.max_seconds`, and checks each `On-screen text` against `on_screen_text.max_chars_per_beat`. Frontmatter adds `duration_s` (the sum) and `title`. Vault check rules for a `shorts` Draft: `## Script` present with at least two beats, every beat has Footage and Seconds, `duration_s` equals the sum and is within the limit, each On-screen text within its limit, `title` within `text.max_title_length`. The Editor gets two Shorts items replacing items 5 and 6 when the Channel is `shorts`: hook lands in the first beat within 2 seconds and the clip ends on the payoff or a loop; one idea with no setup and every On-screen text readable at phone size (short labels, never a sentence pair). Threshold stays 7 of 8 with 7 and 8 at 1.

**Blocked by:** 02 (Shorts Channel rules)

**Status:** ready-for-agent

- [ ] A Shorts Draft has caption, `## Title`, `## Script` beat table, `duration_s`, `title`
- [ ] Vault check fails: missing Script, beat without Footage or Seconds, duration over the limit or not equal to the sum, on-screen text over the limit, title over the limit
- [ ] Editor checklist has the Shorts variant of items 5 and 6; Writer hands the Editor the caption, hooks, title and the beat table
- [ ] Hooks Pass for Shorts puts the payoff in beat 1
- [ ] Fixtures cover each new rule

## Comments
