# 05: Capture list

**What to build:** A script next to the Vault check builds `Capture list/<project>.md` from the Shot lists of every approved Topic: one checkbox line per file still missing from Attachments, with the Topic, the file name, what to capture and the duration, grouped by a `scene:` tag the Shot list line may carry. A Shot list line names its expected file in backticks; the Scout and the Owner Topic template require that. The Writer runs the script at the end of `/write`; the Producer points to the Capture list when it refuses a Draft for missing footage. The Shorts Channel rules gain a "Capture" section (1080x1920 portrait window or a crop around one junction, HUD hidden unless the beat shows it, game clock in the file name, no overlays). The note is regenerated, never edited by hand, and the Vault check does not check it. The Glossary defines Capture list.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Script runs on the Vault or a path, writes the note, exits zero; the note shrinks when a file appears in Attachments
- [ ] Test on a fixture Vault with two approved Topics and one captured file compares the written note to the expected text
- [ ] Scout prompt and Owner Topic template: file name in backticks per Shot list line, optional `scene:` tag
- [ ] `/write` runs the script at the end; `/produce` names the Capture list in its refusal
- [ ] Shorts rules "Capture" section; Glossary entry "Capture list"; README documents the script
