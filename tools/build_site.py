"""Generates the static Access MS site into ../site (plain HTML output, no runtime deps)."""
import random, os, sys

OUT = sys.argv[1]
SITE = "https://accessms.ca"
EMAIL = "admin@accessms.ca"
LINKEDIN = "https://ca.linkedin.com/in/access-ms-scientific-ba0167292"

# ---------------- shared bits ----------------
PEAKS_E = ('<svg viewBox="0 0 20 16" aria-hidden="true"><g stroke="currentColor" stroke-width="1.6" stroke-linecap="round">'
           '<line x1="4" y1="15" x2="4" y2="8"/><line x1="7.5" y1="15" x2="7.5" y2="11"/><line x1="10" y1="15" x2="10" y2="1.5"/>'
           '<line x1="12.8" y1="15" x2="12.8" y2="10"/><line x1="16" y1="15" x2="16" y2="5.5"/></g>'
           '<line x1="1" y1="15.2" x2="19" y2="15.2" stroke="currentColor" stroke-width="1"/></svg>')

def chain(bg="var(--paper)"):
    pills = "".join(f'<rect x="{x}" y="10" width="17" height="8" rx="4" fill="{bg}"/>' for x in (1, 23.5, 46))
    return ('<svg class="chain" viewBox="0 0 64 28" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2">'
            '<rect x="9" y="2" width="21" height="24" rx="9"/><rect x="34" y="2" width="21" height="24" rx="9"/>'
            f'{pills}</svg>')

def logo(cls="", bg="var(--paper)", href="index.html"):
    return (f'<a class="logo {cls}" href="{href}" aria-label="Access MS Scientific — home">'
            f'<span class="wordmark">ACC<span class="e">e{PEAKS_E}</span>SS<span class="gap"></span>MS</span>{chain(bg)}</a>')

ICON = {
 "arrow": '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8h11M9 4l4 4-4 4"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m7.5 12.3 3 3 6-6.3"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4v11.25H3zM9.5 9.75h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-4.98c0-1.19-.02-2.72-1.66-2.72-1.66 0-1.92 1.3-1.92 2.63V21h-4z"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.5"/><path d="M12 7v5.2l3.4 2"/></svg>',
 # service icons
 "consult": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9h20a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3H15l-6 5v-5H6a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3z"/><path d="M29 15h5a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3h-2v4l-5-4h-6a3 3 0 0 1-3-3"/><path d="M10 15h12M10 19h8"/></svg>',
 "plan": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="6" width="24" height="30" rx="3"/><path d="M15 4h10v5H15z"/><path d="M13 17l2 2 4-4M13 26l2 2 4-4M22 17h6M22 27h6"/></svg>',
 "sample": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M15 4h10M17 4v12L8 32a3 3 0 0 0 2.6 4.5h18.8A3 3 0 0 0 32 32l-9-16V4"/><path d="M12 26h16"/><circle cx="17" cy="31" r="1.2"/><circle cx="23" cy="29.5" r="1"/></svg>',
 "data": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4 34h32"/><path d="M8 34v-6M12 34V14M16 34v-9M20 34V6M24 34v-13M28 34v-5M32 34V18"/></svg>',
 "analysis": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="12" r="3"/><circle cx="29" cy="9" r="3"/><circle cx="20" cy="22" r="3.5"/><circle cx="9" cy="31" r="3"/><circle cx="31" cy="30" r="3"/><path d="M12.4 13.8l5.3 6M26.6 10.8l-4.8 8.6M17.3 24.4l-6 4.8M23 24l5.4 4.4"/></svg>',
 "publish": '<svg viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M10 4h14l8 8v22a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="M24 4v8h8"/><path d="M13 28v-4M17 28v-8M21 28v-5M25 28v-10"/></svg>',
}

NAV = [("services.html", "Services"), ("analytics.html", "Analytics"), ("about.html", "About")]

