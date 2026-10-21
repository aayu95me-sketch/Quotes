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

## Sync with the "Static Automation" Claude Code project (2026-10-21)
- Static Automation is a Claude Code project with the repo attached (Settings > Environment > Project repositories). Default branch is now `claude/eager-bell-i41n67`. `CLAUDE.md` at the repo root gives it scope, rules and the REPORT format; it writes reports to `inbox/` and pushes. The builder reads them with `git fetch` and `git pull`.
- `publish.yml` now has a cheap "anything due?" check so scheduled runs on the default branch cost seconds, not minutes.

## Operator report received (2026-10-21)
- The Static Automation operator session pushed `inbox/2026-10-21-static-automation-sync.md` and `inbox/2026-10-21-tasks-2b-2c-3-status.md` to branch `claude/project-thread-stzy0k`; the builder merged them (fast-forward). **Sync through git works.**
- **Correction:** Tasks 2B, 2C and 3 were **never run**. No Meta developer app exists yet and there is no App ID. Only Task 1 (audit) and Task 2 (bios set on B1, A2, B2) ran.
- Operator tools: git (repo only), Chrome on the owner's Mac (Instagram signed in as B1 only, so A1 is out of reach), an image-upload tool that failed earlier, Meta ads connector (not used), Mac folders not yet approved. The operator did not read passwords or tokens.
- Handle target for B1 is `@the.disciplinequiet` everywhere (docs/11 scope block fixed). Fallbacks: `disciplinequiet.official`, `disciplinequiet_`.
- Owner still has to do (no tool can): the three Facebook password steps (B2 username, B2 name "Quiet Discipline", A2 name "Roz Ka Rule"), profile pictures on all four, 2FA on Facebook and both Instagram accounts, Security Checkup on B1's account, A1 Account Status/name/bio/category on the phone, Creator vs Business.
- Next operator run: Prompts 2B then 2C (see QUICK RUN in docs/11), then Prompt 3.

## Public check (relay run 2009, 2026-10-21)
- Facebook A2 now named **"Roz Ka Rule"**, B2 **"Quiet Discipline"** with username **/disciplinequiet** working. Both show a profile photo. A2 has no username yet. So the three Facebook password steps appear **done**. Instagram profiles are login-walled (cannot verify publicly); the operator verifies with Prompt 2D.

## Operator reports 2B, 2C, 2D (2026-10-21)
- **2B (read-only):** the two "Quiet Discipline" entries with full access to B2 are **people** in the business portfolio "Quite Discipline" (1370046235203586), signed in with **Instagram** (IDs 61566292079484 active today; 61567045532811 never active). A third/fourth Instagram-login person "Quite Discipline @disciplinequite" (61567537685833) also exists. "Ayush Sharma" (Facebook login, 61568936982799) is the real owner. Likely Business Suite profiles created when the owner signed in with the Instagram accounts; not proven. They have full control of the portfolio, including deleting it. Owner decision pending: confirm they are yours, then remove the never-used one(s) in Business Suite > Settings > People. A business asset group "quitediscipline" also exists.
- **2C:** nothing changed. The operator's tool blocks Save clicks and typing categories in Meta; Chrome's Instagram is signed in as A1, not B1.
- **2D (read-only):** A1: name "Rozkarule" (needs "Roz Ka Rule"), category Art, bio empty, picture yes. A2: name "Roz Ka Rule", username none (rozkarule is available), category Arts & entertainment, bio yes, picture yes. B1 (public view): still @disciplinequite, name "Quite Discipline", bio yes, picture yes; `the.disciplinequiet` is free. B2: name "Quiet Discipline", username disciplinequiet, category Arts & entertainment, bio yes, picture yes.
- **Working pattern:** operator prefills screens, owner presses Save and enters passwords (Prompt 2E in docs/11).
- Remaining: A2 username, A1 name/bio/category, B1 rename and category, Education on A2 and B2, two-factor and Security Checkup, the portfolio people question, then Prompt 3 (developer app).

## Complete setup checklist (2026-10-21)
- The owner asked to stop going back and forth: `docs/13-account-setup-complete.md` is the single full checklist for all four assets with every text and image (profile pictures plus new Facebook cover photos in `brand/`). The owner does the saves and passwords; the operator only verifies afterwards (Prompt 2D). After "setup done" and 3-5 days of warm-up comes Phase 2.

## Public check #2 (relay run 2010, 2026-10-21)
- **A2 Facebook Page "Roz Ka Rule": username `rozkarule` works (facebook.com/rozkarule resolves), category Education, name correct, two photos present.** Done.
- **B2 "Quiet Discipline": name and username `disciplinequiet` correct, two photos present, but category is still "Arts & entertainment".** Needs Education.
- Facebook About text and intro are not visible to logged-out visitors, so not verified. Instagram profiles are login-walled; A1 and B1 can only be verified by the operator (Prompt 2D) or by the owner. No new operator reports since 2B/2C/2D.

## Account state after owner's updates (operator read-only recheck, 2026-10-21)
- **Done:** A1 @rozkarule: name "Roz Ka Rule", bio, category Education, picture. A2 Page "Roz Ka Rule": username rozkarule, category Education, intro/About, picture. B1 renamed to **@the.disciplinequiet**, name "Quiet Discipline", bio, picture (old @disciplinequite URL is gone). B2 Page "Quiet Discipline": username disciplinequiet, category Education, intro/About, picture.
- **Open:** Facebook **cover photos** on both Pages (none yet; files `brand/page_a_cover.png`, `page_b_cover.png`); B1 category and account types (Creator vs Business) unverified; **two-factor and Security Checkup** unverified (B1 was OFF); A1 Account Status unchecked; the unused Instagram-login people in the portfolio (owner decision); Chrome's Facebook is acting as the Page B2 (switch back).
- Facebook Page About text is the one-line bio, not the longer About from docs/13. Optional.
- My relay's Instagram fetches now get HTTP 429/403 from Instagram; the builder stops probing Instagram and relies on operator reports.
- Next: Prompt 3 (Meta developer app) while the accounts warm up.

