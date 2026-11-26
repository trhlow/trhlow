"""Rebuild the pinned-repo cards in both READMEs from repos tagged with the `showcase` topic.

Run by .github/workflows/update-readme.yml. Only the owner's own repos count (no forks, no archived).
"""
import json
import os
import re
import sys
import urllib.request

OWNER = os.environ.get("OWNER", "trhlow")
TOPIC = "showcase"
READMES = {"README.md": "", "README.vi.md": "&locale=vi"}
BLOCK = re.compile(r"(<!-- showcase:start -->\n).*?(<!-- showcase:end -->)", re.S)


def showcase(repos):
    picked = [r for r in repos if TOPIC in r.get("topics", []) and not r["fork"] and not r["archived"] and r["name"] != OWNER]
    return [r["name"] for r in sorted(picked, key=lambda r: r["pushed_at"], reverse=True)]


def cards(names, locale):
    card = ('<a href="https://github.com/{o}/{n}">\n  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/'
            '?username={o}&repo={n}&theme=tokyonight{l}" />\n</a>')
    rows = [names[i:i + 2] for i in range(0, len(names), 2)]  # two cards per row
    return "\n\n".join("\n".join(card.format(o=OWNER, n=n, l=locale) for n in row) for row in rows) + "\n"


def fetch():
    req = urllib.request.Request(f"https://api.github.com/users/{OWNER}/repos?per_page=100&type=owner",
                                 headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main():
    names = showcase(fetch())
    if not names:
        # an empty list is far more likely a missing tag or an API hiccup than intent; keep what is there
        print(f"no repo has the '{TOPIC}' topic; READMEs left unchanged")
        return
    for path, locale in READMES.items():
        text = open(path, encoding="utf-8").read()
        assert BLOCK.search(text), f"{path} is missing the showcase markers"
        new = BLOCK.sub(lambda m: m.group(1) + cards(names, locale) + m.group(2), text)
        if new != text:
            open(path, "w", encoding="utf-8", newline="\n").write(new)
    print("showcase:", ", ".join(names))


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        repo = lambda n, d, **k: {"name": n, "pushed_at": d, "fork": False, "archived": False, "topics": [TOPIC], **k}
        got = showcase([repo("a", "2026-01-01"), repo("b", "2026-03-01"), repo("fork", "2026-05-01", fork=True),
                        repo("old", "2026-05-01", archived=True), repo("plain", "2026-05-01", topics=[]), repo(OWNER, "2026-05-01")])
        assert got == ["b", "a"], got
        out = cards(["a", "b", "c"], "&locale=vi")
        assert out.count("<a ") == 3 and out.count("\n\n") == 1 and "repo=c&theme=tokyonight&locale=vi" in out, out
        print("self-test ok")
    else:
        main()
