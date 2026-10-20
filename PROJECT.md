# PROJECT: Faceless Automated Social Pages (Claude-run)

Living state file. Update every session. Start here. Branch: `claude/eager-bell-i41n67` (private repo `aayu95me-sketch/Quotes`).

## Goal and targets
Maximise income from two faceless pages posting designed text carousels and static-image Reels (trending audio), grown organically.

- **Owner's stated target (2026-10-20): every post viral, 1M followers in one month.** I told the owner this is **not a realistic plan target**: no source I found shows new faceless text pages doing it, and nothing in our research supports a forecast. We aim high but **steer by leading indicators**, set below. Working targets are my judgement, to be revised after the first 2 weeks of real data.
- **Leading indicators (per page):** reach per post, share of reach from non-followers, saves + shares per 1,000 reach, follows gained per post, share of posts that beat the page's median reach by 3x or more.
- **Working targets for pilot day 30 (provisional):** at least 25% of posts above the median by 3x; non-follower reach above 50%; at least one post that clearly breaks out (10x median). Followers are an outcome, not the target. Revisit at day 14.

## Owner profile (confirmed)
India-based; payouts to an Indian bank account. Budget **₹0**. Has a MacBook, Claude, Gemini Pro, ChatGPT Go. Unlimited hours. Will create the accounts (with step-by-step help). Approves every post for the first month. Repo is private. Will book a CA call (tax/GST/LUT).

## Status (2026-10-20)
- **Research:** done to the extent possible. See docs 01-03, 06, 07. Verified facts are in doc 06 (official pages fetched through the relay).
- **Accounts:** owner created Instagram **@rozkarule** (Page A) and **@disciplinequite** was created with a typo; owner asked (2026-10-20) to correct it to **@disciplinequiet.official** in the Instagram and Facebook Page settings (owner action; files already use the corrected spelling) plus matching Facebook Pages. Still to confirm: Professional (Creator) switch, Page-to-Instagram link, 2FA, profile pictures and bios.
- **Brand:** approved. **Roz Ka Rule** (Page A, India, Hinglish+English) and **Quiet Discipline** (Page B, US/UK/CA/AU, English). Profile images in `brand/`.
- **Content:** week 1 fully written: 7 draft carousels plus 3 static-image Reels per page (20 total) in `content/posts/`, all `status: draft`, dates 27 Oct to 2 Nov (shift to real go-live). Plan for days 8-30 (hooks) in `docs/09-content-plan.md`. Weeks 2-4 get written one week at a time after reading the previous week's data.
- **Audio:** trending, mood-matched music for Reels via Meta's Audio API (`pipeline/audio.py`, `content/audio_moods.json`, weekly shortlist job). Strategy and limits in `docs/10-audio-strategy.md`. Music cannot be attached to carousels or Stories through the API.
- **Pipeline:** render (carousels and 9:16 Reels), static Reel slideshow builder, approval CLI, publisher (render + upload to public assets repo + Graph API + AI flag, safety rails), research relay. All tested locally or on Actions except **live publishing, which has not been run**. `publish.yml` is a dry run unless repo variable `LIVE_PUBLISH=true`, and only activates once merged to `main`.
- **Owner next:** Phase 1 of `docs/08-account-setup-guide.md` (create the two Instagram accounts, Facebook Pages, 2FA, profile pictures, bios). Then 3-5 days of warm-up. Then Phase 2 (Meta developer app, tokens, secrets) with Claude guiding step by step.

## Account audit (Claude chat read-only check, 2026-10-20)
- A1 IG @rozkarule, IG ID 17841469203264060, linked to A2 Page "Rozkarule" (ID 1345396148663682). B1 IG @disciplinequite, IG ID 17841422691847840, linked to B2 Page "Quietdiscipline" (ID 1436529449539802). Links correct. Both IG accounts are Professional (type Creator vs Business unconfirmed; B1 looks Business), category "Art" (wrong), no photos or bios, public. B1 Account Status clean.
- Issues: B1 2FA off (owner); A1 2FA and Account Status unknown (owner, on phone); Page names are one word ("Rozkarule", "Quietdiscipline") and B1 display name is "Quite Discipline" (Prompt 2 fixes); **B2 has two extra "Quiet Discipline" entries with full access, unidentified** (Prompt 2B, read-only); A1 is owned by portfolio "Quite Discipline" while A2 is in "Roz ka Rule" (leave until the API test); B1 account has 3 Security Checkup recommendations (owner).
- Next: Prompt 2 and 2B (docs/11), the manual phone steps, then Phase 2 (developer app).

