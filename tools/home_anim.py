"""Home-page extras: (1) 'sample to manuscript' background animation in the hero,
(2) 'ask a question' demo section. Re-runnable. Usage: python home_anim.py <site_dir> [build_script]"""
import sys, os, re, random

SITE = sys.argv[1]
SCRIPT = sys.argv[2] if len(sys.argv) > 2 else None

# ======================= (1) hero morph animation =======================
BASE = 430
PEAKS = [(230, 300), (262, 350), (290, 250), (318, 380), (350, 200), (380, 330), (412, 270), (446, 360), (480, 240), (515, 310)]
TARGET = [(245, 180), (360, 360), (275, 130), (395, 340), (300, 220), (375, 385), (460, 200), (410, 370), (490, 140), (515, 240)]
SIG = {0, 2, 4, 6, 8, 9}
EDGES = [(0, 2), (2, 4), (0, 4), (4, 6), (6, 8), (8, 9), (6, 9), (2, 8)]

def v(**kw):
    return 'style="' + ";".join(f"--{k}:{val}" for k, val in kw.items()) + '"'

parts = []
# sample tube + liquid + drops
parts.append('<path class="m-tube m-d" pathLength="1" d="M70 60v110a20 20 0 0 0 40 0V60M62 60h56"/>')
parts.append('<rect class="m-liq m-fill" x="74" y="112" width="32" height="76" rx="16"/>')
for i in range(4):
    parts.append(f'<circle class="m-drop m-fill" cx="90" cy="198" r="4.5" {v(o=f"{i*0.55:.2f}s")}/>')
# column + bands
parts.append('<rect class="m-col m-d" pathLength="1" x="78" y="240" width="24" height="165" rx="12"/>')
for i, y in enumerate((282, 322, 362)):
    parts.append(f'<rect class="m-band m-fill" x="82" y="{y}" width="16" height="12" rx="4" {v(o=f"{i*0.45:.2f}s")}/>')
# baseline + ions + peaks + tip dots
parts.append(f'<path class="m-base m-d" pathLength="1" d="M215 {BASE}h345"/>')
for i, (px, tip) in enumerate(PEAKS):
    o = f"{i*0.12:.2f}s"
    parts.append(f'<circle class="m-ion m-fill" cx="90" cy="410" r="4" {v(o=o, dx=f"{px-90}px", dy=f"{BASE-410}px", mx=f"{(px-90)*0.5:.0f}px")}/>')
    parts.append(f'<line class="m-pk" x1="{px}" x2="{px}" y1="{BASE}" y2="{tip}" {v(o=o)}/>')
for i, (px, tip) in enumerate(PEAKS):
    tx, ty = TARGET[i]
    cls = "m-dot sig" if i in SIG else "m-dot ns"
    parts.append(f'<circle class="{cls}" cx="{px}" cy="{tip}" r="6" {v(dx=f"{tx-px}px", dy=f"{ty-tip}px")}/>')
# volcano axes + background cloud
parts.append('<path class="m-ax m-d" pathLength="1" d="M220 405h320M320 120v285M440 120v285M220 300h320"/>')
rnd = random.Random(4)
for _ in range(30):
    x = 380 + rnd.gauss(0, 34)
    y = 400 - abs(x - 380) * rnd.uniform(.5, 1.3) - rnd.uniform(0, 30)
    parts.append(f'<circle class="m-cloud m-fill" cx="{x:.0f}" cy="{max(y, 300):.0f}" r="3.2"/>')
# network edges between significant hits (drawn at their volcano positions)
for a, b in EDGES:
    (x1, y1), (x2, y2) = TARGET[a], TARGET[b]
    parts.append(f'<path class="m-edge m-d" pathLength="1" d="M{x1} {y1}L{x2} {y2}"/>')
