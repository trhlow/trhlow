"""Generate the flat animated SVGs used by the profile README.

Usage: python tools/generate_assets.py .
"""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', Consolas, Menlo, monospace"
W = 880
DURATION = 9  # seconds for one full pass
TRAVEL = 88  # % of the loop spent moving; the rest is a short rest and fade

THEMES = {
    "dark": {"text": "#e6edf3", "muted": "#8b949e", "line": "#30363d", "accent": "#3fb950"},
    "light": {"text": "#1f2328", "muted": "#59636e", "line": "#d1d9e0", "accent": "#1a7f37"},
}

FLOWS = {
    "flow-tvu": ["Register", "Organizer approves", "Signed QR ticket", "One-time check-in"],
    "flow-cambridge": ["Import paper", "Open session", "Live proctoring", "Grading"],
    "flow-cong-tin": ["Search listings", "Verify phone OTP", "Book a viewing", "Broker confirms"],
}
HEADER_FLOW = ["request", "controller", "service", "repository", "database"]


def pipeline(labels, y, theme, family, size):
    """A line of nodes with a dot that walks along it, returning (svg, css)."""
    t = THEMES[theme]
    n = len(labels)
    x0, x1 = 8, W - 8
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    length = x1 - x0
    step = TRAVEL / (n - 1)
    rest = TRAVEL + 6

    move, draw, css = [], [], []
    for i, x in enumerate(xs):
        arrive = i * step
        move.append(f"{arrive:.1f}%{{transform:translateX({x:.1f}px);opacity:1}}")
        draw.append(f"{arrive:.1f}%{{stroke-dashoffset:{length - (x - x0):.1f};opacity:1}}")
        if i < n - 1:
            hold = arrive + step * 0.35
            move.append(f"{hold:.1f}%{{transform:translateX({x:.1f}px);opacity:1}}")
            draw.append(f"{hold:.1f}%{{stroke-dashoffset:{length - (x - x0):.1f};opacity:1}}")
    move.append(f"{rest}%{{transform:translateX({x1:.1f}px);opacity:1}}")
    move.append(f"100%{{transform:translateX({x1:.1f}px);opacity:0}}")
    draw.append(f"{rest}%{{stroke-dashoffset:0;opacity:1}}")
    draw.append("100%{stroke-dashoffset:0;opacity:0}")

    css.append(f".dot{{animation:dot {DURATION}s ease-in-out infinite}}@keyframes dot{{{''.join(move)}}}")
    css.append(f".trail{{animation:trail {DURATION}s ease-in-out infinite}}@keyframes trail{{{''.join(draw)}}}")

    out = [
        f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{t["line"]}" stroke-width="1.5"/>',
        f'<line class="trail" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{t["accent"]}" stroke-width="1.5" '
        f'stroke-dasharray="{length}" stroke-dashoffset="{length}"/>',
    ]
    for i, (x, label) in enumerate(zip(xs, labels)):
        arrive = i * step
        anchor = "start" if i == 0 else "end" if i == n - 1 else "middle"
        lx = 0 if i == 0 else W if i == n - 1 else x
        css.append(f".n{i}{{animation:n{i} {DURATION}s linear infinite}}"
                   f"@keyframes n{i}{{0%,{max(arrive - 0.1, 0):.1f}%{{opacity:0}}"
                   f"{arrive:.1f}%,{rest}%{{opacity:1}}100%{{opacity:0}}}}")
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="5" fill="none" stroke="{t["muted"]}" stroke-width="1.5"/>')
        out.append(f'<circle class="n{i}" cx="{x:.1f}" cy="{y}" r="5" fill="{t["accent"]}" opacity="0"/>')
        out.append(f'<text x="{lx:.1f}" y="{y + 28}" text-anchor="{anchor}" font-family="{family}" '
                   f'font-size="{size}" fill="{t["muted"]}">{escape(label)}</text>')
    out.append(f'<circle class="dot" cx="0" cy="{y}" r="3" fill="{t["accent"]}"/>')
    return "\n".join(out), "\n".join(css)


def document(height, body, css):
    style = css + "\n@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" role="img">\n'
            f"<style>\n{style}\n</style>\n{body}\n</svg>\n")


def save(name, content):
    path = os.path.join(OUT, "assets", name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def header(theme):
    t = THEMES[theme]
    flow, css = pipeline(HEADER_FLOW, 132, theme, MONO, 13)
    body = (f'<text x="0" y="48" font-family="{SANS}" font-size="40" font-weight="600" fill="{t["text"]}">Trần Hoàng Long</text>\n'
            f'<text x="0" y="84" font-family="{SANS}" font-size="18" fill="{t["muted"]}">Backend Java Developer · Vinh Long, Viet Nam</text>\n'
            f"{flow}")
    save(f"header-{theme}.svg", document(190, body, css))


def flows(theme):
    for name, labels in FLOWS.items():
        flow, css = pipeline(labels, 10, theme, SANS, 14)
        save(f"{name}-{theme}.svg", document(52, flow, css))


for theme in THEMES:
    header(theme)
    flows(theme)
print("ok")
