"""Adds the six-stage background animation to the home page. Usage: python hero_anim.py <site_dir> [build_script]"""
import sys, re, os

SITE = sys.argv[1]
SCRIPT = sys.argv[2] if len(sys.argv) > 2 else None

def d(o=0):  # line-drawing element attrs
    return f'class="d" pathLength="1" style="--o:{o}s"'

def pop(o=0, extra=""):
    return f'class="p{extra}" style="--o:{o}s"'

def rise(o=0):
    return f'class="r fill" style="--o:{o}s"'

LABELS = ["Initial consultation", "Experimental project plan", "Sample preparation",
          "Data generation", "Data analysis", "Pre-publication services"]

S = []
# 1 — consultation: two speech bubbles, typing dots
S.append(f"""
<path {d()} d="M110 120h190a22 22 0 0 1 22 22v76a22 22 0 0 1-22 22H176l-40 32v-32h-26a22 22 0 0 1-22-22v-76a22 22 0 0 1 22-22z"/>
<g class="typing"><circle cx="165" cy="180" r="7"/><circle cx="205" cy="180" r="7"/><circle cx="245" cy="180" r="7"/></g>
<path {d(.9)} d="M300 270h170a22 22 0 0 1 22 22v62a22 22 0 0 1-22 22h-16v30l-36-30H300a22 22 0 0 1-22-22v-62a22 22 0 0 1 22-22z"/>
<path {d(1.3)} d="M310 310h130M310 338h90"/>
<g {pop(1.7)}><circle cx="470" cy="160" r="26"/><path d="M458 160l9 9 16-18" stroke-width="3"/></g>
""")
# 2 — plan: clipboard with ticking checklist
rows = "".join(f'<rect x="232" y="{170+i*58}" width="26" height="26" rx="5"/>'
               f'<path {d(.6+i*.35)} d="M237 {183+i*58}l7 7 13-15"/>'
               f'<path {d(.4+i*.35)} d="M282 {183+i*58}h{150 - (i%2)*50}"/>' for i in range(4))
S.append(f"""
<rect {d()} x="200" y="110" width="270" height="340" rx="16"/>
<rect {d(.2)} x="280" y="94" width="110" height="34" rx="8"/>
{rows}
""")
# 3 — sample prep: pipette, falling drop, tubes filling
tubes = ""
for i, x in enumerate((215, 300, 385)):
    tubes += (f'<path {d(.1*i)} d="M{x-28} 250v130a28 28 0 0 0 56 0V250"/><path d="M{x-36} 250h72"/>'
              f'<rect {rise(.9+.35*i)} x="{x-24}" y="{330-i*14}" width="48" height="{78+i*14}" rx="22"/>')
S.append(f"""
<g class="pip"><path {d()} d="M300 70v26M284 96h32l-6 70h-20zM296 166l4 26 4-26"/></g>
<circle class="drop" cx="300" cy="200" r="7"/>
{tubes}
""")
# 4 — data generation: chromatogram trace + spectrum
chrom = "M110 400 C150 400 160 398 175 392 S190 300 200 300 S212 392 225 395 S260 380 270 340 S285 250 295 250 S310 395 330 398 S360 360 372 330 S384 300 392 330 S410 398 440 399 S470 395 490 400"
bars = "".join(f'<rect {rise(1.0+i*.07)} x="{120+i*24}" y="{140+h}" width="6" height="{110-h}" rx="2"/>'
               for i, h in enumerate([70, 40, 85, 10, 60, 30, 92, 50, 0, 75, 45, 88, 25, 66, 80, 55]))
