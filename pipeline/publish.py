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
MAX_LATE = dt.timedelta(hours=120)  # an outage shorter than two days catches up; older posts must be rescheduled on purpose
MAX_PER_RUN = 3


STATE = ROOT / "state" / "blocked.json"
BLOCK_HOURS = 3  # after Instagram says "action is blocked", leave that account alone this long instead of retrying hourly


PAUSE = ROOT / "state" / "pause"


def paused():
    return PAUSE.exists()


def blocked_pages(now):
    try:
        data = json.loads(STATE.read_text())
    except Exception:
        return {}
    return {pg: u for pg, u in data.items() if dt.datetime.fromisoformat(u) > now}


def block_page(page, now):
    try:
        data = json.loads(STATE.read_text())
    except Exception:
        data = {}
    data[page] = (now + dt.timedelta(hours=BLOCK_HOURS)).isoformat()
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(data, indent=2) + "\n")


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


def _asset_targets():
    """Where slides and videos are hosted, in order of preference: the assets repo (ASSETS_PAT), then this repo itself
    through the workflow's own GITHUB_TOKEN (works when the personal token has expired or is missing)."""
    out = []
    if os.environ.get("ASSETS_REPO") and os.environ.get("ASSETS_PAT"):
        out.append((os.environ["ASSETS_REPO"], "main", os.environ["ASSETS_PAT"], ""))
    if os.environ.get("GITHUB_REPOSITORY") and os.environ.get("GITHUB_TOKEN"):
        out.append((os.environ["GITHUB_REPOSITORY"], os.environ.get("GITHUB_REF_NAME", "main"), os.environ["GITHUB_TOKEN"], "assets/"))
    return out


def _put_asset(repo, branch, token, rel, data):
    api_url = f"https://api.github.com/repos/{repo}/contents/{rel}"
    hdr = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    body = {"message": f"slide {rel}", "content": base64.b64encode(data).decode(), "branch": branch}
    try:  # overwrite if it already exists
        with urllib.request.urlopen(urllib.request.Request(api_url + f"?ref={branch}", headers=hdr), timeout=30) as r:
            body["sha"] = json.loads(r.read())["sha"]
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise
    urllib.request.urlopen(urllib.request.Request(api_url, data=json.dumps(body).encode(), headers=hdr, method="PUT"), timeout=60).read()
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{rel}"


def upload_assets(paths, page, stem):
    """Host rendered PNGs/MP4 on a public URL; return the raw URLs. Falls back to this repo when the assets-repo token fails."""
    targets, last_err, urls = _asset_targets(), None, None
    for repo, branch, token, prefix in targets:
        try:
            urls = [_put_asset(repo, branch, token, f"{prefix}{page}/{stem}/{p.name}", p.read_bytes()) for p in paths]
            break
        except urllib.error.HTTPError as e:
            last_err = e
            print(f"WARN asset host {repo} refused ({e.code}); trying the next one")
    if urls is None:
        raise RuntimeError(f"ASSET HOSTING FAILED: {last_err}")
    for u in urls:  # wait until each URL is actually reachable
        for _ in range(10):
            try:
                urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=15)
                break
            except Exception:
                time.sleep(3)
    return urls


def fb_page_id(page):
    return json.loads((ROOT / "content" / "pages" / f"{page}.json").read_text())["fb_page_id"]


def fb_carousel(post, page, slide_urls, token, ver):
    """Mirror a carousel to the Facebook Page as a multi-photo post (photos are uploaded unpublished, then attached)."""
    fid = fb_page_id(page)
    ids = [api("POST", f"{fid}/photos", {"url": u, "published": "false", "access_token": token}, ver)["id"] for u in slide_urls]
    attached = json.dumps([{"media_fbid": i} for i in ids])
    return api("POST", f"{fid}/feed", {"message": post["caption"], "attached_media": attached, "access_token": token}, ver)["id"]


def fb_reel(post, page, video_url, token, ver):
    """Mirror a Reel to the Facebook Page via the video_reels flow (start, upload from a hosted file, finish)."""
    fid = fb_page_id(page)
    start = api("POST", f"{fid}/video_reels", {"upload_phase": "start", "access_token": token}, ver)
    vid, upload_url = start["video_id"], start["upload_url"]
    req = urllib.request.Request(upload_url, method="POST", headers={"Authorization": f"OAuth {token}", "file_url": video_url})
    try:
        out = json.loads(urllib.request.urlopen(req, timeout=300).read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"fb reel upload {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")
    if not out.get("success"):
        raise RuntimeError(f"fb reel upload failed: {out}")
    api("POST", f"{fid}/video_reels", {"upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED",
                                        "description": post["caption"], "access_token": token}, ver)
    return vid