# manuscript page
parts.append('<path class="m-page m-d" pathLength="1" d="M215 66h280l55 55v330a12 12 0 0 1-12 12H215a12 12 0 0 1-12-12V78a12 12 0 0 1 12-12z"/>')
parts.append('<path class="m-page m-d" pathLength="1" d="M495 66v55h55"/>')
parts.append('<path class="m-txt m-d" pathLength="1" d="M228 92h150M228 106h95"/>')
parts.append('<rect class="m-txt m-d" pathLength="1" x="226" y="112" width="312" height="148" rx="6"/>')
parts.append('<path class="m-txt m-d" pathLength="1" d="M228 300h300M228 324h300M228 348h300M228 372h210"/>')
parts.append('<g class="m-ok"><circle cx="520" cy="432" r="30" stroke-width="3"/><path d="M506 432l10 10 19-21" stroke-width="4"/></g>')
# captions
CAPS = ["Sample", "Separation", "Detection", "Statistics", "Biology", "Publication"]
for i, t in enumerate(CAPS):
    parts.append(f'<text class="m-cap" x="300" y="508" text-anchor="middle" {v(c=i)}>{t}</text>')

MORPH = ('<div class="hero-morph" aria-hidden="true"><svg viewBox="0 0 600 520" fill="none" stroke="currentColor" '
         'stroke-width="3" stroke-linecap="round" stroke-linejoin="round">' + "".join(parts) + '</svg></div>')

# ======================= (3) question demo =======================
CHIPS = ["Consultation", "Project plan", "Sample prep", "Data generation", "Analysis", "Publication"]
rnd = random.Random(21)
vdots = []
for _ in range(70):
    fc = rnd.gauss(0, 1.0)
    p = abs(fc) * rnd.uniform(.4, 1.5) * 20 + rnd.uniform(0, 7)
    x, y = 90 + fc * 26, 104 - min(p, 92)
    if not (6 < x < 174):
        continue
    sig = abs(fc) > 1.15 and p > 26
    vdots.append(f'<circle class="{"vs" if sig else "vn"}" cx="{x:.1f}" cy="{y:.1f}" r="{3 if sig else 2.2}" style="--k:{len(vdots)}"/>')
VOLC = ('<svg class="demo-volc" viewBox="0 0 180 110" aria-hidden="true">'
        '<path d="M6 106h168M58 6v100M122 6v100M6 70h168" />' + "".join(vdots) + '</svg>')

chips = "".join(f'<li class="chip" data-i="{i}"><span class="ci">{i+1}</span>{t}</li>' for i, t in enumerate(CHIPS))
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
DEMO = f"""<!-- demo:start -->
<section class="demo-sec">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">From question to answer</p>
      <h2>Start with a question. Finish with a result.</h2>
      <p class="lead">You bring the biology. We turn it into a study design, run the samples, and hand back an answer you can act on, with every step documented along the way.</p>
      <div class="actions"><a class="btn" href="contact.html">Ask us your question {ARROW}</a></div>
    </div>
    <div class="demo reveal" aria-label="Animated example of a project moving from a research question to a result">
      <div class="demo-top"><span></span><span></span><span></span><b>New project</b></div>
      <div class="demo-body">
        <p class="demo-label">Your research question</p>
        <p class="demo-q"><span class="demo-qt">Which plasma proteins change after treatment?</span><i class="caret"></i></p>
        <ol class="demo-chips">{chips}</ol>
        <div class="demo-res">
          {VOLC}
          <div>
            <span class="tag demo-type">Discovery proteomics</span>
            <p class="demo-find">38 proteins changed · 4 pathways enriched</p>
            <p class="demo-note">Illustrative example</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<!-- demo:end -->
"""

