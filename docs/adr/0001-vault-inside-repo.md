# The Vault lives inside the postforge repository

The Office's shared memory is an Obsidian vault kept inside the postforge git repository, next to the Roles' skills and config. The Owner opens that folder as its own vault. This puts code and content under one history, lets Roles and the Owner edit the same files, and keeps the Office's notes apart from the Owner's personal vault at `~/Documents/Obsidian Vault`.

## Considered Options

- A `Postforge/` folder inside the Owner's existing vault: rejected because personal notes would mix with Office state and the content would not be versioned with the skills.
- A separate vault outside the repo: rejected because it splits one change (a skill and the notes it reads) across two places.

## Consequences

Attachments are committed to git, so large video files need Git LFS or must stay out of the Vault before the repository gets big.
