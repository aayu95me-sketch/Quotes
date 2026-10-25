# Growth strategy, SWOT and honest odds (2026-10-25)

Owner goal: 1M followers on Instagram and on Facebook within 6 months. Written after 5 days live, so every number below is either measured (marked **[data]**), arithmetic (**[math]**), or my judgement (**[judgement]**). Nothing here is a guarantee, and I won't promise one.

## 1. Can we be "sure" of 1M in 6 months?
No. Nobody can be, for a new account, on any platform. What can be said:
- **[math]** 1M in 180 days is about 5,600 net new followers per day, per account. If the goal means 1M on each of 4 assets (2 Instagram + 2 Facebook), that is 4M followers.
- **[data]** Today: 3 followers on each Instagram page. A Reel reaches about 100-160 accounts, almost all non-followers; a carousel reaches about 3 (only followers). Saves and shares are about zero. Sample is tiny (n=9 posts), so this is a starting point, not a verdict.
- **[judgement]** Reaching 1M this fast depends on a few posts going far outside the norm (an outlier getting millions of views), not on steady growth. We can raise the odds of an outlier; we cannot schedule one. Realistic six-month outcomes for a faceless text page, in my judgement and not from data: most likely thousands to low tens of thousands per account; a strong run, tens of thousands to low hundreds of thousands; 1M is a lottery ticket we improve the odds of, not a plan.
- **Steering metric instead of the follower count:** share of Reels that reach 5x our median non-follower reach, saves+shares per 1,000 reach, follows per 1,000 non-follower reach. These move weeks before followers do.

## 2. SWOT
**Strengths:** fully automated pipeline (no daily work), consistent posting, a hands-off safety net, daily insights, original text only, Reels with licensed trending audio, two audiences (India Hinglish, global English), zero budget burn.
**Weaknesses:** brand-new accounts with no history; static-image Reels (weakest Reel type, low watch time); carousels get no reach beyond followers; Facebook Pages receive nothing yet (see gaps); no replies to comments; two pages with five pillars each (diluted topic signal); no lead magnet or email list; one owner for approvals and security steps; faceless means no personality or trust signal.
**Opportunities:** Reels reach non-followers from day 1; Hinglish self-improvement is large and under-served by careful, plain writing; evergreen topics can be reused as Reels; Facebook Reels get separate distribution; Collabs; repurposing winners; email list and affiliates once past ~1k engaged followers.
**Threats:** algorithm and policy changes (Meta demotes repetitive or unoriginal content; AI-generated label may reduce reach, unverified); account locks if a security flag is missed; crowded self-improvement niche; the owner's time; token or app problems; copycat templated look.

## 3. Gaps we had not covered (ranked by effect on the goal) and what we do
1. **Facebook gets no posts.** The publisher only posts to Instagram. Fix: publish the same content to the two Facebook Pages (photos/albums for carousels, Reels for videos). First check the stored tokens allow it (read check added to `verify-setup`). **Status 2026-10-25:** the code is built and live (every new post and a 2-per-hour catch-up of the 19 older ones). The stored tokens can READ both Pages but Facebook rejects posting with `(#200) Permissions error`, so the tokens need the `pages_manage_posts` permission. Owner step: regenerate both Page tokens once (docs/08 step 6-8) and replace the two GitHub secrets IG_PAGE_A_TOKEN / IG_PAGE_B_TOKEN. Until then nothing is posted to Facebook and nothing breaks on Instagram.
2. **Reel format is weak.** Slideshow Reels have low watch time. Test, one change at a time: shorter (4-5 slides), a hook that pays off in 1.5 s, faster cuts, first slide a question. Add `ig_reels_avg_watch_time` and a 3-second hold metric to the weekly review. Owner decision later: kinetic-text animation or a voice-over (AI voice) variant.
3. **Carousels reach nobody new.** Use carousels to convert and retain; use Reels to discover. Shift the mix toward more Reels (week 5 already at 5 per page), keep one carousel a day for the profile grid.
4. **No engagement loop.** The algorithm rewards early comments, saves and shares. Rule 3 forbids bots, so owner replies manually, 5 minutes a day on the phone, to every comment. CTA lines already ask for a comment, a save or a share; keep one question per post.
5. **Profile does not convert.** Reach without follows. Check: bio promise, 3 pinned posts, highlights, link in bio. Owner/operator task (prompt in docs/11) once we have 100+ non-follower profile visits a week.
6. **Topic dilution.** After day 60, cut each page to its 2-3 best pillars by saves+shares per 1,000 reach (rule: 8+ scored posts per pillar before cutting).
7. **No owned audience.** Add a Broadcast Channel (Instagram) and a free checklist lead magnet at ~1k followers (docs/04). Money starts well below 1M.
8. **Single points of failure.** 2FA, Meta "Confirm Account" prompts, tokens. Safety net and Sunday routine exist; owner must keep the phone reachable.
9. **Policy risk.** Keep every post original, vary slide layouts and phrasing so the feed is not "repetitive", keep the AI label on. Review monthly against Meta's current guidance.
10. **Timing.** Posting times are a first guess (India evening, US morning). Test two time slots per page for 2 weeks each, then lock.
11. **Other platforms** (YouTube Shorts, TikTok, X) multiply reach from the same Reels, but CLAUDE.md rule 3 says no new accounts without the owner's approval. Decision for the owner, not assumed.

## 4. Decision gates (what we change, and when)
| Day | If this is true | Then |
|---|---|---|
| 14 | median Reel non-follower reach < 100 | change hook style and slide count, keep audio |
| 30 | no Reel above 5x median, follows < 1 per 1,000 reach | rework Reel format (kinetic text / voice-over) |
| 60 | pillars with 8+ posts each scored | drop weakest pillars, double the best |
| 90 | < 1,000 followers per page | re-think niche or language mix; consider one flagship page |
| 120 | an outlier (>50k views) exists | clone its format and topic for 2 weeks |
Every Sunday the routine reports these numbers in plain words.
