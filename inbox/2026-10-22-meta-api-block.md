# REPORT: Prompt 4, Meta API access blocked (read-only)

Date: 2026-10-22 (checked about 13:55 to 14:05 UTC)
Operator: Claude Code, project "Static Automation", using the owner's Chrome ("Browser 1", macOS)
Mode: read-only. Nothing was changed, no password was typed, the App Secret and tokens were not opened or shown.

**task:** Prompt 4. Find why the API says "Cannot call API for app 1454446477743438 on behalf of user 28142739095405684" / "API access blocked".

**done:** partly. The likely cause was found (step 1), but the app screens behind it could not be read.

## Most likely cause
The owner's **Meta developer account is blocked pending confirmation**. Every developer page for the app redirects to `developers.facebook.com/r/user/error/` (page title "Developer Platform Blocked User Error - Meta for Developers"), which shows:

> **Account confirmation needed**
> "We've noticed unusual activity on this developer account. Please complete the confirmation steps to regain access."
> Button: **Confirm Account**

I did NOT press "Confirm Account". It starts an identity/security check that the owner must do personally.

This matches the API error: the token belongs to this developer user, and Meta blocks API calls from a developer account that is in this state. The Accounts Centre also shows **"We detected unrecognised logins"** and Facebook notifications show **"We noticed a new login from a device or location that you don't usually use"** about 1 day ago (about 21 Oct, the same day tokens stopped at 17:07 UTC). That is the likely trigger.

## Step by step

| # | Screen | Read? | What it shows |
|---|---|---|---|
| 1 | developers.facebook.com > app 1454446477743438 > Dashboard | **No** (blocked) | Redirects to the "Account confirmation needed" screen above. App Mode, banners, App roles, Alerts/Notifications/App Review could NOT be read. |
| 2 | Same app > Settings > Basic | **No** (blocked) | Same redirect. Live/Development status and any "Action required" could NOT be read. |
| 3a | Business Support Home (facebook.com/business-support-home) | Yes | "Recent account issues, last 30 days (23 Sep to 22 Oct 2026): **No account or asset issues**." Support cases: **No support cases**. |
| 3b | Business Support Home > My accounts | Yes | Facebook account Ayush Sharma: **No advertising issues**. Portfolios "Quite Discipline" (1370046235203586) and "Roz ka Rule" (885074191266141): **No advertising issues**. (This page only covers advertising standards, not the developer platform.) |
| 3c | facebook.com/support (Support Inbox) | Yes | Only one old item: "You had a billing issue with your advertisements", 13 Feb 2024. Nothing new, nothing about the Pages or Instagram accounts. |
| 3d | Facebook notifications | Yes | No restriction or warning on the Pages or IG accounts. One security item: "We noticed a new login from a device or location that you don't usually use. Please review." (1d ago, unread, not opened). Also a DM notification on Page "Quiet Discipline" addressed to `the.disciplinequiet`. |
| 4 | Instagram > Account status, both accounts | **No** | No Account status page on Instagram web (URL gives "Page not found"). Chrome's Instagram is signed in as **@rozkarule (A1)**, so B1 can't be checked here either. Check both in the phone app. |
| 5 | Accounts Centre > Password and security > Where you're logged in | Yes (top level only) | Warning: **"We detected unrecognised logins. Review devices"**. I did not open "Review devices" and changed nothing. No sign of a forced logout today: Chrome is still signed in to Facebook and Instagram. |
| 6a | Business settings > People, portfolio "Quite Discipline" (1370046235203586) | Yes | 4 people, all Full access: (1) "Quite Discipline" **@the.disciplinequiet**, Instagram login, No activity, Inactive, **new since the 21 Oct report**; (2) "Quiet Discipline", Instagram login, last active 21 Oct 2026, Active; (3) "Quiet Discipline", Instagram login, No activity, Inactive; (4) Ayush Sharma (you), last active 22 Oct 2026. No removed roles seen. |
| 6b | Business settings > People, portfolio "Roz ka Rule" (885074191266141) | **No** | My browser tool's safety check refused to open this page. Owner can check it in Business settings > Users > People. |

## Screens I could NOT read
1. App Dashboard (mode, banners, roles, alerts, App Review): blocked by "Account confirmation needed".
2. App Settings > Basic (Live/Development, Action required): same block.
3. Instagram Account status for A1 and B1: not available on web; B1 not signed in in Chrome.
4. "Review devices" detail list: not opened on purpose (security screen, owner's call).
5. People list of portfolio "Roz ka Rule": tool refused to navigate there.

## What the owner should do (owner only)
1. Open developers.facebook.com in your own browser and press **Confirm Account**. Follow Meta's steps (it may ask for a login, code or ID). Do not do this through Claude.
2. Accounts Centre > Password and security > Where you're logged in > **Review devices**. Log out any device you don't recognise, then change your Facebook password and turn on 2FA (CLAUDE.md manual step).
3. When developer access is back, tell Claude Code. We then re-read App Dashboard and Settings > Basic (steps 1 and 2) and, if clean, regenerate tokens with `pipeline/setup_tokens.py` and update the four GitHub secrets.
4. Confirm whether the new "Quite Discipline @the.disciplinequiet" person in portfolio 1370046235203586 is your own Instagram login (likely created by the B1 rename).

## REPORT
- **task:** Prompt 4, Meta API block investigation (read-only)
- **done:** partly
- **assets touched:** none changed. Viewed only: portfolios Quite Discipline (1370046235203586) and Roz ka Rule (885074191266141) on the support overview; People list of Quite Discipline. Developer app "Quotes Publisher" (1454446477743438) not reachable.
- **what changed:** nothing. Only "Continue" on two Facebook redirect-confirmation screens was clicked (navigation). Facebook did a `forced_account_switch` redirect on the way to Business Support Home, so the Facebook session may now act as the personal profile instead of a Page.
- **what I could not do and why:** app Dashboard and Settings > Basic (developer account blocked: "Account confirmation needed"); Instagram Account status (not on web, B1 not signed in); Review devices (security screen, not opened); Roz ka Rule People list (tool refused).
- **current state of the four assets:** no restriction, warning or case found for A1 @rozkarule (17841469203264060), A2 Page "Roz Ka Rule" (1345396148663682), B1 (17841422691847840), B2 Page "Quiet Discipline" (1436529449539802). B1's handle appears as **@the.disciplinequiet** in the portfolio People list and in a Page notification, so the rename looks done (not verified on the profile itself).
- **unexpected / out of scope, noticed but NOT touched:** Business Support Home also lists portfolios "Ayush Sharma" (2208419812797513), "Chunav Diary" (1181531260120456) and "LuvKush" (786537768713352), all "No advertising issues"; not opened. One Business Suite URL redirected to Chunav Diary's home; I left at once. "Where you're logged in" lists other Instagram accounts (chunavdiary, ayushluvsharma); not opened.
