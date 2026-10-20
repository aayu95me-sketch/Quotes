"""Generate 1080x1080 profile pictures for each page into brand/ (uses theme colours in content/pages/*.json)."""
import json
import pathlib
from playwright.sync_api import sync_playwright
import os

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = {"page_a": "RKR", "page_b": "QD"}

with sync_playwright() as p:
    exe = os.environ.get("CHROMIUM_PATH")
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1080})
    for f in sorted((ROOT / "content" / "pages").glob("*.json")):
        c = json.loads(f.read_text()); t = c["theme"]
        pg.set_content(f"""<body style="margin:0;width:1080px;height:1080px;background:{t['bg']};display:flex;
        align-items:center;justify-content:center;font-family:{t['font']}">
        <div style="width:760px;height:760px;border-radius:50%;border:14px solid {t['accent']};display:flex;
        align-items:center;justify-content:center;color:{t['fg']};font-size:{250 if len(MARK[c['id']])==3 else 300}px;font-weight:800;
        letter-spacing:-6px">{MARK[c['id']]}</div></body>""")
        out = ROOT / "brand" / f"{c['id']}_profile.png"
        pg.screenshot(path=str(out)); print(out)
    b.close()
