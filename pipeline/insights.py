"""Pull Instagram insights for every published post and write a plain-language report.

Writes research/insights/latest.json and research/insights/<date>.md. Never prints tokens.
Needs IG_PAGE_*_USER_ID / IG_PAGE_*_TOKEN. The token needs the instagram_manage_insights permission;
if a metric is refused, the report says so instead of guessing.

Decision rules (kept deliberately cautious, because the sample is tiny early on):
  - Only posts at least 48h old are scored (insights are still settling before that).
  - Main score = (saves + shares) per 1,000 reach. Secondary: non-follower share of reach, Reel views.
  - "Winner" = score at least 3x the page median AND at least 3 posts scored. No format/language/pillar
    conclusions until each compared group has at least 8 scored posts; before that the report says "too early".
"""
import datetime as dt
import json
import os
import pathlib
import statistics
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
V = os.environ.get("GRAPH_VERSION", "v26.0")
MIN_AGE = dt.timedelta(hours=48)
MIN_GROUP = 8


def get(path, token, **params):
    params["access_token"] = token
    url = f"https://graph.facebook.com/{V}/{path}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=40) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return {"error": json.loads(e.read()).get("error", {}).get("message", str(e.code))}
        except Exception:
            return {"error": str(e.code)}


def media_insights(mid, token, is_reel):
    metrics = ["reach", "saved", "shares", "likes", "comments", "total_interactions", "views"]
    if is_reel:
        metrics += ["ig_reels_avg_watch_time"]
    out, errs = {}, []
    for m in metrics:  # one call per metric so one unsupported metric does not hide the rest
        r = get(f"{mid}/insights", token, metric=m)
        if "error" in r:
            errs.append(f"{m}: {r['error'][:90]}")
            continue
        try:
            out[m] = r["data"][0]["values"][0]["value"]
        except Exception:
            errs.append(f"{m}: empty")
    return out, errs


def account(uid, token):
    base = get(uid, token, fields="followers_count,media_count")
    ins = get(f"{uid}/insights", token, metric="reach", period="day", metric_type="total_value", breakdown="follow_type")
    split = {}
    try:
        for b in ins["data"][0]["total_value"]["breakdowns"][0]["results"]:
            split[b["dimension_values"][0]] = b["value"]
    except Exception:
        split = {"error": ins.get("error", "no breakdown")}
    return {"followers": base.get("followers_count"), "media": base.get("media_count"), "reach_by_follow_type_1d": split, "err": base.get("error")}


def score(i):
    reach = i.get("reach") or 0
    return round((i.get("saved", 0) + i.get("shares", 0)) / reach * 1000, 1) if reach else None


def main():
    now = dt.datetime.now(dt.timezone.utc)
    posts = {"page_a": [], "page_b": []}
    for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
        p = json.loads(f.read_text())
        if p.get("status") == "published" and p.get("media_id"):
            p["_file"] = f.stem
            posts[p["page"]].append(p)
    result, md = {"generated": now.isoformat(), "pages": {}}, [f"# Insights report {now:%Y-%m-%d %H:%M} UTC\n"]
    for page, items in posts.items():
        key = page.upper()
        uid, tok = os.environ.get(f"IG_{key}_USER_ID"), os.environ.get(f"IG_{key}_TOKEN")
        if not uid or not tok:
            md.append(f"## {page}\nSecrets missing, skipped.\n")
            continue
        acc = account(uid, tok)
        rows = []
        for p in items:
            age = now - dt.datetime.fromisoformat(p["published_at"])
            ins, errs = media_insights(p["media_id"], tok, p["type"] == "reel")
            rows.append({"post": p["_file"], "type": p["type"], "lang": p.get("lang"), "pillar": p.get("pillar"),
                         "age_h": round(age.total_seconds() / 3600), "scored": age >= MIN_AGE, "insights": ins, "score": score(ins), "errors": errs})
        result["pages"][page] = {"account": acc, "posts": rows}
        scored = [r for r in rows if r["scored"] and r["score"] is not None]
        md.append(f"## {page}\nFollowers: {acc['followers']} | media: {acc['media']} | reach by follower type (last day): {acc['reach_by_follow_type_1d']}\n")
        md.append("| post | type | age h | reach | saves | shares | likes | views | saves+shares per 1k reach |\n|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            i = r["insights"]
            md.append(f"| {r['post']} | {r['type']} | {r['age_h']}{'' if r['scored'] else ' (too new)'} | {i.get('reach','-')} | {i.get('saved','-')} | {i.get('shares','-')} | {i.get('likes','-')} | {i.get('views','-')} | {r['score'] if r['score'] is not None else '-'} |")
        errs = sorted({e for r in rows for e in r["errors"]})
        if errs:
            md.append("\nMetrics refused or empty: " + "; ".join(errs[:6]))
        if len(scored) >= 3:
            med = statistics.median(r["score"] for r in scored)
            wins = [r["post"] for r in scored if med > 0 and r["score"] >= 3 * med]
            md.append(f"\nMedian score {med}. Winners (>=3x median): {', '.join(wins) or 'none yet'}.")
        else:
            md.append(f"\nOnly {len(scored)} scored post(s): too early for winners.")
        for dim in ("type", "lang", "pillar"):
            groups = {}
            for r in scored:
                groups.setdefault(r[dim], []).append(r["score"])
            if groups and all(len(v) >= MIN_GROUP for v in groups.values()) and len(groups) > 1:
                md.append(f"By {dim}: " + ", ".join(f"{k} median {statistics.median(v)} (n={len(v)})" for k, v in groups.items()))
            else:
                md.append(f"By {dim}: too early (need {MIN_GROUP}+ scored posts per group).")
        md.append("")
    out = ROOT / "research" / "insights"
    out.mkdir(parents=True, exist_ok=True)
    (out / "latest.json").write_text(json.dumps(result, indent=2) + "\n")
    (out / f"{now:%Y-%m-%d}.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
