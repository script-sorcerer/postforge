---
name: revise
description: Applies the Owner's prompt (such as "shorter hook, no emoji") to one Draft and marks the change as an Owner edit. Use when the Owner runs /revise.
argument-hint: "<draft> <what to change>"
model: opus
disable-model-invocation: true
---

# Revise

You make an Owner edit for the Owner (see `GLOSSARY.md`): you apply their prompt to one Draft, word for word as they asked. You run from the postforge repository root; the Vault is this repository.

## Rules

- Change only the named Draft in `Drafts/`, and only what the prompt asks.
- **Never set `status: ready`, and never change `status` at all.** Only the Owner marks a Draft ready.
- What you write is the Owner's: it always wins over the Writer and the Editor.

## Steps

1. Find the Draft: the first argument is its name or path in `Drafts/`. If it is ambiguous or missing, ask the Owner. The rest of the argument is the prompt; if there is none, ask for it.
2. Read the Draft, then `Voice guide/Voice guide.md` and `Channel rules/<Channel>.md` for its Channel.
3. Apply the prompt to the Post text, the Alternative hooks or, on Reddit, the `title`. Keep everything the prompt does not touch.
4. Mark each changed span in the body as an Owner edit by wrapping it in Obsidian comment markers, on one line or across lines:

   ```markdown
   %% owner %%Cars now queue at full roads.%% /owner %%
   ```

   If the change falls inside or overlaps an existing Owner block, edit inside that block or widen it; never nest markers. A `title` change in frontmatter needs no marker.
5. Record the fingerprints: `scripts/vault_check.py --seal "<draft path>"`. It rewrites only `owner_edits` in the frontmatter.
6. Run `scripts/vault_check.py`. If the Owner's text now breaks a Channel limit (length, hashtags, title), do not trim it: tell the Owner what breaks and by how much, and suggest a cut.
7. Tell the Owner what you changed, with the Draft's path.
