---
kind: schedule
project: "[[traffic_jam]]"
# Per Channel: Posts a week and the weekdays they go out on. Each Channel has its own days,
# so one Topic's Posts spread over the week. The Packager picks the next free day; edit a
# package's `publish_on` to move it.
cadence:
  shorts:
    per_week: 2
    weekdays: [Tuesday, Saturday]
  x:
    per_week: 2
    weekdays: [Monday, Thursday]
  reddit:
    per_week: 1
    weekdays: [Wednesday]
  linkedin:
    per_week: 1
    weekdays: [Friday]
---

# Schedule: traffic_jam

A rhythm the Owner can keep in the worst week: six Posts a week, one Channel a day, Sunday free.
