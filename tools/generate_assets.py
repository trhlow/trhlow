"""Generate the animated isometric SVG assets for the trhlow profile README."""
import os
import sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
SANS = "'Segoe UI', Inter, -apple-system, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, Menlo, monospace"
C30, S30 = 0.8660254, 0.5


def esc(s):
    return escape(s, {'"': "&quot;"})


def shade(hex_color, f):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 1:
        r, g, b = (int(c + (255 - c) * (f - 1)) for c in (r, g, b))
    else:
        r, g, b = (int(c * f) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


class Iso:
    def __init__(self, ox, oy, u):
        self.ox, self.oy, self.u = ox, oy, u

    def p(self, x, y, z):
        return (self.ox + (x - y) * C30 * self.u, self.oy + (x + y) * S30 * self.u - z * self.u)

    def poly(self, pts, fill, extra=""):
        s = " ".join(f"{a:.1f},{b:.1f}" for a, b in (self.p(*q) for q in pts))
        return f'<polygon points="{s}" fill="{fill}" {extra}/>'

    def box(self, x, y, z, w, d, h, color, stroke=None, rack=0, leds=None):
        st = f'stroke="{stroke}" stroke-width="1" stroke-linejoin="round"' if stroke else ""
        out = [
            self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], shade(color, 0.72), st),
            self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], shade(color, 0.48), st),
            self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], shade(color, 1.18), st),
        ]
        # rack lines on both visible side faces
        for i in range(1, rack + 1):
            zz = z + h * i / (rack + 1)
            a, b = self.p(x + 0.15, y + d, zz), self.p(x + w - 0.15, y + d, zz)
            out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{shade(color, 0.45)}" stroke-width="1.4"/>')
            a, b = self.p(x + w, y + 0.15, zz), self.p(x + w, y + d - 0.15, zz)
            out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{shade(color, 0.3)}" stroke-width="1.4"/>')
        if leds:
            for i in range(rack + 1):
                zz = z + h * (i + 0.5) / (rack + 1)
                cx, cy = self.p(x + 0.45, y + d, zz)
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.2" fill="{leds}" class="led" style="animation-delay:{i * 0.37:.2f}s"/>')
        return "\n".join(out)

    def face_text(self, x, y, z, text, size, fill, plane="top", weight=700, family=MONO, anchor="middle"):
        """Text lying on an iso plane. top: x/y plane, left: x/z plane at fixed y."""
        tx, ty = self.p(x, y, z)
        if plane == "top":
            m = f"matrix({C30:.4f},{S30:.4f},{-C30:.4f},{S30:.4f},{tx:.1f},{ty:.1f})"
        else:
            m = f"matrix({C30:.4f},{S30:.4f},0,1,{tx:.1f},{ty:.1f})"
        return (f'<text transform="{m}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
                f'fill="{fill}" text-anchor="{anchor}" dominant-baseline="middle">{esc(text)}</text>')


def svg(w, h, body, style="", defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">\n'
            f'<style>{style}</style>\n<defs>{defs}</defs>\n{body}\n</svg>\n')


