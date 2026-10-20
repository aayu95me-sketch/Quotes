"""Render a post JSON into 1080x1350 PNG slides (carousel) via headless Chromium.

Usage: python pipeline/render.py content/posts/page_a/<post>.json [--out out]
"""
import argparse
import html
import json
import os
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1080, 1350

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{w}px;height:{h}px;background:{bg};color:{fg};font-family:{font};
  display:flex;flex-direction:column;justify-content:space-between;padding:110px 96px 90px}}
.top{{display:flex;justify-content:space-between;font-size:30px;color:{muted};letter-spacing:.04em}}
.bar{{position:absolute;left:96px;right:96px;top:70px;height:6px;background:{muted}33;border-radius:3px}}
.bar i{{display:block;height:100%;width:{pct}%;background:{accent};border-radius:3px}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.text{{font-size:{size}px;line-height:1.22;font-weight:{weight};letter-spacing:-.01em}}
.sub{{margin-top:48px;font-size:38px;color:{accent};font-weight:600}}
.rule{{width:120px;height:8px;background:{accent};border-radius:4px;margin-bottom:56px}}
.foot{{font-size:30px;color:{muted}}}
</style></head><body>
<div class="bar"><i></i></div>
<div class="top"><span>{name}</span><span>{idx}/{total}</span></div>
<div class="main"><div class="rule"></div><div class="text">{text}</div>{sub}</div>
<div class="foot">{footer}</div>
</body></html>"""


def slide_html(page, slide, idx, total):
    t = page["theme"]
    kind = slide["kind"]
    text = slide["text"]
    n = len(text)
    size = (84 if n < 70 else 74) if kind == "hook" else 78 if n < 60 else 68 if n < 100 else 60 if n < 150 else 54
    sub = f'<div class="sub">{html.escape(slide["sub"])}</div>' if slide.get("sub") else ""
    return TEMPLATE.format(
        w=W, h=H, bg=t["bg"], fg=t["fg"], muted=t["muted"], accent=t["accent"],
        font=t["font"], size=size, weight=800 if kind == "hook" else 600,
        pct=round(idx / total * 100), name=html.escape(page["name"]), idx=idx, total=total,
        text=html.escape(text), sub=sub, footer=html.escape(page["footer"]),
    )


def render(post_path, out_dir):
    post_path = pathlib.Path(post_path)
    post = json.loads(post_path.read_text())
    page = json.loads((ROOT / "content" / "pages" / f"{post['page']}.json").read_text())
    out = pathlib.Path(out_dir) / post["page"] / post_path.stem
    out.mkdir(parents=True, exist_ok=True)
    slides = post["slides"]
    exe = os.environ.get("CHROMIUM_PATH") or None
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = browser.new_page(viewport={"width": W, "height": H})
        paths = []
        for i, s in enumerate(slides, 1):
            pg.set_content(slide_html(page, s, i, len(slides)))
            f = out / f"slide_{i:02d}.png"
            pg.screenshot(path=str(f))
            paths.append(f)
        browser.close()
    return paths


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("post")
    ap.add_argument("--out", default=str(ROOT / "out"))
    a = ap.parse_args()
    for f in render(a.post, a.out):
        print(f)
