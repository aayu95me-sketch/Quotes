# India Addendum: Research Round 1b

Date: 2026-10-20. Owner is **India-based; payouts must reach an Indian bank account.** Tools: MacBook, Claude, Gemini Pro, free/open-source software. Owner can create any accounts and approve posts for the first month.

Evidence labels as in doc 01: **[Solid]** = official or benchmark, **[Soft]** = blog or vendor, **[My judgement]** = inference. All tax and legal points are **research notes, not advice**. Get a CA to confirm before the first rupee comes in.

---

## 1. What being in India changes

### Platform payouts: weak for an India-based, India-audience page
- **Instagram Reels bonus:** reported closed to new and renewing participants in major markets including India since 2025 [Soft]. Replacement income (Gifts, Stars, Subscriptions) has unclear India availability [Soft, unverified].
- **Facebook Content Monetization:** thresholds conflict across sources, and availability by country is gradual and partly invite-only [Soft]. India payouts need a **PAN, a W-8BEN tax form and a bank account with a SWIFT code**; one guide cites a monthly payout with a $25–$100 minimum [Soft]. India-audience RPM is reported as very low (about $0.30–$1 per 1,000 views on some estimates, far lower on others) [Soft].
- **X:** the old programme paid Indian creators via Stripe, but I found **no 2026 information on India eligibility for the replacement ("Original Content Rewards") or on X Money in India** [unverified]. Needs Premium (₹ paid).
- **TikTok:** not available in India [My judgement, from the eligible-country lists seen, plus the known ban]. Ignore it.
- **YouTube Shorts:** AdSense works in India, but RPM is tiny and static slideshows risk the "inauthentic content" classification.

**Conclusion:** platform payouts are a rounding error for an India page. Money must come from **sponsors, affiliates, own products and owned audience.**

### Audience choice (Instagram is huge in India)
- India is the world's largest Instagram audience: about 414M (Buffer) to 532M (NapoleonCat) users, by different methods [Soft]. 25–34 is the biggest age group, and about 69% of users are men.
- Fastest virality is likely with an **Indian audience** (huge, share-happy, DM-forwarding culture) [My judgement]. Highest dollar value per follower is with **US/UK/CA/AU English audiences** [Soft].
- Content is text, so the audience is decided by topic, references, language and hashtags, not by where the owner lives. You can aim at either.

**Proposed split (pilot design, [My judgement]):**
| Page | Audience | Why | Monetisation path |
|---|---|---|---|
| **A** | India, English/Hinglish | Fastest follower growth; Indian brands pay in INR; Indian affiliates pay in INR | INR sponsors, Cuelinks/Amazon India affiliates, own digital product sold in INR via UPI |
| **B** | US/UK/CA/AU, English | Higher value per follower; global affiliate and SaaS offers | Global affiliates (recurring SaaS commissions), dollar sponsors, digital products, Facebook CMP if eligible |

The pilot's job is to find out which is better. Don't decide on a hunch.

