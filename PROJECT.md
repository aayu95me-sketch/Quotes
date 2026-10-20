# PROJECT: Faceless Automated Social Page (Claude-run)

This is the project's living state file. Update it every session. Start here.

## Goal
Maximise income from faceless, automated text-image carousels and static-image reels with trending audio, grown organically.

## Owner profile (confirmed 2026-10-20)
- Based in **India**; payouts must land in an **Indian bank account**.
- Has a MacBook, Claude, Gemini Pro and free/open-source tools. Can give unlimited hours.
- Will create any accounts needed. Will follow the plan. Will **approve every post for the first month**.

## Status
- **Phase 0, Research:** Round 1 and 1b done → [docs/01-market-research.md](docs/01-market-research.md), [docs/02-india-addendum.md](docs/02-india-addendum.md). Round 2 (competitor teardown, official-policy verification) open.
- **Phase 1, Setup:** not started.
- **Phase 2, Pilot:** not started.

## Key finding
Platform payouts are small, and for an India-based page they are smaller still (Reels bonus closed to new India participants, Facebook CMP availability unclear, TikTok unavailable, X India eligibility unknown). Income must come from **sponsors, affiliates, own digital products and an owned audience (email/WhatsApp).**

## Decisions so far
| # | Decision | Status |
|---|---|---|
| 1 | Primary platform: Instagram (carousels lead, static Reels for reach) | Proposed |
| 2 | Mirror to Facebook; Threads for testing | Proposed |
| 3 | Skip TikTok/YouTube/X for now | Proposed |
| 4 | Pilot with **2 pages** to test audience: **A = India (English/Hinglish)**, **B = US/UK/CA/AU English** | Proposed |
| 5 | Niches: discipline/habits, psychology, career/productivity, relationships. **Money content only as financial literacy** (SEBI risk, see doc 02). Final pick after competitor teardown | Proposed |
| 6 | Claude writes original lines (not recycled famous quotes) | Proposed |
| 7 | Income order: affiliate/products → sponsors → owned list → platform payouts | Proposed |
| 8 | Engine: Claude only at first; Gemini/open-source only if a gap appears | Proposed |
| 9 | Pipeline runs on GitHub Actions (always on); secrets in GitHub Secrets | Proposed |
| 10 | Human approves every post for the first 30 days | **Confirmed by owner** |

## Open questions for the owner
1. Monthly budget in ₹ (even if ₹0)? Near-zero is workable.
2. Any niche you want to avoid, or have expertise in?
3. Hinglish: are you comfortable approving Hinglish posts, or English only?
4. Okay to book a one-hour call with a CA (tax/GST/LUT structure) before the first income?

## Next steps (proposed order)
1. **Claude:** Round 2 research: competitor teardown for the candidate niches (India and Tier-1); verify official policies where reachable.
2. **Claude:** brand brief per page (name options, voice, visual system, content pillars, 30-day content plan).
3. **Owner:** after the briefs are approved, create the accounts (checklist in doc 02, section 4).
4. **Claude:** build the pipeline in this repo: content generator, HTML→PNG renderer, static-reel builder (ffmpeg), approval queue, publisher (Graph API), analytics puller.
5. **Together:** spike-test the Instagram Audio API on a test account.
6. **Pilot:** 30 days, 1 post per day per page, owner approves each batch.
7. **Weekly review:** keep, change or kill, using the criteria below.

## Proposed KPIs and kill criteria (to be confirmed)
- Track per post: reach, non-follower reach %, saves, shares, follows gained.
- Day 30: if a page has fewer than 500 followers and no post is above 2x the page's median reach, change the niche angle.
- Day 60: if still flat, kill the page and redeploy effort to the best performer.
- Monetisation gate: don't build products until a page has about 5k engaged followers. Start the email/WhatsApp list from day 1.

## Guardrails
- Official APIs only. No bought accounts, no engagement bots, no bulk account creation. Accounts belong to the owner.
- No reposting others' content. Original text only.
- Disclose AI where the platform requires it. Mark sponsored and affiliate posts.
- No stock/crypto tips, no returns claims, no medical or legal advice. Fixed disclaimer on money content.
- No tax or legal decisions without a CA.

## File map
- `PROJECT.md`: this file (state, decisions, next steps).
- `docs/01-market-research.md`: Round 1 market research (platforms, money, niches, risks).
- `docs/02-india-addendum.md`: India-specific payouts, tax notes, SEBI, tooling, account checklist.
