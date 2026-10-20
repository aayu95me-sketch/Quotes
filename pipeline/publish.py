"""Publish approved, due carousel posts via the official Instagram Graph API.

Dry-run by default. Pass --live to actually publish. NOT yet tested against the live API:
the first live run must be on a test post on one of the owner's own accounts.

Env (live mode only):
  ASSETS_BASE_URL   public base URL where rendered slides are hosted,
                    e.g. https://<user>.github.io/<assets-repo>   (slides at <base>/<page>/<post>/slide_NN.png)
  IG_<PAGE>_USER_ID / IG_<PAGE>_TOKEN   e.g. IG_PAGE_A_USER_ID, IG_PAGE_A_TOKEN
  GRAPH_VERSION     optional, default v21.0 (check Meta docs for the current version)

Flow per carousel: one child container per image (is_carousel_item=true) -> parent
container (media_type=CAROUSEL, children=ids, caption) -> media_publish.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRAPH = "https://graph.facebook.com"


def api(method, path, params, version):
    url = f"{GRAPH}/{version}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data if method == "POST" else None, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def due_posts(now):
    for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
        post = json.loads(f.read_text())
        if post.get("status") != "approved":
            continue
        if dt.datetime.fromisoformat(post["publish_at"]) <= now:
            yield f, post


def publish_carousel(post, stem, live):
    page = post["page"]
    base = os.environ.get("ASSETS_BASE_URL", "https://example.invalid")
    urls = [f"{base}/{page}/{stem}/slide_{i:02d}.png" for i in range(1, len(post["slides"]) + 1)]
    if not live:
        print(f"[dry-run] {page}/{stem}: {len(urls)} slides, caption {len(post['caption'])} chars")
        return None
    key = page.upper()
    uid, token = os.environ[f"IG_{key}_USER_ID"], os.environ[f"IG_{key}_TOKEN"]
    ver = os.environ.get("GRAPH_VERSION", "v21.0")
    kids = []
    for u in urls:
        kids.append(api("POST", f"{uid}/media", {"image_url": u, "is_carousel_item": "true", "access_token": token}, ver)["id"])
    parent = api("POST", f"{uid}/media", {
        "media_type": "CAROUSEL", "children": ",".join(kids),
        "caption": post["caption"], "access_token": token}, ver)["id"]
    for _ in range(12):  # wait for processing
        st = api("GET", parent, {"fields": "status_code", "access_token": token}, ver)
        if st.get("status_code") == "FINISHED":
            break
        time.sleep(5)
    return api("POST", f"{uid}/media_publish", {"creation_id": parent, "access_token": token}, ver)["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    n = 0
    for f, post in due_posts(now):
        if post["type"] != "carousel":
            print(f"skip {f.name}: type {post['type']} not supported yet")
            continue
        media_id = publish_carousel(post, f.stem, a.live)
        if a.live and media_id:
            post["status"] = "published"
            post["media_id"] = media_id
            f.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
        n += 1
    print(f"{n} post(s) processed ({'live' if a.live else 'dry-run'})")


if __name__ == "__main__":
    main()
