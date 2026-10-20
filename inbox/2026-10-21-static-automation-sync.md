# Static Automation sync (2026-10-21)

Written by the Static Automation operator session after reading `CLAUDE.md`, `PROJECT.md` and `docs/11-claude-chat-prompts.md`. No account was opened or changed.

## 1. The project in plain English

**What it is.** Two faceless pages that post original, designed text carousels and static-image Reels: **Roz Ka Rule** (India, Hinglish and English: A1 Instagram @rozkarule, A2 Facebook Page) and **Quiet Discipline** (US/UK/CA/AU, English: B1 Instagram @disciplinequite, B2 Facebook Page). Claude writes and renders the posts; GitHub Actions publishes them through Meta's official API once you approve each one. Budget is ₹0. Income should come later from affiliates, own products, sponsors and an email/WhatsApp list.

**What is done.** Research, brand, profile images, and week 1 content (20 draft posts, 27 Oct to 2 Nov). The pipeline (render, Reels, approval, publisher, audio, research relay) is built and tested, but nothing has gone live. The read-only audit confirmed all four assets and their links. Bios are set on B1, A2 and B2.

**What you must do next.**
1. Facebook name changes in Chrome (need your password): A2 to "Roz Ka Rule", B2 to "Quiet Discipline", B2 username `disciplinequiet`. Spelling must be exact (60-day lock).
2. Upload the profile pictures on all four.
3. On your phone: 2FA on B1 (and check A1), Security Checkup, A1 Account Status, A1 name and bio, Creator vs Business.
4. Rename B1 to @the.disciplinequiet (plain @disciplinequiet is taken).
5. Then 3 to 5 days of warm-up, Phase 2 (developer app, tokens into GitHub Secrets), approve week 1, and one live test post.

**What I (the operator) do.** Account-level tasks from `docs/11` (Prompts 2B, 2C, 3), only on the four assets, only when you ask. I never handle passwords, 2FA codes or tokens. I write each result to `inbox/` in the REPORT format and push it. I do not edit `pipeline/`, `content/` or `PROJECT.md`; the builder session owns those.

## 2. Tools in this project

| Tool | What it can do here | Read-only? |
|---|---|---|
| git + GitHub (repo `aayu95me-sketch/Quotes` only) | Read the repo, commit and push to `claude/*` branches | No (read and write); I write only `inbox/` |
| Chrome control (your Mac, "Browser 1") | Open pages, click, type, read pages | No. Its Instagram is signed in as @disciplinequite, so A1 is not reachable. Not used for this task |
| File upload in the browser | An image-upload tool exists, but it failed to upload the profile pictures in the earlier audit | Effectively unavailable; you upload pictures |
| Your Mac's folders and screen | Two folders listed (`~/claude-test`, `~/Downloads`), neither approved yet; screen control tools also present | Not used; would need your approval |
| Meta connector ("Meta traffic agent") | Ads only: list Pages/IG/ad accounts, boost, create ads | Has write tools, but I treat it as read-only. It cannot rename accounts or publish organic posts. Not used |
| Project shared folder and file attachments | Send you files, copy files to your Mac once a folder is approved | Read and write |
| Make, Gmail, Google Drive, Google Sheets | Connected but not part of this project | Not used |
| Zapier | Failed to connect this session | Unavailable |

---

REPORT
task: Read CLAUDE.md, PROJECT.md and docs/11; explain the project, next steps and operator role; list available tools; write this file, commit, push. No account changes.
done: yes
assets touched (handle or name + ID): none
what changed: added `inbox/2026-10-21-static-automation-sync.md` (this file). Nothing else.
what I could not do and why: nothing in scope was blocked. Pushed to the operator branch `claude/project-thread-stzy0k` (this session's assigned branch; CLAUDE.md allows an own branch and the builder fetches all `claude/*` branches), not to the default branch.
current state of the four assets (from the earlier audit and project memory, not re-checked today):
- A1 IG @rozkarule, ID 17841469203264060: Professional (Creator vs Business unconfirmed), linked to A2, 2FA unknown. Not reachable from Chrome (signed in as B1). No bio or picture yet. Owned by portfolio "Quite Discipline" (left alone on purpose).
- A2 Page "Rozkarule", ID 1345396148663682: linked to A1, bio set, rename to "Roz Ka Rule" waiting on your password, no picture yet.
- B1 IG @disciplinequite, ID 17841422691847840: Professional (looks Business), linked to B2, 2FA OFF, bio set. Username unchanged because @disciplinequiet is taken; planned @the.disciplinequiet. No picture yet.
- B2 Page "Quietdiscipline", ID 1436529449539802: linked to B1, bio set, name "Quiet Discipline" and username `disciplinequiet` waiting on your password, no picture yet.
anything unexpected or outside scope that I noticed but did NOT touch:
- `origin/main` now exists (single "Initial commit"); the working default per CLAUDE.md is still `claude/eager-bell-i41n67`.
- Docs still mention two different B1 handle targets: `docs/11` scope block says "@disciplinequiet.official", PROJECT.md and CLAUDE.md say "@the.disciplinequiet". Builder should align.
- Still open from the audit: two unidentified "Quiet Discipline" entries with full access on B2 (Prompt 2B), category "Art" on the Instagram accounts.
- Several connectors failed to connect (Zapier and others); not needed for this project.
