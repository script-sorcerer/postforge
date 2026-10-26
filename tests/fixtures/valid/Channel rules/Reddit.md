---
kind: channel-rules
channel: reddit
status: proposed
text:
  max_length: 40000
  max_title_length: 300
attachments:
  image: {max_count: 20, formats: [jpg, png], max_size_mb: 20}
hashtags:
  max: 0
subreddits: [IndieDev]
destination:  # set once in the profile by the Owner: packages carry no pinned_comment
  kind: profile_link
  template: "{landing}"
  fallback: "Devlog of a mobile traffic puzzle game"
---

Etiquette.
