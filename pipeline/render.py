"""Render a post JSON into 1080x1350 PNG slides (carousel) via headless Chromium.

Usage: python pipeline/render.py content/posts/page_a/<post>.json [--out out]
"""
import argparse
import html
import json
import os
import pathlib
import re

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1080, 1350          # carousel (4:5)
RW, RH = 1080, 1920        # reel / story (9:16); keep text inside the safe zone (UI covers top and bottom)

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{w}px;height:{h}px;background:{bg};color:{fg};font-family:{font};
  display:flex;flex-direction:column;justify-content:space-between;padding:{pt}px 96px {pb}px}}
.top{{display:flex;justify-content:space-between;font-size:30px;color:{muted};letter-spacing:.04em}}
.bar{{position:absolute;left:96px;right:96px;top:{bar}px;height:6px;background:{muted}33;border-radius:3px}}
.bar i{{display:block;height:100%;width:{pct}%;background:{accent};border-radius:3px}}
.main{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.text{{font-size:{size}px;line-height:1.22;font-weight:{weight};letter-spacing:-.01em}}
.sub{{margin-top:48px;font-size:38px;color:{accent};font-weight:600}}
.hl{{color:{accent};font-weight:800}}
.rule{{width:120px;height:8px;background:{accent};border-radius:4px;margin-bottom:56px}}
.foot{{font-size:30px;color:{muted}}}
</style></head><body>
<div class="bar"><i></i></div>
<div class="top"><span>{name}</span><span>{idx}/{total}</span></div>
<div class="main"><div class="rule"></div><div class="text">{text}</div>{sub}</div>
<div class="foot">{footer}</div>
</body></html>"""


def slide_html(page, slide, idx, total, reel=False):
    t = page["theme"]
    kind = slide["kind"]
    text = slide["text"]
    n = len(text)
    size = (96 if n < 50 else 84) if kind == "hook" else 88 if n < 50 else 76 if n < 90 else 64 if n < 140 else 54
    sub = f'<div class="sub">{html.escape(slide["sub"])}</div>' if slide.get("sub") else ""
    if reel:
        size = int(size * 1.12)
    return TEMPLATE.format(
        w=RW if reel else W, h=RH if reel else H, pt=300 if reel else 110, pb=380 if reel else 90, bar=230 if reel else 70, bg=t["bg"], fg=t["fg"], muted=t["muted"], accent=t["accent"],
        font=t["font"], size=size, weight=800 if kind == "hook" else 600,
        pct=round(idx / total * 100), name=html.escape(page["name"]), idx=idx, total=total,
        text=re.sub(r"\*(.+?)\*", r'<span class="hl">\1</span>', html.escape(text)), sub=sub, footer=html.escape(page["footer"]),
    )


def render(post_path, out_dir):
    post_path = pathlib.Path(post_path)
    post = json.loads(post_path.read_text())
    page = json.loads((ROOT / "content" / "pages" / f"{post['page']}.json").read_text())
    out = pathlib.Path(out_dir) / post["page"] / post_path.stem
    out.mkdir(parents=True, exist_ok=True)
    slides = post["slides"]
    reel = post.get("type") == "reel"
    exe = os.environ.get("CHROMIUM_PATH") or None
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = browser.new_page(viewport={"width": RW if reel else W, "height": RH if reel else H})
        paths = []
        for i, s in enumerate(slides, 1):
            pg.set_content(slide_html(page, s, i, len(slides), reel))
            f = out / f"slide_{i:02d}.png"
            pg.screenshot(path=str(f))
            paths.append(f)
        browser.close()
    return paths


def _kinetic_text(text):
    """Return (html, word_count): every word wrapped in span.w so it can be revealed one at a time."""
    parts, n = [], 0
    for seg in re.split(r"(\*[^*]+\*)", text):
        if not seg:
            continue
        hl = seg.startswith("*") and seg.endswith("*") and len(seg) > 2
        words = (seg[1:-1] if hl else seg).split()
        wrapped = []
        for w in words:
            wrapped.append(f'<span class="w">{html.escape(w)}</span>')
            n += 1
        inner = " ".join(wrapped)
        parts.append(f'<span class="hl">{inner}</span>' if hl else inner)
        parts.append(" ")
    return "".join(parts).strip(), n


_KIN_CSS = "<style>.w{visibility:hidden}.w.on{visibility:visible}.sub{visibility:hidden}.sub.on{visibility:visible}</style>"


def render_kinetic(post_path, out_dir):
    """Word-by-word reveal frames for a Reel. Returns [(png_path, seconds), ...]. Much shorter and with motion from the first frame."""
    post_path = pathlib.Path(post_path)
    post = json.loads(post_path.read_text())
    page = json.loads((ROOT / "content" / "pages" / f"{post['page']}.json").read_text())
    out = pathlib.Path(out_dir) / post["page"] / (post_path.stem + "_kinetic")
    out.mkdir(parents=True, exist_ok=True)
    exe = os.environ.get("CHROMIUM_PATH") or None
    frames = []
    slides = post["slides"]
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = browser.new_page(viewport={"width": RW, "height": RH})
        for si, sl in enumerate(slides, 1):
            doc = slide_html(page, sl, si, len(slides), True)
            inner, n = _kinetic_text(sl["text"])
            doc = re.sub(r'(<div class="text">).*?(</div>)', lambda m: m.group(1) + inner + m.group(2), doc, count=1, flags=re.S)
            doc = doc.replace("</head>", _KIN_CSS + "</head>", 1)
            pg.set_content(doc)
            kind = sl["kind"]
            per, hold = (0.30, 0.7) if kind == "hook" else (0.20, 1.4) if kind == "cta" else (0.22, 0.8)
            for k in range(1, n + 1):
                pg.evaluate("k => document.querySelectorAll('.w').forEach((e, i) => e.classList.toggle('on', i < k))", k)
                if k == n:
                    pg.evaluate("() => { const s = document.querySelector('.sub'); if (s) s.classList.add('on'); }")
                f = out / f"s{si:02d}_{k:02d}.png"
                pg.screenshot(path=str(f))
                frames.append((f, per if k < n else per + hold))
        browser.close()
    return frames


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("post")
    ap.add_argument("--out", default=str(ROOT / "out"))
    a = ap.parse_args()
    for f in render(a.post, a.out):
        print(f)