S.append(f"""
<path {d()} d="M100 410h400M100 410V280M100 255V120"/>
<path {d(.3)} d="{chrom}"/>
<path d="M100 255h400" stroke-dasharray="3 7"/>
{bars}
""")
# 5 — analysis: network forming + volcano dots
nodes = [(300,260,16),(210,190,11),(395,180,11),(185,320,9),(410,340,11),(300,385,9),(250,255,7),(355,270,7),(130,240,6),(470,250,6),(320,130,6),(230,410,6),(380,420,6)]
edges = [(0,1),(0,2),(0,6),(0,7),(1,3),(1,8),(2,9),(2,10),(4,7),(4,9),(5,6),(5,7),(3,11),(5,12),(4,12),(1,6),(2,7),(3,6)]
net = "".join(f'<path {d(.25+i*.04)} d="M{nodes[a][0]} {nodes[a][1]}L{nodes[b][0]} {nodes[b][1]}" stroke-width="1.8"/>' for i,(a,b) in enumerate(edges))
net += "".join(f'<circle {pop(.05*i, " fill" if r>=9 else " hollow")} cx="{x}" cy="{y}" r="{r}"/>' for i,(x,y,r) in enumerate(nodes))
S.append(net)
# 6 — publication: manuscript page with figure + accepted stamp
S.append(f"""
<path {d()} d="M190 90h170l60 60v290a14 14 0 0 1-14 14H190a14 14 0 0 1-14-14V104a14 14 0 0 1 14-14z"/>
<path {d(.2)} d="M360 90v60h60"/>
<path {d(.35)} d="M205 135h120M205 160h90"/>
<rect {d(.5)} x="205" y="190" width="190" height="120" rx="6"/>
<rect {rise(.8)} x="225" y="250" width="22" height="45" rx="2"/>
<rect {rise(.9)} x="262" y="225" width="22" height="70" rx="2"/>
<rect {rise(1.0)} x="299" y="265" width="22" height="30" rx="2"/>
<rect {rise(1.1)} x="336" y="210" width="22" height="85" rx="2"/>
<path {d(.7)} d="M205 340h190M205 365h190M205 390h130"/>
<g {pop(1.6)}><circle cx="420" cy="400" r="40" stroke-width="3"/><path d="M402 400l12 12 24-26" stroke-width="4"/></g>
""")

scenes = ""
for i, body in enumerate(S):
    scenes += (f'<g class="scene" style="--s:{i}">{body}'
               f'<text x="300" y="488" text-anchor="middle">0{i+1} · {LABELS[i]}</text></g>')
dots = "".join(f'<circle class="dot" style="--s:{i}" cx="{225+i*30}" cy="512" r="5"/>' for i in range(6))
rail = '<path d="M225 512h150" stroke-width="1.5"/>'

