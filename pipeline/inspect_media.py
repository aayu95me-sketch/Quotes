"""Inspect published Reels: fetch media_url and measure audio loudness with ffmpeg. Prints no tokens.
Usage: python pipeline/inspect_media.py page_a:<media_id> page_b:<media_id> ...
"""
import json, os, subprocess, sys, tempfile, urllib.parse, urllib.request

V = os.environ.get("GRAPH_VERSION", "v26.0")
for arg in sys.argv[1:]:
    page, mid = arg.split(":")
    tok = os.environ[f"IG_{page.upper()}_TOKEN"]
    url = f"https://graph.facebook.com/{V}/{mid}?" + urllib.parse.urlencode({"fields": "id,media_type,media_product_type,permalink,media_url,timestamp", "access_token": tok})
    try:
        d = json.loads(urllib.request.urlopen(url, timeout=40).read())
    except Exception as e:
        print(arg, "API error", str(e)[:200]); continue
    print(arg, {k: d.get(k) for k in ("media_type", "media_product_type", "permalink", "timestamp")})
    mu = d.get("media_url")
    if not mu:
        print("  no media_url returned"); continue
    f = tempfile.mktemp(suffix=".mp4")
    urllib.request.urlretrieve(mu, f)
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,duration", "-of", "csv=p=0", f], capture_output=True, text=True)
    print("  streams:", p.stdout.strip().replace("\n", " | "))
    r = subprocess.run(["ffmpeg", "-i", f, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True)
    print("  loudness:", [l.split("] ")[-1] for l in r.stderr.splitlines() if "mean_volume" in l or "max_volume" in l] or "no audio stream / none measured")
