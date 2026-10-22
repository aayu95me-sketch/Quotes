"""Publish approved, due carousel posts via the official Instagram Graph API.

Handles carousels and static-image Reels (trending, mood-matched audio via the Audio API).
Dry-run by default. Pass --live to actually publish. NOT yet tested against the live API:
the first live run must be a test post on one of the owner's own accounts.

Env (live mode only):
  ASSETS_REPO       public repo "owner/name" used to host slide images (raw.githubusercontent.com URLs)
  ASSETS_PAT        fine-grained token with Contents:write on ASSETS_REPO only
  IG_<PAGE>_USER_ID / IG_<PAGE>_TOKEN   e.g. IG_PAGE_A_USER_ID, IG_PAGE_A_TOKEN (long-lived Page token)
  GRAPH_VERSION     optional, default v26.0 (latest per Meta docs, Jun 2026)

Meta docs (checked 2026-10-20): limit 100 API posts per rolling 24h (carousel = 1), up to 20 items per carousel;
no publish_time parameter, so scheduling is done by our own cron (GitHub Actions).
Flow per carousel: one child container per image (is_carousel_item=true) -> parent
container (media_type=CAROUSEL, children=ids, caption, is_ai_generated on the parent only) -> media_publish.
Slides are rendered and uploaded just before publishing, so nothing is public until it is due.
"""
import argparse
import base64
import datetime as dt
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
GRAPH = "https://graph.facebook.com"
MAX_LATE = dt.timedelta(hours=24)  # never publish something that is more than a day overdue
MAX_PER_RUN = 3


def api(method, path, params, version):
    url = f"{GRAPH}/{version}/{path}"
    data = urllib.parse.urlencode(params).encode() if method == "POST" else None
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Graph API {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")


def upload_assets(paths, page, stem):
    """Push rendered PNGs to the public assets repo; return their raw URLs."""
    repo, pat = os.environ["ASSETS_REPO"], os.environ["ASSETS_PAT"]
    urls = []
    for p in paths:
        rel = f"{page}/{stem}/{p.name}"
        api_url = f"https://api.github.com/repos/{repo}/contents/{rel}"
        hdr = {"Authorization": f"Bearer {pat}", "Accept": "application/vnd.github+json"}
        body = {"message": f"slide {rel}", "content": base64.b64encode(p.read_bytes()).decode()}
        try:  # overwrite if it already exists
            with urllib.request.urlopen(urllib.request.Request(api_url, headers=hdr), timeout=30) as r:
                body["sha"] = json.loads(r.read())["sha"]
        except urllib.error.HTTPError:
            pass
        req = urllib.request.Request(api_url, data=json.dumps(body).encode(), headers=hdr, method="PUT")
        urllib.request.urlopen(req, timeout=60).read()
        urls.append(f"https://raw.githubusercontent.com/{repo}/main/{rel}")
    for u in urls:  # wait until each URL is actually reachable
        for _ in range(10):
            try:
                urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=15)
                break
            except Exception:
                time.sleep(3)
    return urls


def due_posts(now):
    for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
        post = json.loads(f.read_text())
        if post.get("status") != "approved":
            continue
        when = dt.datetime.fromisoformat(post["publish_at"])
        if when > now:
            continue
        if now - when > MAX_LATE:
            print(f"skip {f.name}: more than 24h overdue, reschedule it")
            continue
        yield f, post


