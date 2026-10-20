# Quotes: faceless automated social pages

Start with [PROJECT.md](PROJECT.md) for current state, decisions and next steps. Research is in `docs/`.

## Pipeline (`pipeline/`)
```
pip install -r requirements.txt   # then provide Chromium (CHROMIUM_PATH) or run `playwright install chromium`
python pipeline/render.py content/posts/page_a/<post>.json     # slides -> out/<page>/<post>/slide_NN.png
python pipeline/reel.py out/.../slide_01.png out/reel.mp4      # static-image Reel (ffmpeg)
python pipeline/approve.py list|approve|reject <post.json>     # owner approval gate
python pipeline/publish.py [--live]                            # publishes approved + due posts (dry-run by default)
```
Content lives in `content/pages/*.json` (brand) and `content/posts/<page>/*.json` (posts, `status`: draft/approved/published/rejected).
`publish.py` has not yet been run against the live Instagram API.