def save(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def extruded(x, y, text, size, front, back, depth=6, anchor="start", family=SANS, weight=800, extra=""):
    """Text with a stacked 3D extrusion behind it."""
    layers = []
    for i in range(depth, 0, -1):
        layers.append(f'<text x="{x + i:.1f}" y="{y + i:.1f}" fill="{back}" font-family="{family}" font-size="{size}" '
                      f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(text)}</text>')
    layers.append(f'<text x="{x}" y="{y}" fill="{front}" font-family="{family}" font-size="{size}" '
                  f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(text)}</text>')
    return "\n".join(layers)


COMMON_STYLE = """
.float{animation:float 6s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.led{animation:blink 1.6s steps(2,start) infinite}
@keyframes blink{50%{opacity:.15}}
.tw{animation:tw 3.2s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}
.glint{animation:glint 4s ease-in-out infinite}
@keyframes glint{0%,100%{opacity:1}50%{opacity:.72}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""


def stars(w, h, n, seed=7):
    import random
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y, r = rnd.uniform(0, w), rnd.uniform(0, h), rnd.uniform(0.6, 1.8)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#cfe3ff" class="tw" '
                   f'style="animation-delay:{rnd.uniform(0, 3.2):.2f}s"/>')
    return "\n".join(out)


# --------------------------------------------------------------------------- hero
def hero():
    W, H = 1200, 470
    iso = Iso(905, 168, 25)
    defs = """
<radialGradient id="bg" cx="70%" cy="40%" r="85%"><stop offset="0" stop-color="#16244a"/><stop offset=".55" stop-color="#0b1228"/><stop offset="1" stop-color="#05070f"/></radialGradient>
<linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="#ffd27a"/><stop offset=".5" stop-color="#ff9d4d"/><stop offset="1" stop-color="#7ee0a1"/></linearGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7ee0a1" stop-opacity=".55"/><stop offset="1" stop-color="#7ee0a1" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
<clipPath id="frame"><rect width="1200" height="470" rx="26"/></clipPath>
"""
    style = COMMON_STYLE + """
.f1{animation-delay:0s}.f2{animation-delay:-1.5s}.f3{animation-delay:-3s}.f4{animation-delay:-4.5s}
.d1{animation-delay:.1s}.d2{animation-delay:.3s}.d3{animation-delay:.5s}.d4{animation-delay:.7s}.d5{animation-delay:.9s}
.cursor{animation:blink 1s steps(2,start) infinite}
.scan{animation:scan 7s linear infinite}
@keyframes scan{from{transform:translateY(-40px)}to{transform:translateY(520px)}}
.pulse{animation:pulse 3s ease-in-out infinite;transform-origin:905px 300px}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:.8}}
"""
    b = ['<g clip-path="url(#frame)">', '<rect width="1200" height="470" fill="url(#bg)"/>', stars(W, H, 70)]
    # perspective floor grid
    vx, vy = 905, 250
    g = []
    for i in range(-14, 15):
        g.append(f'<line x1="{vx}" y1="{vy}" x2="{vx + i * 120}" y2="{H + 40}"/>')
    for j, yy in enumerate([300, 322, 350, 386, 432, 490]):
        g.append(f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" opacity="{0.25 + j * 0.12:.2f}"/>')
    b.append(f'<g stroke="#3d6bd6" stroke-width="1" opacity=".22">{"".join(g)}</g>')
    b.append('<rect x="0" y="0" width="1200" height="40" fill="#7ee0a1" opacity=".04" class="scan"/>')
    b.append('<ellipse cx="905" cy="330" rx="260" ry="70" fill="#3d7bff" opacity=".35" filter="url(#soft)" class="pulse"/>')

    # ---- isometric scene
    sc = ['<g class="float f1">']
    sc.append(iso.box(-0.5, -0.5, -0.9, 11, 11, 0.9, "#1d2b57", stroke="#3b5bb0"))
    # platform grid
    for t in range(1, 11):
        a, c = iso.p(-0.5 + t, -0.5, 0), iso.p(-0.5 + t, 10.5, 0)
        sc.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{c[0]:.1f}" y2="{c[1]:.1f}" stroke="#6d8cf0" stroke-width=".8" opacity=".45"/>')
        a, c = iso.p(-0.5, -0.5 + t, 0), iso.p(10.5, -0.5 + t, 0)
        sc.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{c[0]:.1f}" y2="{c[1]:.1f}" stroke="#6d8cf0" stroke-width=".8" opacity=".45"/>')
    # data paths on the platform
    nodes = {"api": (2.5, 2.5), "pg": (7.5, 2.5), "redis": (2.5, 7.5), "mq": (7.5, 7.5)}
    links = [("api", "pg"), ("api", "redis"), ("pg", "mq"), ("redis", "mq")]
    for k, (a, c) in enumerate(links):
        p1, p2 = iso.p(*nodes[a], 0), iso.p(*nodes[c], 0)
        d = f"M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}"
        sc.append(f'<path d="{d}" stroke="#7ee0a1" stroke-width="2" opacity=".5" stroke-dasharray="5 6"/>')
        for j in range(2):
            sc.append(f'<circle r="3.6" fill="#b8ffd0" filter="url(#glow)"><animateMotion dur="2.6s" begin="{k * 0.45 + j * 1.3:.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
    sc.append("</g>")
    b.append("\n".join(sc))

    servers = [
        ("API", "Spring Boot", 1, 1, 4.6, "#4caf50", "f2"),
        ("SQL", "PostgreSQL", 6, 1, 3.2, "#3f7fd6", "f3"),
        ("KV", "Redis", 1, 6, 2.4, "#e0473c", "f4"),
        ("MQ", "RabbitMQ", 6, 6, 2.8, "#ff8a2a", "f1"),
    ]
    for label, sub, x, y, h, col, fc in servers:
        s = [f'<g class="float {fc}">']
        # light beam under each server
        bx, by = iso.p(x + 1.5, y + 1.5, 0)
        s.append(f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="44" ry="20" fill="{col}" opacity=".28" filter="url(#soft)"/>')
        s.append(iso.box(x, y, 0.35, 3, 3, h, col, stroke=shade(col, 1.35), rack=3 if h > 3 else 2, leds="#c8ffd8"))
        s.append(iso.face_text(x + 1.5, y + 1.5, 0.35 + h, label, 21, shade(col, 0.35), "top"))
        lx, ly = iso.p(x + 1.5, y + 1.5, 0.35 + h)
        s.append(f'<g class="fade d3"><line x1="{lx:.1f}" y1="{ly - 10:.1f}" x2="{lx:.1f}" y2="{ly - 34:.1f}" stroke="{col}" stroke-width="1.4" opacity=".8"/>'
                 f'<rect x="{lx - 52:.1f}" y="{ly - 58:.1f}" width="104" height="24" rx="12" fill="#0b1228" stroke="{col}" stroke-width="1.4"/>'
                 f'<text x="{lx:.1f}" y="{ly - 41.5:.1f}" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{shade(col, 1.45)}">{esc(sub)}</text></g>')
        s.append("</g>")
        b.append("\n".join(s))

    # ---- left column
    t = []
    t.append(f'<g class="fade d1"><rect x="70" y="70" width="236" height="32" rx="16" fill="#7ee0a1" fill-opacity=".1" stroke="#7ee0a1" stroke-opacity=".5"/>'
             f'<circle cx="90" cy="86" r="5" fill="#7ee0a1" class="led"/>'
             f'<text x="104" y="91" font-family="{MONO}" font-size="14" fill="#a8f0c2">available for backend roles</text></g>')
    t.append(f'<g class="fade d2"><text x="70" y="148" font-family="{MONO}" font-size="20" fill="#8fa7d8">Xin chào, I\'m</text></g>')
    t.append('<g class="fade d3">' + extruded(70, 214, "Trần Hoàng Long", 60, "url(#name)", "#5a2c12", depth=7) + "</g>")
    t.append(f'<g class="fade d4"><text x="70" y="262" font-family="{SANS}" font-size="27" font-weight="600" fill="#e8eeff">Backend Java Developer</text>'
             f'<text x="70" y="296" font-family="{MONO}" font-size="15.5" fill="#8fa7d8">Spring Boot · Distributed Systems · Clean Architecture</text></g>')
    chips = [("Vinh Long, Viet Nam", "#ffb36b"), ("Tra Vinh University", "#7ee0a1"), ("Java 25 · Spring Boot 4", "#7fb2ff")]
    cx = 70
    ch = ['<g class="fade d5">']
    for text, col in chips:
        w = len(text) * 8.1 + 30
        ch.append(f'<rect x="{cx}" y="330" width="{w:.0f}" height="30" rx="8" fill="{col}" fill-opacity=".1" stroke="{col}" stroke-opacity=".55"/>'
                  f'<circle cx="{cx + 13}" cy="345" r="3.5" fill="{col}"/>'
                  f'<text x="{cx + 23}" y="350" font-family="{MONO}" font-size="13.5" fill="{col}">{esc(text)}</text>')
        cx += w + 10
    ch.append("</g>")
    t.append("".join(ch))
    t.append(f'<g class="fade d5"><text x="70" y="410" font-family="{MONO}" font-size="15" fill="#5f79b5">$ ./mvnw spring-boot:run <tspan fill="#7ee0a1">--profile=production</tspan>'
             f'<tspan class="cursor" fill="#7ee0a1"> ▍</tspan></text></g>')
    b.append("\n".join(t))
    b.append('</g><rect x="1" y="1" width="1198" height="468" rx="25" fill="none" stroke="#2a3f7a" stroke-width="2"/>')
    save("assets/hero.svg", svg(W, H, "\n".join(b), style, defs))


# --------------------------------------------------------------------------- section titles
def titles():
    items = [
        ("about", "01", "ABOUT ME", "#ff9d4d", "#7a3a10"),
        ("flagship", "02", "FLAGSHIP PROJECT", "#7ee0a1", "#1f5a36"),
        ("projects", "03", "PROJECTS", "#7fb2ff", "#1f3f7a"),
        ("lab", "04", "LAB & COURSEWORK", "#c49bff", "#45227a"),
        ("stack", "05", "TECH STACK", "#ffd27a", "#7a5410"),
        ("principles", "06", "HOW I BUILD", "#ff7b8a", "#7a1f2a"),
        ("activity", "07", "GITHUB ACTIVITY", "#6fe3e3", "#14605f"),
    ]
    for key, num, text, front, back in items:
        W, H = 900, 90
        style = """.in{animation:bob 5s ease-in-out infinite}@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.bar{animation:sweep 3.5s ease-in-out infinite}@keyframes sweep{0%,100%{opacity:.35}50%{opacity:.9}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}"""
        width = len(text) * 24.5 + 70
        x0 = (W - width) / 2
        body = [f'<g class="in">',
                f'<text x="{x0:.0f}" y="58" font-family="{MONO}" font-size="20" font-weight="700" fill="{front}" opacity=".75">{num}</text>',
                extruded(x0 + 44, 60, text, 40, front, back, depth=5, extra='letter-spacing="2"'),
                "</g>",
                f'<rect class="bar" x="{W / 2 - 160}" y="76" width="320" height="4" rx="2" fill="{front}" opacity=".7"/>']
        save(f"assets/titles/{key}.svg", svg(W, H, "\n".join(body), style))


# --------------------------------------------------------------------------- project cards
def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def card(name, title, tagline, desc, chips, accent, mono, badge, W=600, H=330, compact=False):
    D = 12  # extrusion depth
    cw, chh = W - D - 4, H - D - 4
    defs = f"""
