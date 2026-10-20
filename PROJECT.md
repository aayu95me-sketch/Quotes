# PROJECT: Faceless Automated Social Page (Claude-run)

This is the project's living state file. Update it every session. Start here.

## Goal
Maximise income from faceless, automated text-image carousels and static-image reels with trending audio, grown organically.

## Owner profile (confirmed 2026-10-20)
- Based in **India**; payouts must land in an **Indian bank account**.
- Has a MacBook, Claude, Gemini Pro and free/open-source tools. Can give unlimited hours.
- Will create any accounts needed. Will follow the plan. Will **approve every post for the first month**.

## Status
- **Phase 0, Research:** Rounds 1, 1b and 2 done → docs 01–03. Competitor data is thin (no Instagram access from here); owner can add real examples. Official-policy verification still open.
- **Phase 1, Setup:** briefs **approved**; names chosen: **Roz Ka Rule** (Page A), **Quiet Discipline** (Page B). Pipeline v0 built and tested locally (render, static reel, approve, dry-run publish); live publish untested. 2 sample drafts in `content/posts/`. Owner next: connect Gemini in Zapier, create accounts.
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

## Owner answers (2026-10-20)
- Budget: **₹0**. Everything must use free tools and free tiers.
- Niche: left to Claude. Language: Hinglish and English both fine. Will book the CA call.

## Owner answers, round 2 (2026-10-20)
- Briefs approved; names left to Claude. Repo is **private**. Owner skipped manual account research and asked Claude to use Zapier/Make with Gemini or Claude instead.

## Research tooling via Zapier (state)
- Zapier MCP works. Connected there already: Google Sheets/Docs, Gmail, ChatGPT (OpenAI), Kartra, PhantomBuster. Make MCP works but the account lacks org-view rights.
- **Gemini connected and working** (model `gemini-3.8-flash`; `gemini-2.5-flash` is retired). But the free API key returned **quota exceeded** on search-grounded prompts (retried several times, 2026-10-20). Fallback: owner runs the ready prompts in `docs/05-research-prompts.md` in the Gemini app or Claude chat and pastes answers back. Retry Zapier-Gemini later (quota may reset). Anthropic (Claude) app exists in Zapier but is not enabled or connected.
- Gemini rate-limit screenshots (owner, 2026-10-20): `gemini-3.8-flash` is 5 requests/min free; usage was low, yet every **search-grounded** call (3.8 and 3.6 flash, sequential) still returned quota-exceeded, and one ungrounded call returned 'high demand'. Likely cause: no free quota for Google Search grounding. Ungrounded Gemini works (use for drafting, not research).
- ChatGPT via Zapier uses an **OpenAI API key with no credits** ('no credits remaining'). A ChatGPT Go subscription does not fund API calls. So the owner must run research prompts manually in the ChatGPT or Gemini apps (both have web search).

## Open questions for the owner
1. Optional but valuable: run P1-P4 from `docs/05-research-prompts.md` in the Gemini app and paste back the answers.
2. Create the accounts (checklist in doc 02, section 4).

## Technical notes (₹0 constraints)
- Instagram's API needs **publicly reachable image URLs**. Plan: a separate **public** repo/GitHub Pages for rendered slides only, with strategy and secrets kept out of it.
- GitHub Actions is free for public repos, and has a monthly free-minute allowance for private ones. The posting job is small.
- Use only the **official Graph API**. Avoid unofficial/private-API libraries (account-restriction risk).
- Whether the API supports delayed scheduling is unverified; fall back to a GitHub Actions cron that publishes approved posts at set times.

## Next steps (proposed order)
1. **Claude:** retry Zapier-Gemini research when quota allows; otherwise use answers the owner pastes from the prompts file.
2. **Owner:** create the accounts (checklist in doc 02, section 4).
3. **Claude:** add GitHub Actions workflow, analytics puller, Graph API test on a real account.
4. **Claude:** generate the first 30-day content batch per page for owner approval.
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
- `docs/03-competitor-notes.md`: what exists, hook patterns, gaps, risks.
- `docs/04-brand-briefs.md`: Page A (India) and Page B (Tier-1) briefs, shared rules, sample hooks.
- `pipeline/`, `content/`: renderer, reel builder, approval CLI, publisher; brand configs and posts. See README.md.
