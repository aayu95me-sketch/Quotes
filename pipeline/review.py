"""Build a phone-friendly review PDF per page: every draft post with its slides, caption, schedule and audio pick.

Usage: python pipeline/review.py            -> out/review_page_a.pdf, out/review_page_b.pdf
Needs Chromium (CHROMIUM_PATH) and the render pipeline.
"""
import base64
import datetime as dt
import html
import io
import json
import os
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
from render import render  # noqa: E402


def thumb(path, w):
    im = Image.open(path).convert("RGB")
    im.thumbnail((w, w * 2))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=70)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def post_html(f, post, idx, slides):
    reel = post["type"] == "reel"
    w = 150 if reel else 170
    imgs = "".join(f'<img src="{thumb(p, 300)}" style="width:{w}px;margin:3px;border:1px solid #bbb">' for p in slides)
    when = dt.datetime.fromisoformat(post["publish_at"])
    audio = post.get("audio_pick")
    audio_line = f"<div><b>Audio:</b> {html.escape(audio['title'])} - {html.escape(audio['artist'])} (mood {html.escape(post.get('mood',''))})</div>" if audio else ""
    return f"""<section style="page-break-inside:avoid;margin:0 0 18px;padding:10px;border:2px solid #333;border-radius:8px">
    <div style="font-size:15px"><b>#{idx} {post['type'].upper()}</b> | {html.escape(f.stem)} | {when:%a %d %b %H:%M %Z} | lang {post.get('lang','')} | pillar {html.escape(post.get('pillar',''))} | status {post['status']}</div>
    {audio_line}
    <div style="margin:6px 0">{imgs}</div>
    <div style="font-size:13px;white-space:pre-wrap;background:#f3f3f3;padding:6px;border-radius:4px"><b>Caption</b>
{html.escape(post['caption'])}</div>
    <div style="font-size:12px;color:#555">AI flag: {post.get('ai_label')} | file: content/posts/{post['page']}/{f.name}</div></section>"""


def main():
    exe = os.environ.get("CHROMIUM_PATH") or None
    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    plan = {}
    for page_id in ("page_a", "page_b"):  # render first (each render opens its own browser)
        files = sorted((ROOT / "content" / "posts" / page_id).glob("*.json"), key=lambda f: json.loads(f.read_text())["publish_at"])
        plan[page_id] = [(f, json.loads(f.read_text()), render(f, out)) for f in files]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        for page_id, items in plan.items():
            cfg = json.loads((ROOT / "content" / "pages" / f"{page_id}.json").read_text())
            files = items
            body = "".join(post_html(f, post, i, slides) for i, (f, post, slides) in enumerate(items, 1))
            doc = f"<html><body style='font-family:Arial;margin:14px'><h2>{html.escape(cfg['name'])} ({html.escape(cfg['handle'])}): review {len(files)} drafts</h2>{body}</body></html>"
            pg = b.new_page()
            pg.set_content(doc)
            target = out / f"review_{page_id}.pdf"
            pg.pdf(path=str(target), format="A4", margin={"top": "10mm", "bottom": "10mm", "left": "8mm", "right": "8mm"})
            print(target)
        b.close()


if __name__ == "__main__":
    main()
