# CLAUDE.md: read this first (auto-loaded by Claude Code sessions)

Project: two faceless Instagram + Facebook pages run with Claude. State, decisions and next steps are in `PROJECT.md`. Owner answers and account reports go in `inbox/`. Account-level prompt pack: `docs/11-claude-chat-prompts.md`. Bridge notes: `docs/12-bridge-claude-chat.md`.

## Assets in scope (and nothing else)
- A1 Instagram `@rozkarule` (IG ID 17841469203264060); A2 Facebook Page "Roz Ka Rule" (ID 1345396148663682)
- B1 Instagram `@the.disciplinequiet` once renamed, currently `@disciplinequite` (IG ID 17841422691847840); B2 Facebook Page "Quiet Discipline" (ID 1436529449539802)

Anything else in the owner's Meta Business Suite (other Pages, accounts, businesses, ad accounts, catalogs, payments, roles, portfolios) is OUT OF SCOPE. Never open, edit or post to it.

## Hard rules
1. Never ask for, print, store or commit passwords, 2FA or backup codes, the App Secret, or access tokens. Tokens live only in GitHub Secrets. If a step needs one, stop and tell the owner to do it.
2. Ask the owner before: changing passwords/2FA/recovery, deleting or unlinking anything, spending money, accepting terms, changing roles or portfolios, or anything not in the task.
3. Official APIs only. No bots for likes/follows/comments. No new accounts. Posts are original text only; the AI flag is set on every post.
4. Posts publish only when `status: approved` (owner approves; first 30 days every post).
5. Money posts: educational only, no stock/crypto tips, no returns claims. Mental-health posts: no diagnosis, add the disclaimer.

## Writing rules
Easy to read: one idea per slide, body slides max 10 words, concrete examples, plain words, highlight key words with *asterisks*. Full rules in `docs/14-writing-style.md`.

## Who does what (two Claude Code sessions share this repo)
- **Claude Code "Market research for project" session (builder):** research, content, pipeline, workflows, reports. Branch `claude/eager-bell-i41n67` (the repo default branch).
- **Claude Code project "Static Automation" (operator, has the owner's browser/device):** account-level tasks from `docs/11-claude-chat-prompts.md`. It writes results as a file `inbox/YYYY-MM-DD-topic.md` using the REPORT format, commits and pushes (own branch is fine; the builder fetches all `claude/*` branches). It does not edit `pipeline/`, `content/` or `PROJECT.md`.
- Avoid edit collisions: one writer per folder. Builder owns everything except `inbox/`. Operator writes only `inbox/`.
- Before working: `git pull --rebase`. After finishing: commit and push.

## REPORT format (end every account task with this)
REPORT / task / done: yes|partly|no / assets touched (name or handle + ID) / what changed / what I could not do and why / current state of the four assets / anything unexpected or out of scope that I noticed but did NOT touch.
