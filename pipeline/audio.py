"""Pick trending Instagram audio that matches a post's mood, using Meta's official Audio API.

Docs (fetched 2026-10-20): GET /ig_audio?audio_type=music|original_sound&user_id=..&[search_query=..]
returns trending audio when no query is given; returns only audio authorised for third-party publishing.
Attach with audio_configuration={"audio_id","audio_volume","video_volume"} when creating a REELS container.
Only the Facebook-Login setup supports it. Music can NOT be attached to carousels or stories through the API
(only Reels), so carousels stay silent unless music is added by hand in the app.

Scoring (heuristic, tracks give no mood tags): +3 if currently trending, +2 per mood-query search that returns it,
+1 if marked ads-eligible, -5 if reused within avoid_reuse_days, hard filter on duration (must cover the reel).

CLI:  python pipeline/audio.py shortlist [--page page_a]   -> research/audio/<date>_<page>.md  (needs IG env vars)
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "content" / "audio_moods.json").read_text())
LOG = ROOT / "content" / "audio_log.json"
GRAPH = "https://graph.facebook.com"


def _get(path, params, ver):
    url = f"{GRAPH}/{ver}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Audio API {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def search(uid, token, ver, audio_type="music", query=None):
    p = {"audio_type": audio_type, "user_id": uid, "access_token": token}
    if query:
        p["search_query"] = query
    return _get("ig_audio", p, ver).get("audio", [])


def mood_cfg(page, mood):
    base = CFG["moods"].get(mood, CFG["moods"]["focus"])
    return {**base, **CFG.get("page_overrides", {}).get(page, {}).get(mood, {})}


def _recent_ids(page):
    if not LOG.exists():
        return set()
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=CFG["avoid_reuse_days"])
    return {e["audio_id"] for e in json.loads(LOG.read_text()).get(page, [])
            if dt.datetime.fromisoformat(e["used_at"]) > cutoff}


def record_use(page, audio):
    data = json.loads(LOG.read_text()) if LOG.exists() else {}
    data.setdefault(page, []).append({"audio_id": audio["audio_id"], "title": audio.get("title"),
                                      "artist": audio.get("display_artist"),
                                      "used_at": dt.datetime.now(dt.timezone.utc).isoformat()})
    LOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def rank(page, mood, uid, token, ver, audio_type="music", min_ms=0, extra_queries=()):
    cfg = mood_cfg(page, mood)
    trending = {a["audio_id"]: a for a in search(uid, token, ver, audio_type)}
    pool, hits = dict(trending), {}
    for q in list(cfg["queries"]) + list(extra_queries):
        for a in search(uid, token, ver, audio_type, q):
            pool.setdefault(a["audio_id"], a)
            hits[a["audio_id"]] = hits.get(a["audio_id"], 0) + 1
    recent = _recent_ids(page)
    ranked = []
    for aid, a in pool.items():
        if min_ms and a.get("duration_in_ms", 0) < min_ms:
            continue
        score = (3 if aid in trending else 0) + 2 * hits.get(aid, 0) + (1 if a.get("is_ads_eligible") else 0) - (5 if aid in recent else 0)
        ranked.append((score, a))
    ranked.sort(key=lambda x: -x[0])
    return ranked


def pick(page, mood, uid, token, ver, audio_type="music", seconds=10, extra_queries=()):
    min_ms = int(seconds * 1000 + CFG["min_duration_ms_margin"])
    ranked = rank(page, mood, uid, token, ver, audio_type, min_ms, extra_queries)
    if not ranked:
        return None, mood_cfg(page, mood)["volume"]
    return ranked[0][1], mood_cfg(page, mood)["volume"]


def shortlist(pages):
    ver = os.environ.get("GRAPH_VERSION", "v26.0")
    day = dt.date.today().isoformat()
    for page in pages:
        key = page.upper()
        uid, token = os.environ[f"IG_{key}_USER_ID"], os.environ[f"IG_{key}_TOKEN"]
        lines = [f"# Audio shortlist for {page} on {day}", "", "Pin a pick by adding `\"audio_id\": \"<id>\"` to a reel post JSON. Scores are heuristic (see audio.py).", ""]
        for mood in CFG["moods"]:
            lines += [f"## {mood}", "", "| score | id | title | artist | sec | ads-eligible |", "|---|---|---|---|---|---|"]
            try:
                for score, a in rank(page, mood, uid, token, ver)[:8]:
                    lines.append(f"| {score} | {a['audio_id']} | {a.get('title','')} | {a.get('display_artist','')} | {a.get('duration_in_ms',0)//1000} | {a.get('is_ads_eligible')} |")
            except Exception as e:
                lines.append(f"| error | | {e} | | | |")
            lines.append("")
        out = ROOT / "research" / "audio" / f"{day}_{page}.md"
        out.write_text("\n".join(lines) + "\n")
        print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["shortlist"])
    ap.add_argument("--page", action="append")
    a = ap.parse_args()
    shortlist(a.page or ["page_a", "page_b"])
