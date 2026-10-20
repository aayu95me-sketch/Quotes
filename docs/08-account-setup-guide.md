# Account and Setup Guide (step by step)

For: the owner. Total hands-on time: about 2-3 hours, spread over a week. Steps marked **[official]** come from Meta's own pages that I fetched on 2026-10-20 (`research/answers/2007-*`, `2008-*`). Menu names move around often, so if a screen does not match, **send me a screenshot and I'll adjust**. Never paste passwords, tokens or the App Secret into chat or screenshots. Tokens go only into GitHub Secrets.

## Rules that keep the accounts safe
- Use **your own real phone number and email**, and your **own phone** on your normal network. No VPN, no emulators, no bulk-creation tools, no buying accounts.
- Two pages is fine. Instagram lets you log in to up to 10 accounts on one app **[official]**.
- Turn on **two-factor authentication** on Facebook and on both Instagram accounts (Settings > Accounts Center > Password and security > Two-factor authentication). Use an authenticator app (Google Authenticator or similar), and save the backup codes somewhere safe.
- Don't post yet. **Warm up each new account for 3-5 days**: add the profile picture and bio, follow 10-20 real accounts in the niche, like and save a few posts a day, watch some Reels. This is my judgement, not a Meta rule.

## Phase 1: do this now (no technical skill needed)
Gets the accounts ready. Takes about 45 minutes.

1. **Facebook:** log in to your normal personal Facebook account. If you don't have one, create one with your real name. (Pages are managed by a real personal profile.)
2. **Create two Instagram accounts** in the Instagram app (Add account > Create new account). Use two different emails (a free Gmail alias such as `yourname+rozkarule@gmail.com` works for the email field) and your phone number for verification.
   - Page A username: `rozkarule`. Page B username: `quietdiscipline`.
   - **If a name is taken**, try (in order): Page A `roz.ka.rule`, `rozkarule.in`, `rozkarule_daily`. Page B `quiet.discipline`, `quietdiscipline.co`, `quietdiscipline_daily`. Tell me the final handles so I can update the files.
3. **Profile pictures:** use `brand/page_a_profile.png` and `brand/page_b_profile.png` from the repo (download them from GitHub on your Mac and AirDrop them to your phone, or save them from the GitHub app).
4. **Bios** (paste, then adjust if you wish):
   - Page A (Instagram, max 150 chars): `Roz ka ek rule. Discipline, career aur dimaag ke liye simple tips. 🇮🇳 Save karo, follow karo.`
   - Page B: `One small rule a day for discipline, focus and a calmer mind. Save what helps.`
5. **Switch each account to Professional (Creator)** **[official]**: Profile > More (the menu) > Settings and activity > under *For professionals* tap **Account type and tools** > **Switch to professional account** > pick a category (for example *Education*, or *Personal blog*) > choose **Creator** > Next. Note: a private account becomes public when switched.
6. **Create a Facebook Page for each** (needed to connect to the API): Facebook > Pages > Create new Page. Names: `Roz Ka Rule` and `Quiet Discipline`. Category: Education or Personal blog. Use the same profile picture.
7. **Link each Instagram account to its Facebook Page:** in the Instagram app go to Settings and activity > Account type and tools (or the *Connected accounts / Accounts Center* area) and connect the Page. In the professional-account flow, the step *Login to Facebook > connect to an existing Page* does the same **[official]**. Link **Page A to Instagram A**, and **Page B to Instagram B**, not crossed.
8. **Turn on 2FA** (see Rules above) for Facebook and both Instagram accounts.
9. **Tell me**: the final handles and Page names. Then I update the repo.

**Then warm up for 3-5 days.** Do phase 2 in this window.

## Phase 2: Meta developer app and tokens (about 1 hour)
We'll go through this together over chat. Do one step at a time and tell me where you are.

1. **Register as a Meta developer** **[official]**: while logged in to Facebook, open https://developers.facebook.com/async/registration, accept the terms, confirm the code sent to your phone and email, and choose an occupation. (You do not need a company.)
2. **Create the app** **[official]**: App Dashboard > **Create App** > use case **Other** > app type **Business** > give it any name (for example `Quotes Publisher`) and your contact email > Create. You can skip connecting a business portfolio for now.
3. **Add the Instagram product** **[official]**: on the app dashboard scroll to **Instagram** > **Set up**. Choose **API setup with Facebook login**. (**Do not use the Instagram-login option.** The trending-audio feature only works with Facebook login.)
4. **Access level:** your app stays in *Standard Access*. That is enough for accounts you own and manage, since your own Facebook user already has the admin role on the app. **No App Review and no Business Verification should be needed** for your own accounts **[official, with the caveat that Meta can change this]**. App Review only matters for serving other people's accounts.
5. **Get the App ID and App Secret:** App settings > Basic. **Copy the App Secret only to your own computer. Never into chat.**
6. **Make a short-lived token:** open the Graph API Explorer (developers.facebook.com/tools/explorer), select your app, click **Generate Access Token**, and tick these permissions: `instagram_basic`, `instagram_content_publish`, `instagram_manage_insights`, `pages_show_list`, `pages_read_engagement`. Log in and allow both Pages. (If a permission is missing from the list, tell me which.)
7. **Turn it into a long-lived Page token on your own Mac.** Long-lived **Page** tokens do not expire unless invalidated **[official]**. Run the helper from the repo:
   ```
   git clone https://github.com/aayu95me-sketch/Quotes.git && cd Quotes
   git checkout claude/eager-bell-i41n67
   python3 pipeline/setup_tokens.py
   ```
   It asks for the App ID, the App Secret (hidden) and the short-lived token (hidden), then prints each Page, its Instagram user ID and its long-lived Page token **in your terminal only**.
8. **Save the secrets** in GitHub: repo `Quotes` > Settings > Secrets and variables > Actions > **New repository secret**:
   - `IG_PAGE_A_USER_ID`, `IG_PAGE_A_TOKEN` (for Page A)
   - `IG_PAGE_B_USER_ID`, `IG_PAGE_B_TOKEN` (for Page B)
9. **Slide hosting** (Instagram must fetch images from a public URL):
   - Create a new **public** GitHub repo, for example `quotes-slides` (empty, with a README so it has a `main` branch). It contains only the slides we publish, nothing else.
   - Create a **fine-grained personal access token**: GitHub > Settings > Developer settings > Personal access tokens > Fine-grained > only repository `quotes-slides`, permission **Contents: Read and write**. Save it as the secret `ASSETS_PAT`.
   - Add a repository **variable** (not secret) `ASSETS_REPO` = `aayu95me-sketch/quotes-slides`.
10. **Test post (dry run first):** I run the publisher in dry-run, then you approve one draft and I trigger one live post on one account, and we check it on your phone.
11. **Go live:** set the repository variable `LIVE_PUBLISH` = `true` and merge the branch to `main` (scheduled GitHub jobs only run from `main`). I'll ask before doing the merge.

## Token upkeep
- Page tokens should not expire, but they stop working if you change your Facebook password, remove the app, or Meta invalidates them. If publishing starts failing with an auth error, rerun step 7.
- Check the app's status monthly in the App Dashboard.

## What I need back from you after phase 1
Final handles, Page names, and a yes that two-factor is on. Then I'll tell you when to start phase 2.
