"""Run this ON YOUR OWN COMPUTER (not in chat). It turns a short-lived Graph API Explorer token into
a long-lived, non-expiring Page token and finds your Instagram user ID. Output stays in your terminal.

  python3 pipeline/setup_tokens.py

You will be prompted (input hidden) for: App ID, App Secret, short-lived user token.
Nothing is written to disk. Copy the printed values into GitHub: repo > Settings > Secrets and variables > Actions.
"""
import getpass
import json
import urllib.parse
import urllib.request

V = "v26.0"


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
pages = get("me/accounts", access_token=user_token, fields="name,id,access_token,instagram_business_account{id,username}", limit=50)["data"]
if not pages:
    raise SystemExit("No Pages found. Check the token has pages_show_list and that you are an admin of the Pages.")
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