<linearGradient id="face" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#141d3a"/><stop offset="1" stop-color="#0a0f22"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shade(accent, 0.55)}"/><stop offset="1" stop-color="{shade(accent, 0.25)}"/></linearGradient>
<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="halo" cx="85%" cy="15%" r="60%"><stop offset="0" stop-color="{accent}" stop-opacity=".28"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>
<clipPath id="cl"><rect x="2" y="2" width="{cw}" height="{chh}" rx="20"/></clipPath>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
"""
    style = COMMON_STYLE + """
.sh{animation:sh 5.5s ease-in-out infinite}@keyframes sh{0%{transform:translateX(-420px) skewX(-20deg)}60%,100%{transform:translateX(820px) skewX(-20deg)}}
"""
    b = []
    # extruded slab: stacked offsets give a solid 3D edge
    for i in range(D, 0, -2):
        b.append(f'<rect x="{2 + i}" y="{2 + i}" width="{cw}" height="{chh}" rx="20" fill="url(#edge)"/>')
    b.append(f'<rect x="2" y="2" width="{cw}" height="{chh}" rx="20" fill="url(#face)" stroke="{accent}" stroke-opacity=".55" stroke-width="1.5"/>')
    b.append(f'<g clip-path="url(#cl)"><rect x="2" y="2" width="{cw}" height="{chh}" fill="url(#halo)"/>')
    b.append(f'<rect class="sh" x="0" y="-20" width="160" height="{H + 40}" fill="url(#shine)"/></g>')

    # floating iso emblem in the top-right corner
    s = 0.72 if compact else 1
    iso = Iso(cw - 70 * s, 70 * s, 17 * s)
    b.append(f'<g class="float"><ellipse cx="{cw - 70 * s:.1f}" cy="{122 * s:.1f}" rx="{40 * s:.1f}" ry="{12 * s:.1f}" fill="{accent}" opacity=".18"/>')
    b.append(iso.box(-1.6, -1.6, 0, 3.2, 3.2, 2.2, accent, stroke=shade(accent, 1.4), rack=1, leds="#ffffff"))
    b.append(iso.face_text(0, 0, 2.2, mono, 15, shade(accent, 0.3), "top"))
    b.append("</g>")

    pad = 30 if not compact else 24
    y = 56 if not compact else 48
    if badge:
        bw = len(badge) * 7.6 + 30
        b.append(f'<rect x="{pad}" y="{y - 26}" width="{bw:.0f}" height="24" rx="12" fill="{accent}" fill-opacity=".14" stroke="{accent}" stroke-opacity=".6"/>'
                 f'<circle cx="{pad + 13}" cy="{y - 14}" r="3.5" fill="{accent}" class="led"/>'
                 f'<text x="{pad + 23}" y="{y - 9.5}" font-family="{MONO}" font-size="12" font-weight="700" fill="{shade(accent, 1.4)}">{esc(badge)}</text>')
        y += 30
    tsize = 31 if not compact else 25
    b.append(extruded(pad, y, title, tsize, "#f2f5ff", shade(accent, 0.4), depth=3))
    y += 28 if not compact else 24
    b.append(f'<text x="{pad}" y="{y}" font-family="{SANS}" font-size="{17 if not compact else 15}" font-weight="600" fill="{shade(accent, 1.35)}">{esc(tagline)}</text>')
    y += 32 if not compact else 28
    for line in wrap(desc, 54 if not compact else 38):
        b.append(f'<text x="{pad}" y="{y}" font-family="{SANS}" font-size="{16.5 if not compact else 15}" fill="#b4c0e2">{esc(line)}</text>')
        y += 24 if not compact else 21

    # tech chips, laid out in rows and anchored to the bottom edge
    fs = 13 if not compact else 12.5
    rows, cur, cx = [], [], pad
    for c in chips:
        w = len(c) * fs * 0.62 + 18
        if cur and cx + w > cw - pad:
            rows.append(cur)
            cur, cx = [], pad
        cur.append((cx, w, c))
        cx += w + 7
    rows.append(cur)
    cy = chh - 22 - 30 * len(rows)
    for row in rows:
        for x, w, c in row:
            b.append(f'<rect x="{x:.0f}" y="{cy}" width="{w:.0f}" height="24" rx="6" fill="#ffffff" fill-opacity=".05" stroke="#ffffff" stroke-opacity=".16"/>'
                     f'<text x="{x + 9:.0f}" y="{cy + 16.5}" font-family="{MONO}" font-size="{fs}" fill="#d4dcf5">{esc(c)}</text>')
        cy += 30
    assert y < chh - 22 - 30 * len(rows), f"{name}: description collides with chips"
    save(f"assets/cards/{name}.svg", svg(W, H, "\n".join(b), style, defs))
    return rows


def cards():
    main = [
        ("tvu-event-ticket", "TVU Event & Ticket", "Event management & e-ticketing for TVU clubs",
         "Signed QR tickets scanned exactly once at the door. Seats cannot be oversold: 500 concurrent approvals vs 100 seats, load-tested.",
         ["Java 25", "Spring Boot 4", "React 19", "PostgreSQL", "Redis", "RabbitMQ"], "#7ee0a1", "QR", "LIVE · evts.id.vn"),
        ("cong-tin-land", "Công Tín Land", "Real-estate platform for Tra Vinh",
         "Listings, broker dashboards and SMS-OTP verified viewing bookings. Argon2id, JWT revocation and Redis rate limiting.",
         ["Spring Boot 4", "React 19", "PostgreSQL 18", "Redis", "Docker"], "#ffb36b", "CTL", "MONOREPO"),
        ("inchat", "InChat", "Real-time chat system",
         "STOMP over WebSocket for rooms, presence and delivery status. Friends, attachments, refresh-token auth, OpenTelemetry.",
         ["Spring Boot 4", "MongoDB", "WebSocket", "Redis", "React TS"], "#7fb2ff", "IN", "REALTIME"),
        ("educycle", "EduCycle", "P2P marketplace for students' books",
         "Edu-email OTP sign-up, moderation, transaction chat with OTP hand-off confirmation, reviews and a server-side AI chat proxy.",
         ["Spring Boot", "React", "Vite", "PostgreSQL", "Nginx"], "#c49bff", "EDU", "FULLSTACK"),
        ("personal-ai-manager", "Personal AI Manager", "Goals → plans → tasks, finance & insights",
         "Mobile-first life manager: budgets, reminders, spending plans and AI insights that advise but never modify your data.",
         ["Spring Boot", "Flutter", "JWT", "PostgreSQL"], "#ff7b8a", "PAI", "MOBILE"),
    ]
    for args in main:
        card(*args)
    lab = [
        ("vietfood-ai", "VietFood AI", "Vietnamese food recognition",
         "YOLO detects the dish, the API maps it to a calorie dataset.", ["Python", "YOLO", "FastAPI"], "#6fe3e3", "AI", "AI"),
        ("am-thuc-mien-tay", "Ẩm Thực Miền Tây", "Mekong Delta cuisine website",
         "Food & heritage of 13 provinces, responsive web design.", ["HTML", "CSS", "JS"], "#ff9d4d", "WEB", "WEB"),
        ("snake-game", "Snake Game", "Unity coursework project",
         "Classic snake with scoring, collisions and restart.", ["C#", "Unity 6", "HLSL"], "#9be36f", "SNK", "GAME"),
    ]
    for args in lab:
        card(*args, W=400, H=290, compact=True)


# --------------------------------------------------------------------------- layered stack
def stack():
    W, H = 1100, 560
    iso = Iso(330, 292, 26)
    layers = [
        ("INFRA", "Docker · Caddy · Nginx · GitHub Actions · CodeQL", "#ffd27a"),
        ("DATA", "PostgreSQL · MongoDB · Redis · RabbitMQ · Flyway", "#7fb2ff"),
        ("BACKEND", "Java · Spring Boot · Spring Security · JPA · WebSocket", "#7ee0a1"),
        ("CLIENT", "React · TypeScript · Vite · Tailwind · Flutter", "#ff7b8a"),
    ]
    style = COMMON_STYLE + """