## Account fixes status (2026-10-20, after Prompt 2 report)
- Done by Claude chat: bios on B1, A2, B2. Not done: names/passwords/pictures (owner), A1 items (chat only had B1 signed in on Instagram web).
- **Instagram @disciplinequiet.official is taken.** Chosen Instagram handle for B1: **@the.disciplinequiet** (alternatives free: disciplinequiet_, disciplinequiet.in, disciplinequiet.official). Facebook Page B2 username: `disciplinequiet` (reported available). Slide footers and reels use @the.disciplinequiet.
- Owner phone/Chrome checklist given: Page name changes (B2 "Quiet Discipline", A2 "Roz Ka Rule", Meta review up to 3 days, then 60-day lock), usernames, profile pictures, IG renames, 2FA, Security Checkup, A1 Account Status, Creator switch.
- Still open: Prompt 2B (identify two unknown full-access "Quiet Discipline" entries on B2) before generating any tokens.

## Prompt 2 result (2026-10-20)
- Done by Claude chat: bios on B1, A2, B2. Not done: names, pictures, A1 anything (Chrome is signed in only as B1).
- **@disciplinequiet is taken on Instagram** (also @quietdiscipline). Page B Instagram handle decision stays **@the.disciplinequiet** (files already use it); fallbacks `disciplinequiet.official`, `disciplinequiet_`. Facebook Page B2 username `disciplinequiet` was available (separate namespace).
- Owner must do (passwords): B2 username (box open in Chrome), B2 name -> "Quiet Discipline", A2 name -> "Roz Ka Rule". Facebook reviews page-name changes (up to 3 days) and then locks the name for 60 days, so the spelling must be exact.
- Owner on phone: profile pictures for A1, A2, B1, B2 (files sent to the owner); A1 bio, name "Roz Ka Rule", category; 2FA; Account Status for A1; Creator vs Business.
- Prompt 2C covers category, B1 handle and display name via Chrome.

