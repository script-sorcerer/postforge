---
kind: channel-rules
channel: x
status: proposed
text:
  max_length: 280
attachments:
  image: {max_count: 4, formats: [jpg, png], max_size_mb: 5}
  video: {max_count: 1, formats: [mp4], max_size_mb: 512}
hashtags:
  max: 1
destination:
  kind: email
  template: "Store page: {store}"
  fallback: "more clips on this channel"
---

Etiquette.