CSS = r"""
/* ==== home extras ==== */
/* hero: sample -> manuscript background animation */
.hero .wrap > :not(.hero-morph) { position: relative; z-index: 1; }
.hero-morph { position: absolute; z-index: 0; top: -40px; right: -30px; width: 520px; color: var(--green-700); opacity: .22; pointer-events: none; }
.hero-morph svg { width: 100%; height: auto; overflow: visible; }
.hero-morph .m-fill { fill: currentColor; stroke: none; }
.hero-morph .m-pk { stroke-width: 3.5; }
.hero-morph .m-dot { fill: currentColor; stroke: none; }
.hero-morph .m-ax { stroke-width: 1.6; stroke-dasharray: 1; }
.hero-morph .m-edge { stroke-width: 2; }
.hero-morph .m-cap { font: 500 18px var(--mono); fill: currentColor; stroke: none; letter-spacing: .12em; text-transform: uppercase; }
.hero-morph svg * { opacity: 0; }
.hero-morph .m-ok, .hero-morph .m-ok * { opacity: 1; }
.hero-morph .m-ok { opacity: 0; }
@media (prefers-reduced-motion: no-preference) {
  .hero-morph svg * { animation-duration: 18s; animation-iteration-count: infinite; animation-fill-mode: both; animation-timing-function: ease-in-out; animation-delay: var(--o, 0s); }
  .hero-morph .m-ok * { animation: none; }
  .hero-morph .m-d { stroke-dasharray: 1; }
  .hero-morph .m-tube { animation-name: mo-tube; }
  .hero-morph .m-liq { transform-box: fill-box; transform-origin: bottom; animation-name: mo-liq; }
  .hero-morph .m-drop { animation-name: mo-drop; }
  .hero-morph .m-col { animation-name: mo-col; }
  .hero-morph .m-band { animation-name: mo-band; }
  .hero-morph .m-base { animation-name: mo-base; }
  .hero-morph .m-ion { animation-name: mo-ion; }
  .hero-morph .m-pk { transform-box: fill-box; transform-origin: bottom; animation-name: mo-pk; }
  .hero-morph .m-dot { transform-box: fill-box; transform-origin: center; animation-name: mo-ns; }
  .hero-morph .m-dot.sig { animation-name: mo-sig; }
  .hero-morph .m-cloud { animation-name: mo-cloud; }
  .hero-morph .m-ax { animation-name: mo-ax; }
  .hero-morph .m-edge { animation-name: mo-edge; }
  .hero-morph .m-page { animation-name: mo-page; }
  .hero-morph .m-txt { animation-name: mo-txt; }
  .hero-morph .m-ok { transform-box: fill-box; transform-origin: center; animation-name: mo-ok; }
  .hero-morph .m-cap { animation-name: mo-cap; animation-delay: calc(var(--c) * 3s); }
}
@media (prefers-reduced-motion: reduce) {
  .hero-morph .m-page, .hero-morph .m-txt, .hero-morph .m-edge, .hero-morph .m-ok { opacity: 1; }
  .hero-morph .m-dot.sig { opacity: 1; transform: translate(var(--dx), var(--dy)) scale(1.5); transform-box: fill-box; transform-origin: center; }
}
@keyframes mo-tube { 0% { opacity: 1; stroke-dashoffset: 1; } 5% { stroke-dashoffset: 0; } 30% { opacity: 1; stroke-dashoffset: 0; } 34% { opacity: 0; } 100% { opacity: 0; stroke-dashoffset: 0; } }
@keyframes mo-liq { 0% { opacity: 1; transform: scaleY(0); } 3% { transform: scaleY(0); } 12% { transform: scaleY(1); } 18% { transform: scaleY(1); } 28% { transform: scaleY(.04); opacity: 1; } 31% { opacity: 0; } 100% { opacity: 0; transform: scaleY(0); } }
@keyframes mo-drop { 0%, 16% { opacity: 0; transform: translateY(0); } 17% { opacity: 1; } 20% { opacity: 1; transform: translateY(38px); } 20.5%, 100% { opacity: 0; transform: translateY(38px); } }
@keyframes mo-col { 0%, 13% { opacity: 1; stroke-dashoffset: 1; } 19% { stroke-dashoffset: 0; } 46% { opacity: 1; stroke-dashoffset: 0; } 50% { opacity: 0; } 100% { opacity: 0; stroke-dashoffset: 0; } }
@keyframes mo-band { 0%, 20% { opacity: 0; } 24% { opacity: 1; } 44% { opacity: 1; } 48%, 100% { opacity: 0; } }
@keyframes mo-base { 0%, 32% { opacity: 1; stroke-dashoffset: 1; } 37% { stroke-dashoffset: 0; } 58% { opacity: 1; stroke-dashoffset: 0; } 62%, 100% { opacity: 0; stroke-dashoffset: 0; } }
@keyframes mo-ion { 0%, 31% { opacity: 0; transform: translate(0, 0); } 33% { opacity: 1; transform: translate(0, 0); } 37.5% { transform: translate(var(--mx), -60px); } 42% { opacity: 1; transform: translate(var(--dx), var(--dy)); } 43%, 100% { opacity: 0; transform: translate(var(--dx), var(--dy)); } }
@keyframes mo-pk { 0%, 41% { opacity: 0; transform: scaleY(0); } 42% { opacity: 1; } 46% { transform: scaleY(1); } 52% { opacity: 1; transform: scaleY(1); } 55% { opacity: 1; transform: scaleY(0); } 56%, 100% { opacity: 0; transform: scaleY(0); } }
@keyframes mo-ns { 0%, 51% { opacity: 0; transform: translate(0, 0); } 53% { opacity: 1; transform: translate(0, 0); } 62% { opacity: 1; transform: translate(var(--dx), var(--dy)); } 67% { opacity: .9; transform: translate(var(--dx), var(--dy)); } 71%, 100% { opacity: 0; transform: translate(var(--dx), var(--dy)); } }
@keyframes mo-sig { 0%, 51% { opacity: 0; transform: translate(0, 0) scale(1); } 53% { opacity: 1; transform: translate(0, 0) scale(1); } 62% { transform: translate(var(--dx), var(--dy)) scale(1); } 68% { transform: translate(var(--dx), var(--dy)) scale(1); } 72% { transform: translate(var(--dx), var(--dy)) scale(1.7); } 95% { opacity: 1; transform: translate(var(--dx), var(--dy)) scale(1.7); } 99%, 100% { opacity: 0; transform: translate(var(--dx), var(--dy)) scale(1.7); } }
@keyframes mo-cloud { 0%, 56% { opacity: 0; } 62% { opacity: .55; } 66% { opacity: .55; } 70%, 100% { opacity: 0; } }
@keyframes mo-ax { 0%, 55% { opacity: 1; stroke-dashoffset: 1; } 61% { stroke-dashoffset: 0; } 66% { opacity: 1; stroke-dashoffset: 0; } 70%, 100% { opacity: 0; stroke-dashoffset: 0; } }
@keyframes mo-edge { 0%, 71% { opacity: 1; stroke-dashoffset: 1; } 79% { stroke-dashoffset: 0; } 95% { opacity: 1; stroke-dashoffset: 0; } 99%, 100% { opacity: 0; stroke-dashoffset: 0; } }
@keyframes mo-page { 0%, 79% { opacity: 1; stroke-dashoffset: 1; } 86% { stroke-dashoffset: 0; } 95% { opacity: 1; stroke-dashoffset: 0; } 99%, 100% { opacity: 0; stroke-dashoffset: 0; } }
@keyframes mo-txt { 0%, 83% { opacity: 1; stroke-dashoffset: 1; } 89% { stroke-dashoffset: 0; } 95% { opacity: 1; stroke-dashoffset: 0; } 99%, 100% { opacity: 0; stroke-dashoffset: 0; } }
@keyframes mo-ok { 0%, 89% { opacity: 0; transform: scale(0); } 91% { opacity: 1; transform: scale(1.15); } 92% { transform: scale(1); } 95% { opacity: 1; transform: scale(1); } 99%, 100% { opacity: 0; transform: scale(1); } }
@keyframes mo-cap { 0% { opacity: 0; } 2% { opacity: 1; } 15% { opacity: 1; } 16.7%, 100% { opacity: 0; } }
@media (max-width: 1020px) { .hero-morph { width: 420px; right: -60px; opacity: .13; } }
@media (max-width: 820px)  { .hero-morph { top: 30px; right: -120px; width: 340px; opacity: .08; } }

/* question -> answer demo */
.demo { background: var(--white); border: 1px solid var(--line); border-radius: 16px; box-shadow: 0 30px 60px -40px rgba(11,42,20,.45); overflow: hidden; }
.demo-top { display: flex; align-items: center; gap: 6px; padding: 12px 16px; border-bottom: 1px solid var(--line); background: var(--green-50); }
.demo-top span { width: 9px; height: 9px; border-radius: 50%; background: var(--green-200); }
.demo-top b { margin-left: 10px; font: 500 .74rem var(--mono); letter-spacing: .1em; text-transform: uppercase; color: var(--ink-3); }
.demo-body { padding: 26px 26px 24px; }
.demo-label { font: 500 .72rem var(--mono); letter-spacing: .1em; text-transform: uppercase; color: var(--green-600); margin: 0 0 8px; }
.demo-q { font: 500 1.15rem/1.45 var(--serif); color: var(--green-900); min-height: 3.2em; margin: 0 0 20px; padding: 12px 14px; border: 1px solid var(--line); border-radius: 10px; background: var(--paper); }
.caret { display: inline-block; width: 2px; height: 1.05em; background: var(--green-700); vertical-align: -0.15em; margin-left: 2px; animation: caret 1s steps(1) infinite; }
@keyframes caret { 50% { opacity: 0; } }
.demo-chips { list-style: none; margin: 0 0 20px; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.chip { display: flex; align-items: center; gap: 8px; font-size: .84rem; color: var(--ink-3); border: 1px solid var(--line); border-radius: 999px; padding: 6px 10px 6px 6px; transition: color .3s, border-color .3s, background .3s; white-space: nowrap; }
.chip .ci { width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font: 500 .7rem var(--mono); background: var(--green-50); color: var(--ink-3); flex: none; transition: background .3s, color .3s; }
.chip.on { color: var(--green-800); border-color: var(--green-400); }
.chip.on .ci { background: var(--white); color: var(--green-700); box-shadow: 0 0 0 2px var(--green-400); animation: chip-pulse 1s ease-in-out infinite; }
.chip.done { color: var(--green-800); border-color: var(--green-200); background: var(--green-50); }
.chip.done .ci { background: var(--green-700); color: #fff; font-size: 0; }
.chip.done .ci::after { content: "✓"; font-size: .75rem; }
@keyframes chip-pulse { 50% { box-shadow: 0 0 0 5px rgba(79,154,90,.18); } }
.demo-res { display: grid; grid-template-columns: 180px 1fr; gap: 20px; align-items: center; padding: 18px; border-radius: 12px; background: var(--green-50); border: 1px solid var(--line); opacity: .35; transition: opacity .5s; }
.demo-res.show { opacity: 1; }
.demo-volc { width: 100%; height: auto; }
.demo-volc path { fill: none; stroke: var(--green-200); stroke-width: 1; stroke-dasharray: 3 3; }
.demo-volc circle { transform-box: fill-box; transform-origin: center; transform: scale(0); transition: transform .35s cubic-bezier(.3,1.6,.5,1); transition-delay: calc(var(--k) * 12ms); }
.demo-volc .vn { fill: var(--green-200); }
.demo-volc .vs { fill: var(--green-700); }
.demo-res.show .demo-volc circle { transform: scale(1); }
.demo-type { margin-bottom: 10px; }
.demo-find { font: 600 1.12rem/1.35 var(--serif); color: var(--green-900); margin: 0 0 6px; }
.demo-note { font-size: .78rem; color: var(--ink-3); margin: 0; font-style: italic; }
@media (max-width: 560px) {
  .demo-chips { grid-template-columns: repeat(2, 1fr); }
  .demo-res { grid-template-columns: 1fr; }
  .demo-volc { max-width: 240px; }
  .demo-body { padding: 20px 18px; }
}
/* ==== end home extras ==== */
"""