## Operating model: who does what
- **Owner (identity and security only):** create/rename accounts, 2FA, passwords, Meta developer registration, copying tokens into GitHub Secrets, approving posts, payouts/tax. No tool can or should do these for the owner.
- **Claude Code (this repo):** research via the relay, ideas, writing, rendering, scheduling logic, audio picks, analytics, weekly reports, and fixing the pipeline.
- **GitHub Actions (always on):** publishes approved posts, pulls audio shortlists, runs research requests.
- **Prompt relay (agreed 2026-10-20):** whenever an account-level change is needed, Claude Code writes a ready prompt (see `docs/11-claude-chat-prompts.md`); the owner pastes it into the Claude chat project; the owner pastes the REPORT back. Secrets never go through chat.
- **Claude chat project "New Bot Planning" (owner's claude.ai):** not reachable from Claude Code. To share state, give it this repo (GitHub connector in the project) or paste `PROJECT.md` into its knowledge. Use it for approvals and brainstorming on the phone; the repo stays the source of truth.
- **Meta Ads connector in this session:** advertising tools only (list pages/ad accounts, boost posts, create ads). It cannot create accounts, rename them, or publish organic posts. One Pages lookup was blocked by the permission classifier and was not retried; one ad-account list lookup ran (read-only, nothing changed). Not used further for this project.

## Key findings
- Platform payouts are small for an India page; income must come from sponsors, affiliates, own digital products and an owned audience (email/WhatsApp).
- **Facebook Content Monetization officially lists India and the English and Hindi languages for public Reels** (doc 06). Photo/text eligibility and thresholds still need the owner's Meta account.
- Instagram's originality rules (doc 06) reward content we design from our own text; aggregators and reposts lose recommendations.
- Instagram Audio API (trending audio on Reels at creation time) works only with the **Facebook Login** setup. No scheduled-publish parameter exists; our own cron schedules. Stories can be published via the API (`media_type=STORIES`); **Highlights cannot be created by API** (manual).
- Standard Access (no App Review) should be enough for the owner's own accounts.

## Decisions
| # | Decision | Status |
|---|---|---|
| 1 | Instagram primary (carousels lead, static Reels for reach); mirror to Facebook later; Threads for testing | Proposed |
| 2 | Skip TikTok/YouTube/X for now | Proposed |
| 3 | Two pilot pages: A India, B Tier-1 English | Approved |
| 4 | Niches: discipline/habits, psychology, career, relationships; money content only as literacy (SEBI) | Approved |
| 5 | Claude writes original lines; no lifted quotes; no invented studies | Approved |
| 6 | Income order: affiliate/products, sponsors, owned list, platform payouts | Proposed |
| 7 | Publishing on GitHub Actions; secrets only in GitHub Secrets; official Graph API only | Approved |
| 8 | Owner approves every post for the first 30 days (weekly batches) | Confirmed |
| 9 | n8n not needed (GitHub Actions already schedules and is free); Zapier/Make kept as backups | Decided |
| 10 | Weekly autonomous sessions (Claude writes next batch and report without being asked) | **Offered, owner has not answered** |

## Research relay (how Claude gets information it cannot reach)
- Commit a request file to `research/requests/` on a `claude/**` branch; `.github/workflows/research-relay.yml` runs `pipeline/relay.py` on GitHub Actions (open internet) and commits results to `research/answers/<id>/`. Round trip about a minute. It fetches pages (direct, then r.jina.ai), runs free web searches (DuckDuckGo, Mojeek, Bing with pauses) and can call Gemini/Groq/OpenAI if a repo secret exists (`GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENAI_API_KEY`).
- To rerun a request, use a new filename (answers with `done.json` are skipped).
- Zapier (Gemini connected, grounded search quota-blocked on the free key) and Make (Free plan, AI Web Search needs a paid plan) are backups. ChatGPT via Zapier has no API credits.
- Groq key works but the free account has no web-search model. Use Groq/Gemini only for summarising fetched text.

## Next steps
1. **Owner:** Phase 1 of the setup guide; report handles and Page names.
2. **Claude:** write week 2 (days 8-14) after owner review of week 1; tune templates from owner feedback.
3. **Owner + Claude:** Phase 2 of the guide (developer app, tokens, assets repo, secrets).
4. **Together:** one live test post, then set `LIVE_PUBLISH=true`, merge to `main` (ask first), start the pilot.
5. **Claude:** add static Reel and Story support to the publisher; analytics puller and weekly report; Audio API spike.
6. **Weekly:** review, keep/change/kill per the criteria below.

## Kill criteria (provisional)
- Day 30: a page under 500 followers with no post above 2x the page median, change the angle.
- Day 60: still flat, kill the page and move effort to the better one.
- Don't build products until about 5k engaged followers. Start the email/WhatsApp list from day 1.

## Guardrails
- Official APIs only. No bought accounts, no engagement bots, no bulk account creation. Accounts belong to the owner, with 2FA.
- Original text only. No reposts of others' content.
- AI flag on every post (`is_ai_generated`); sponsored and affiliate posts labelled.
- No stock/crypto tips, no returns claims, no medical or legal advice. Disclaimers on money and mental-health posts.
- No tax or legal decisions without a CA.
- Never paste tokens, App Secret or passwords into chat.

## File map
- `PROJECT.md` this file. `README.md` how to run the pipeline.
- `docs/01-market-research.md` platforms, money, risks. `02-india-addendum.md` India payouts, tax, SEBI. `03-competitor-notes.md`. `04-brand-briefs.md` page briefs. `05-research-prompts.md` manual prompts (mostly superseded). `06-verified-facts.md` official facts. `07-competitors-and-rates.md`. `08-account-setup-guide.md` **owner's step-by-step**. `09-content-plan.md` 30-day plan. `10-audio-strategy.md` audio. `11-claude-chat-prompts.md` prompt pack for account-level tasks.
- `content/pages/*.json` brand config. `content/posts/<page>/*.json` posts. `brand/` profile images.
- `pipeline/`: `render.py`, `reel.py`, `audio.py`, `approve.py`, `publish.py`, `relay.py`, `brand.py`, `setup_tokens.py`. `content/audio_moods.json`.
- `research/requests`, `research/answers`: relay. `research/audio`: weekly audio shortlists. `.github/workflows/`: `research-relay.yml`, `publish.yml`, `audio-shortlist.yml`.
