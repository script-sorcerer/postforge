# 04: Hooks Pass with five levers and anti-patterns

**What to build:** Fold the hook practice of samber/cc-skills `copywriting-hooks` into the Writer's `hooks` Pass, as text in `.claude/skills/write/SKILL.md`, no install. The three hooks must pull different levers from five: open a gap, break a prediction, drop into a scene, promise a payoff, borrow weight (a real number or name from the Source material). At least one hook is sensory (a scene or a concrete detail) and one is reader-direct (a problem, a conditional, a promise). A hook anti-pattern list goes into the Voice guide's "Banned words and patterns" section so the Editor's item 7 already covers it: rhetorical throat-clearing ("Have you ever wondered", "Did you know"), hype labels ("Hot take:", "Unpopular opinion:"), unsourced statistics ("studies show"), "It's not just X, it's Y", time framing without a date ("recently"). The Writer notes record each hook's lever in one word so the Owner can see the spread. Editor item 1 adds: the hook pulls at least one lever and leads with the thing itself.

**Blocked by:** none

**Status:** resolved

- [x] Writer `hooks` Pass names the five levers and the diversification rule
- [x] Voice guide lists the hook anti-patterns under Banned words and patterns
- [x] Writer notes record the lever per hook
- [x] Editor item 1 names the lever test
- [x] One existing Draft rewritten through the new Pass as a check, by hand, not committed as a Post

## Comments

- 2026-10-26: Resolved in commit HASH04. Levers, diversification rule and the `Hooks: body=..., 1=..., 2=...` Writer notes line are in `.claude/skills/write/SKILL.md`; the anti-patterns sit under the Voice guide's Banned words and patterns (the Voice guide is Owner-approved: the Owner should reread that section); Editor item 1 names the lever test. The Vault has no real Draft yet, so the hand check used the fixture `tests/fixtures/valid/Drafts/Road capacity explained - x.md`: its three hooks pull weight, scene and gap, but none is reader-direct, which the new rule catches. Rewritten by hand, not committed: body (scene) "Past a road's capacity, cars in my traffic puzzle game now queue at the junction instead of driving through each other."; 1 (payoff, reader-direct) "If your traffic sim feels fake, give every road one number: its capacity."; 2 (prediction) "I expected a capacity rule to be a balance tweak. It changed how the whole map plays." Left out: no Vault check rule for levers (it is prose judgement, scored by the Editor).