JS = r"""
/* ==== home extras: question demo ==== */
(function () {
  var demo = document.querySelector('.demo');
  if (!demo) return;
  var qt = demo.querySelector('.demo-qt'), chips = demo.querySelectorAll('.chip'),
      res = demo.querySelector('.demo-res'), type = demo.querySelector('.demo-type'), find = demo.querySelector('.demo-find');
  var EX = [
    ['Which plasma proteins change after treatment?', 'Discovery proteomics', '38 proteins changed · 4 pathways enriched'],
    ['Is this compound rewiring kinase signalling in our cells?', 'Phosphoproteomics', '112 phosphosites regulated · 3 kinases implicated'],
    ['Which metabolites separate responders from non-responders?', 'Untargeted metabolomics', '17 discriminating metabolites · clear group separation']
  ];
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function done() { chips.forEach(function (c) { c.className = 'chip done'; }); res.classList.add('show'); }
  if (reduce) { done(); return; }
  var visible = false, running = false, n = 0;
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  async function cycle() {
    running = true;
    while (visible) {
      var ex = EX[n++ % EX.length];
      chips.forEach(function (c) { c.className = 'chip'; });
      res.classList.remove('show');
      qt.textContent = '';
      await wait(500);
      for (var i = 1; i <= ex[0].length; i++) { qt.textContent = ex[0].slice(0, i); await wait(32); }
      type.textContent = ex[1]; find.textContent = ex[2];
      await wait(600);
      for (var k = 0; k < chips.length; k++) {
        chips[k].className = 'chip on'; await wait(k === 3 || k === 4 ? 1100 : 750);
        chips[k].className = 'chip done';
      }
      res.classList.add('show');
      await wait(4800);
    }
    running = false;
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible && !running) cycle();
    }, { threshold: 0.35 }).observe(demo);
  } else { done(); }
})();
/* ==== end home extras ==== */
"""