### Niche in India: the SEBI problem
Finance is the highest-paying niche globally, but in India **SEBI regulates "finfluencers".** What I found [Soft, media coverage, not SEBI's text]:
- 2024: regulated entities (brokers, mutual funds, etc.) barred from associating with unregistered finfluencers who give advice or make performance claims, and told to cut ties within three months. Pure investor *education* without explicit recommendations or performance claims is exempt.
- 2025–26: further proposals/notifications restricting associations and forbidding unregistered people from return/performance claims. Final text and dates **unconfirmed**.

**Implication:** an Indian page may do **money-habits and financial literacy** (budgeting, saving, scams, general concepts) but must not give stock/crypto tips, name securities, or claim returns. And **regulated brokers and AMCs likely can't pay us** for referrals. Don't plan on demat or mutual-fund referral income until SEBI's current rules are read directly.

Safer high-ceiling Indian niches [My judgement]: **career and exam/job motivation, discipline and habits, psychology facts, productivity and study, relationships.** I will confirm with a competitor teardown.

---

## 2. Getting paid in India (research notes)

| Item | What I found | Status |
|---|---|---|
| Income tax | Creator income is generally business/professional income; expenses are deductible. One source mentions a new profession code for creators and a presumptive scheme (44ADA) | [Soft]; CA to confirm |
| GST | Registration needed above ₹20 lakh turnover (₹10 lakh in some NE states). Platform ad revenue from abroad is described as an **export of service at 0% GST, with a Letter of Undertaking (LUT) filed on the GST portal** | [Soft]; CA to confirm |
| Non-cash perks | 10% TDS can apply to benefits like free gadgets or trips above ₹20,000 a year (likely Section 194R) | [Soft] |
| Foreign platform payouts | PAN + W-8BEN (+ SWIFT bank details) | [Soft] |
| Selling digital products | **SuperProfile**: UPI/cards for India, buyers abroad can pay in their own currency, rupee payout T+1 (needs paid plan). **Instamojo**: UPI/cards, fees about 5–10% + ₹3. **Lemon Squeezy** (5% + 50c) and **Gumroad** (10% + 50c): Merchant-of-Record, but India payout details **not confirmed**. Stan Store: PayPal only for India sellers | [Soft]; verify payout support before choosing |
| Indian affiliates | **Cuelinks** (800+ Indian merchants, auto-linking, about ₹500 minimum payout). **Amazon Associates India** (1–9% commission, 24-hour cookie) | [Soft]; terms vary by merchant |

**Action:** book a one-hour call with a CA early to decide the structure (sole proprietor versus company, GST registration, LUT, advance tax). It costs little compared with a tax mess later.

---

## 3. Tooling, given the owner's setup

- **Claude:** all writing, ideation, analysis, and code. This is the core engine.
- **Gemini Pro / open-source:** optional. Possible uses are batch idea generation, background images, or backup. Only worth adding if a specific gap appears; one engine keeps things simple.
- **Rendering (free):** HTML/CSS → PNG with Playwright or Pillow. Static-image Reels with **ffmpeg** (a still image plus audio, no motion needed). Both run on a MacBook.
- **Publishing:** Instagram Graph API, via a small script. Hosting options: (a) the MacBook with `launchd` (must be on and awake), or (b) **GitHub Actions** on a schedule (free tier, always on). I prefer (b) for reliability.
- **Storage:** this repo (content calendar, templates, performance logs). Secrets (tokens) go in GitHub Secrets, never in the repo.
- **Cost:** near zero apart from the optional X Premium, any paid product-selling plan, and a domain/link-in-bio page.

---

## 4. Account checklist (owner to create)

Use real details, one person, no bulk creation. Accounts must belong to the owner.

1. **Facebook personal account** (the owner's real one) → create a **Facebook Page per pilot page** (needed to link Instagram to the API).
2. **Instagram account per page**, switched to **Professional (Creator or Business)** and linked to its Facebook Page. Two accounts to start (A and B).
3. **Meta Developer account + app** (developers.facebook.com) with Instagram Graph API access. I'll guide the setup; app review may be needed for full access, but a test-user setup works on your own accounts without review [My judgement, verify].
4. **GitHub**: already in use. Confirm that Actions is enabled on this repo.
5. **Gmail alias or dedicated email** for the brand (one per page).
6. **Link-in-bio + email list tool** (free tier): decide later. Candidates: a simple static page on GitHub Pages, plus a free-tier email service.
7. **PAN-linked bank account** (already have) and a **UPI ID**.

Do **not** create accounts yet. First I need the brand briefs (next step), so the names and handles are right.

---

## 5. Open items / things to verify

- [ ] Exact Meta CMP, Gifts, Stars and subscriptions availability **in India**, from the owner's Meta Business Suite.
- [ ] SEBI current notifications (read directly) before any finance-adjacent content.
- [ ] Which product-selling platform pays out to Indian banks (Lemon Squeezy / Gumroad / SuperProfile).
- [ ] Whether Instagram Audio API works for these accounts (spike test).
- [ ] Competitor teardown for India English/Hinglish niches and for Tier-1 English niches.
- [ ] Hinglish versus English performance, a pilot variable.

## Sources
- [Buffer: Instagram statistics 2026](https://buffer.com/resources/instagram-statistics/)
- [NapoleonCat: Instagram users in India](https://napoleoncat.com/stats/instagram-users-in-india/)
- [TechnologyChecker: Instagram user statistics](https://technologychecker.io/blog/instagram-user-statistics)
- [Socialchamp: Facebook monetisation 2026](https://www.socialchamp.com/blog/facebook-monetization/)
- [TechieGigs: Facebook monetisation India](https://techiegigs.com/how-to-apply-for-facebook-monetization/)
- [Ranktracker: Instagram Reels bonus program](https://www.ranktracker.com/it/blog/how-to-join-instagram-s-reels-bonus-program-and-what-to-do-now/)
- [Lilach Bullock: Instagram Reels pay in India](https://www.lilachbullock.com/how-much-does-instagram-pay-for-reels-views-in-india/)
- [TaxAJ: GST and income tax for creators in India](https://www.taxaj.com/learn/gst-and-income-tax-for-influencers-and-content-creators-in-india-2026/)
- [Outlook Business: Reels income and ITR](https://www.outlookbusiness.com/news/making-money-from-reels-your-income-isnt-tax-free-heres-how-influencers-should-file-itr)
- [InCorpX: creator taxes India](https://www.incorpx.io/blog/content-creator-taxes-compliance-india)
- [Outlook Business: SEBI amends rules to regulate finfluencers](https://www.outlookbusiness.com/markets/sebi-amends-rules-to-regulate-finfluencers)
- [Storyboard18: SEBI finfluencer ties](https://stgwww.storyboard18.com/amp/how-it-works/sebi-mandates-regulated-entities-to-sever-ties-with-finfluencers-within-3-months-46304.htm)
- [Cuelinks: top affiliate programs India](https://www.cuelinks.com/blog/top-10-affiliate-programs-india/)
- [Cashfree: best affiliate programs India](https://www.cashfree.com/blog/10-best-affiliate-programs-in-india/)
- [SuperProfile: Gumroad alternatives for India](https://superprofile.bio/compare/gumroad-alternatives-india)
- [Dodo Payments: Lemon Squeezy review](https://dodopayments.com/blogs/lemonsqueezy-review)
- [Fonearena: X Premium+ price hike](https://www.fonearena.com/blog/442852/x-premium-plus-price-hike.html/amp)