def publish_carousel(f, post, live, prepare=False):
    page, stem = post["page"], f.stem
    n = len(post["slides"])
    if not live:
        print(f"[dry-run] {page}/{stem}: {n} slides, caption {len(post['caption'])} chars, ai_label={post.get('ai_label')}")
        return None
    from render import render
    paths = render(f, ROOT / "out")
    urls = upload_assets(paths, page, stem)
    key = page.upper()
    uid, token = os.environ[f"IG_{key}_USER_ID"], os.environ[f"IG_{key}_TOKEN"]
    ver = os.environ.get("GRAPH_VERSION", "v26.0")
    kids = [api("POST", f"{uid}/media", {"image_url": u, "is_carousel_item": "true", "access_token": token}, ver)["id"] for u in urls]
    params = {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": post["caption"], "access_token": token}
    if post.get("ai_label"):  # self-disclosure; carousel container only, not children
        params["is_ai_generated"] = "true"
    parent = api("POST", f"{uid}/media", params, ver)["id"]
    status = None
    for _ in range(20):  # wait for processing
        status = api("GET", parent, {"fields": "status_code", "access_token": token}, ver).get("status_code")
        if status == "FINISHED":
            break
        time.sleep(5)
    if prepare:  # dry end-to-end test: everything except the final publish
        print(f"PREPARED carousel {page}/{stem}: parent container {parent}, {len(kids)} children, status {status}")
        return None
    return api("POST", f"{uid}/media_publish", {"creation_id": parent, "access_token": token}, ver)["id"]


def rupload(container_id, mp4, token, ver):
    """Resumable upload of a local video to Meta (rupload.facebook.com), as documented for Reels."""
    data = pathlib.Path(mp4).read_bytes()
    req = urllib.request.Request(f"https://rupload.facebook.com/ig-api-upload/{ver}/{container_id}", data=data, method="POST",
                                 headers={"Authorization": f"OAuth {token}", "offset": "0", "file_size": str(len(data))})
    try:
        out = json.loads(urllib.request.urlopen(req, timeout=300).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"rupload {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    if not out.get("success"):
        raise RuntimeError(f"rupload failed: {out}")


def publish_reel(f, post, live, prepare=False):
    """Static-image Reel: render 9:16 slides, build a silent slideshow mp4, attach trending mood-matched audio."""
    page, stem = post["page"], f.stem
    per = float(post.get("seconds_each", 3.5))
    if not live:
        print(f"[dry-run] {page}/{stem}: reel, {len(post['slides'])} slides x {per}s, mood={post.get('mood')}, "
              f"audio_id={post.get('audio_id', 'auto-pick at publish time')}")
        return None
    from render import render
    from reel import build_slideshow
    import audio as audio_mod
    paths = render(f, ROOT / "out")
    mp4 = str(ROOT / "out" / page / f"{stem}.mp4")
    build_slideshow([str(x) for x in paths], mp4, per)
    key = page.upper()
    uid, token = os.environ[f"IG_{key}_USER_ID"], os.environ[f"IG_{key}_TOKEN"]
    ver = os.environ.get("GRAPH_VERSION", "v26.0")
    params = {"media_type": "REELS", "upload_type": "resumable", "caption": post["caption"], "access_token": token}
    if post.get("ai_label"):
        params["is_ai_generated"] = "true"
    chosen, vol = None, audio_mod.mood_cfg(page, post.get("mood", "focus"))["volume"]
    try:
        if post.get("audio_id"):
            chosen = {"audio_id": post["audio_id"]}
        else:
            chosen, vol = audio_mod.pick(page, post.get("mood", "focus"), uid, token, ver,
                                         post.get("audio_type", "music"), per * len(post["slides"]),
                                         post.get("audio_queries", []))
    except Exception as e:  # audio failure should not block the post; publish silent and note it
        print(f"WARN audio lookup failed ({e}); publishing without audio")
    if chosen:
        params["audio_configuration"] = json.dumps({"audio_id": chosen["audio_id"], "audio_volume": int(post.get("audio_volume", 80)), "video_volume": 1})  # docs: both 1-100; 0 is out of range
    cid = api("POST", f"{uid}/media", params, ver)["id"]
    rupload(cid, mp4, token, ver)
    st = None
    for _ in range(40):
        st = api("GET", cid, {"fields": "status_code", "access_token": token}, ver).get("status_code")
        if st == "FINISHED":
            break
        if st == "ERROR":
            raise RuntimeError("Reel processing failed")
        time.sleep(6)
    if prepare:
        print(f"PREPARED reel {page}/{stem}: container {cid}, status {st}, audio {chosen.get('title') if chosen else 'none'} ({chosen.get('audio_id') if chosen else '-'})")
        return None
    mid = api("POST", f"{uid}/media_publish", {"creation_id": cid, "access_token": token}, ver)["id"]
    if chosen and chosen.get("title"):
        audio_mod.record_use(page, chosen)
        post["audio_used"] = {k: chosen.get(k) for k in ("audio_id", "title", "display_artist")}
    return mid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--count", action="store_true", help="print the number of approved, due posts and exit (cheap check for CI)")
    ap.add_argument("--prepare-only", action="store_true", help="live API test: build containers (carousel children, reel upload with audio) but do NOT publish")
    ap.add_argument("--only", nargs="*", help="with --prepare-only: post files to test regardless of status and date")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    if a.count:
        print(sum(1 for _ in due_posts(now)))
        return
    n = 0
    if a.only and not a.prepare_only:
        sys.exit("--only is only allowed together with --prepare-only (it must never publish)")
    queue = [(pathlib.Path(x), json.loads(pathlib.Path(x).read_text())) for x in a.only] if a.only else due_posts(now)
    live = a.live or a.prepare_only
    for f, post in queue:
        if n >= MAX_PER_RUN and not a.only:
            break
        if post["type"] not in ("carousel", "reel"):
            print(f"skip {f.name}: type {post['type']} not supported yet")
            continue
        try:
            media_id = (publish_reel if post["type"] == "reel" else publish_carousel)(f, post, live, a.prepare_only)
        except Exception as e:  # never crash the whole run; record and move on
            print(f"ERROR {f.name}: {e}")
            if any(k in str(e) for k in ("OAuthException", "access blocked", "Error validating access token", "Cannot call API")):
                print("AUTH PROBLEM: stopping this run; posts stay approved and will retry once tokens/app access are fixed")
                break
            if a.live and not a.prepare_only:
                post["status"] = "failed"
                post["error"] = str(e)[:300]
                f.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
            continue
        if a.live and not a.prepare_only and media_id:
            post["status"] = "published"
            post["media_id"] = media_id
            post["published_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            f.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
        n += 1
    print(f"{n} post(s) processed ({'prepare-only test' if a.prepare_only else 'live' if a.live else 'dry-run'})")


if __name__ == "__main__":
    main()
