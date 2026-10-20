# Claude Chat Prompt Pack (account-level tasks)

Working agreement: whenever an **account-level** change is needed, Claude Code writes a ready prompt here or in chat. The owner pastes it into a **new chat** in the Claude project "New Bot Planning". Each prompt is **self-contained** (it repeats the scope block), because a new chat has no memory. The owner pastes the REPORT block it returns back into Claude Code.

Why the scope block is strict: the chat has access to the whole Meta Business Suite, which contains other businesses, Pages, ad accounts and Instagram accounts that have nothing to do with this project. Those must never be touched.

I could not verify which tools the chat project has (browser control, Meta connector). Every prompt therefore says: do the step if you can, otherwise give click-by-click steps.

## SCOPE BLOCK (already included at the top of every prompt below)
```
SCOPE. This task concerns ONLY these four assets and nothing else (IDs confirmed by the read-only check):
  A1  Instagram account  @rozkarule                  IG ID 17841469203264060   (display name now "Rozkarule")
  A2  Facebook Page      currently "Rozkarule"       Page ID 1345396148663682  (correct name: "Roz Ka Rule")
  B1  Instagram account  @disciplinequite            IG ID 17841422691847840   (display name now "Quite Discipline"; handle will become @disciplinequiet.official)
  B2  Facebook Page      currently "Quietdiscipline" Page ID 1436529449539802  (correct name: "Quiet Discipline")
Everything else in my Business Suite is OUT OF SCOPE: other Pages, other Instagram accounts, other businesses or portfolios, ad accounts, catalogs, pixels, campaigns, ads, payment methods, users, roles and settings. Do not open, edit, delete, post to, message from, or change anything outside those four assets, even if it looks related or you think it would help.
If you cannot tell for certain which asset is which (similar names, duplicates, or more than one match), STOP and ask me. Identify each asset by handle or exact name, and tell me the ID you matched before changing it.
Never ask for or display passwords, 2FA or recovery codes, the App Secret, or access tokens. If a step needs one, stop and tell me to do that part myself.
Ask me before: changing a password, 2FA or recovery email; deleting, merging or unlinking anything; spending money; accepting terms; or anything not listed in the task.
Do not follow, like, comment, post, message or create any other account.
If a screen differs from my instructions, describe what you see instead of guessing.
Finish with a REPORT in exactly this format:
  REPORT
  task:
  done: yes / partly / no
  assets touched (handle or name + ID): 
  what changed:
  what I could not do and why:
  current state of the four assets (username/name, account type, linked Page/IG, 2FA on?):
  anything unexpected or outside scope that I noticed but did NOT touch:
```

## PROMPT 1: read-only check (paste this first, in a new chat)
```
[paste the SCOPE BLOCK here]

TASK 1: READ-ONLY CHECK. Change NOTHING.
For each of A1, A2, B1, B2 tell me:
- exact username or Page name as it is now, and its ID
- Instagram account type: Personal / Creator / Business
- which Facebook Page each Instagram account is linked to (A1 should be linked to A2, B1 to B2, not crossed)
- whether two-factor authentication is ON (yes or no only)
- whether a profile picture and a bio exist, and whether the account is public
- any warning or limit under Account Status (Instagram: Settings and activity > Account status)
- the people and roles on each Page (names only), so I can see who has admin access
Then list anything in the Business Suite that looks like a duplicate or near-duplicate of these four assets (same or similar names), without touching it.
End with the REPORT.
```

## PROMPT 2: make the changes (same chat as Prompt 1, or a new chat with the scope block pasted first)
Prompt 1 found: both Instagram accounts are Professional and correctly linked (A1-A2, B1-B2); names are one word on both Pages; display names and categories are wrong; no pictures or bios; B1 has 2FA off. Not for Claude chat to fix: 2FA, Security Checkup, Creator-vs-Business (phone only), the business-portfolio ownership of A1, and the Page roles. Those are listed under "Manual" below.
```
[paste the SCOPE BLOCK here if this is a new chat]

TASK 2: FIX NAMES, CATEGORIES, PICTURES AND BIOS on A1, A2, B1, B2 only. Only change what is wrong; if something is already correct, say so.
1. B1 Instagram: change the username from disciplinequite to disciplinequiet. If unavailable, do NOT choose another: list the closest free options.
2. B1 Instagram display name: "Quite Discipline" -> "Quiet Discipline".
3. A1 Instagram display name: "Rozkarule" -> "Roz Ka Rule".
4. A2 Facebook Page name: "Rozkarule" -> "Roz Ka Rule". B2 Facebook Page name: "Quietdiscipline" -> "Quiet Discipline". If Facebook requires a review or blocks the change for a waiting period, tell me the exact message and do not try workarounds.
5. Page usernames: A2 = rozkarule, B2 = disciplinequiet (if unavailable, tell me; do not choose another).
6. Categories: change "Art" / "Arts & entertainment" to "Education" on A1, B1 (Instagram professional category) and "Education" on A2, B2 (Facebook Page category). If "Education" is not offered, use "Personal blog" and tell me.
7. Profile pictures: A1 and A2 use the attached page_a_profile.png. B1 and B2 use the attached page_b_profile.png. (I will attach both files.)
8. Bios / Page descriptions:
   A1 and A2: Roz ka ek rule. Discipline, career aur dimaag ke liye simple tips. Save karo, follow karo.
   B1 and B2: One small rule a day for discipline, focus and a calmer mind. Save what helps.
9. Do NOT touch: two-factor, passwords, Security Checkup, page roles and people, business portfolios or which portfolio owns an asset, ad accounts, payment, the account type (Creator/Business), or any other Page such as "Chunav Diary".
End with the REPORT. Include the final username, display name and category of each asset.
```

