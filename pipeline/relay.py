"""Research relay: runs inside GitHub Actions (open internet) so Claude Code can get info it can't reach.

Each file research/requests/<id>.json is processed once; output goes to research/answers/<id>/.

Request format:
{
  "fetch": ["https://..."],                 # public pages, saved as text (direct fetch, r.jina.ai fallback)
  "search": {"queries": ["..."], "top": 3}, # free web search (DuckDuckGo HTML, Bing fallback); top N result pages are fetched too
  "ask": {                                   # optional LLM call, needs a repo secret for the provider
    "provider": "gemini" | "groq" | "openai",
    "model": "gemini-3.8-flash",             # optional
    "grounding": true,                       # gemini: Google Search; groq uses groq/compound (built-in search)
    "use_fetched": false,                    # include fetched page text as context
    "prompt": "..."
  }
}
Secrets (env): GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY
"""
import html
import json
import os
import pathlib
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ, ANS = ROOT / "research" / "requests", ROOT / "research" / "answers"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
MAX_PAGE = 80_000


def http(url, data=None, headers=None, timeout=90):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def strip_html(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", "\n", raw)
    raw = html.unescape(raw)
    return re.sub(r"\n\s*\n+", "\n\n", re.sub(r"[ \t]+", " ", raw)).strip()


def fetch(url):
    try:
        text = strip_html(http(url))
        if len(text) > 1500:
            return "direct", text[:MAX_PAGE]
    except Exception as e:
        text = f"(direct fetch failed: {e})"
    try:
        return "r.jina.ai", http("https://r.jina.ai/" + url, headers={"Accept": "text/plain"})[:MAX_PAGE]
    except Exception as e:
        return "failed", f"{text}\n(jina fallback failed: {e})"


def web_search(query, n=8):
    """Return [(title, url)] from DuckDuckGo HTML, falling back to Bing."""
    out = []
    try:
        page = http("https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query))
        for href, title in re.findall(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', page, re.S):
            m = re.search(r"uddg=([^&]+)", href)
            url = urllib.parse.unquote(m.group(1)) if m else href
            out.append((strip_html(title), url))
    except Exception:
        pass
    if not out:
        try:
            page = http("https://www.bing.com/search?q=" + urllib.parse.quote(query))
            for url, title in re.findall(r'<li class="b_algo".*?<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', page, re.S):
                out.append((strip_html(title), url))
        except Exception:
            pass
    return out[:n]


def post_json(url, body, headers, tries=4):
    for i in range(tries):
        try:
            return json.loads(http(url, json.dumps(body).encode(), {"Content-Type": "application/json", **headers}, timeout=180))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:500]
            if e.code in (429, 500, 503) and i < tries - 1:
                time.sleep(20 * (i + 1))
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")


def ask_llm(a, context):
    prompt = a["prompt"] + (f"\n\n--- FETCHED PAGES ---\n{context}" if context else "")
    sysmsg = a.get("system", "Be accurate. Cite a URL for each claim. Never invent handles, numbers or quotes; write 'unverified' when unsure.")
    p = a["provider"]
    if p == "gemini":
        model = a.get("model", "gemini-3.8-flash")
        body = {"systemInstruction": {"parts": [{"text": sysmsg}]},
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": a.get("max_tokens", 12000)}}
        if a.get("grounding"):
            body["tools"] = [{"google_search": {}}]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        try:
            r = post_json(url, body, {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
        except RuntimeError as e:
            if not a.get("grounding"):
                raise
            body.pop("tools")
            r = post_json(url, body, {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
            return f"> NOTE: grounded search failed ({e}); answer below is from the model WITHOUT live search.\n\n" + _gem(r)
        return _gem(r)
    if p in ("groq", "openai"):
        base, key = ("https://api.groq.com/openai/v1", "GROQ_API_KEY") if p == "groq" else ("https://api.openai.com/v1", "OPENAI_API_KEY")
        model = a.get("model", "groq/compound" if p == "groq" else "gpt-5-mini")
        r = post_json(f"{base}/chat/completions", {"model": model, "messages": [
            {"role": "system", "content": sysmsg}, {"role": "user", "content": prompt}]},
            {"Authorization": f"Bearer {os.environ[key]}"})
        return r["choices"][0]["message"]["content"]
    raise RuntimeError(f"unknown provider {p}")


def _gem(r):
    c = r["candidates"][0]
    text = "".join(p.get("text", "") for p in c["content"].get("parts", []))
    srcs = c.get("groundingMetadata", {}).get("groundingChunks", [])
    links = "\n".join(f"- {s['web'].get('title','')} {s['web'].get('uri','')}" for s in srcs if "web" in s)
    return text + (f"\n\n### Grounding sources\n{links}" if links else "")


def main():
    for f in sorted(REQ.glob("*.json")):
        out = ANS / f.stem
        if (out / "done.json").exists():
            continue
        out.mkdir(parents=True, exist_ok=True)
        req = json.loads(f.read_text())
        log, context = [], []
        for i, url in enumerate(req.get("fetch", []), 1):
            how, text = fetch(url)
            (out / f"page_{i:02d}.txt").write_text(f"URL: {url}\nMETHOD: {how}\n\n{text}\n")
            log.append(f"- page_{i:02d}.txt  {how}  {len(text)} chars  {url}")
            context.append(f"## {url}\n{text[:20000]}")
        sq = req.get("search")
        if sq:
            lines, seen = [], set(req.get("fetch", []))
            for q in sq["queries"]:
                results = web_search(q)
                lines.append(f"### {q}")
                lines += [f"- {t} {u}" for t, u in results] or ["- (no results)"]
                for t, u in results[: sq.get("top", 3)]:
                    if u in seen:
                        continue
                    seen.add(u)
                    i = len(log) + 1
                    how, text = fetch(u)
                    (out / f"page_{i:02d}.txt").write_text(f"URL: {u}\nQUERY: {q}\nMETHOD: {how}\n\n{text}\n")
                    log.append(f"- page_{i:02d}.txt  {how}  {len(text)} chars  {u}  (query: {q})")
                    context.append(f"## {u}\n{text[:20000]}")
            (out / "search_results.md").write_text("\n".join(lines) + "\n")
        answer = ""
        if req.get("ask"):
            try:
                answer = ask_llm(req["ask"], "\n\n".join(context) if req["ask"].get("use_fetched") else "")
            except Exception as e:
                answer = f"ERROR calling {req['ask'].get('provider')}: {e}"
        (out / "answer.md").write_text(f"# {f.stem}\n\n## Fetched\n" + "\n".join(log) + f"\n\n## Answer\n{answer}\n")
        (out / "done.json").write_text(json.dumps({"finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}))
        print("processed", f.name)


if __name__ == "__main__":
    main()