def head(title, desc, path):
    full = title if title.startswith("Access MS") else f"{title} — Access MS Scientific"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{'' if path=='index.html' else path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Access MS Scientific">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{'' if path=='index.html' else path}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#04530e">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,500;0,8..60,600;1,8..60,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

def header(active):
    AC = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{AC if h == active else ""}>{t}</a>' for h, t in NAV)
    cur = ' aria-current="page"' if active == "contact.html" else ""
    return f"""<header class="site-header">
  <div class="wrap">
    {logo()}
    <button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn" href="contact.html"{cur}>Start a project</a></nav>
  </div>
</header>
<main id="main">
"""

FOOTER = f"""</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="top">
      <div>
        {logo(bg="var(--green-900)")}
        <p class="tagline">All-in-one mass spectrometry research facilitation services. Based in Toronto, working with researchers everywhere.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul><li><a href="services.html">Services</a></li><li><a href="analytics.html">Analytics</a></li><li><a href="about.html">About</a></li><li><a href="contact.html">Contact</a></li></ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Toronto, Ontario, Canada</li></ul>
        <div class="social"><a href="{LINKEDIN}" aria-label="Access MS Scientific on LinkedIn" rel="noopener" target="_blank">{ICON['linkedin']}</a><a href="mailto:{EMAIL}" aria-label="Email Access MS Scientific">{ICON['mail']}</a></div>
      </div>
    </div>
    <div class="bottom"><span>© <span id="year">2026</span> Access MS Scientific Inc.</span><span>Mass spectrometry · Proteomics · Metabolomics · Bioinformatics</span></div>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""

def cta(title="Have a project in mind?", text="Tell us about your samples and your research question. We'll reply with a recommended approach and next steps."):
    return f"""<section class="cta"><div class="wrap"><div class="cta-box reveal">
  {spectrum_svg(seed=7, w=600, h=160, labels=False, cls='bg', n=46)}
  <div><h2>{title}</h2><p>{text}</p></div>
  <div class="actions"><a class="btn btn--light" href="contact.html">Start a project {ICON['arrow']}</a></div>
</div></div></section>
"""

def btn(href, text, ghost=False):
    return f'<a class="btn{" btn--ghost" if ghost else ""}" href="{href}">{text} {ICON["arrow"]}</a>'

# ---------------- spectrum ----------------
def spectrum_svg(seed=3, w=1160, h=230, labels=True, cls="spectrum", n=110):
    rnd = random.Random(seed)
    base = h - (26 if labels else 2)
    top = 30 if labels else 4
    out = [f'<svg class="{cls}" viewBox="0 0 {w} {h}" aria-hidden="true" preserveAspectRatio="none">' if cls == "bg"
           else f'<div class="spectrum-wrap"><svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="Stylized mass spectrum">']
    big = {} if not labels else {0.12: ("301.14", .55), 0.27: ("445.21", .78), 0.41: ("612.33", 1.0), 0.58: ("788.40", .66), 0.74: ("905.47", .84), 0.9: ("1102.55", .48)}
    xs = sorted(rnd.uniform(0.02, 0.98) for _ in range(n))
    i = 0
    for x in xs:
        hh = rnd.random() ** 3 * 0.42 + 0.02
        klass = "pk lo" if hh < .12 else "pk"
        X = round(x * w, 1)
        out.append(f'<line class="{klass}" style="--i:{i};--x:{x:.3f}" x1="{X}" x2="{X}" y1="{base}" y2="{round(base - hh*(base-top),1)}"' + (' stroke="currentColor"' if cls == "bg" else '') + '/>')
        i += 1
    for x, (lab, hh) in big.items():
        X = round(x * w, 1); Y = round(base - hh * (base - top), 1)
        out.append(f'<line class="pk hi" style="--i:{i-n};--x:{x}" x1="{X}" x2="{X}" y1="{base}" y2="{Y}"/>')
        out.append(f'<text class="lbl" style="--x:{x}" x="{X}" y="{Y-9}" text-anchor="middle">{lab}</text>')
        i += 1
    if labels:
        out.append(f'<line class="scan" x1="0" x2="0" y1="{top-22}" y2="{base}"/>')
        out.append(f'<line class="base" x1="0" x2="{w}" y1="{base}" y2="{base}"/>')
        for t in range(1, 10):
            X = round(t * w / 10, 1)
            out.append(f'<line class="base" x1="{X}" x2="{X}" y1="{base}" y2="{base+5}"/><text x="{X}" y="{base+19}" text-anchor="middle">{t*125}</text>')
        out.append(f'<text x="{w-2}" y="{base+19}" text-anchor="end">m/z</text>')
    out.append("</svg>" + ("</div>" if cls != "bg" else ""))
    return "".join(out)

# ---------------- tier mini-visuals ----------------
G7, G4, G2 = "#04530e", "#4f9a5a", "#cfe3cf"
STROKE_LO = 'stroke="#4f9a5a" stroke-width=".4"'
def viz_qc():
    s = ['<svg viewBox="0 0 200 110" aria-hidden="true">']
    rnd = random.Random(11)
    for i in range(10):
        x = 14 + i * 19; mid = 55 + rnd.uniform(-6, 6); iqr = rnd.uniform(9, 14)
        s.append(f'<line x1="{x}" x2="{x}" y1="{mid-iqr-12}" y2="{mid+iqr+12}" stroke="{G4}" stroke-width="1.2"/>')
        s.append(f'<rect x="{x-6}" y="{mid-iqr}" width="12" height="{2*iqr}" rx="2" fill="{G2}" stroke="{G7}" stroke-width="1.2"/>')
        s.append(f'<line x1="{x-6}" x2="{x+6}" y1="{mid}" y2="{mid}" stroke="{G7}" stroke-width="1.6"/>')
    s.append(f'<line x1="4" x2="196" y1="104" y2="104" stroke="{G4}" stroke-width="1"/></svg>')
    return "".join(s)

def viz_volcano():
    rnd = random.Random(5); s = ['<svg viewBox="0 0 200 110" aria-hidden="true">']
    for _ in range(170):
        fc = rnd.gauss(0, 1.1); p = abs(fc) * rnd.uniform(.4, 1.6) * 22 + rnd.uniform(0, 8)
        x = 100 + fc * 32; y = 102 - min(p, 92)
        if not (4 < x < 196): continue
        sig = abs(fc) > 1.2 and p > 30
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.4 if sig else 1.7}" fill="{G7 if sig else G2}" {"" if sig else STROKE_LO}/>')
    s.append(f'<line x1="61" x2="61" y1="4" y2="104" stroke="{G4}" stroke-dasharray="3 3" stroke-width="1"/><line x1="139" x2="139" y1="4" y2="104" stroke="{G4}" stroke-dasharray="3 3" stroke-width="1"/>')
    s.append(f'<line x1="4" x2="196" y1="72" y2="72" stroke="{G4}" stroke-dasharray="3 3" stroke-width="1"/></svg>')
    return "".join(s)

def viz_pca():
    rnd = random.Random(9); s = ['<svg viewBox="0 0 200 110" aria-hidden="true">']
    s.append(f'<ellipse cx="66" cy="62" rx="40" ry="26" transform="rotate(-18 66 62)" fill="{G2}" fill-opacity=".55" stroke="{G4}" stroke-width="1"/>')
    s.append(f'<ellipse cx="138" cy="44" rx="38" ry="24" transform="rotate(-18 138 44)" fill="none" stroke="{G7}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    for _ in range(18):
        s.append(f'<circle cx="{66+rnd.gauss(0,13):.1f}" cy="{62+rnd.gauss(0,8):.1f}" r="3" fill="#fff" stroke="{G4}" stroke-width="1.4"/>')
    for _ in range(18):
        s.append(f'<circle cx="{138+rnd.gauss(0,12):.1f}" cy="{44+rnd.gauss(0,8):.1f}" r="3" fill="{G7}"/>')
    s.append(f'<line x1="8" x2="196" y1="104" y2="104" stroke="{G4}" stroke-width="1"/><line x1="8" x2="8" y1="4" y2="104" stroke="{G4}" stroke-width="1"/></svg>')
    return "".join(s)

def viz_net():
    nodes = [(100,55,7),(55,30,5),(150,28,5),(40,78,4),(160,82,5),(100,95,4),(75,60,3.5),(128,62,3.5),(22,45,3),(184,52,3),(118,14,3),(70,100,3),(140,104,3)]
    edges = [(0,1),(0,2),(0,6),(0,7),(1,3),(1,8),(2,9),(2,10),(4,7),(4,9),(5,6),(5,7),(3,11),(5,12),(4,12),(1,6),(2,7),(3,6)]
    s = ['<svg viewBox="0 0 200 110" aria-hidden="true">']
    for a, b in edges:
        s.append(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{G4}" stroke-width="1" stroke-opacity=".7"/>')
    for i, (x, y, r) in enumerate(nodes):
        hub = r >= 5
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{G7 if hub else "#fff"}" stroke="{G7}" stroke-width="1.3"/>')
    s.append("</svg>")
    return "".join(s)

# ---------------- content ----------------
STEPS = [
 ("consult", "Initial consultation", "We start with your research question, not with an instrument.",
  "A scientist-to-scientist conversation about your hypothesis, sample types, timelines and budget. We tell you candidly what mass spectrometry can and cannot answer for your project.",
  ["Review of your research question and existing data", "Feasibility and sample-size discussion", "Recommended analytical strategy and scope"]),
 ("plan", "Experimental project plan", "A written plan you can take to your lab, your PI or your grant.",
  "We design the study around statistical power and the biology you care about, then match it to the most suitable acquisition strategy and platform.",
  ["Study design, controls and randomization", "Choice of quantitation strategy (label-free, labelled or targeted)", "Sample submission guide and timeline"]),
 ("sample", "Sample preparation", "Robust, reproducible preparation is where good data begins.",
  "Protocols are optimized for your matrix — cells, tissue, plasma or serum, biofluids or purified material — with QC samples and standards built in from the start.",
  ["Extraction, digestion and clean-up", "Enrichment for post-translational modifications", "Process controls and pooled QC samples"]),
 ("data", "Data generation", "Current-generation LC-MS, matched to the question.",
  "Your samples are acquired on the platform best suited to the project, either in-house or through trusted partner facilities, with performance monitored throughout every run.",
  ["Discovery (DDA / DIA) and targeted acquisition", "System-suitability and QC monitoring", "Raw data and acquisition metadata delivered"]),
 ("analysis", "Data analysis", "From raw spectra to statistically sound biological insight.",
  "Identification, quantitation and statistics are performed with established, documented pipelines, then integrated with pathways, networks and your other data.",
  ["Identification, quantitation and QC reporting", "Differential, multivariate and network analysis", "Interactive review of results with your team"]),
 ("publish", "Pre-publication services", "Support until the paper is out the door.",
  "We help you present the work clearly and meet journal and repository requirements, and stay available through peer review.",
  ["Publication-quality figures and tables", "Methods text and supplementary data", "Repository deposition and reviewer responses"]),
]

AREAS = [
 ("Proteomics", "Global protein identification and quantitation across cells, tissues and biofluids."),
 ("Post-translational modifications", "Phosphoproteomics, glycosylation and other PTMs, with site-level localization."),
 ("Metabolomics", "Targeted and untargeted profiling of small-molecule metabolites."),
 ("RNA modifications", "Detection and quantitation of modified nucleosides by LC-MS."),
 ("Biomarker analysis", "Discovery, verification and targeted panels for translational studies."),
 ("Drug discovery", "Target engagement, mechanism of action and compound characterization."),
 ("Toxicology", "Quantitation of drugs, metabolites and exposures in complex matrices."),
 ("Small-molecule analysis", "Accurate-mass identification and quantitative small-molecule assays."),
]

TIERS = [
 ("Organization &amp; quality control", viz_qc(), "Raw output is organized, normalized and checked before any biology is interpreted.",
  "Missing-value handling, normalization, batch and run-order assessment, and outlier detection.",
  "QC report with clean, analysis-ready tables"),
 ("Pairwise analysis", viz_volcano(), "Which molecules change between conditions, by how much, and with what confidence.",
  "Fold-change and significance testing with appropriate multiple-testing correction.",
  "Ranked differential lists and volcano plots"),
 ("Multidimensional analysis", viz_pca(), "Patterns across many samples and conditions at once.",
  "PCA, clustering, heatmaps, time-course and multi-group designs, plus classification where appropriate.",
  "Sample-level structure, clusters and candidate signatures"),
 ("Network biology &amp; integration", viz_net(), "Placing your results in biological context.",
  "Pathway and enrichment analysis, interaction networks, and integration with transcriptomic or clinical data.",
  "Pathways, networks and an integrated biological story"),
]

def write(name, html):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)

# ---------------- index ----------------
flow = "".join(f'<li class="reveal" style="transition-delay:{i*60}ms"><div class="num">0{i+1}</div><h3>{t}</h3><p>{short}</p></li>'
               for i, (_, t, short, *_r) in enumerate(STEPS))
areas = "".join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in AREAS)
tierlist = "".join(f'<div><span class="k">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, _v, d, *_r) in enumerate(TIERS[:3]))

index = head("Access MS Scientific — Mass spectrometry research services",
             "All-in-one mass spectrometry research facilitation: experimental design, sample preparation, data generation, bioinformatic analysis and pre-publication support. Based in Toronto.",
             "index.html") + header("index.html") + f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Mass spectrometry research services · Toronto</p>
    <h1>Mass spectrometry expertise, <em>from question to publication.</em></h1>
    <p class="lead">Access MS Scientific is an all-in-one research facilitation service. We design your experiment, prepare and run your samples on the right platform, and turn raw spectra into results you can publish, so your team can stay focused on the science.</p>
    <div class="actions">{btn("contact.html", "Start a project")}{btn("services.html", "Explore services", ghost=True)}</div>
    {spectrum_svg()}
    <div class="strip">
      <div><b>End-to-end</b><span>One partner from the first call to the final figure</span></div>
      <div><b>Platform-independent</b><span>Matched to your question, not to a single instrument</span></div>
      <div><b>Expert-led</b><span>Founded by mass spectrometry scientists from the University of Toronto</span></div>
      <div><b>Publication-ready</b><span>Figures, methods text and data deposition support</span></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">How it works</p><h2>Six stages, one accountable team.</h2></div>
      <p>Engage us for the whole journey or for just the stage you need. Every project begins with a consultation and an agreed plan before a single sample is run.</p>
    </div>
    <ol class="flow">{flow}</ol>
    <div class="actions">{btn("services.html", "See what each stage includes", ghost=True)}</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">Applications</p><h2>Built for the questions biomedical researchers ask.</h2></div>
      <p>From global discovery proteomics to targeted quantitation of a single compound, we support projects across the life sciences.</p>
    </div>
    <div class="areas reveal">{areas}</div>
  </div>
</section>

<section class="dark">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Analytics</p>
      <h2>Data is only the beginning.</h2>
      <p>Our analysis services range from qualitative characterization of a single molecule to in-depth integration of large multi-omics datasets. You receive results you can understand, defend and build on.</p>
      <div class="actions"><a class="btn btn--light" href="analytics.html">Explore analytics {ICON['arrow']}</a></div>
    </div>
    <div class="principles reveal" style="grid-template-columns:1fr; gap:28px">{tierlist}<div><span class="k">04</span><h3>Network biology &amp; integration</h3><p>Placing your results in biological context.</p></div></div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Why Access MS</p>
      <h2>More than a data file at the end of a queue.</h2>
      <p class="lead">Many providers stop at the data file. We stay with the project, from shaping the design up front to supporting you through peer review.</p>
    </div>
    <ul class="checklist reveal">
      <li>{ICON['check']}<strong>Design before data</strong><span>A clear, written experimental plan with the controls and statistics your reviewers will expect.</span></li>
      <li>{ICON['check']}<strong>The right platform for each project</strong><span>We are not tied to one vendor or instrument, and route each study to the best-suited platform, in-house or through trusted partners.</span></li>
      <li>{ICON['check']}<strong>Quality control at every step</strong><span>QC samples, standards and performance monitoring are built in, and reported back to you.</span></li>
      <li>{ICON['check']}<strong>Results you can publish</strong><span>Figures, methods and repository deposition prepared to journal standards.</span></li>
    </ul>
  </div>
</section>
""" + cta() + FOOTER
write("index.html", index)

# ---------------- services ----------------
steps = "".join(f"""<article class="step reveal" id="{k}">
  <div class="n">Stage 0{i+1}</div>
  <div><h3>{t}</h3><p><strong>{short}</strong></p><p>{long}</p></div>
  <ul>{''.join(f'<li>{x}</li>' for x in items)}</ul>
</article>""" for i, (k, t, short, long, items) in enumerate(STEPS))
cards = "".join(f'<div class="card reveal"><div class="ico">{ICON[k]}</div><h3>{t}</h3><p>{short}</p></div>' for k, t, short, *_ in STEPS)

services = head("Services", "Mass spectrometry services from initial consultation and experimental design through sample preparation, data generation, data analysis and pre-publication support.", "services.html") + header("services.html") + f"""
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Services</p>
    <h1>Everything your mass spectrometry project needs, in one place.</h1>
    <p class="lead">We give researchers access to advanced mass spectrometry technologies, rigorous experimental design and proven analysis pipelines, with the service and scientific depth to see a project through to publication.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">At a glance</p><h2>Pick a single stage, or hand us the whole project.</h2></div>
      <p>Each stage stands on its own, but they work best together. Most clients begin with a consultation and decide the scope from there.</p>
    </div>
    <div class="grid-3">{cards}</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">In detail</p><h2>What each stage includes.</h2></div>
      <p>Deliverables are agreed in writing at the planning stage, so you always know what you will receive and when.</p>
    </div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">Applications</p><h2>Areas of expertise.</h2></div>
      <p>Proteomics, metabolomics and beyond, applied wherever mass spectrometry can move the research forward.</p>
    </div>
    <div class="areas reveal">{areas}</div>
  </div>
</section>
""" + cta() + FOOTER
write("services.html", services)

# ---------------- analytics ----------------
tiers = "".join(f"""<article class="tier reveal" style="transition-delay:{i*70}ms">
  <div class="viz">{v}</div>
  <div class="body"><span class="tag">Tier 0{i+1}</span><h3>{t}</h3><p>{d}</p><p>{how}</p></div>
  <div class="out"><b>You receive</b>{out}</div>
</article>""" for i, (t, v, d, how, out) in enumerate(TIERS))

analytics = head("Analytics", "Mass spectrometry data analysis: quality control, pairwise and multidimensional statistics, network biology and multi-omics integration.", "analytics.html") + header("analytics.html") + f"""
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Analytics</p>
    <h1>From raw spectra to biological insight.</h1>
    <p class="lead">Our analysis services range from single-molecule qualitative (bio)chemical analyses to in-depth analysis and integration of large -omics datasets. Each tier builds on the one before it.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">Analysis tiers</p><h2>Four levels of analysis, one consistent pipeline.</h2></div>
      <p>Choose the depth your project needs. Every tier is documented and reproducible, and comes with a walkthrough of the results with your team.</p>
    </div>
    <div class="tiers">{tiers}</div>
  </div>
</section>

<section class="band">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Deliverables</p>
      <h2>Results you can understand, defend and reuse.</h2>
      <p class="lead">We don't send a spreadsheet and disappear. You receive a complete, documented package and a scientist to talk it through with.</p>
      <div class="actions">{btn("contact.html", "Discuss your data")}</div>
    </div>
    <ul class="checklist reveal">
      <li>{ICON['check']}<strong>Quality-control report</strong><span>How the data behaved, what was filtered and why.</span></li>
      <li>{ICON['check']}<strong>Annotated results tables</strong><span>Identifications, quantities and statistics, ready for your own follow-up.</span></li>
      <li>{ICON['check']}<strong>Publication-quality figures</strong><span>Volcano plots, heatmaps, PCA, pathway and network figures in editable formats.</span></li>
      <li>{ICON['check']}<strong>Methods and parameters</strong><span>Written methods text and full processing parameters for reproducibility.</span></li>
      <li>{ICON['check']}<strong>Bring your own data</strong><span>Already have MS data? We can analyze or re-analyze existing datasets.</span></li>
    </ul>
  </div>
</section>
""" + cta("Already have data waiting to be analyzed?", "Send us a short description of your dataset and goals. We'll suggest the right analysis tier and timeline.") + FOOTER
write("analytics.html", analytics)

# ---------------- about ----------------
about = head("About", "Access MS Scientific is a Toronto-based mass spectrometry research facilitation company founded by mass spectrometry scientists from the University of Toronto.", "about.html") + header("about.html") + f"""
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">About us</p>
    <h1>Mass spectrometry scientists, working on your side.</h1>
    <p class="lead">Access MS Scientific was founded by a team of mass spectrometry experts from the University of Toronto to make advanced MS accessible to every research group, whether or not it has a mass spectrometer down the hall.</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Who we are</p>
      <h2>A partner, not a queue.</h2>
      <p>Based in Toronto, Ontario, we provide consultation for all MS-based research needs: experimental design, access to current-generation mass spectrometry, and a complete analysis pipeline.</p>
      <p>Our team has hands-on experience across proteomics, post-translational modifications, metabolomics, RNA modifications, drug discovery, biomarker analysis and toxicology. That breadth lets us see a project from every angle: the chemistry, the biology and the statistics.</p>
      <div class="actions">{btn("services.html", "Our services", ghost=True)}</div>
    </div>
    <div class="reveal">
      <div class="areas" style="grid-template-columns:1fr 1fr">{''.join(f'<div><h3>{t}</h3></div>' for t, _ in AREAS)}</div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">How we work</p><h2>Principles behind every project.</h2></div>
      <p>The things we would want from a mass spectrometry partner ourselves.</p>
    </div>
    <div class="principles">
      <div class="reveal"><span class="k">01 — Independent</span><h3>The right tool for the question</h3><p>We are not tied to a single vendor or instrument. Each project runs on the most suitable platform, in-house or through trusted partner facilities.</p></div>
      <div class="reveal"><span class="k">02 — Rigorous</span><h3>Quality you can see</h3><p>Controls, QC samples and documented pipelines are standard, and you get the evidence, not just our word for it.</p></div>
      <div class="reveal"><span class="k">03 — Collaborative</span><h3>Scientist to scientist</h3><p>You work directly with experienced researchers who explain the choices, the caveats and the results in plain terms.</p></div>
    </div>
  </div>
</section>
""" + cta() + FOOTER
write("about.html", about)

# ---------------- contact ----------------
import urllib.parse
body = ("Hello Access MS team,\n\n"
        "Research question / goal:\n\n"
        "Sample type(s) and approximate number:\n\n"
        "Analysis of interest (e.g. proteomics, PTMs, metabolomics, targeted quantitation):\n\n"
        "Timeline:\n\n"
        "Services needed (consultation / design / sample prep / data generation / analysis / publication support):\n\n"
        "Thank you,\n")
mailto = f"mailto:{EMAIL}?subject=" + urllib.parse.quote("Project inquiry") + "&body=" + urllib.parse.quote(body)

contact = head("Contact", "Start a mass spectrometry project with Access MS Scientific. Email admin@accessms.ca.", "contact.html") + header("contact.html") + f"""
<section class="page-hero">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Let's talk about your project.</h1>
    <p class="lead">Every project starts with a conversation. Send us a few details and a member of our scientific team will get back to you with a suggested approach and next steps.</p>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Before you write</p>
      <h2>What helps us respond quickly.</h2>
      <p>Rough answers are fine; we'll refine everything together during the consultation.</p>
      <ul class="checklist">
        <li>{ICON['check']}<strong>Your research question</strong><span>What you want to learn, and any hypotheses you are testing.</span></li>
        <li>{ICON['check']}<strong>Samples</strong><span>Sample type (cells, tissue, plasma, etc.), approximate number and how they are stored.</span></li>
        <li>{ICON['check']}<strong>Analysis of interest</strong><span>Proteomics, PTMs, metabolomics, targeted quantitation, or simply "not sure yet".</span></li>
        <li>{ICON['check']}<strong>Timeline and stage</strong><span>Grant, manuscript or project deadlines, and which services you think you need.</span></li>
      </ul>
    </div>
    <aside class="contact-card reveal" aria-label="Contact details">
      <div class="row">{ICON['mail']}<div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
      <div class="row">{ICON['linkedin']}<div><b>LinkedIn</b><a href="{LINKEDIN}" target="_blank" rel="noopener">Access MS Scientific</a></div></div>
      <div class="row">{ICON['pin']}<div><b>Location</b><span>Toronto, Ontario, Canada</span></div></div>
      <a class="btn" href="{mailto}">Email us a project inquiry {ICON['arrow']}</a>
    </aside>
  </div>
</section>
""" + FOOTER
write("contact.html", contact)

# 404 page
nf = head("Page not found", "The page you are looking for could not be found.", "404.html") + header("") + f"""
<section class="page-hero" style="border:0;min-height:52vh">
  <div class="wrap">
    <p class="eyebrow">404 · no peak detected</p>
    <h1>We couldn't find that page.</h1>
    <p class="lead">It may have moved when we updated the site.</p>
    <div class="actions">{btn("index.html", "Back to home")}{btn("contact.html", "Contact us", ghost=True)}</div>
  </div>
</section>
""" + FOOTER
write("404.html", nf)
print("built")

# --- hero animation (added) ---
import subprocess as _sp
_sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "hero_anim.py"), OUT], check=True)

# --- home extras (added) ---
_sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_anim.py"), OUT], check=True)