def fb_mirror(post, page, stem, token, ver, urls=None, video_url=None):
    """Best effort: a Facebook failure never marks the Instagram post failed. Result is stored on the post."""
    try:
        if post["type"] == "reel":
            post["fb_post_id"] = fb_reel(post, page, video_url, token, ver)
        else:
            post["fb_post_id"] = fb_carousel(post, page, urls, token, ver)
        post.pop("fb_error", None)
        print(f"FB mirrored {page}/{stem}: {post['fb_post_id']}")
    except Exception as e:
        msg = str(e)
        print(f"FB ERROR {page}/{stem}: {msg[:300]}")
        if any(k in msg for k in ("(#200)", "(#10)", "permission", "OAuthException")):
            return "permission"  # token lacks Page posting access: leave the post untouched so it retries after the fix
        post["fb_error"] = msg[:300]
    return None


def fb_catchup(now, limit=2):
    """Mirror already-published Instagram posts that have no Facebook copy yet (slides/videos are in the assets repo)."""
    repo = os.environ.get("ASSETS_REPO", "")
    done = 0
    for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
        if done >= limit:
            break
        post = json.loads(f.read_text())
        if post.get("status") != "published" or post.get("fb_post_id") or post.get("fb_error") or not post.get("published_at"):
            continue
        page, stem = post["page"], f.stem
        base = post.get("asset_base") or f"https://raw.githubusercontent.com/{repo}/main/{page}/{stem}"
        token = os.environ[f"IG_{page.upper()}_TOKEN"]
        ver = os.environ.get("GRAPH_VERSION", "v26.0")
        if post["type"] == "reel":
            res = fb_mirror(post, page, stem, token, ver, video_url=f"{base}/{stem}.mp4")
        else:
            res = fb_mirror(post, page, stem, token, ver, urls=[f"{base}/slide_{i:02d}.png" for i in range(1, len(post["slides"]) + 1)])
        f.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
        done += 1
        if res == "permission":
            print("FB PERMISSION PROBLEM: Page posting not allowed with the stored token; stopping Facebook catch-up")
            break


PER_PAGE_PER_RUN = 2
DAILY_CAP = 3  # per Instagram account per UTC day; the plan is 1 carousel + 1-2 Reels


def posted_today(page, now):
    n = 0
    for f in (ROOT / "content" / "posts" / page).glob("*.json"):
        p = json.loads(f.read_text())
        pa = p.get("published_at")
        if p.get("status") == "published" and pa and dt.datetime.fromisoformat(pa).date() == now.date():
            n += 1
    return n


def find_recent(page, caption, since, ver=None):
    """Return the oldest Instagram media with this exact caption published since `since`, else None.
    Makes publishing idempotent: Instagram sometimes creates the post and then answers with an error, and a retry would post a duplicate."""
    key = page.upper()
    uid, token = os.environ[f"IG_{key}_USER_ID"], os.environ[f"IG_{key}_TOKEN"]
    ver = ver or os.environ.get("GRAPH_VERSION", "v26.0")
    r = api("GET", f"{uid}/media", {"fields": "id,caption,timestamp", "limit": "50", "access_token": token}, ver)
    hits = []
    for m in r.get("data", []):
        when = dt.datetime.fromisoformat(m["timestamp"].replace("+0000", "+00:00"))
        if (m.get("caption") or "").strip() == caption.strip() and when >= since:
            hits.append((when, m["id"]))
    return min(hits) if hits else None