SVG = (f'<div class="hero-anim" aria-hidden="true"><svg viewBox="0 0 600 530" fill="none" stroke="currentColor" '
       f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{scenes}{rail}{dots}</svg></div>')

CSS = """
/* ---------- Hero background animation: six project stages ---------- */
.page-hero { position: relative; overflow: hidden; }
.page-hero .wrap { position: relative; }
.page-hero .wrap > :not(.hero-anim) { position: relative; z-index: 1; }
.hero-anim { position: absolute; z-index: 0; top: -58px; right: -10px; width: 420px; color: var(--green-700); opacity: .22; pointer-events: none; }
.hero-anim svg { width: 100%; height: auto; overflow: visible; }
.hero-anim text { font: 500 17px var(--mono); fill: currentColor; stroke: none; letter-spacing: .06em; }
.hero-anim .fill { fill: currentColor; stroke: none; }
.hero-anim .typing circle, .hero-anim .drop { fill: currentColor; stroke: none; }
.hero-anim .dot, .hero-anim .hollow { fill: var(--paper); stroke-width: 2; }
.hero-anim .hollow { stroke-width: 2.5; }
.hero-anim .scene { opacity: 0; }
@media (prefers-reduced-motion: no-preference) {
  .hero-anim .scene, .hero-anim .d, .hero-anim .p, .hero-anim .r, .hero-anim .dot {
    animation-duration: 21s; animation-iteration-count: infinite; animation-fill-mode: both; animation-timing-function: ease-in-out;
  }
  .hero-anim .scene { animation-name: ha-scene; animation-delay: calc(var(--s) * 3.5s); }
  .hero-anim .scene .d, .hero-anim .scene .p, .hero-anim .scene .r { animation-delay: calc(var(--s) * 3.5s + var(--o, 0s)); }
  .hero-anim .d { stroke-dasharray: 1; animation-name: ha-draw; }
  .hero-anim .p { transform-box: fill-box; transform-origin: center; animation-name: ha-pop; }
  .hero-anim .r { transform-box: fill-box; transform-origin: bottom; animation-name: ha-rise; }
  .hero-anim .dot { animation-name: ha-dot; animation-delay: calc(var(--s) * 3.5s); }
  .hero-anim .typing circle { animation: ha-blink 1.2s infinite; }
  .hero-anim .typing circle:nth-child(2) { animation-delay: .2s; }
  .hero-anim .typing circle:nth-child(3) { animation-delay: .4s; }
  .hero-anim .scene:nth-child(3) .drop { animation: ha-drop 1.4s ease-in infinite; }
}
@media (prefers-reduced-motion: reduce) {
  .hero-anim .scene:nth-child(4) { opacity: 1; }
  .hero-anim .dot:nth-of-type(4) { fill: currentColor; }
}
@keyframes ha-scene { 0% { opacity: 0; } 2.5% { opacity: 1; } 14.5% { opacity: 1; } 16.7% { opacity: 0; } 100% { opacity: 0; } }
@keyframes ha-draw  { 0% { stroke-dashoffset: 1; } 6% { stroke-dashoffset: 0; } 16.5% { stroke-dashoffset: 0; } 17% { stroke-dashoffset: 1; } 100% { stroke-dashoffset: 1; } }
@keyframes ha-pop   { 0% { transform: scale(0); } 3% { transform: scale(1.15); } 4.5% { transform: scale(1); } 16.5% { transform: scale(1); } 17% { transform: scale(0); } 100% { transform: scale(0); } }
@keyframes ha-rise  { 0% { transform: scaleY(0); } 6% { transform: scaleY(1); } 16.5% { transform: scaleY(1); } 17% { transform: scaleY(0); } 100% { transform: scaleY(0); } }
@keyframes ha-dot   { 0% { fill: var(--paper); } 1% { fill: currentColor; } 16.6% { fill: currentColor; } 16.7% { fill: var(--paper); } 100% { fill: var(--paper); } }
@keyframes ha-blink { 0%, 100% { opacity: .25; } 50% { opacity: 1; } }
@keyframes ha-drop  { 0% { transform: translateY(-20px); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(150px); opacity: 0; } }
@media (max-width: 1020px) { .hero-anim { width: 360px; right: -50px; opacity: .13; } }
@media (max-width: 820px)  { .hero-anim { top: -30px; right: -110px; width: 300px; opacity: .08; } }
"""

# --- remove from home, add to Services page header (re-runnable) ---
for page, anchor, add in (("index.html", '<section class="hero">\n  <div class="wrap">\n', False),
                          ("services.html", '<section class="page-hero">\n  <div class="wrap">\n', True)):
    p = os.path.join(SITE, page)
    h = open(p, encoding="utf-8").read()
    h = re.sub(r'    <div class="hero-anim".*?</svg></div>\n', '', h, flags=re.S)
    if add:
        assert anchor in h
        h = h.replace(anchor, anchor + "    " + SVG + "\n", 1)
    open(p, "w", encoding="utf-8").write(h)

# --- patch CSS (re-runnable) ---
c = os.path.join(SITE, "assets", "css", "style.css")
css = open(c, encoding="utf-8").read()
css = css.split("\n/* ---------- Hero background animation")[0].rstrip() + "\n" + CSS
open(c, "w", encoding="utf-8").write(css)

# --- keep the page generator in sync so a rebuild doesn't drop the animation ---
if SCRIPT:
    s = open(SCRIPT, encoding="utf-8").read()
    marker = "# --- hero animation (added) ---"
    if marker not in s:
        s += f'\n{marker}\nimport subprocess as _sp\n_sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "hero_anim.py"), OUT], check=True)\n'
        open(SCRIPT, "w", encoding="utf-8").write(s)
print("animation added")
