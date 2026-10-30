"""Generate the flat animated SVG scenes used by the profile README.

Usage: pip install segno && python tools/generate_assets.py .

Every scene is drawn in its finished state, so it still reads correctly as a
still image or with reduced motion; animation only replays how it got there.
"""
import math
import os
import random
import sys
from xml.sax.saxutils import escape

import segno

OUT = sys.argv[1]
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', Consolas, Menlo, monospace"
W = 880
EMAIL = "thlong190705@gmail.com"

THEMES = {
    "dark": {"text": "#e6edf3", "muted": "#8b949e", "line": "#30363d", "accent": "#3fb950", "warm": "#d29922", "bg": "#0d1117"},
    "light": {"text": "#1f2328", "muted": "#59636e", "line": "#d1d9e0", "accent": "#1a7f37", "warm": "#9a6700", "bg": "#ffffff"},
}


# Scene wording for the Vietnamese README; anything not listed stays as written.
VI = {
    "Backend Java Developer · Vinh Long, Viet Nam": "Lập trình viên Backend Java · Vĩnh Long, Việt Nam",
    "STAGE": "SÂN KHẤU",
    "SOLD OUT · 0 OVERSOLD": "HẾT VÉ · KHÔNG BÁN VƯỢT",
    "approvals processed": "lượt duyệt đã xử lý",
    "tickets issued": "vé đã phát hành",
    "still pending, no seat taken": "vẫn chờ duyệt, không giữ ghế",
    "A2 Key · Reading and Writing": "A2 Key · Đọc và Viết",
    "live over SignalR": "trực tiếp qua SignalR",
    "server clock": "đồng hồ server",
    "paused": "tạm dừng",
    "18 candidates online · no incidents": "18 thí sinh trực tuyến · không có sự cố",
    "proctor → C08: pause": "giám thị → C08: tạm dừng",
    "proctor → C08: add 2 minutes": "giám thị → C08: cộng 2 phút",
    "proctor → C08: resume": "giám thị → C08: làm tiếp",
    "Enter SMS code": "Nhập mã SMS",
    "Viewing booked": "Đã đặt lịch xem",
    "Broker confirmed": "Môi giới xác nhận",
    "ADMIT ONE": "VÉ VÀO CỬA",
    "No. 0001": "Số 0001",
    "LANGUAGES": "NGÔN NGỮ",
    "DATA": "DỮ LIỆU",
    "INFRA": "HẠ TẦNG",
    "scan to say hi": "quét để làm quen",
    "CHECKED IN": "ĐÃ SOÁT VÉ",
}
lang = "en"


def text(x, y, value, fill, size=14, family=SANS, anchor="start", weight=400, extra=""):
    if lang == "vi":
        value = VI.get(value, value)
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>')


def document(height, body, css):
    style = css + "\n@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" role="img">\n'
            f"<style>\n{style}\n</style>\n{body}\n</svg>\n")


