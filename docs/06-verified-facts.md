# Verified Facts (from official or primary pages, fetched via the research relay)

Fetched 2026-10-20 by `pipeline/relay.py` on GitHub Actions. Raw pages are in `research/answers/001-official-docs/` and `research/answers/002-policy-search/`. These upgrade earlier [Soft] claims to **[Official]**.

## Instagram publishing and audio (Meta developer docs)
- **Audio API** (page updated Jun 16, 2026): search or fetch **trending** original sounds and music and **attach them to Reels at creation time**. Needs an Instagram **Business or Creator** account, a connected **Facebook Page**, a Facebook App with `instagram_basic` + `instagram_content_publish`, and a user access token. **Only the "Instagram API with Facebook Login" supports it**, not Instagram Login. It returns only audio authorised for third-party use, so the list can differ from the app. If no search query is given, trending audio is returned. No Reel preview with audio through the API. Endpoint: `GET /ig_audio?audio_type=music|original_sound&user_id=...`.
  - Consequence: use **Facebook Login** when setting up the Meta app. Trending audio on static Reels is feasible through the API.
- **Limits:** 100 API-published posts per rolling 24 hours; a carousel counts as one. Carousels up to **20** items (the page also contains an older "50 posts" line; treat 100 as current and check `GET /<IG_ID>/content_publishing_limit`).
- **No scheduled-publish parameter** is documented. The docs tell apps to enforce their own limit "if your app allows app users to schedule posts". Our own scheduler (GitHub Actions cron) is the right design.
- **AI self-disclosure:** set `is_ai_generated=true` on the container; for carousels set it **only on the carousel container**, not on children. `publish.py` now does this when a post has `ai_label: true`.
- **Paid-partnership label** is available via `is_paid_partnership` / `branded_content_sponsor_ids` (Facebook Login only). Use it for sponsored posts.

## Instagram originality (Instagram for Creators blog, "Rewarding original creators")
- Protections previously on Reels now apply to **photos and carousels**: accounts that **primarily post unoriginal content** are **not shown in recommendation surfaces**. Followers still see their posts.
- Original = "work you wholly created or that reflects your unique perspective" (photos you took, content you **designed**, content you materially edited).
- Not original: re-uploading someone else's work with only a border, watermark, subtitles or caption credit.
- Recovery: an account becomes eligible again when **most of its recent posts are original over a rolling 30 days**. Check **Account Status**; appeals are possible.
- Consequence: pages made of **original, Claude-written text designed into our own templates** qualify as "content you designed". Reposted famous quotes in a template are the risky pattern.

## Instagram AI labels (Instagram for Creators blog)
- The "AI-generated profile" label is for **profiles featuring an AI-generated person**. "Creators who simply use AI tools as part of their creative process don't need to add the label." Our faceless text pages show no AI-generated person, so the profile label should not apply. We still set `is_ai_generated` on posts as a conservative disclosure; revisit once we see how it affects reach.

## Facebook monetisation (Meta Partner Monetization Policies)
- Public content on Facebook **Pages, profiles in professional mode**, Events and Groups can be monetised.
- You must **reside in an eligible country**, and **connected financial entities must also be in an eligible country**.
- Quote: "Content that is unoriginal or reproduced without making meaningful enhancements (commentary, parody, creative editing, etc.) cannot be monetized."
- An established presence of **at least 30 days** is needed for all features; in-stream ads also need a follower base and minimum videos.
- Meta can modify or end monetisation features at any time.
- India's current eligibility is **not stated** on this page. Check the owner's Meta Business Suite.

## SEBI (secondary legal explainers, not the circulars themselves)
- Since 2024 SEBI-regulated entities may not associate with unregistered persons who give securities advice or recommendations.
- A SEBI social-media disclosure circular is reported **effective May 1, 2026**: regulated entities and their agents must disclose registered name and registration number.
- Basic financial education (what mutual funds, stocks, diversification are) does not require registration. Repeated buy/sell/hold encouragement of specific securities does, and a bare "educational purposes" disclaimer does not protect a paid promoter.
- Our rule stands: **no securities tips, no returns claims, no paid promotion of securities products**.

## GST export of services (GST portal tutorial)
- A registered person who supplies services to a client outside India **without paying IGST** must furnish a **Letter of Undertaking (Form GST RFD-11) before** the supply, on the GST portal: Services > User Services > Furnish Letter of Undertaking. Filed per financial year, with two witnesses' details.
- LUT applies only if registered under GST. Registration is mandatory only above the turnover threshold (earlier notes said ₹20 lakh); a CA should confirm whether and when it applies to this income.

## Still unverified
- Facebook Content Monetization eligibility for India and photo/text post eligibility (owner can check in Meta Business Suite).
- Instagram Gifts, Subscriptions and Bonuses availability in India (`creators.instagram.com/bonuses`, `/earn-money/...`).
- Broadcast Channels requirements (search returned no result; `creators.instagram.com/create/broadcast-channels` exists).
- Competitor accounts and Hinglish-versus-English performance (needs a search-grounded LLM or manual check).