def due_posts(now):
    for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
        post = json.loads(f.read_text())
        if post.get("status") != "approved":
            continue
        when = dt.datetime.fromisoformat(post["publish_at"])
        if when > now:
            continue
        if now - when > MAX_LATE:
            print(f"skip {f.name}: more than 48h overdue, reschedule it")
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
    post["asset_base"] = urls[0].rsplit("/", 1)[0]
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
    mid = api("POST", f"{uid}/media_publish", {"creation_id": parent, "access_token": token}, ver)["id"]
    fb_mirror(post, page, stem, token, ver, urls=urls)
    return mid


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
    from render import render, render_kinetic
    from reel import build_slideshow, build_kinetic
    import audio as audio_mod
    mp4 = str(ROOT / "out" / page / f"{stem}.mp4")
    (ROOT / "out" / page).mkdir(parents=True, exist_ok=True)
    if post.get("style") == "kinetic":  # word-by-word reveal, about 8-10 s instead of 13-16 s
        total_s = build_kinetic(render_kinetic(f, ROOT / "out"), mp4)
    else:
        build_slideshow([str(x) for x in render(f, ROOT / "out")], mp4, per)
        total_s = per * len(post["slides"])
    key = page.upper()
    uid, token = os.environ[f"IG_{key}_USER_ID"], os.environ[f"IG_{key}_TOKEN"]
    ver = os.environ.get("GRAPH_VERSION", "v26.0")
    base = {"media_type": "REELS", "caption": post["caption"], "access_token": token}
    if post.get("ai_label"):
        base["is_ai_generated"] = "true"
    chosen, vol = None, audio_mod.mood_cfg(page, post.get("mood", "focus"))["volume"]
    try:
        if post.get("audio_id"):
            chosen = {"audio_id": post["audio_id"]}
        else:
            chosen, vol = audio_mod.pick(page, post.get("mood", "focus"), uid, token, ver,
                                         post.get("audio_type", "music"), total_s,
                                         post.get("audio_queries", []))
    except Exception as e:  # audio failure should not block the post; publish silent and note it
        print(f"WARN audio lookup failed ({e}); publishing without audio")
    if chosen:
        # Same shape as Meta's documented example: audio_volume 1-100, video_volume 1-100 (our video track is silent).
        base["audio_configuration"] = json.dumps({"audio_id": chosen["audio_id"], "audio_volume": int(post.get("audio_volume", 80)), "video_volume": 50})
    # Documented flow: video_url on a public server + audio_configuration. (The earlier resumable-upload flow published
    # Reels WITHOUT the music; measured and confirmed by the owner 2026-10-22.)
    video_url = upload_assets([pathlib.Path(mp4)], page, stem)[0]
    post["asset_base"] = video_url.rsplit("/", 1)[0]
    print(f"reel video hosted for container: {video_url}")
    cid = api("POST", f"{uid}/media", {**base, "video_url": video_url}, ver)["id"]
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
    fb_mirror(post, page, stem, token, ver, video_url=video_url)
    return mid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--count", action="store_true", help="print the number of approved, due posts and exit (cheap check for CI)")
    ap.add_argument("--fb-pending", action="store_true", help="print how many published posts still need their Facebook copy and exit")
    ap.add_argument("--reconcile", action="store_true", help="with --live: only record posts that are already on Instagram (never posts anything); works while paused")
    ap.add_argument("--health", action="store_true", help="exit 1 (so GitHub emails the owner) if a post is >8h overdue or fewer than 5 days of approved posts remain")
    ap.add_argument("--prepare-only", action="store_true", help="live API test: build containers (carousel children, reel upload with audio) but do NOT publish")
    ap.add_argument("--only", nargs="*", help="with --prepare-only: post files to test regardless of status and date")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    if a.count:
        print(0 if paused() else sum(1 for _ in due_posts(now)))
        return
    if paused() and not a.prepare_only and not a.only and not a.reconcile:
        print("PAUSED: state/pause exists, nothing is published until it is removed")
        return
    if a.fb_pending:
        print(sum(1 for f in (ROOT / "content" / "posts").rglob("*.json")
                  if (lambda p: p.get("status") == "published" and p.get("published_at") and not p.get("fb_post_id") and not p.get("fb_error"))(json.loads(f.read_text()))))
        return
    if a.health:
        late, last = [], now
        for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
            post = json.loads(f.read_text())
            if post.get("status") != "approved":
                continue
            when = dt.datetime.fromisoformat(post["publish_at"])
            if now - when > dt.timedelta(hours=8) and post["page"] not in blocked_pages(now):
                late.append(f.name)
            last = max(last, when)
        runway = (last - now).total_seconds() / 86400
        print(f"approved posts run {runway:.1f} more days; overdue by more than 8h: {late or 'none'}")
        if late or runway < 5:
            sys.exit(f"HEALTH ALERT: {'overdue posts: ' + ', '.join(late) if late else 'less than 5 days of approved posts left, approve the next batch'}")
        return
    n = 0
    if a.only and not a.prepare_only:
        sys.exit("--only is only allowed together with --prepare-only (it must never publish)")
    auth_failed = False
    done_pages = {}
    block_alert = False
    blocked = blocked_pages(now)
    for pg, u in blocked.items():
        print(f"{pg}: Instagram blocked this account, resting until {u[:16]} UTC")
    queue = [(pathlib.Path(x), json.loads(pathlib.Path(x).read_text())) for x in a.only] if a.only else due_posts(now)
    live = a.live or a.prepare_only
    for f, post in queue:
        if n >= MAX_PER_RUN and not a.only:
            break
        if a.live and not a.prepare_only:
            try:  # already on Instagram (an earlier attempt succeeded but answered with an error)? then record it, never post again
                hit = find_recent(post["page"], post["caption"], now - dt.timedelta(hours=72))
            except Exception as e:
                hit = None
                print(f"WARN duplicate check failed for {f.name}: {str(e)[:120]}")
            if hit:
                post["status"], post["media_id"] = "published", hit[1]
                post["published_at"] = hit[0].isoformat()
                post["note"] = "reconciled: found on Instagram, not published again"
                f.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
                print(f"RECONCILED {f.name}: already on Instagram as {hit[1]}")
                continue
        if a.reconcile:
            continue  # reconcile-only: never publish
        if done_pages.get(post["page"], 0) >= PER_PAGE_PER_RUN and not a.only:
            continue  # at most two posts per account per run (GitHub runs the schedule only every few hours), never a burst
        if not a.only and posted_today(post["page"], now) >= DAILY_CAP:
            print(f"{post['page']}: daily cap of {DAILY_CAP} reached, {f.name} waits for tomorrow")
            continue
        if post["page"] in blocked:
            continue
        if post["type"] not in ("carousel", "reel"):
            print(f"skip {f.name}: type {post['type']} not supported yet")
            continue
        try:
            media_id = (publish_reel if post["type"] == "reel" else publish_carousel)(f, post, live, a.prepare_only)
        except Exception as e:  # never crash the whole run; record and move on
            print(f"ERROR {f.name}: {e}")
            if a.live and not a.prepare_only:
                try:
                    hit = find_recent(post["page"], post["caption"], now - dt.timedelta(minutes=30))
                except Exception:
                    hit = None
                if hit:  # the post was created although the call answered with an error: record it, do not retry
                    post["status"], post["media_id"] = "published", hit[1]
                    post["published_at"] = hit[0].isoformat()
                    post["note"] = f"published although the API answered: {str(e)[:120]}"
                    f.write_text(json.dumps(post, indent=2, ensure_ascii=False) + "\n")
                    print(f"RECORDED {f.name} as published ({hit[1]}) despite the error")
                    if "2207051" in str(e) or '"code":4,' in str(e):
                        block_page(post["page"], now)
                        blocked[post["page"]] = "now"
                    continue
            if "ASSET HOSTING FAILED" in str(e) or "HTTP Error 401" in str(e):
                print("ASSET HOSTING PROBLEM: posts stay approved; renew ASSETS_PAT (fine-grained, Contents read/write on the assets repo)")
                auth_failed = True
                break
            if "2207051" in str(e) or '"code":4,' in str(e):  # "Application request limit reached / Action is blocked": rest this account, keep the other running
                block_page(post["page"], now)
                blocked[post["page"]] = "now"
                print(f"INSTAGRAM BLOCKED {post['page']}: resting {BLOCK_HOURS}h; the owner may need to check Account Status / Business Suite")
                block_alert = True
                continue
            if any(k in str(e) for k in ("OAuthException", "access blocked", "Error validating access token", "Cannot call API")):
                print("AUTH PROBLEM: stopping this run; posts stay approved and will retry once tokens/app access are fixed")
                auth_failed = True
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
        done_pages[post["page"]] = done_pages.get(post["page"], 0) + 1
    if a.live and not a.prepare_only and not auth_failed and not a.reconcile and not paused():
        fb_catchup(now)
    print(f"{n} post(s) processed ({'prepare-only test' if a.prepare_only else 'live' if a.live else 'dry-run'})")
    if block_alert:
        sys.exit("INSTAGRAM BLOCKED an account (see log); resting it for a few hours")  # non-zero exit makes GitHub email the owner once per block
    if auth_failed:
        sys.exit("AUTH PROBLEM: see log; posts stay approved")  # non-zero exit makes GitHub email the owner


if __name__ == "__main__":
    main()