# ---------------- apply (re-runnable) ----------------
p = os.path.join(SITE, "index.html")
h = open(p, encoding="utf-8").read()
h = re.sub(r'    <div class="hero-morph".*?</svg></div>\n', '', h, flags=re.S)
h = re.sub(r'<!-- demo:start -->.*?<!-- demo:end -->\n', '', h, flags=re.S)
anchor = '<section class="hero">\n  <div class="wrap">\n'
assert anchor in h
h = h.replace(anchor, anchor + "    " + MORPH + "\n", 1)
# demo goes right after the "How it works" section (before Applications)
anchor2 = '<section class="band">'
assert anchor2 in h
h = h.replace(anchor2, DEMO + anchor2, 1)
open(p, "w", encoding="utf-8").write(h)

c = os.path.join(SITE, "assets", "css", "style.css")
css = open(c, encoding="utf-8").read()
css = re.sub(r'\n/\* ==== home extras ==== \*/.*?/\* ==== end home extras ==== \*/\n', '\n', css, flags=re.S).rstrip() + "\n" + CSS
open(c, "w", encoding="utf-8").write(css)

j = os.path.join(SITE, "assets", "js", "site.js")
js = open(j, encoding="utf-8").read()
js = re.sub(r'\n/\* ==== home extras: question demo ==== \*/.*?/\* ==== end home extras ==== \*/\n', '\n', js, flags=re.S).rstrip() + "\n" + JS
open(j, "w", encoding="utf-8").write(js)

if SCRIPT:
    s = open(SCRIPT, encoding="utf-8").read()
    marker = "# --- home extras (added) ---"
    if marker not in s:
        s += f'\n{marker}\n_sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_anim.py"), OUT], check=True)\n'
        open(SCRIPT, "w", encoding="utf-8").write(s)
print("home extras added")
