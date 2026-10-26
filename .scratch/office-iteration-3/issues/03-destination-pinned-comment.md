# 03: Destination and pinned comment

**What to build:** Each Channel rules note says where a Post sends a viewer: `destination` with `kind` (`pinned_comment`, `profile_link` or `description`), `template` with placeholders for the public links, and `fallback` text for while a link is empty. The Fact sheet records `public_links` (`store`, `pre_registration`, `landing`), empty until public. The Packager writes `pinned_comment` in every package from the template and the links, using the fallback while a link is empty. The Vault check fails a ready package without `pinned_comment` on a Channel whose rules define a destination (`pinned-comment`); the existing `private-repo-link` rule covers its text. The Voice guide stays unchanged. The Glossary defines Destination.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] All four Channel rules notes carry a `destination` with template and fallback; `channel-rules` reports a malformed one
- [ ] Fact sheet carries `public_links`
- [ ] `/package` writes `pinned_comment`; with empty links it uses the fallback and says so to the Owner
- [ ] `pinned-comment` fixture Vault; a pinned comment linking the private repository fails `private-repo-link` (fixture)
- [ ] Glossary entry "Destination"; README documents the field and where the Owner pastes it