def save(name, content):
    path = os.path.join(OUT, "assets", "" if lang == "en" else lang, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def reel(name, x, y, values, keyframes, duration, fill, size=30, anchor="start"):
    """A clipped column of numbers that rolls; it rests on the last value."""
    lh = size + 8
    end = -(len(values) - 1) * lh
    rows = "".join(f'<text y="{i * lh}">{escape(str(v))}</text>' for i, v in enumerate(values))
    frames = "".join(f"{p}%{{transform:translateY({v * lh}px);{t}}}" for p, v, t in keyframes)
    css = (f".{name}{{transform:translateY({end}px);animation:{name} {duration}s linear infinite}}"
           f"@keyframes {name}{{{frames}}}")
    box_w = size * 6
    box_x = x if anchor == "start" else x - box_w
    svg = (f'<clipPath id="c-{name}"><rect x="{box_x}" y="{y - size}" width="{box_w}" height="{lh}"/></clipPath>'
           f'<g clip-path="url(#c-{name})"><g transform="translate({x} {y})" font-family="{MONO}" font-size="{size}" '
           f'font-weight="600" fill="{fill}" text-anchor="{anchor}"><g class="{name}">{rows}</g></g></g>')
    return svg, css


# ---------------------------------------------------------------------------
# Header: a request is a boat calling at each pier on a Mekong Delta river.
# ---------------------------------------------------------------------------
def palm(x, base, height, lean, t, delay):
    tx, ty = x + lean, base - height
    fronds = []
    for dx, dy in ((-34, 14), (-26, -8), (-6, -18), (18, -12), (34, 12)):
        cx, cy = tx + dx * 0.55, ty + dy - 12
        fronds.append(f"M{tx} {ty} Q{cx:.0f} {cy:.0f} {tx + dx} {ty + dy}")
    return (f'<path d="M{x} {base} Q{x + lean * 0.2:.0f} {base - height * 0.55:.0f} {tx} {ty}" fill="none" stroke="{t["muted"]}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<g style="transform-origin:{tx}px {ty}px;animation:sway 6s ease-in-out {delay}s infinite">'
            f'<path d="{" ".join(fronds)}" fill="none" stroke="{t["muted"]}" stroke-width="1.8" stroke-linecap="round"/></g>')


def waves(t):
    out, css = [], []
    for i, (y, speed) in enumerate(((222, 9), (240, 13), (258, 7))):
        d = f"M-160 {y} q20 -4 40 0 " + "t40 0 " * 28
        out.append(f'<path class="w{i}" d="{d}" fill="none" stroke="{t["line"]}" stroke-width="1.5" stroke-dasharray="{70 + i * 20} {90 - i * 20}"/>')
        css.append(f".w{i}{{animation:drift {speed}s linear infinite}}")
    css.append("@keyframes drift{to{transform:translateX(160px)}}")
    return "".join(out), "\n".join(css)


def boat(t):
    return (f'<path d="M-44 0 Q-30 15 0 15 Q30 15 46 -5 Q20 3 -44 0 Z" fill="{t["bg"]}" stroke="{t["text"]}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M-26 1 Q-24 -18 -4 -18 Q12 -18 14 0" fill="{t["bg"]}" stroke="{t["muted"]}" stroke-width="1.8"/>'
            f'<line x1="-40" y1="-1" x2="-52" y2="20" stroke="{t["muted"]}" stroke-width="1.8" stroke-linecap="round"/>'
            f'<rect x="20" y="-11" width="11" height="11" rx="2" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="1.8"/>'
            f'<rect class="cargo" x="20" y="-11" width="11" height="11" rx="2" fill="{t["accent"]}"/>')


def header(theme):
    t = THEMES[theme]
    T = 22
    piers = [(60, "client"), (250, "controller"), (440, "service"), (630, "repository"), (820, "database")]
    xs = [x for x, _ in piers]
    n = len(xs)
    # Hold at each pier on the way out, then again on the way back.
    stops = xs + xs[-2::-1]
    span = 96 / (len(stops) - 1)
    frames = []
    for i, x in enumerate(stops):
        arrive = i * span
        frames.append(f"{arrive:.1f}%{{transform:translate({x}px,212px)}}")
        if i < len(stops) - 1:
            frames.append(f"{arrive + span * 0.4:.1f}%{{transform:translate({x}px,212px)}}")
    frames.append(f"100%{{transform:translate({xs[0]}px,212px)}}")
    turn = (n - 1) * span + span * 0.2

    css = [
        f".ship{{transform:translate({xs[0]}px,212px);animation:ship {T}s ease-in-out infinite}}@keyframes ship{{{''.join(frames)}}}",
        f".hull{{animation:hull {T}s steps(1,end) infinite}}@keyframes hull{{0%{{transform:scaleX(1)}}{turn:.1f}%{{transform:scaleX(-1)}}100%{{transform:scaleX(1)}}}}",
        ".bob{animation:bob 3.2s ease-in-out infinite}@keyframes bob{50%{transform:translateY(3px) rotate(-1.2deg)}}",
        f".cargo{{animation:cargo {T}s steps(1,end) infinite}}@keyframes cargo{{0%{{opacity:0}}{turn:.1f}%{{opacity:1}}100%{{opacity:0}}}}",
        f".req{{animation:req {T}s steps(1,end) infinite}}@keyframes req{{0%{{opacity:1}}{turn:.1f}%{{opacity:0}}100%{{opacity:1}}}}",
        f".res{{animation:res {T}s steps(1,end) infinite}}@keyframes res{{0%{{opacity:0}}{turn:.1f}%{{opacity:1}}100%{{opacity:0}}}}",
        "@keyframes sway{50%{transform:rotate(3deg)}}",
        ".tw{animation:tw 4s ease-in-out infinite}@keyframes tw{50%{opacity:.25}}",
        ".fly{animation:fly 26s linear infinite}@keyframes fly{from{transform:translateX(-60px)}to{transform:translateX(960px)}}",
    ]
    wave_svg, wave_css = waves(t)
    css.append(wave_css)

    b = [text(0, 48, "Trần Hoàng Long", t["text"], 40, weight=600),
         text(0, 84, "Backend Java Developer · Vinh Long, Viet Nam", t["muted"], 18)]

    if theme == "dark":
        b.append(f'<path d="M806 30 a26 26 0 1 0 24 40 a21 21 0 1 1 -24 -40 Z" fill="none" stroke="{t["muted"]}" stroke-width="1.8"/>')
        for i, (sx, sy) in enumerate(((610, 34), (668, 74), (726, 22), (560, 92), (760, 104), (852, 92), (520, 46))):
            b.append(f'<circle class="tw" cx="{sx}" cy="{sy}" r="1.5" fill="{t["muted"]}" style="animation-delay:{i * 0.6:.1f}s"/>')
    else:
        rays = "".join(f'<line x1="{800 + 30 * math.cos(a):.1f}" y1="{56 + 30 * math.sin(a):.1f}" x2="{800 + 38 * math.cos(a):.1f}" y2="{56 + 38 * math.sin(a):.1f}"/>'
                       for a in (i * math.pi / 6 for i in range(12)))
        b.append(f'<circle cx="800" cy="56" r="22" fill="none" stroke="{t["muted"]}" stroke-width="1.8"/>')
        b.append(f'<g stroke="{t["muted"]}" stroke-width="1.8" stroke-linecap="round" style="transform-origin:800px 56px;animation:spin 40s linear infinite">{rays}</g>')
        css.append("@keyframes spin{to{transform:rotate(360deg)}}")
        b.append(f'<g class="fly"><path d="M0 40 q7 -7 13 0 q7 -7 13 0 M40 62 q6 -6 11 0 q6 -6 11 0" fill="none" stroke="{t["muted"]}" stroke-width="1.5" stroke-linecap="round"/></g>')

    b.append('<g transform="translate(0 34)">')
    for x, height, lean, delay in ((156, 88, 12, 0), (346, 72, -10, -2), (532, 94, 10, -3.5), (726, 70, -8, -1.2)):
        b.append(palm(x, 190, height, lean, t, delay))
    b.append(f'<path d="M0 192 q110 -5 220 0 t220 0 t220 0 t220 0" fill="none" stroke="{t["muted"]}" stroke-width="1.8"/>')

    for i, (x, label) in enumerate(piers):
        out_at, back_at = i * span, (len(stops) - 1 - i) * span
        css.append(f".l{i}{{animation:l{i} {T}s steps(1,end) infinite}}"
                   f"@keyframes l{i}{{0%{{opacity:{1 if i == 0 else 0}}}{out_at:.1f}%{{opacity:1}}{back_at + span * 0.4:.1f}%{{opacity:{1 if i == 0 else 0}}}100%{{opacity:{1 if i == 0 else 0}}}}}")
        b.append(f'<path d="M{x - 16} 192 H{x + 16} M{x - 11} 192 V212 M{x + 11} 192 V212" stroke="{t["muted"]}" stroke-width="2" stroke-linecap="round"/>')
        b.append(f'<line x1="{x + 16}" y1="192" x2="{x + 16}" y2="170" stroke="{t["muted"]}" stroke-width="1.6"/>')
        b.append(f'<circle cx="{x + 16}" cy="166" r="4" fill="{t["bg"]}" stroke="{t["muted"]}" stroke-width="1.6"/>')
        b.append(f'<circle class="l{i}" cx="{x + 16}" cy="166" r="4" fill="{t["accent"]}"/>')
        b.append(text(x, 284, label, t["muted"], 13, MONO, "middle"))

    b.append(wave_svg)
    halo = f'stroke="{t["bg"]}" stroke-width="5" paint-order="stroke"'
    req = text(0, 36, "request", t["accent"], 12, MONO, "middle", extra=f'class="req" {halo}')
    res = text(0, 36, "response", t["accent"], 12, MONO, "middle", extra=f'class="res" {halo}')
    b.append(f'<g class="ship">{req}{res}<g class="bob"><g class="hull">{boat(t)}</g></g></g></g>')
    save(f"header-{theme}.svg", document(328, "\n".join(b), "\n".join(css)))


# ---------------------------------------------------------------------------
# TVU: 500 approvals race for 100 seats; the ticket count stops dead at 100.
# ---------------------------------------------------------------------------
def seats(theme):
    t = THEMES[theme]
    T = 15
    reset, start, full, done = 10, 13, 40, 74
    rnd = random.Random(19)
    order = list(range(100))
    rnd.shuffle(order)
    buckets = 24
    css, b = [], []

    for k in range(buckets):
        at = start + (full - start) * (k + 1) / buckets
        css.append(f".s{k}{{animation:s{k} {T}s linear infinite}}"
                   f"@keyframes s{k}{{0%,{reset - 1}%{{opacity:1}}{reset}%,{at:.1f}%{{opacity:0}}{at + 0.4:.1f}%,100%{{opacity:1}}}}")

    b.append(f'<path d="M60 26 Q250 2 440 26" fill="none" stroke="{t["muted"]}" stroke-width="1.8" stroke-linecap="round"/>')
    b.append(text(250, 34, "STAGE", t["muted"], 12, MONO, "middle"))
    x0, y0, px, py = 12, 52, 24, 24
    for i in range(100):
        col, row = i % 20, i // 20
        x, y = x0 + col * px, y0 + row * py
        seat = f'x="{x}" y="{y}" width="18" height="17" rx="4"'
        b.append(f'<rect {seat} fill="none" stroke="{t["line"]}" stroke-width="1.5"/>'
                 f'<rect class="s{order[i] % buckets}" {seat} fill="{t["accent"]}"/>')

    b.append(f'<g class="stamp" transform="rotate(-2 170 196)"><rect x="12" y="192" width="316" height="30" rx="5" fill="none" stroke="{t["accent"]}" stroke-width="1.8"/>'
             + text(170, 212, "SOLD OUT · 0 OVERSOLD", t["accent"], 15, MONO, "middle", 700, 'letter-spacing="1"') + "</g>")
    css.append(f".stamp{{animation:stamp {T}s steps(1,end) infinite}}@keyframes stamp{{0%{{opacity:1}}{reset}%{{opacity:0}}{full + 1}%{{opacity:1}}100%{{opacity:1}}}}")

    # approvals = tickets + pending at every moment of the loop
    approvals = list(range(101)) + [100 + i * 5 for i in range(1, 81)]
    tickets = list(range(101))
    pending = [i * 5 for i in range(81)]
    a_frames = [(0, -180, ""), (reset - 1, -180, ""), (reset, 0, ""), (start, 0, "animation-timing-function:steps(100,end)"),
                (full, -100, "animation-timing-function:steps(80,end)"), (done, -180, ""), (100, -180, "")]
    t_frames = [(0, -100, ""), (reset - 1, -100, ""), (reset, 0, ""), (start, 0, "animation-timing-function:steps(100,end)"), (full, -100, ""), (100, -100, "")]
    p_frames = [(0, -80, ""), (reset - 1, -80, ""), (reset, 0, ""), (full, 0, "animation-timing-function:steps(80,end)"), (done, -80, ""), (100, -80, "")]

    for name, label, values, frames, fill, y in (("ra", "approvals processed", approvals, a_frames, t["text"], 70),
                                                 ("rt", "tickets issued", tickets, t_frames, t["accent"], 142),
                                                 ("rp", "still pending, no seat taken", pending, p_frames, t["muted"], 214)):
        b.append(text(610, y - 34, label, t["muted"], 13))
        svg, c = reel(name, 610, y, values, frames, T, fill)
        b.append(svg)
        css.append(c)
    save(f"seats-{theme}.svg", document(232, "\n".join(b), "\n".join(css)))


# ---------------------------------------------------------------------------
# Cambridge: a proctor board; one candidate is paused, given time, resumed.
# ---------------------------------------------------------------------------
def proctor(theme):
    t = THEMES[theme]
    T = 18
    pause, added, resume = 26, 46, 60
    rnd = random.Random(8)
    cols, rows, tw, th, gx, gy = 6, 3, 138, 52, 10, 10
    x0, y0 = 1, 50
    bar = tw - 24
    hot = 7  # C08
    css, b = [], []
    css.append(f".board{{animation:board {T}s linear infinite}}@keyframes board{{0%,97%{{opacity:1}}98.5%{{opacity:0}}100%{{opacity:1}}}}")

    b.append(text(1, 22, "A2 Key · Reading and Writing", t["text"], 15, weight=600))
    b.append(f'<circle class="live" cx="9" cy="37" r="3.5" fill="{t["accent"]}"/>')
    css.append(".live{animation:live 2s ease-in-out infinite}@keyframes live{50%{opacity:.25}}")
    b.append(text(20, 41, "live over SignalR", t["muted"], 12, MONO))
    remaining = [f"00:{(11 * 60 + 42 - s) // 60:02d}:{(11 * 60 + 42 - s) % 60:02d}" for s in range(T + 1)]
    clock, c = reel("clock", W - 1, 34, remaining,
                    [(0, 0, f"animation-timing-function:steps({T},end)"), (100, -T, "")], T, t["text"], 26, "end")
    b.append(clock)
    css.append(c)
    b.append(text(W - 1, 11, "server clock", t["muted"], 12, MONO, "end"))

    b.append('<g class="board">')
    for i in range(cols * rows):
        col, row = i % cols, i // cols
        x, y = x0 + col * (tw + gx), y0 + row * (th + gy)
        lo, hi = rnd.uniform(0.25, 0.5), rnd.uniform(0.72, 0.97)
        a, z = bar * (1 - lo), bar * (1 - hi)
        if i == hot:
            mid = bar * (1 - (lo + (hi - lo) * pause / 100))
            frames = (f"0%{{stroke-dashoffset:{a:.1f}}}{pause}%,{resume}%{{stroke-dashoffset:{mid:.1f}}}100%{{stroke-dashoffset:{z:.1f}}}")
        else:
            frames = f"0%{{stroke-dashoffset:{a:.1f}}}100%{{stroke-dashoffset:{z:.1f}}}"
        css.append(f".b{i}{{stroke-dashoffset:{z:.1f};animation:b{i} {T}s linear infinite}}@keyframes b{i}{{{frames}}}")
        b.append(f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="6" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>')
        b.append(text(x + 12, y + 22, f"C{i + 1:02d}", t["text"], 13, MONO))
        if i == hot:
            b.append(f'<g class="on-hold"><rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="6" fill="none" stroke="{t["warm"]}" stroke-width="2"/>'
                     + text(x + tw - 12, y + 22, "paused", t["warm"], 12, MONO, "end") + "</g>")
            b.append(f'<g class="grant">{text(x + tw - 12, y + 22, "+2:00", t["accent"], 12, MONO, "end", 700)}</g>')
        b.append(f'<line x1="{x + 12}" y1="{y + 37}" x2="{x + 12 + bar}" y2="{y + 37}" stroke="{t["line"]}" stroke-width="3" stroke-linecap="round"/>')
        b.append(f'<line class="b{i}" x1="{x + 12}" y1="{y + 37}" x2="{x + 12 + bar}" y2="{y + 37}" stroke="{t["accent"]}" stroke-width="3" stroke-linecap="round" stroke-dasharray="{bar}"/>')
    b.append("</g>")

    logs = [("proctor → C08: pause", pause, added), ("proctor → C08: add 2 minutes", added, resume), ("proctor → C08: resume", resume, 80)]
    y = y0 + rows * (th + gy) + 18
    idle = "18 candidates online · no incidents"
    b.append(f'<g class="idle">{text(1, y, idle, t["muted"], 13, MONO)}</g>')
    css.append(f".idle{{animation:idle {T}s steps(1,end) infinite}}@keyframes idle{{0%{{opacity:1}}{pause}%{{opacity:0}}80%{{opacity:1}}100%{{opacity:1}}}}")
    for i, (msg, s, e) in enumerate(logs):
        b.append(f'<g class="log{i}">{text(1, y, msg, t["warm"] if i == 0 else t["accent"], 13, MONO)}</g>')
        css.append(f".log{i}{{opacity:0;animation:log{i} {T}s steps(1,end) infinite}}@keyframes log{i}{{0%{{opacity:0}}{s}%{{opacity:1}}{e}%{{opacity:0}}100%{{opacity:0}}}}")
    css.append(f".on-hold{{opacity:0;animation:hold {T}s steps(1,end) infinite}}@keyframes hold{{0%{{opacity:0}}{pause}%{{opacity:1}}{resume}%{{opacity:0}}100%{{opacity:0}}}}")
    css.append(f".grant{{opacity:0;animation:grant {T}s steps(1,end) infinite}}@keyframes grant{{0%{{opacity:0}}{resume}%{{opacity:1}}82%{{opacity:0}}100%{{opacity:0}}}}")
    save(f"proctor-{theme}.svg", document(y0 + rows * (th + gy) + 30, "\n".join(b), "\n".join(css)))


# ---------------------------------------------------------------------------
# Công Tín Land: a pin picks a place, the phone verifies, the broker confirms.
# ---------------------------------------------------------------------------
def street(theme):
    t = THEMES[theme]
    T = 16
    ground = 186
    line = f'stroke="{t["muted"]}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" fill="none"'
    b, css = [], []

    # phòng trọ: a row of rooms
    rooms = [f'<path d="M20 {ground} V118 H210 V{ground}" {line}/>', f'<path d="M12 118 H218" {line}/>']
    for i in range(4):
        x = 34 + i * 45
        rooms.append(f'<rect x="{x}" y="{ground - 40}" width="20" height="40" rx="1" {line}/>'
                     f'<rect x="{x + 1}" y="132" width="18" height="14" rx="1" {line}/>')
    b.append("".join(rooms))
    # nhà: a house with a tiled roof
    b.append(f'<path d="M290 {ground} V106 H420 V{ground}" {line}/><path d="M276 110 L355 58 L434 110" {line}/>'
             f'<rect x="340" y="{ground - 46}" width="30" height="46" rx="1" {line}/>'
             f'<rect x="304" y="124" width="24" height="24" rx="1" {line}/><rect x="382" y="124" width="24" height="24" rx="1" {line}/>'
             f'<path d="M388 74 V58 H402 V83" {line}/>')
    # đất: a staked plot
    stakes = "".join(f'<path d="M{x} {ground} V{ground - 16}" {line}/>' for x in range(490, 640, 30))
    b.append(stakes + f'<path d="M490 {ground - 12} H610" stroke="{t["muted"]}" stroke-width="1.4" stroke-dasharray="4 4" fill="none"/>')
    b.append(f'<path d="M0 {ground} H640" {line}/>')
    for x, label in ((115, "Trọ"), (355, "Nhà"), (550, "Đất")):
        b.append(text(x, ground + 22, label, t["muted"], 13, SANS, "middle"))

    # the pin visits each plot and settles on the house
    stops = [(115, 92), (550, 138), (355, 46)]
    frames = [f"0%,6%{{transform:translate({stops[2][0]}px,{stops[2][1]}px)}}", f"8%,20%{{transform:translate({stops[0][0]}px,{stops[0][1]}px)}}",
              f"30%,40%{{transform:translate({stops[1][0]}px,{stops[1][1]}px)}}", f"50%,100%{{transform:translate({stops[2][0]}px,{stops[2][1]}px)}}"]
    css.append(f".pin{{transform:translate({stops[2][0]}px,{stops[2][1]}px);animation:pin {T}s ease-in-out infinite}}@keyframes pin{{{''.join(frames)}}}")
    css.append(".hop{animation:hop 1.8s ease-in-out infinite}@keyframes hop{50%{transform:translateY(-6px)}}")
    b.append(f'<g class="pin"><g class="hop"><path d="M0 0 C-14 -16 -14 -32 0 -32 C14 -32 14 -16 0 0 Z" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="2"/>'
             f'<circle cy="-21" r="4.5" fill="{t["accent"]}"/></g></g>')

    # phone: OTP boxes fill in, then the booking is confirmed
    px, py, pw, ph = 690, 8, 128, 196
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="none" stroke="{t["muted"]}" stroke-width="2"/>')
    b.append(f'<line x1="{px + 48}" y1="{py + 13}" x2="{px + 80}" y2="{py + 13}" stroke="{t["muted"]}" stroke-width="2" stroke-linecap="round"/>')
    b.append(text(px + pw / 2, py + 42, "Enter SMS code", t["muted"], 12, SANS, "middle"))
    digits = "482915"
    for i, d in enumerate(digits):
        x = px + 12 + i * 18
        at = 52 + i * 2.6
        b.append(f'<rect x="{x}" y="{py + 54}" width="15" height="21" rx="3" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>')
        b.append(f'<g class="d{i}">{text(x + 7.5, py + 70, d, t["text"], 13, MONO, "middle", 600)}</g>')
        css.append(f".d{i}{{animation:d{i} {T}s steps(1,end) infinite}}@keyframes d{i}{{0%{{opacity:1}}5%{{opacity:0}}{at:.1f}%{{opacity:1}}100%{{opacity:1}}}}")
    cy = py + 112
    b.append(f'<g class="ok"><circle cx="{px + pw / 2}" cy="{cy}" r="17" fill="{t["accent"]}"/>'
             f'<path d="M{px + pw / 2 - 8} {cy} l6 6 l10 -11" fill="none" stroke="{t["bg"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>')
    b.append(f'<g class="ok">{text(px + pw / 2, cy + 36, "Viewing booked", t["text"], 12.5, SANS, "middle", 600)}</g>')
    b.append(f'<g class="brk">{text(px + pw / 2, cy + 56, "Broker confirmed", t["accent"], 12, SANS, "middle")}</g>')
    css.append(f".ok{{animation:ok {T}s steps(1,end) infinite}}@keyframes ok{{0%{{opacity:1}}5%{{opacity:0}}70%{{opacity:1}}100%{{opacity:1}}}}")
    css.append(f".brk{{animation:brk {T}s steps(1,end) infinite}}@keyframes brk{{0%{{opacity:1}}5%{{opacity:0}}82%{{opacity:1}}100%{{opacity:1}}}}")
    save(f"street-{theme}.svg", document(216, "\n".join(b), "\n".join(css)))


# ---------------------------------------------------------------------------
# Ticket: the stack as an admission ticket with a real, scannable QR code.
# ---------------------------------------------------------------------------
def ticket(theme):
    t = THEMES[theme]
    T = 7
    L, H, cut, notch = W - 2, 236, 650, 11
    outline = (f"M13 1 H{cut - notch} a{notch} {notch} 0 0 0 {notch * 2} 0 H{L - 11} a12 12 0 0 1 12 12 V{H - 13} a12 12 0 0 1 -12 12 "
               f"H{cut + notch} a{notch} {notch} 0 0 0 {-notch * 2} 0 H13 a12 12 0 0 1 -12 -12 V13 a12 12 0 0 1 12 -12 Z")
    b = [f'<path d="{outline}" fill="none" stroke="{t["muted"]}" stroke-width="1.8"/>',
         f'<line x1="{cut}" y1="20" x2="{cut}" y2="{H - 18}" stroke="{t["muted"]}" stroke-width="1.5" stroke-dasharray="3 7"/>',
         text(28, 36, "ADMIT ONE", t["muted"], 12, MONO, extra='letter-spacing="3"'),
         text(622, 36, "No. 0001", t["muted"], 12, MONO, "end"),
         text(28, 72, "Trần Hoàng Long", t["text"], 26, weight=600)]
    rows = (("LANGUAGES", "Java · C# · TypeScript"),
            ("BACKEND", "Spring Boot · Spring Security · ASP.NET Core"),
            ("DATA", "PostgreSQL · MySQL · MongoDB · Redis · RabbitMQ"),
            ("FRONTEND", "React · Tailwind CSS"),
            ("INFRA", "Docker · Caddy · GitHub Actions"))
    for i, (key, value) in enumerate(rows):
        y = 106 + i * 24
        b.append(text(28, y, key, t["muted"], 12, MONO))
        b.append(text(136, y, value, t["text"], 14))

    qr = segno.make(f"mailto:{EMAIL}", error="m", boost_error=False)
    matrix = [list(row) for row in qr.matrix]
    size = len(matrix)
    quiet = 3
    box = 164
    m = box / (size + quiet * 2)
    qx, qy = cut + (L - cut - box) / 2, 18
    # a white panel keeps the code scannable on both themes
    b.append(f'<rect x="{qx:.1f}" y="{qy}" width="{box}" height="{box}" rx="6" fill="#ffffff"/>')
    d = "".join(f"M{qx + (quiet + c) * m:.2f} {qy + (quiet + r) * m:.2f}h{m:.2f}v{m:.2f}h{-m:.2f}z"
                for r, row in enumerate(matrix) for c, v in enumerate(row) if v)
    b.append(f'<path d="{d}" fill="#1f2328" shape-rendering="crispEdges"/>')
    b.append(f'<line class="scan" x1="{qx - 6:.1f}" y1="{qy + 6}" x2="{qx + box + 6:.1f}" y2="{qy + 6}" stroke="{t["accent"]}" stroke-width="2.4" stroke-linecap="round"/>')
    b.append(text(qx + box / 2, qy + box + 26, "scan to say hi", t["muted"], 13, MONO, "middle"))

    css = [f".scan{{animation:scan {T}s ease-in-out infinite}}@keyframes scan{{0%{{transform:translateY(0);opacity:0}}6%{{opacity:1}}45%{{transform:translateY({box - 12}px);opacity:1}}50%,100%{{transform:translateY({box - 12}px);opacity:0}}}}",
           f".stamp{{animation:stamp {T}s steps(1,end) infinite}}@keyframes stamp{{0%{{opacity:1}}4%{{opacity:0}}48%{{opacity:1}}100%{{opacity:1}}}}"]
    b.append(f'<g class="stamp" transform="rotate(-7 530 186)"><rect x="446" y="168" width="168" height="36" rx="5" fill="none" stroke="{t["accent"]}" stroke-width="2"/>'
             + text(530, 192, "CHECKED IN", t["accent"], 18, MONO, "middle", 700, 'letter-spacing="2"') + "</g>")
    save(f"ticket-{theme}.svg", document(H + 2, "\n".join(b), "\n".join(css)))


for lang in ("en", "vi"):
    for theme in THEMES:
        header(theme)
        seats(theme)
        proctor(theme)
        street(theme)
        ticket(theme)
print("ok")
