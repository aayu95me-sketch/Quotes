"""Run this ON YOUR OWN COMPUTER (not in chat). It turns a short-lived Graph API Explorer token into
a long-lived, non-expiring Page token and finds your Instagram user ID. Output stays in your terminal.

  python3 pipeline/setup_tokens.py

You will be prompted (input hidden) for: App ID, App Secret, short-lived user token.
Nothing is written to disk. Copy the printed values into GitHub: repo > Settings > Secrets and variables > Actions.
"""
import getpass
import json
import urllib.error
import urllib.parse
import urllib.request

V = "v26.0"
KNOWN_PAGE_IDS = ["1345396148663682", "1436529449539802"]  # A2 "Roz Ka Rule", B2 "Quiet Discipline"


def get(path, **params):
    url = f"https://graph.facebook.com/{V}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Graph API error {e.code}: {e.read().decode()[:300]}")


app_id = input("App ID: ").strip()
secret = getpass.getpass("App Secret (hidden): ").strip()
short = getpass.getpass("Short-lived user token from Graph API Explorer (hidden): ").strip()

ll = get("oauth/access_token", grant_type="fb_exchange_token", client_id=app_id, client_secret=secret, fb_exchange_token=short)
user_token = ll["access_token"]
print(f"\nLong-lived user token obtained (valid about {ll.get('expires_in', 0) // 86400} days). Fetching your Pages...\n")
FIELDS = "name,id,access_token,instagram_business_account{id,username}"
perms = get("me/permissions", access_token=user_token).get("data", [])
print("Permissions granted :", ", ".join(sorted(x["permission"] for x in perms if x["status"] == "granted")) or "(none)")
print("Permissions declined:", ", ".join(sorted(x["permission"] for x in perms if x["status"] != "granted")) or "(none)")
pages = get("me/accounts", access_token=user_token, fields=FIELDS, limit=50)["data"]
if not pages:
    # Pages owned by a business portfolio can be missing from /me/accounts. Ask for the two known Pages directly.
    print("\n/me/accounts returned nothing. Trying the two known Page IDs directly...")
    for pid in KNOWN_PAGE_IDS:
        try:
            url = f"https://graph.facebook.com/{V}/{pid}?" + urllib.parse.urlencode({"fields": FIELDS, "access_token": user_token})
            with urllib.request.urlopen(url, timeout=30) as r:
                d = json.loads(r.read())
            if d.get("access_token"):
                pages.append(d)
            else:
                print(f"  Page {pid}: readable but no Page token returned (you need full control of the Page and the pages_show_list / business_management permissions).")
        except urllib.error.HTTPError as e:
            print(f"  Page {pid}: Graph API error {e.code}: {e.read().decode()[:200]}")
if not pages:
    raise SystemExit("No Pages found. In Graph API Explorer add business_management and pages_show_list, click Generate Access Token again, "
                     "and in the Facebook dialog select BOTH Pages and BOTH Instagram accounts. Then rerun.")
for p in pages:
    ig = p.get("instagram_business_account")
    print("=" * 60)
    print("Facebook Page :", p["name"], f"(id {p['id']})")
    if not ig:
        print("  No Instagram account linked to this Page.")
        continue
    print("Instagram     :", "@" + ig.get("username", "?"), f"(IG user id {ig['id']})")
    print("  -> secret IG_<PAGE>_USER_ID =", ig["id"])
    print("  -> secret IG_<PAGE>_TOKEN   =", p["access_token"], "(long-lived Page token; keep private)")
print("\nPaste these into GitHub Secrets only. Do not paste them into chat, email or screenshots.")
