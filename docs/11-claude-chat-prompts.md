# Claude Chat Prompt Pack (account-level tasks)

Working agreement: whenever an **account-level** change is needed, Claude Code writes a ready prompt here or in chat. The owner pastes it into a **new chat** in the Claude project "New Bot Planning". Each prompt is **self-contained** (it repeats the scope block), because a new chat has no memory. The owner pastes the REPORT block it returns back into Claude Code.

Why the scope block is strict: the chat has access to the whole Meta Business Suite, which contains other businesses, Pages, ad accounts and Instagram accounts that have nothing to do with this project. Those must never be touched.

I could not verify which tools the chat project has (browser control, Meta connector). Every prompt therefore says: do the step if you can, otherwise give click-by-click steps.

## SCOPE BLOCK (already included at the top of every prompt below)
```
SCOPE. This task concerns ONLY these four assets and nothing else:
  A1  Instagram account  @rozkarule
  A2  Facebook Page      "Roz Ka Rule"
  B1  Instagram account  @disciplinequite   (spelling is wrong on purpose here: it is the CURRENT handle; it will be renamed to @disciplinequiet)
  B2  Facebook Page      "Quite Discipline" or "Quiet Discipline" (whichever exists; the correct name is "Quiet Discipline")
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

## PROMPT 2: make the changes (paste after Prompt 1, in a new chat or the same one)
```
[paste the SCOPE BLOCK here]

TASK 2: SET UP THE FOUR ASSETS. Only change what is wrong. If an item is already correct, leave it and say so.
1. B1 Instagram: change username @disciplinequite to @disciplinequiet. If it is unavailable, do NOT pick another: tell me and list the closest free options.
2. B2 Facebook Page: name must be exactly "Quiet Discipline" (fix "Quite Discipline" if that is what it says). Set the Page username to disciplinequiet (if unavailable, tell me the options).
3. A1 and B1 must be Instagram CREATOR accounts. If either is Personal, switch it (Settings and activity > Account type and tools > Switch to professional account > category "Education" > Creator).
4. Link A1 to A2 and B1 to B2. Do not cross-link. If a link already exists to the wrong Page, STOP and ask me before unlinking.
5. Profile pictures: A1 and A2 use the attached page_a_profile.png. B1 and B2 use the attached page_b_profile.png. (I will attach both files.)
6. Bios and Page descriptions:
   A1 and A2: "Roz ka ek rule. Discipline, career aur dimaag ke liye simple tips. Save karo, follow karo."
   B1 and B2: "One small rule a day for discipline, focus and a calmer mind. Save what helps."
7. Confirm A1 and B1 are public.
8. Do NOT turn on or change two-factor, passwords, ads, payment, roles or anything else. If 2FA is off, only tell me.
End with the REPORT.
```

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
