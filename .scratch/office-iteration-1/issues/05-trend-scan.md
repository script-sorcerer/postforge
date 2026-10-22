# 05: Trend scan

**What to build:** Before each Digest, the Scout writes a dated Trend scan: hot threads in the chosen gamedev subreddits, current meme formats, gaming and mobile news, and calendar hooks such as #ScreenshotSaturday and #WIPWednesday. It also refreshes the rules of the chosen subreddits in the Reddit Channel rules. Topics may cite the Trend scan in their "why now". A Trend scan older than two weeks is never used.

**Blocked by:** 03 (First Digest from git history)

**Status:** ready-for-agent

- [x] Each `/scout` run writes a dated Trend scan note before the Digest
- [x] The Trend scan covers the four areas listed above
- [x] Topics can cite the Trend scan
- [x] A Trend scan older than two weeks is treated as stale and replaced, not reused
- [x] Subreddit rules in the Reddit Channel rules are refreshed during the scan
