"""Read-only engagement check: comments, likes and replies on recent Instagram posts and Facebook posts.

Writes research/engagement/<date>.md. Only GET requests. Never prints tokens. Comment texts are written as data for the owner to read;
replies are NOT posted by this script.
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


def main():
    now = dt.datetime.now(dt.timezone.utc)
    md = [f"# Engagement {now:%Y-%m-%d %H:%M} UTC\n"]
    for page in ("page_a", "page_b"):
        key = page.upper()
        uid, tok = os.environ.get(f"IG_{key}_USER_ID"), os.environ.get(f"IG_{key}_TOKEN")
        fbid = json.loads((ROOT / "content" / "pages" / f"{page}.json").read_text())["fb_page_id"]
        md.append(f"## {page}")
        acc = get(uid, tok, fields="username,followers_count,follows_count,media_count")
        md.append(f"Instagram: {acc}")
        r = get(f"{uid}/media", tok, fields="id,caption,media_type,timestamp,like_count,comments_count,permalink", limit=50)
        if "error" in r:
            md.append(f"Media list error: {r['error']}")
            continue
        media = r.get("data", [])
        tot_likes = sum(m.get("like_count", 0) for m in media)
        tot_comments = sum(m.get("comments_count", 0) for m in media)
        md.append(f"Last {len(media)} posts: {tot_likes} likes, {tot_comments} comments in total.")
        with_comments = [m for m in media if m.get("comments_count")]
        md.append(f"Posts with comments: {len(with_comments)}")
        for m in with_comments:
            c = get(f"{m['id']}/comments", tok, fields="id,text,username,timestamp,like_count,replies{id,text,username,timestamp}", limit=50)
            md.append(f"\n### {m['timestamp'][:16]} {m['media_type']} | {(m.get('caption') or '')[:50]!r} | {m.get('permalink')}")
            if "error" in c:
                md.append(f"- comments error: {c['error']}")
                continue
            for cm in c.get("data", []):
                reps = cm.get("replies", {}).get("data", [])
                md.append(f"- @{cm.get('username')} ({cm['timestamp'][:16]}, {cm.get('like_count', 0)} likes): {cm.get('text')!r} | our replies: {len(reps)} | id {cm['id']}")
        # Facebook
        fb = get(f"{fbid}/posts", tok, fields="id,created_time,message,comments.summary(true).limit(10){from,message,created_time,id},reactions.summary(true).limit(0),shares", limit=50)
        if "error" in fb:
            md.append(f"\nFacebook posts error: {fb['error']}")
        else:
            posts = fb.get("data", [])
            rc = sum(p.get("reactions", {}).get("summary", {}).get("total_count", 0) for p in posts)
            cc = sum(p.get("comments", {}).get("summary", {}).get("total_count", 0) for p in posts)
            md.append(f"\nFacebook: {len(posts)} recent posts, {rc} reactions, {cc} comments.")
            for p in posts:
                for cm in p.get("comments", {}).get("data", []):
                    md.append(f"- FB {p['created_time'][:16]} {(p.get('message') or '')[:40]!r}: {cm.get('from', {}).get('name')}: {cm.get('message')!r} | id {cm['id']}")
        md.append("")
    out = ROOT / "research" / "engagement"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{now:%Y-%m-%d}.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
