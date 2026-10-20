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
