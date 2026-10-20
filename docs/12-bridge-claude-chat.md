# Bridge between Claude Code (this repo) and the Claude chat project "static automation"

Fact: Claude Code runs in a cloud container and has no tool that opens claude.ai chats or projects. Claude chat cannot see this container. They only share things that **both** can reach: the GitHub repo, Google Drive/Docs (if the chat has that connector), and what the owner pastes.

## Options
| Option | Direction | Setup | Limits |
|---|---|---|---|
| **A. Repo as the shared brain** (recommended base) | Chat reads the repo; Claude Code reads and writes it | In the chat project: Add content > GitHub, pick only `aayu95me-sketch/Quotes` (branch `claude/eager-bell-i41n67`, later `main`). Re-sync when files change. | Chat's copy is a snapshot; the chat cannot push to the repo (do not give it write access) |
| **B. Shared Google Doc as a mailbox** | Both read and write | One doc "Claude Bridge" in the owner's Drive; Claude Code reads and writes it through its Drive tools; the chat uses its Drive connector | Works only if the chat can write to Drive (unverified; many setups are read-only) |
| **C. Share link of a chat** | Chat to Claude Code, one way | Owner shares the chat (Share button) and sends the link; the research relay fetches it | Snapshot only; the chat page may be JS-rendered; the content lands in the private repo |
| **D. Copy and paste a REPORT** | Both ways, manual | Works today | Manual, but the most reliable |

Recommended: **A for reading, D for reporting back**, and try **B** if the capability test shows the chat can write to Drive.

## Capability test (paste into the new chat, answer comes back to Claude Code)
```
Please answer these plainly, without doing anything yet. Do not change anything.
1. Which connectors or tools do you have in this project (Meta/Facebook, Instagram, Google Drive, Gmail, GitHub, browser or computer control, file upload, anything else)?
2. For each: read-only or can it write/edit?
3. Can you create or edit a Google Doc or Drive file? Can you read a GitHub repository added as project knowledge?
4. Can you upload a file from the chat to a website in the browser (for example a profile picture)? 
5. Can you see the "New Bot Planning" project chats from here? (yes/no only)
```

## Instructions text for the project "static automation" (paste into Project instructions)
```
This project supports a content business with two Instagram + Facebook Page pairs. Source of truth is the GitHub repo aayu95me-sketch/Quotes (PROJECT.md first, then docs/11-claude-chat-prompts.md).
Assets in scope, and nothing else in my Business Suite:
  A1 Instagram @rozkarule (IG ID 17841469203264060); A2 Facebook Page "Roz Ka Rule" (ID 1345396148663682)
  B1 Instagram @the.disciplinequiet or its current handle (IG ID 17841422691847840); B2 Facebook Page "Quiet Discipline" (ID 1436529449539802)
Rules: never ask for or show passwords, 2FA codes, App Secret or access tokens. Never touch other Pages, accounts, businesses, ad accounts, payments, roles or portfolios. Ask me before any change not listed in the task prompt. Finish every task with the REPORT format from the repo. Prompts for account-level tasks come from Claude Code (the coding assistant that works on the repo); do exactly what the prompt says.
```

---
# Step-by-step: getting both in sync (written 2026-10-20)

## Blocker to know about
The repo's default branch `main` only contains the first README. All the work is on `claude/eager-bell-i41n67`. If the chat project syncs `main`, it will see almost nothing. Fix, pick one: (1) ask Claude Code to open and merge a pull request into `main` (recommended; it also activates the scheduled GitHub jobs, which stay in dry-run until `LIVE_PUBLISH=true`); or (2) in GitHub: repo > Settings > Branches > change the default branch to `claude/eager-bell-i41n67`.

## Steps
1. **Decide the branch** (see above). Tell Claude Code "merge to main" or change the default branch yourself.
2. **Connect the repo to the chat project:** claude.ai > project "static automation" > Project knowledge > + > GitHub > authorise GitHub for **only** the repo `aayu95me-sketch/Quotes` > select the default branch > add the whole repo (the files `PROJECT.md`, `docs/`, `content/`, `pipeline/`). Read-only. After Claude Code pushes big changes, press the sync/refresh icon next to the repo.
3. **Paste the project instructions** (above) into Project instructions.
4. **Run the capability test** (above) and paste the answer to Claude Code.
5. **Run Prompt S1** (below) so the chat reads the repo and explains it. Paste its SYNC NOTE to Claude Code.
6. **Claude Code reads the chat's side** from what you paste (SYNC NOTE or REPORT) or from a share link of the chat. Claude Code explains it back to you and updates `PROJECT.md`.
7. **Optional upgrade:** if the capability test shows the chat can write to Google Drive or Claude Docs, Claude Code creates a shared "Claude Bridge" doc and both sides use it as a mailbox.

## Routine after setup
- After any chat task: paste the REPORT to Claude Code.
- After any Claude Code session: Claude Code updates `PROJECT.md` ("Last sync" line) and tells you to press re-sync in the project.
- Weekly: Prompt S2 in the chat, to turn the week's repo state into a short approval summary on your phone.

## Prompt S1: chat reads and explains the repo (paste in "static automation")
```
Read the project knowledge (the GitHub repo). Start with PROJECT.md, then docs/11-claude-chat-prompts.md, docs/12-bridge-claude-chat.md and docs/08-account-setup-guide.md.
Then explain to me in plain English, in under 400 words:
1. What this project is and what the goal is.
2. What has been built and what state each of the four assets (A1, A2, B1, B2) is in according to the repo.
3. What I (the owner) still have to do, in order.
4. What Claude Code is doing and what it needs from me.
5. Anything in the repo that contradicts what you can see in my accounts, or anything you do not understand.
Do not change anything and do not touch any account. End with:
SYNC NOTE
repo state read: <date of the most recent commit you can see, and branch>
what I understood: <3 bullets>
what I need from Claude Code: <bullets, or none>
what Claude Code should know from my side: <bullets, or none>
```

## Prompt S2: weekly approval summary (paste in "static automation")
```
Read the latest PROJECT.md and the draft posts in content/posts/ (status "draft"). For the coming week, list each post as: date, page, type (carousel or reel), first-slide text, language, and whether it contains a disclaimer where needed. Flag anything that looks wrong, risky or repetitive. Do not approve anything. I will tell Claude Code which posts to approve.
```
