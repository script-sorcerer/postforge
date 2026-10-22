# 11: `/package` and Publish package

**What to build:** The Owner runs `/package` on a ready Draft and gets a Publish package: the final text, the Attachments in order and alt text for each image, plus a list of anything missing (such as a Shot list item not yet captured). The Owner adds captured Attachments to the Topic or Draft. The Packager runs the Vault check, which checks each Attachment's presence on disk, count, format and size against the Channel rules. After publishing by hand, the Owner records the link and marks the Post published, and it joins the history of published Posts. The Publish package is shaped so that a scheduler such as Postiz could take it later.

**Blocked by:** 06 (Voice guide and Channel rules), 07 (`/write` for one Channel (X))

**Status:** ready-for-agent

- [ ] `/package` refuses a Draft that is not ready
- [ ] The Publish package holds final text, ordered Attachments, alt text and a missing-items list
- [ ] The Packager runs on the cheaper model
- [ ] The Vault check fails a Publish package with a missing Attachment file, too many Attachments, a wrong format or size, or an image without alt text
- [ ] Marking a Post published with its link adds it to the history of published Posts
- [ ] Fixtures cover each Attachment rule
