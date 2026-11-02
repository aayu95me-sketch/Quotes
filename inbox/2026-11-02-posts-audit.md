# Posts audit and goal alignment (2026-11-02, ~04:00 UTC)

Read-only audit by the Static Automation operator. Nothing on Meta or in GitHub settings was changed. No tokens, App Secret or passwords were read or shown.

## Sources used
- `content/posts/page_a|page_b/*.json` (status, publish_at, media_id, fb_post_id)
- `research/insights/2026-10-23.md` to `2026-11-01.md` and `latest.json` (daily Graph API pull)
- `state/blocked.json`, `pipeline/publish.py`
- GitHub Actions `publish.yml` runs 295 to 334 and job logs of runs 297 (31 Oct 17:29 UTC) and 330 (1 Nov 23:32 UTC)
- `PROJECT.md`, `CLAUDE.md`, `docs/`, earlier `inbox/` reports

## What I could NOT read
- **The Instagram and Facebook profiles themselves.** The Chrome extension on Ayush's Mac was not connected during this run, so I could not look at the @rozkarule / @the.disciplinequiet grids or the two Facebook Pages.
- **Live Graph API data** (media list, captions, timestamps). That needs the stored tokens, which I must not use or read.
- The Meta Ads connector can list Instagram media only through an ad account, and ad accounts are out of scope, so I did not use it.
- So the duplicate count below is **inferred from the API's media count plus the run logs**. It is not confirmed by looking at the posts.

## Summary
- Published through the pipeline: **19 posts on each Instagram account** (21 to 30 Oct). All 38 were mirrored to the matching Facebook Page (each has an `fb_post_id`). No wrong-account posts found in the repo records. A2 posts carry the A2 Page ID prefix 1345396148663682 and B2 posts carry 1436529449539802.
- Since **31 Oct 13:30 UTC nothing has been recorded as published**. Instagram answers every attempt with code 4 / subcode 2207051 ("Action is blocked").
- **The "failed" attempts appear to be going live anyway**, which creates duplicates. Details below.

## Discrepancies

### 1. Probable duplicate posts on A1 @rozkarule (HIGH, ongoing)
- Media count from the API: **19 on 31 Oct 05:50 UTC, then 34 on 1 Nov 05:50 UTC.** In the same window the repo recorded **0** new publishes.
- Between those times there were **15 failed publish attempts for Page A**: hourly runs 295 to 308 (14 attempts, all `2026-10-31-subah-uthna`) plus manual run 309. That gives **15 unexplained media and 15 failed attempts.**
- Most likely cause: `media_publish` (or the container step) actually publishes, Instagram then returns the block error, the pipeline treats it as a failure and tries again next run. Result: about **15 copies of the "subah uthna" carousel** on @rozkarule.
- Runs 316 (1 Nov 09:40), 323 (16:34) and 330 (23:32) tried again after each 6 h rest, so there may be **up to 18 copies** now. The next try is due at about **05:32 UTC on 2 Nov** (`state/blocked.json`).
- Facebook: none of these copies were mirrored, because mirroring only runs after a successful Instagram publish.

### 2. Probable duplicate posts on B1 @the.disciplinequiet (MEDIUM)
- Media count: **19, then 20** in the same window. Page B was only tried from run 309 onward. Before that, the first auth-type error stopped the whole run before Page B was reached.
- Likely **1 to 4 copies of `2026-10-31-feedback`** (one per attempt in runs 309, 316, 323, 330, if each published).

### 3. Missing posts (expected, caused by the block)
- Approved but not published: A `2026-10-31-subah-uthna`, `2026-11-01-reel-ghar-walon-career`, `2026-11-01-ghar-walon-career`; B `2026-10-31-feedback`, `2026-11-01-reel-friction`, `2026-11-01-friction`. 2 Nov posts (A subscriptions 13:30 UTC, B parkinson 17:00 UTC) are next.
- `publish.py` skips posts more than 48 h overdue **without changing their status**. The 31 Oct posts cross 48 h today (A 13:30 UTC, B 17:00 UTC). They will then stay `approved` but never publish.

### 4. Alerts are muted while an account rests (MEDIUM)
- `--health` ignores overdue posts on a rested account (run 330 printed "overdue by more than 3h: none"). The owner gets an email only once per 6 h failure, not a running count of missed posts.
- The duplicate risk is not covered at all: nothing checks the media count after an error.

### 5. Schedule mismatches (LOW)
- `page_b/2026-10-23-reel-two-minute-rule` went out on 22 Oct 15:36 UTC (the audio test pulled forward). The file date does not match the live date.
- A and B each had two Reels on 24 Oct and 26 Oct (companion Reels plus the original Reels). The repo intended this, but the cadence was about **3 posts per account per day** on 4 to 5 follower accounts. That cadence is the builder's own suspected cause of the block.
- The original procrastination (A) and willpower (B) Reels were deleted and republished on 22 Oct. Their `media_id` values in the repo are the new ones, so the records are consistent.

