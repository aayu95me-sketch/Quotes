# REPORT: Prompt 3 (Meta developer app "Quotes Publisher")

- **task:** Prompt 3 from docs/11-claude-chat-prompts.md (developer registration + ONE new app)
- **done:** yes
- **assets touched:** none of A1/A2/B1/B2. Only the owner's Meta for Developers registration and the one new app.
- **what changed:**
  1. Owner was not yet a registered Meta developer. I filled the "About you" step (Owner/founder). The owner pressed Complete Registration (terms).
  2. Create App > use case "Other" > type "Business" > name "Quotes Publisher", no business portfolio. The owner pressed Create app.
  3. Added the Instagram product and opened "API setup with Facebook login" (not Instagram login). Nothing further configured there: no Facebook Login for Business setup, no webhooks, no app review, no accounts added.
  4. Verified: App Mode = **Development**; App roles > Roles shows Ayush Sharma as **Administrator** (only person on the app).
- **App ID:** `1454446477743438`
- **App Secret:** not read, copied or shown. It is under App settings > Basic. Adding Instagram also created an Instagram-login app secret on the "API setup with Instagram login" page, which I also did not reveal.
- **what I could not do and why:** Complete Registration and Create app were pressed by the owner because they accept Meta terms.
- **current state of the four assets:** unchanged by this task.
- **unexpected / out of scope:** (a) The app contact email was prefilled with a different Gmail address (from the owner's Facebook account) than the one used with Claude. Change it in App settings > Basic if unwanted. (b) The "Other" use case is flagged by Meta as "going away soon", so this app uses the old-style product experience.
- **next (manual, owner):** Graph API Explorer token and `pipeline/setup_tokens.py`; secrets into GitHub Secrets.