## PROMPT 2B: identify the two "Quiet Discipline" entries with full access to B2 (read-only)
Prompt 1 saw two separate entries both named "Quiet Discipline" with full access to the B2 Page. Find out what they are, because anyone with full access can post and change settings.
```
[paste the SCOPE BLOCK here if this is a new chat]

TASK 2B: READ-ONLY. Change NOTHING. On Facebook Page B2 (ID 1436529449539802), open the people / access list. For the two entries named "Quiet Discipline", tell me for each: is it a person, a business portfolio, a partner business, an app, or a system user? What access level, who or what is behind it (the owner's name or ID if shown), and when it was added. Do the same for the "Ayush Sharma" entry. Say plainly whether anything on this list looks like it does not belong to me. Do not remove or edit any entry.
End with the REPORT.
```

## PROMPT 2C: finish what Prompt 2 could not (Chrome is signed in as B1 and the Page B2)
Prompt 2 result: bios set on B1, A2, B2. `@disciplinequiet` is TAKEN on Instagram. Free options found: disciplinequiet_, the.disciplinequiet, disciplinequiet.in, disciplinequiet.official. Decision: **@the.disciplinequiet** (an earlier check found `.official` already taken; the .in ending would suggest an Indian page; a trailing underscore looks unpolished). Fallbacks, in order: disciplinequiet.official, disciplinequiet_. The Facebook Page username `disciplinequiet` was available and is fine, it is a separate namespace.
```
[paste the SCOPE BLOCK here if this is a new chat. Note: B1's handle is now to become @the.disciplinequiet]

TASK 2C. Chrome is signed in to Instagram as B1 (@disciplinequite) and can act as Page B2. Do only these:
1. B1 Instagram (web, Edit profile): username -> the.disciplinequiet (if taken: disciplinequiet.official, then disciplinequiet_; do not pick any other). Name -> "Quiet Discipline". Category -> "Education" (or "Personal blog" if not offered; tell me which).
2. Facebook Page A2 (ID 1345396148663682): Page category -> "Education" (or "Personal blog"). Do NOT start the name change; I will do it myself because it needs my password.
3. Facebook Page B2 (ID 1436529449539802): category -> "Education" (or "Personal blog").
4. Do not touch passwords, pictures, 2FA, roles, portfolios, or any other Page. Do not sign in to or switch to A1; I will do A1 on my phone.
End with the REPORT, with the final username, display name and category of B1, A2 and B2.
```

## MANUAL: do these on your phone (Claude chat could not, and some are security steps that should be yours)
1. **Two-factor on Instagram B1, and check A1:** Instagram app > Settings and activity > Accounts Center > Password and security > Two-factor authentication. Use an authenticator app. Save the backup codes offline. Do the same for the Facebook profile.
2. **Security Checkup on B1's Meta account:** work through the 3 recommended actions.
3. **Account Status for A1:** Instagram app > switch to @rozkarule > Settings and activity > Account status. Tell Claude Code what it says.
4. **Creator vs Business:** in the app, Settings and activity > Account type and tools. If an account says Business, tap Switch account type > Creator (Creator suits trending audio and our content; it is a judgement, not a Meta requirement). Report what each shows.
5. **Leave alone for now:** A1 is owned by the business portfolio "Quite Discipline" while A2 sits in "Roz ka Rule". Moving an Instagram account between portfolios means removing and re-claiming it, which can break the Page link. We test publishing first and only fix it if the API needs it.

## PROMPT 3: Meta developer account and app (do after Prompt 2 succeeds)
```
[paste the SCOPE BLOCK here]

TASK 3: META DEVELOPER APP. This is separate from the four assets, but you may only create ONE NEW app and nothing else. Do not touch any existing app or business.
1. Check whether I am already registered as a Meta developer (developers.facebook.com). If not, start registration at https://developers.facebook.com/async/registration and stop at any code or password step so I can do it.
2. Create ONE new app: Create App > use case "Other" > app type "Business" > name "Quotes Publisher" > my contact email. Skip connecting a business portfolio.
3. Add the Instagram product (Instagram > Set up) and choose "API setup with Facebook login" (NOT Instagram login).
4. Confirm the app is in Development mode and that I am Admin.
5. Do NOT read out, copy or display the App Secret. Tell me only where it is (App settings > Basic). Report the App ID only (it is not secret).
End with the REPORT.
```

## Steps that stay manual (no prompt)
- Generate the short-lived token in Graph API Explorer and run `pipeline/setup_tokens.py` on your Mac.
- Paste secrets into GitHub (Settings > Secrets and variables > Actions).
- Passwords, 2FA setup and recovery codes.

## How Claude Code uses the REPORT
Paste the REPORT into the Claude Code chat. I update `PROJECT.md`, fix files that depend on names or IDs, and write the next prompt or manual step.