### 6. Token / access after the 21-22 Oct block
- No token failures since 25 Oct. The publish logs show no OAuth 190 or "Cannot call API" errors. The current error is the Instagram **activity block (code 4 / 2207051)**, not a token problem.
- Insights still read fine on 1 Nov, so the tokens work.
- Still open from that incident: 2FA is off, and "unrecognised logins" were never confirmed as reviewed.

### 7. Documentation drift (LOW)
- `CLAUDE.md` still says B1 is "currently `@disciplinequite`". PROJECT.md shows it was renamed to `@the.disciplinequiet` on 21 Oct.
- `PROJECT.md` "Status (2026-10-20)" and "Next steps" sections describe the pre-launch state.

### Captions
- I could not compare live captions with the repo, because I could not read the live posts (see above). The repo records show no caption edits after publishing.

## Recommended next steps (priority order)
1. **Owner, now:** set repo variable `LIVE_PUBLISH=false` before about 05:32 UTC today. This stops more duplicates. It is easy to undo.
2. **Owner (phone):** open @rozkarule and @the.disciplinequiet. Count the duplicate "subah uthna" / "feedback" posts. Check Settings > Account status, and use "Tell us if you think we made a mistake" if it is offered. **Deleting duplicates is the owner's call.** I recommend keeping one copy of each and deleting the rest by hand, so the grid does not look like spam.
3. **Builder:** change `publish.py` so a post is never retried blindly after an error:
   - after any error, look up the account's recent media (caption or timestamp) and mark the post published if it is already live;
   - stop at most one attempt per post per block;
   - count missing posts in `--health` even while an account rests.
4. **Builder + owner:** when the block lifts, restart at **1 post per account per day** (Reel first, since Reels give the reach) for about 2 weeks. Reschedule the skipped 31 Oct to 2 Nov posts and spread the 23-day runway over more days. The owner has to approve this cadence change (it was proposed on 31 Oct and is still unanswered).
5. **Owner:** turn on 2FA on Facebook and both Instagram accounts. Review "unrecognised logins". Both have been open since 21 Oct, and both raise the risk of Meta security flags.
6. **Builder:** fix the doc drift (CLAUDE.md B1 handle, PROJECT.md status). Then run the day-14 review that was due on 4 Nov.

## Are we aligned with the goal?
**Partly. The machine is aligned, but the results and the cadence are not.**

- **Stated goal** (PROJECT.md): earn income from two faceless pages through organic growth. The owner's target is 1M followers in a month. The working targets for day 30 are: 25% of posts at 3x the median or better, more than 50% non-follower reach, and at least one 10x breakout.
- **Aligned:**
  - Publishing, audio, Facebook mirroring, insights and approvals all work through official APIs only.
  - Every post was approved and AI-flagged, and both brands post on-niche original text.
  - Reels do reach non-followers: 80 to 173 accounts each on A and 35 to 108 on B. That meets the "non-follower reach above 50%" indicator.
- **Not aligned:**
  - After 12 days there are **4 followers (A) and 5 (B)**.
  - Carousels reach 1 to 5 accounts, essentially only followers.
  - Saves and shares are about 0, and the median score is 0, so no post is a "winner".
  - The 1M-in-a-month target is out of reach. The day-30 working targets are also at risk: there is no breakout, and the "3x median" test is meaningless while the median is 0.
  - **The cadence works against the goal.** About 3 posts per account per day on brand-new accounts most likely triggered the block. The block has now stopped all posting, and the duplicates it caused can hurt reach further.
  - Income work has not started yet (no email/WhatsApp list, no affiliate setup), although PROJECT.md says to start the list from day 1.
- **To realign:**
  - Fewer, better posts: lead with Reels, aim for saves and shares, and use carousels for people who already follow.
  - Clean up the duplicates.
  - Judge the next 2 weeks by reach and saves per post, not followers.
  - Start a simple owned list (a link in the bio) so the income side begins.

## REPORT
- **task:** audit published posts against the repo plan; next steps; goal alignment
- **done:** partly. The repo, logs and insights were audited. The live profiles could not be viewed (Chrome not connected).
- **assets touched:** none (read-only). Assets in scope: A1 @rozkarule 17841469203264060, A2 Roz Ka Rule 1345396148663682, B1 @the.disciplinequiet 17841422691847840, B2 Quiet Discipline 1436529449539802.
- **what changed:** only this file was added.
- **what I could not do and why:**
  - view the live posts or captions: the browser extension was not connected;
  - query the Graph API: that would need the tokens;
  - use the Meta Ads connector: it needs an ad account, which is out of scope.
- **current state of the four assets:**
  - A1 and B1: Instagram publishing is blocked (code 4/2207051) since 31 Oct 13:30 UTC, and both probably have duplicate posts.
  - A2 and B2: they have all 19 mirrored posts each and no duplicates (nothing was mirrored during the block).
- **noticed, not touched:** `LIVE_PUBLISH` is still `true`. 2FA is off. The builder's 31 Oct cadence proposal is unanswered. The 48 h skip leaves stale `approved` posts.
