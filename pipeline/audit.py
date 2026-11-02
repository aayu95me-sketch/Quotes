"""Read-only audit: compare what the repo says is published with what Instagram and Facebook actually show.

Writes research/audit/<date>.md. Uses only GET requests; never prints tokens.
"""
import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
V = os.environ.get("GRAPH_VERSION", "v26.0")


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


def paged(path, token, **params):
    out, r = [], get(path, token, **params)
    for _ in range(6):
        if "error" in r:
            return out, r["error"]
        out += r.get("data", [])
        nxt = r.get("paging", {}).get("next")
        if not nxt:
            break
        try:
            with urllib.request.urlopen(nxt, timeout=40) as resp:
                r = json.loads(resp.read())
        except Exception as e:
            return out, str(e)
    return out, None


def main():
    now = dt.datetime.now(dt.timezone.utc)
    posts = {"page_a": [], "page_b": []}
    for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
        p = json.loads(f.read_text())
        p["_file"] = f.stem
        posts[p["page"]].append(p)
    md = [f"# Audit {now:%Y-%m-%d %H:%M} UTC\n"]
    for page, items in posts.items():
        key = page.upper()
        uid, tok = os.environ.get(f"IG_{key}_USER_ID"), os.environ.get(f"IG_{key}_TOKEN")
        fbid = json.loads((ROOT / "content" / "pages" / f"{page}.json").read_text())["fb_page_id"]
        md.append(f"## {page}")
        ig, err = paged(f"{uid}/media", tok, fields="id,media_type,media_product_type,timestamp,permalink,caption", limit=50)
        if err:
            md.append(f"Instagram media list error: {err}")
        ig_ids = {m["id"] for m in ig}
        repo_pub = {p["media_id"]: p for p in items if p.get("status") == "published" and p.get("media_id")}
        md.append(f"Instagram shows **{len(ig)}** posts; repo says **{len(repo_pub)}** published.")
        missing_on_ig = [p["_file"] for mid, p in repo_pub.items() if mid not in ig_ids]
        extra_on_ig = [m for m in ig if m["id"] not in repo_pub]
        md.append(f"- In repo as published but NOT on Instagram (deleted or never there): {missing_on_ig or 'none'}")
        md.append("- On Instagram but not in repo (duplicates or manual posts):")
        for m in sorted(extra_on_ig, key=lambda x: x["timestamp"]):
            md.append(f"  - {m['timestamp'][:16]} {m['media_type']} | {(m.get('caption') or '')[:50]!r} | {m.get('permalink')}")
        cap = {}
        for m in ig:
            cap.setdefault((m.get("caption") or "")[:60], []).append(m["timestamp"][:16])
        dups = {k: v for k, v in cap.items() if len(v) > 1}
        md.append("- Captions that appear more than once: " + ("; ".join(f"{k[:40]!r} x{len(v)}" for k, v in dups.items()) or "none"))
        by_day = {}
        for m in ig:
            by_day.setdefault(m["timestamp"][:10], []).append(m["media_type"][:3])
        md.append("- Instagram posts per day: " + ", ".join(f"{d}: {len(v)}" for d, v in sorted(by_day.items())))
        # Facebook
        fb, err = paged(f"{fbid}/posts", tok, fields="id,created_time,message", limit=50)
        fcap = {}
        for m in fb:
            fcap.setdefault((m.get("message") or "")[:60], []).append(m["created_time"][:16])
        fdups = {k: v for k, v in fcap.items() if len(v) > 1}
        md.append(f"Facebook Page shows **{len(fb)}** feed posts" + (f" (error: {err})" if err else "") + f"; repo says {sum(1 for p in items if p.get('fb_post_id'))} mirrored.")
        md.append("- Facebook captions that appear more than once: " + ("; ".join(f"{k[:40]!r} x{len(v)}" for k, v in fdups.items()) or "none"))
        reels, err2 = paged(f"{fbid}/video_reels", tok, fields="id,created_time,description", limit=50)
        md.append(f"Facebook Reels listed: {len(reels)}" + (f" (error: {err2})" if err2 else ""))
        # schedule vs reality
        late = []
        for p in items:
            if p.get("status") == "approved" and dt.datetime.fromisoformat(p["publish_at"]) <= now:
                late.append(p["_file"])
        md.append(f"- Approved, due, not published: {late or 'none'}")
        dup = {}
        for p in items:
            if p.get("status") == "published":
                dup.setdefault(p["publish_at"][:10] + p["type"], []).append(p["_file"])
        md.append("- Published per day by type: " + ", ".join(f"{k}: {len(v)}" for k, v in sorted(dup.items())))
        md.append("")
    out = ROOT / "research" / "audit"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{now:%Y-%m-%d}.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
