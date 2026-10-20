# PROJECT: Faceless Automated Social Page (Claude-run)

This is the project's living state file. Update it every session. Start here.

## Goal
Maximise income from faceless, automated text-image carousels and static-image reels with trending audio, grown organically.

## Status
- **Phase 0, Research:** Round 1 done → [docs/01-market-research.md](docs/01-market-research.md). Round 2 open.
- **Phase 1, Setup:** not started.
- **Phase 2, Pilot:** not started.

## Decisions so far
| # | Decision | Status |
|---|---|---|
| 1 | Primary platform: Instagram (carousels lead, static Reels for reach) | Proposed |
| 2 | Mirror to Facebook; Threads for testing | Proposed |
| 3 | Skip TikTok/YouTube for monetisation (format ineligible or low RPM) | Proposed |
| 4 | Portfolio of 2–3 pages: finance/money mindset, discipline/psychology, one wildcard | Proposed |
| 5 | Target audience: English-speaking Tier-1 | Proposed |
| 6 | Claude writes original lines (not recycled famous quotes) | Proposed |
| 7 | Income order: affiliate/products → sponsors → owned list → platform payouts | Proposed |

## Open questions for the owner (blocking)
1. Which country are you based in, and where will payouts go? (Gates program eligibility and tax.)
2. Budget (monthly) and weekly time you can give to approvals and account setup?
3. Do you already have Instagram/Facebook accounts, or a Meta developer app?
4. Are you OK with a 2–3 page portfolio, or do you want a single page?
5. Any niches you want to avoid, or have expertise in?
6. Preferred approval level: fully automatic posting, or human approval of each batch at first?

## Next steps (proposed order)
1. Owner answers the open questions above.
2. Round 2 research: verify official policies, competitor teardown for the candidate niches, affiliate programs.
3. Pick the niches and write a brand brief for each (name, voice, visual system, content pillars).
4. Build the pipeline in this repo: content generator, HTML→PNG renderer, static-reel builder (ffmpeg), publisher (Graph API), analytics puller.
5. Spike-test the Instagram Audio API on a test account.
6. Pilot: 30 days, 1 post per day per page, human approval of each batch.
7. Weekly review → keep, change or kill, using the criteria below.

## Proposed KPIs and kill criteria (to be confirmed)
- Track per post: reach, non-follower reach %, saves, shares, follows gained.
- Day 30: if a page has fewer than 500 followers and no post is above 2x the page's median reach, change the niche angle.
- Day 60: if still flat, kill the page and redeploy effort to the best performer.
- Monetisation gate: don't build products until a page has about 5k engaged followers. Start the email/WhatsApp list from day 1.

## Guardrails
- Official APIs only. No bought accounts, no engagement bots, no bulk account creation.
- No reposting others' content. Original text only.
- Disclose AI where the platform requires it. Mark sponsored and affiliate posts.
- No specific investment, medical or legal advice. Fixed disclaimer on finance content.

## File map
- `PROJECT.md`: this file (state, decisions, next steps).
- `docs/01-market-research.md`: Round 1 market research.
