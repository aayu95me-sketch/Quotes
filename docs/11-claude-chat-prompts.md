# Claude Chat Prompt Pack (account-level tasks)

Working agreement: whenever an **account-level** change is needed (rename, link, switch type, create an app, change a setting), Claude Code writes a ready prompt here or in chat. The owner pastes it into the Claude chat project "New Bot Planning", Claude chat does the step if its connectors or browser tools allow it, and the owner pastes the **REPORT** block back to Claude Code.

What I could not verify: which tools the chat project really has (browser control, Meta connector, etc.). Every prompt therefore says: do it if you can, otherwise give the owner click-by-click steps.

## Master prompt (paste once as the project's instructions or first message)
```
You are helping set up two Instagram + Facebook Page pairs for a content project.
Page A: Instagram @rozkarule, Facebook Page "Roz Ka Rule".
Page B: Instagram @disciplinequiet, Facebook Page "Quiet Discipline".
All accounts belong to me (the owner). Work ONLY on these four assets.

Rules:
1. Do the step yourself if you have a working tool for it. If not, give me short click-by-click steps for my phone or laptop. Say which one you are doing.
2. NEVER ask me to paste passwords, 2FA codes, backup codes, App Secrets or access tokens into this chat, and never display them if you see them. If a step needs one, stop and tell me to do that part myself.
3. Stop and ask me before: changing a password, 2FA or recovery email; deleting or merging anything; spending money; accepting new terms; or anything not listed in the task.
4. Do not follow, like, comment or post anything. Do not create any other accounts.
5. If a screen differs from the instructions, describe exactly what you see instead of guessing.
6. Finish every task with a REPORT in this format:
   REPORT
   task: <name>
   done: <yes / partly / no>
   what changed: <list>
   what I could not do and why: <list>
   current state (usernames, page names, account types, linked or not): <list>
   screenshots or errors worth showing Claude Code: <list>
```

## Task prompts

### T1. Fix the Page B username (Instagram and Facebook)
```
Task T1. Change the Page B username spelling from "disciplinequite" to "disciplinequiet".
1. Instagram account (currently @disciplinequite): Edit profile > Username > disciplinequiet.
2. Facebook Page "Quiet Discipline": Page settings > Page info (or Edit Page info) > Username > disciplinequiet.
If either name is unavailable, do not pick another. Tell me and list the closest free options (for example disciplinequiet.co, disciplinequiet_daily).
Also check that the Facebook Page NAME is spelled "Quiet Discipline". End with the REPORT.
```

### T2. Verify the Phase 1 state of all four assets (read-only check)
```
Task T2. Check, and only report (change nothing), for each of the four assets:
- Instagram account type: Personal / Creator / Business.
- Is each Instagram account linked to the Facebook Page with the same brand? (A to A, B to B, not crossed.)
- Is two-factor authentication ON? (yes/no only. Never show codes.)
- Profile picture and bio present? Is the account public?
- Any warnings in Account Status (Settings > Account status), or limits on recommendations?
End with the REPORT.
```

### T3. Switch to Creator and link the Page (if T2 shows it is missing)
```
Task T3. For each Instagram account that is not yet a professional account, switch it to a CREATOR account (Settings and activity > Account type and tools > Switch to professional account > pick a category such as Education > Creator).
Then link each Instagram account to its OWN Facebook Page (Page A to "Roz Ka Rule", Page B to "Quiet Discipline"). Do not cross-link.
If Instagram asks to log in to Facebook or approve something, stop and tell me.
End with the REPORT.
```

### T4. Profile picture and bio
Upload the images from the repo's `brand/` folder to the chat (page_a_profile.png, page_b_profile.png).
```
Task T4. Set profile pictures and bios.
Page A (Instagram @rozkarule and Facebook "Roz Ka Rule"): use the attached page_a_profile.png.
  Instagram bio: Roz ka ek rule. Discipline, career aur dimaag ke liye simple tips. Save karo, follow karo.
Page B (Instagram @disciplinequiet and Facebook "Quiet Discipline"): use the attached page_b_profile.png.
  Instagram bio: One small rule a day for discipline, focus and a calmer mind. Save what helps.
Use the same picture on the Facebook Page. Add a short Facebook Page description with the same sentence as the bio. End with the REPORT.
```

### T5. Meta developer account and app (Phase 2, steps 1-5)
```
Task T5. Do these in order, stopping where a step needs my password, a code or my App Secret:
1. Register as a Meta developer at https://developers.facebook.com/async/registration with my personal Facebook account (I will enter any code sent to my phone or email).
2. In the App Dashboard: Create App > use case "Other" > app type "Business" > name "Quotes Publisher" > my contact email > Create. Skip connecting a business portfolio.
3. Add the Instagram product: Instagram > Set up > choose "API setup with Facebook login" (NOT the Instagram login option).
4. Confirm the app is in Development mode and that I have the Admin role.
5. Tell me where to find the App ID and App Secret (App settings > Basic). Do NOT read the App Secret out loud or put it in your reply. I will copy it myself.
End with the REPORT, including the App ID only (the App ID is not secret).
```

### Steps that stay manual (no prompt, do these yourself)
- Generate the short-lived token in Graph API Explorer and run `pipeline/setup_tokens.py` on your Mac.
- Paste secrets into GitHub (Settings > Secrets and variables > Actions).
- Passwords, 2FA setup and recovery codes.

## How Claude Code uses the REPORT
Paste the REPORT into the Claude Code chat. I update `PROJECT.md`, fix any file that depends on names or IDs, and write the next prompt (or the next manual step).
