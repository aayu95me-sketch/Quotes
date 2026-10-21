"""One-off setup check run in GitHub Actions. Prints PASS/FAIL per check. Never prints tokens or secrets.

Checks per page: Instagram user readable, publishing quota readable, trending-audio search works.
Also checks the slide-hosting repo and token. Needs the IG_* secrets and ASSETS_REPO / ASSETS_PAT.
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

V = os.environ.get("GRAPH_VERSION", "v26.0")


def get(url, headers=None):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=40) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {}


def graph(path, token, **params):
    params["access_token"] = token
    return get(f"https://graph.facebook.com/{V}/{path}?" + urllib.parse.urlencode(params))


def line(ok, msg):
    print(("PASS  " if ok else "FAIL  ") + msg)
    return ok


all_ok = True
for page in ("PAGE_A", "PAGE_B"):
    uid, tok = os.environ.get(f"IG_{page}_USER_ID", ""), os.environ.get(f"IG_{page}_TOKEN", "")
    if not uid or not tok:
        all_ok &= line(False, f"{page}: secrets IG_{page}_USER_ID / IG_{page}_TOKEN missing")
        continue
    s, d = graph(uid, tok, fields="username,name,followers_count,media_count")
    all_ok &= line(s == 200 and "username" in d, f"{page}: Instagram account readable -> @{d.get('username')} (id {uid}, name {d.get('name')}, media {d.get('media_count')})" if s == 200 else f"{page}: Instagram account NOT readable: {d.get('error', {}).get('message', s)}")
    s, d = graph(f"{uid}/content_publishing_limit", tok, fields="quota_usage,config")
    all_ok &= line(s == 200, f"{page}: publishing limit readable -> {d.get('data')}" if s == 200 else f"{page}: publishing limit NOT readable: {d.get('error', {}).get('message', s)}")
    s, d = graph("ig_audio", tok, audio_type="music", user_id=uid)
    n = len(d.get("audio", [])) if s == 200 else 0
    all_ok &= line(s == 200 and n > 0, f"{page}: trending audio search returned {n} tracks" if s == 200 else f"{page}: Audio API NOT available: {d.get('error', {}).get('message', s)}")

repo, pat = os.environ.get("ASSETS_REPO", ""), os.environ.get("ASSETS_PAT", "")
if repo and pat:
    s, d = get(f"https://api.github.com/repos/{repo}", {"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json"})
    all_ok &= line(s == 200 and d.get("private") is False, f"slides repo {repo}: reachable, public={not d.get('private', True)}, push permission={d.get('permissions', {}).get('push')}" if s == 200 else f"slides repo {repo}: NOT reachable ({s})")
else:
    all_ok &= line(False, "ASSETS_REPO variable or ASSETS_PAT secret missing")
print("\nRESULT:", "ALL CHECKS PASSED" if all_ok else "SOME CHECKS FAILED")
