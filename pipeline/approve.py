"""Approve or reject draft posts. Approval is the owner's gate: publish.py only posts 'approved'.

Usage:
  python pipeline/approve.py list
  python pipeline/approve.py approve content/posts/page_a/<post>.json [more...]
  python pipeline/approve.py reject  content/posts/page_a/<post>.json
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    cmd, *files = sys.argv[1:] or ["list"]
    if cmd == "list":
        for f in sorted((ROOT / "content" / "posts").rglob("*.json")):
            p = json.loads(f.read_text())
            print(f"{p.get('status','?'):10} {p['publish_at'][:16]}  {f.relative_to(ROOT)}  | {p['slides'][0]['text'][:60]}")
        return
    status = {"approve": "approved", "reject": "rejected"}[cmd]
    for name in files:
        f = pathlib.Path(name)
        p = json.loads(f.read_text())
        p["status"] = status
        f.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n")
        print(f"{status}: {f}")


if __name__ == "__main__":
    main()