.l0{animation:b0 5s ease-in-out infinite}.l1{animation:b1 5s ease-in-out infinite}.l2{animation:b2 5s ease-in-out infinite}.l3{animation:b3 5s ease-in-out infinite}
@keyframes b0{0%,100%{transform:translateY(0)}50%{transform:translateY(10px)}}
@keyframes b1{0%,100%{transform:translateY(0)}50%{transform:translateY(3px)}}
@keyframes b2{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
@keyframes b3{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
"""
    defs = """<radialGradient id="bg" cx="30%" cy="50%" r="80%"><stop offset="0" stop-color="#132046"/><stop offset="1" stop-color="#060914"/></radialGradient>
<filter id="soft"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>"""
    b = ['<rect width="1100" height="560" rx="26" fill="url(#bg)"/>', stars(W, H, 40, seed=3)]
    b.append('<ellipse cx="330" cy="445" rx="250" ry="55" fill="#3d7bff" opacity=".35" filter="url(#soft)"/>')
    gap = 2.9
    for i, (name, techs, col) in enumerate(layers):
        z = i * gap
        g = [f'<g class="l{i}">']
        g.append(iso.box(0, 0, z, 9, 9, 0.85, col, stroke=shade(col, 1.35)))
        # inner inset on top face
        g.append(iso.poly([(0.8, 0.8, z + 0.86), (8.2, 0.8, z + 0.86), (8.2, 8.2, z + 0.86), (0.8, 8.2, z + 0.86)],
                          "none", f'stroke="{shade(col, 0.55)}" stroke-width="1.5" stroke-dasharray="6 5"'))
        g.append(iso.face_text(4.5, 4.5, z + 0.86, name, 30, shade(col, 0.4), "top", weight=800))
        # callout to the right
        ax, ay = iso.p(9, 0, z + 0.45)
        tx = 640
        g.append(f'<path d="M{ax:.1f},{ay:.1f} L{ax + 40:.1f},{ay:.1f} L{tx - 20},{ay:.1f}" stroke="{col}" stroke-width="1.3" opacity=".7" stroke-dasharray="4 4"/>'
                 f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="4" fill="{col}" filter="url(#glow)"/>'
                 f'<text x="{tx}" y="{ay - 6:.1f}" font-family="{MONO}" font-size="19" font-weight="800" fill="{col}" letter-spacing="2">{name}</text>'
                 f'<text x="{tx}" y="{ay + 17:.1f}" font-family="{SANS}" font-size="14.5" fill="#b9c5e8">{esc(techs)}</text>')
        g.append("</g>")
        b.append("\n".join(g))
    # packets travelling vertically through the stack
    for k, (x, y) in enumerate([(2.5, 6.5), (6.5, 2.5), (4.5, 8)]):
        p1, p2 = iso.p(x, y, 0.9), iso.p(x, y, 3 * gap + 0.85)
        d = f"M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}"
        b.append(f'<path d="{d}" stroke="#ffffff" stroke-opacity=".12" stroke-width="2"/>')
        b.append(f'<circle r="4" fill="#ffffff" filter="url(#glow)"><animateMotion dur="3.4s" begin="{k * 1.1:.1f}s" repeatCount="indefinite" path="{d}" keyPoints="1;0;1" keyTimes="0;.5;1" calcMode="linear"/></circle>')
    b.append(f'<text x="640" y="520" font-family="{MONO}" font-size="13" fill="#5f79b5">every layer tested, containerised, shipped by CI</text>')
    save("assets/stack.svg", svg(W, H, "\n".join(b), style, defs))


# --------------------------------------------------------------------------- footer
def footer():
    W, H = 1200, 190
    style = """.w1{animation:w 9s linear infinite}.w2{animation:w 13s linear infinite reverse}.w3{animation:w 17s linear infinite}
@keyframes w{from{transform:translateX(0)}to{transform:translateX(-1200px)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}"""
    def wave(y, amp, col, op, cls):
        pts = []
        for i in range(0, 2401, 40):
            import math
            pts.append(f"{i},{y + amp * math.sin(i / 1200 * 4 * math.pi):.1f}")
        return f'<path class="{cls}" d="M0,{H} L{" L".join(pts)} L2400,{H} Z" fill="{col}" opacity="{op}"/>'
    b = [wave(70, 18, "#ff9d4d", .35, "w3"), wave(95, 22, "#7ee0a1", .35, "w2"), wave(120, 16, "#1d2b57", 1, "w1"),
         f'<text x="600" y="168" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#c9d6ff">build things that stay correct under load</text>']
    save("assets/footer.svg", svg(W, H, "\n".join(b), style))


hero()
titles()
cards()
stack()
footer()
print("ok")