## Owner confirmations (2026-10-21)
- Facebook cover photos uploaded on both Pages. B1 category is Education. A1 and B1 are **Creator** accounts. Account status shows green on all three checks.
- **Owner decisions, noted as risk, not blockers:** two-factor authentication is **on hold**; Security Checkup is **on hold**; the unused Instagram-login profiles in the "Quite Discipline" portfolio are **left in place**. Risk: whoever gets into the owner's Facebook login controls both Pages and the developer app; those profiles have full portfolio access. Revisit before `LIVE_PUBLISH` goes true (2FA at minimum).
- **Account setup is complete.** Next: Phase 2 (Meta developer app and tokens). Warm-up (3-5 days, no posting) runs in parallel.

## Developer app created (operator Prompt 3 report, 2026-10-21)
- Meta app **"Quotes Publisher"**, **App ID 1454446477743438**, Business type, **Development mode**, owner Ayush Sharma is the only Administrator. Instagram product added with **API setup with Facebook login**. App Secret never read (owner keeps it). Contact email on the app was prefilled with another Gmail; optional to change. The "Other" use case is marked "going away soon" by Meta; the app uses the older product experience.
- Next (owner, manual): Graph API Explorer token for the two Pages and two Instagram accounts only, run `pipeline/setup_tokens.py` on the Mac, put 4 secrets plus slides-repo secret/variable into GitHub. Then run workflow `verify-setup` (pipeline/verify.py): checks account access, publishing quota, trending audio, slides repo. No secrets printed.

## Setup verification run (verify-setup, 2026-10-21)
- **PASS:** Page A `@rozkarule` (name "Roz Ka Rule") and Page B `@the.disciplinequiet` (name "Quiet Discipline") are readable with the stored tokens; publishing quota 0/100 per 24h on both; **Audio API returns 25 trending tracks on both accounts** (so trending audio via API works with these tokens).
- **FAIL:** `ASSETS_REPO` variable and `ASSETS_PAT` secret were empty in the workflow. Slide hosting is the only missing piece. (ASSETS_REPO must be a repository *variable*, ASSETS_PAT a *secret*.)
- A commit on this branch ("setup_tokens: show granted permissions and fall back to known Page IDs when /me/accounts is empty") shows the token script had to be adjusted during the owner's token step.

## Trending audio pinned for week-1 Reels (2026-10-21)
- The weekly `audio-shortlist` job works (needed a folder fix). Real trending tracks from Meta's Audio API are in `research/audio/2026-10-21_page_*.md`. Picks were made from title and artist only (not listened to); owner may veto. Page A: procrastination = Maya Maya (Instrumental), exam-night = Piano Mystique, speak-clearly = Knockout. Page B: willpower = Good Vibes, understood = Whistling Through Fall, boundary = Hopeful Ascent. IDs are pinned in each reel's `audio_id`. Tracks flagged ads-eligible False are fine for organic posts but should not be used once a page promotes products.
- Still missing for the first live post: slide hosting (`ASSETS_REPO` variable, `ASSETS_PAT` secret).

## Setup fully verified (verify-setup run 3, 2026-10-21)
- **ALL CHECKS PASSED:** both Instagram accounts readable, publishing quota 0/100, trending audio returns 25 tracks each, slides repo `aayu95me-sketch/quotes-slides` is public and writable with `ASSETS_PAT`. Secrets and variables are in place.
- Review packs built with `pipeline/review.py` (`out/review_page_a.pdf`, `out/review_page_b.pdf`, 10 drafts each) and sent to the owner. Nothing is approved yet; `LIVE_PUBLISH` is not set, so the scheduled job only dry-runs.
- **Go-live plan:** owner reviews, tells Claude which posts to approve (Claude edits `status: approved`); first live post is a single approved carousel with `publish_at` set a few minutes ahead, then `LIVE_PUBLISH=true`. Two-factor is still off (owner decision; risk noted).

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
- `docs/01-market-research.md` platforms, money, risks. `02-india-addendum.md` India payouts, tax, SEBI. `03-competitor-notes.md`. `04-brand-briefs.md` page briefs. `05-research-prompts.md` manual prompts (mostly superseded). `06-verified-facts.md` official facts. `07-competitors-and-rates.md`. `08-account-setup-guide.md` **owner's step-by-step**. `09-content-plan.md` 30-day plan. `10-audio-strategy.md` audio. `11-claude-chat-prompts.md` prompt pack for account-level tasks. `12-bridge-claude-chat.md` how Claude Code and the chat project "static automation" connect.
- `content/pages/*.json` brand config. `content/posts/<page>/*.json` posts. `brand/` profile images.
- `pipeline/`: `render.py`, `reel.py`, `audio.py`, `approve.py`, `publish.py`, `relay.py`, `brand.py`, `setup_tokens.py`. `content/audio_moods.json`.
- `research/requests`, `research/answers`: relay. `research/audio`: weekly audio shortlists. `.github/workflows/`: `research-relay.yml`, `publish.yml`, `audio-shortlist.yml`.
