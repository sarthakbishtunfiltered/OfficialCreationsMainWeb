#!/usr/bin/env python3
"""Builds the Official Creations site into plain HTML files next to this script.

Edit copy in this file, details in site.config.json, styles in assets/css/oc.css.
Run:  python3 build.py
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
esc = html.escape

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&"
    'family=Instrument+Sans:wght@400;500;600;700&display=swap">'
)

# ---------- Icon family: one stroke weight, rounded, slightly hand-drawn ----------
SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-site" viewBox="0 0 24 24"><path d="M4 6.5c0-1 .8-2 2-2h12c1.2 0 2 1 2 2v11c0 1-.8 2-2 2H6c-1.2 0-2-1-2-2z"/><path d="M4.2 9.6c5.2.4 10.5.3 15.6-.1"/><path d="M7 7.2h.01M9.4 7.2h.01"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><path d="M10.5 4.5a6 6 0 1 0 .1 12 6 6 0 0 0-.1-12z"/><path d="M15.2 15.4l4.6 4.4"/></symbol>
<symbol id="i-identity" viewBox="0 0 24 24"><path d="M5 19l1-4.2L16.6 4.3a1.8 1.8 0 0 1 2.6 2.5L8.7 17.6z"/><path d="M14.8 6.2l2.9 2.8"/></symbol>
<symbol id="i-eye" viewBox="0 0 24 24"><path d="M2.8 12.2C5 8 8.3 6 12 6s7 2.1 9.2 6.1C19 16 15.7 18 12 18s-7-2-9.2-5.8z"/><path d="M12 9.6a2.6 2.6 0 1 0 .1 5.2 2.6 2.6 0 0 0-.1-5.2z"/></symbol>
<symbol id="i-social" viewBox="0 0 24 24"><path d="M5 5.5h14c.8 0 1.5.7 1.5 1.5v8c0 .8-.7 1.5-1.5 1.5h-6l-4 3v-3H5c-.8 0-1.5-.7-1.5-1.5V7c0-.8.7-1.5 1.5-1.5z"/></symbol>
<symbol id="i-flow" viewBox="0 0 24 24"><path d="M4.5 5h5.5v4.2H4.5z"/><path d="M14 14.8h5.5V19H14z"/><path d="M7.3 9.2v2.6c0 1.3.8 3 2.6 3H14"/></symbol>
<symbol id="i-system" viewBox="0 0 24 24"><path d="M12 4l8 4-8 4-8-4z"/><path d="M4 12.2l8 4 8-4"/><path d="M4 16l8 4 8-4"/></symbol>
<symbol id="i-funnel" viewBox="0 0 24 24"><path d="M4 5.5h16l-6 7.2v5.3l-4 1.8v-7.1z"/></symbol>
<symbol id="i-loop" viewBox="0 0 24 24"><path d="M19 12a7 7 0 1 1-2.2-5.1"/><path d="M19.2 4.6v3.8h-3.8"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M4 12h15M13.5 6.5L19 12l-5.5 5.5"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/><path d="M8 9.5h8M8 12.5h5"/></symbol>
</defs></svg>"""


def ico(name, cls=""):
    c = f"ico {cls}".strip()
    return f'<svg class="{c}" aria-hidden="true"><use href="#i-{name}"/></svg>'


EDGE_PATH = "M0 34C120 8 260 56 420 30S720 4 900 32s300 22 540-10V60H0z"


def edge(pos):
    return (f'<svg class="edge {pos}" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="{EDGE_PATH}"/></svg>')


def btn(label, href="book.html", ghost=False):
    cls = "btn ghost" if ghost else "btn"
    return f'<a class="{cls}" href="{href}"><span>{label}</span>{ico("arrow")}</a>'


# ---------- Shared chrome ----------
NAV = [
    ("index.html", "Home", "home"),
    ("ecosystem.html", "Our Ecosystem", "ecosystem"),
    ("digital-presence.html", "Digital Presence", "digital"),
    ("business-operations.html", "Business Operations", "ops"),
    ("products.html", "Products", "products"),
    ("about.html", "About", "about"),
]


def header(key):
    items = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if k == key else ""}>{t}</a>' for h, t, k in NAV
    )
    cta_cur = ' aria-current="page"' if key == "book" else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <div class="nav-bar">
    <a class="logo" href="index.html" aria-label="Official Creations, home"><img src="assets/img/oc-logo.png" alt="" width="280" height="336"><small>Official Creations</small></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu"><span></span><span></span></button>
    <nav id="nav-links" class="nav-links" aria-label="Main">
      {items}
      <a class="nav-cta" href="book.html"{cta_cur}>Book a Consultation</a>
    </nav>
  </div>
</header>"""


def footer():
    socials = "".join(
        f'<li><a href="{esc(u)}" rel="noopener">{esc(n)}</a></li>' for n, u in CFG["socials"].items() if u
    )
    email = CFG["contact_email"]
    email_li = "" if "REPLACE_ME" in email else f'<li><a href="mailto:{esc(email)}">{esc(email)}</a></li>'
    contact = f'<li><a href="book.html">Book a Consultation</a></li>{email_li}{socials}'
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div><img class="brand" src="assets/img/oc-logo-white.png" alt="Official Creations" width="280" height="336"><p class="brand-sub">Official Creations. From Offline to Online. Beyond.</p></div>
      <div><h4>Explore</h4><ul>
        <li><a href="index.html">Home</a></li><li><a href="ecosystem.html">Our Ecosystem</a></li>
        <li><a href="products.html">Products</a></li><li><a href="about.html">About</a></li></ul></div>
      <div><h4>Services</h4><ul>
        <li><a href="digital-presence.html">Digital Presence</a></li>
        <li><a href="business-operations.html">Business Operations</a></li></ul></div>
      <div><h4>Contact</h4><ul>{contact}</ul></div>
    </div>
    <div class="legal"><span>&copy; <span id="yr">2026</span> Official Creations</span><span>All rights reserved</span></div>
  </div>
</footer>"""


def page(fname, key, title, desc, body):
    doc = f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#EAE4E5">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="assets/img/oc-logo-white-on-black.png">
<link rel="apple-touch-icon" href="assets/img/oc-logo-white-on-black.png">
{FONTS}
<link rel="stylesheet" href="assets/css/oc.css">
</head>
<body>
{SPRITE}
{header(key)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/oc.js" defer></script>
</body>
</html>
"""
    (ROOT / fname).write_text(doc, encoding="utf-8")


def final_cta(text="Tell us about your business."):
    return f"""<section class="section dark final">{edge("top")}
  <div class="wrap">
    <h2>{text}</h2>
    <p class="lede">A first conversation to understand where your business is and where it could go. Not a sales pitch.</p>
    <div class="cta-row">{btn("Book a Consultation")}</div>
  </div>
</section>"""


# ---------- Ecosystem map (shared by home + ecosystem page) ----------
MAP_NODES = [
    ("Digital Presence", "How people find, judge and contact your business.", "digital-presence.html", "See Digital Presence", 105, 70),
    ("Business Operations", "How the work gets done behind the scenes, with connected systems.", "business-operations.html", "See Business Operations", 495, 70),
    ("Products", "Software and SaaS products shaped around real business problems.", "products.html", "See Products", 495, 390),
    ("Internal tools", "The automation systems OC builds and runs itself, and builds on.", "products.html#internal", "See the systems", 105, 390),
]


def eco_map():
    cx, cy = 300, 230
    lines, cross, nodes = [], [], []
    for _t, _p, _h, _l, x, y in MAP_NODES:
        lines.append(f'<path class="link-line" d="M{cx} {cy} Q{(cx + x) // 2 + (12 if x > cx else -12)} {(cy + y) // 2} {x} {y}"/>')
    order = [0, 1, 2, 3, 0]
    for a, b in zip(order, order[1:]):
        ax, ay = MAP_NODES[a][4], MAP_NODES[a][5]
        bx, by = MAP_NODES[b][4], MAP_NODES[b][5]
        cross.append(f'<path class="link-line cross" d="M{ax} {ay} L{bx} {by}"/>')
    for t, p, h, l, x, y in MAP_NODES:
        w = 212
        nodes.append(
            f'<a class="node" href="{h}" data-title="{esc(t)}" data-text="{esc(p)}" data-href="{h}" data-link="{esc(l)}" '
            f'aria-label="{esc(t)}: {esc(p)}"><rect x="{x - w // 2}" y="{y - 26}" width="{w}" height="52" rx="26"/>'
            f'<text x="{x}" y="{y + 7}">{esc(t)}</text></a>'
        )
    return f"""<div class="map" data-map>
  <svg viewBox="0 0 600 460" role="group" aria-label="Official Creations ecosystem: four connected layers around a shared centre">
    {''.join(cross)}{''.join(lines)}
    <g class="hub"><circle cx="{cx}" cy="{cy}" r="52"/><image href="assets/img/oc-mark-white.png" x="{cx - 23.15}" y="{cy - 28}" width="46.3" height="56" aria-hidden="true"/></g>
    {''.join(nodes)}
  </svg>
  <div class="map-panel" aria-live="polite">
    <h3>Four layers, one system</h3>
    <p>Each layer works alone and gets stronger connected to the others.</p>
    <a class="link" href="ecosystem.html">Open the ecosystem {ico("arrow")}</a>
  </div>
  <p class="map-hint">Hover, focus or tap a layer to explore it.</p>
</div>"""


# ---------- Home ----------
def work_rows():
    out = []
    for w in CFG["work"]:
        out.append(
            f'<div class="row"><h3>{esc(w["name"])}</h3><p>{esc(w["text"])}</p>'
            f'<span class="tag">{esc(w["status"])}</span></div>'
        )
    return "".join(out)


def founder_block():
    name = CFG["founder_name"].strip()
    if not name:
        return ""
    note = esc(CFG["founder_note"].strip())
    return f'<div class="founder"><p><strong>{esc(name)}</strong></p>' + (f"<p>{note}</p>" if note else "") + "</div>"


def faq(items):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in items
    ) + "</div>"


FAQ_HOME = [
    ("What does Official Creations do?",
     "<p>We help businesses move from traditional operations to modern, technology-driven ones. That means websites and a stronger online presence, plus the systems that run behind the scenes: automation, lead management and custom business tools.</p>"),
    ("Who is OC for?",
     "<p>Today, mainly offline businesses and small and medium-sized businesses getting serious about digital. The foundations we build are meant to grow with startups and larger organisations too.</p>"),
    ("What happens in a consultation?",
     "<p>We talk through how your business works today, what's getting in the way, how you currently show up online, and where the opportunities are. If we can help, we'll say what we'd do first and why.</p>"),
    ("Do I have to buy something afterwards?",
     "<p>The consultation is built around understanding your business. Any recommendation follows from that, and what you do with it is up to you.</p>"),
    ("Is OC just a website company?",
     "<p>Websites are where many businesses start, and we put real craft into them. But OC is building a connected ecosystem: digital presence, business operations, software products and internal tools that work together.</p>"),
    ("Are your products available?",
     "<p>Some systems are in use internally, and others are planned. The Products page labels each one by its real status.</p>"),
]


def home():
    body = f"""
<section class="hero"><div class="wrap hero-grid">
  <div>
    <h1><span class="ln"><span>From Offline</span></span><span class="ln"><span>to Online.</span></span><span class="ln"><span>Beyond.</span></span></h1>
    <div class="hero-copy">
      <p class="lede">Official Creations builds the digital and operational foundations that help businesses move online, run better and keep scaling.</p>
      <div class="cta-row">{btn("Book a Consultation")}{btn("Explore Our Ecosystem", "ecosystem.html", ghost=True)}</div>
    </div>
  </div>
  {eco_map()}
</div></section>

<section class="section dark">{edge("top")}
  <div class="wrap intro">
    <h2 class="h2">A website is where it starts. It isn't where it ends.</h2>
    <div class="body">
      <p>Most businesses collect tools one at a time: a site here, a spreadsheet there, a social account nobody has time for. Each piece works alone. Together, they don't.</p>
      <p>OC designs them as one system, so what you build today still fits what you need next year.</p>
    </div>
  </div>
</section>

<section class="section dark" style="padding-top:0">
  <div class="wrap">
    <h2 class="h2">One ecosystem, four layers.</h2>
    <ul class="thread">
      <li><h3>Digital Presence</h3><p>How people find and trust you.</p></li>
      <li><h3>Business Operations</h3><p>How the work gets done behind the scenes.</p></li>
      <li><h3>Products</h3><p>Software and SaaS built around real business problems.</p></li>
      <li><h3>Internal tools</h3><p>The automation systems OC runs itself.</p></li>
    </ul>
    <p class="handoff">A website captures an enquiry. A lead system keeps track of it. A workflow follows it up.</p>
    <p style="margin-top:2rem"><a class="link" href="ecosystem.html">How the layers connect {ico("arrow")}</a></p>
  </div>
  {edge("bottom")}
</section>

<section class="section" id="what-we-do">
  <div class="wrap">
    <h2 class="h2" style="max-width:16ch">Two pillars. One foundation.</h2>
    <div class="pillars">
      <a class="pillar p1" href="digital-presence.html">
        {ico("site", "big")}
        <h3>Digital Presence</h3>
        <p>Help your business be found, understood and trusted online.</p>
        <ul>
          <li class="lead">{ico("site")}Website design and development</li>
          <li>{ico("search")}Search engine optimisation</li>
          <li>{ico("identity")}Digital identity</li>
          <li>{ico("eye")}Online visibility</li>
          <li>{ico("social")}Social media management</li>
        </ul>
        <span class="link">Explore Digital Presence {ico("arrow")}</span>
      </a>
      <a class="pillar p2" href="business-operations.html">
        {ico("system", "big")}
        <h3>Business Operations</h3>
        <p>Run the business on connected systems instead of scattered tools.</p>
        <ul>
          <li>{ico("flow")}Workflow automation</li>
          <li>{ico("system")}Custom business management systems</li>
          <li>{ico("funnel")}Lead generation and management</li>
          <li>{ico("loop")}Operational process optimisation</li>
        </ul>
        <span class="link">Explore Business Operations {ico("arrow")}</span>
      </a>
    </div>
  </div>
</section>

<section class="section dark">{edge("top")}
  <div class="wrap">
    <h2 class="h2" style="max-width:18ch">We understand the business before we build anything.</h2>
    <div class="approach">
      <div class="step"><span class="dot">1</span><div><h3>Discover</h3><p>We start with how your business earns, where it's stuck and what your customers actually do.</p></div></div>
      <div class="step"><span class="dot">2</span><div><h3>Strategise</h3><p>We decide what to fix first, what can wait, and how the pieces will connect.</p></div></div>
      <div class="step"><span class="dot">3</span><div><h3>Build</h3><p>We build in working stages, so you see progress along the way.</p></div></div>
      <div class="step"><span class="dot">4</span><div><h3>Evolve</h3><p>As your business changes, the foundations change with it.</p></div></div>
    </div>
  </div>
  {edge("bottom")}
</section>

<section class="section">
  <div class="wrap">
    <h2 class="h2">Selected work</h2>
    <p class="lede" style="margin-top:1.2rem">The systems we've built and are building. Real work, labelled honestly.</p>
    <div class="rows">{work_rows()}</div>
    <p class="note">More will appear here as projects are ready to share.</p>
  </div>
</section>

<section class="section dark">{edge("top")}
  <div class="wrap">
    <h2 class="h2">Why OC</h2>
    <div class="why">
      <div>{ico("chat")}<h3>Business-first</h3><p>We ask before we recommend. Sometimes the right answer is a simpler site, not a bigger system.</p></div>
      <div>{ico("loop")}<h3>Scalability-first</h3><p>We choose foundations that can grow, so growth doesn't mean starting over.</p></div>
      <div>{ico("system")}<h3>Connected solutions</h3><p>Your site, leads and workflows share information instead of living in separate places.</p></div>
      <div>{ico("eye")}<h3>Long-term partnership</h3><p>The first project is the start of a working relationship, not the end of one.</p></div>
    </div>
  </div>
  {edge("bottom")}
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <h2 class="h2">About OC</h2>
      {founder_block()}
    </div>
    <div>
      <p class="lede">OC is a growing technology company working with businesses that are moving from traditional operations to digital ones.</p>
      <p>We're building toward a single partner that can solve one problem today and support the next ones as they appear.</p>
      <p><a class="link" href="about.html">More about OC {ico("arrow")}</a></p>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <h2 class="h2">Questions</h2>
    {faq(FAQ_HOME)}
  </div>
</section>

{final_cta()}
"""
    page("index.html", "home", "Official Creations | From Offline to Online. Beyond.",
         "Official Creations builds connected digital and operational foundations that help businesses move online, run better and keep scaling.", body)


# ---------- Ecosystem ----------
def ecosystem():
    body = f"""
<section class="page-hero"><div class="wrap">
  <h1>Not isolated services. An ecosystem.</h1>
  <p class="lede">Every layer of OC is designed to hand off to the next, so your business doesn't end up with tools that don't talk to each other.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">{eco_map()}</div></section>

<section class="section dark">{edge("top")}
  <div class="wrap">
    <h2 class="h2" style="max-width:16ch">How the layers work together</h2>
    <div class="cols two">
      <div><h3>Digital Presence</h3><p>Your website and online identity bring people in. It's where enquiries start.</p></div>
      <div><h3>Business Operations</h3><p>Lead systems, workflows and management tools catch what comes in and keep the work moving.</p></div>
      <div><h3>Products</h3><p>Software and SaaS products package what works, so it can be used again instead of rebuilt.</p></div>
      <div id="internal"><h3>Internal tools</h3><p>The automation systems OC builds for itself. They are the proving ground for what later becomes a product.</p></div>
    </div>
    <p class="handoff">A website captures an enquiry. A lead system keeps track of it. A workflow follows it up.</p>
  </div>
  {edge("bottom")}
</section>

<section class="section"><div class="wrap split">
  <h2 class="h2">Room to grow</h2>
  <div>
    <p class="lede">New products slot into an existing layer rather than forcing a restructure.</p>
    <p>That's the point of building an ecosystem: each addition connects to what's already there. Where things stand today is listed honestly on the Products page.</p>
    <p><a class="link" href="products.html">See Products {ico("arrow")}</a></p>
  </div>
</div></section>
{final_cta()}
"""
    page("ecosystem.html", "ecosystem", "Our Ecosystem | Official Creations",
         "How Official Creations' digital presence, business operations, products and internal tools connect into one scalable system.", body)


# ---------- Digital Presence ----------
def digital():
    body = f"""
<section class="page-hero"><div class="wrap">
  <h1>A digital presence that earns trust before the first call.</h1>
  <p class="lede">For businesses that are good at what they do and ready to be found, understood and chosen online.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <h2 class="h2">Where businesses get stuck</h2>
  <ul class="problems">
    <li><h3>Hard to find</h3><p>Customers search for what you do and land on someone else.</p></li>
    <li><h3>The site doesn't match the business</h3><p>The quality of the work isn't reflected in how you look online.</p></li>
    <li><h3>Visitors, but few enquiries</h3><p>People arrive and don't know what to do next.</p></li>
    <li><h3>No time for social</h3><p>Accounts go quiet because nobody owns them.</p></li>
  </ul>
</div></section>

<section class="section dark">{edge("top")}
  <div class="wrap">
    <h2 class="h2">What we do</h2>
    <div class="caps">
      <div class="cap main">{ico("site")}<div><h3>Website design and development</h3><p>Our main craft. Sites designed around how your business actually wins customers, built to be fast, clear and easy to grow.</p></div></div>
      <div class="cap">{ico("search")}<div><h3>Search engine optimisation</h3><p>So the right people find you when they look.</p></div></div>
      <div class="cap">{ico("identity")}<div><h3>Digital identity</h3><p>A look and voice that feel consistent everywhere you appear.</p></div></div>
      <div class="cap">{ico("eye")}<div><h3>Online visibility</h3><p>Making sure your business shows up where it should.</p></div></div>
      <div class="cap">{ico("social")}<div><h3>Social media management</h3><p>Keeping your accounts active without it becoming another job.</p></div></div>
    </div>
  </div>
  {edge("bottom")}
</section>

<section class="section"><div class="wrap split">
  <div><h2 class="h2">How we approach it</h2></div>
  <div>
    <p class="lede">We look at how you present today before we design anything.</p>
    <p>We review your current presence, work out what customers need to see and do, then build in stages. The site is designed to connect with your lead and workflow systems from the start, even if you add them later.</p>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <h2 class="h2">What it can mean for you</h2>
  <ul class="value-list">
    <li>A business that looks as good as it is.</li>
    <li>Clearer paths from first visit to first conversation.</li>
    <li>A foundation you can add to, not replace.</li>
  </ul>
</div></section>
{final_cta("Let's look at how you show up.")}
"""
    page("digital-presence.html", "digital", "Digital Presence | Official Creations",
         "Website design and development, SEO, digital identity and online visibility for businesses ready to be found and trusted online.", body)


# ---------- Business Operations ----------
def ops():
    body = f"""
<section class="page-hero"><div class="wrap">
  <h1>The systems behind the work.</h1>
  <p class="lede">For businesses that run on phone calls, spreadsheets and memory, and are ready to run on something that holds together.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <h2 class="h2">Where businesses get stuck</h2>
  <ul class="problems">
    <li><h3>Enquiries slip through</h3><p>They arrive by phone, chat and email, and some are never followed up.</p></li>
    <li><h3>The same tasks, by hand</h3><p>Hours go to work a system could do.</p></li>
    <li><h3>Information everywhere</h3><p>Customers, orders and notes live in different places.</p></li>
    <li><h3>No clear view</h3><p>It's hard to see what's happening in the business this week.</p></li>
  </ul>
</div></section>

<section class="section dark">{edge("top")}
  <div class="wrap">
    <h2 class="h2" style="max-width:18ch">Four capabilities that work as one.</h2>
    <div class="chain" aria-label="How the capabilities connect">
      <span>Lead systems</span>{ico("arrow")}<span>Workflow automation</span>{ico("arrow")}<span>Management systems</span>{ico("arrow")}<span>Process optimisation</span>
    </div>
    <div class="caps">
      <div class="cap">{ico("funnel")}<div><h3>Lead generation and management</h3><p>Capture enquiries in one place and keep track of every one.</p></div></div>
      <div class="cap">{ico("flow")}<div><h3>Workflow automation</h3><p>Hand repetitive steps to a system so people can do the work that needs them.</p></div></div>
      <div class="cap">{ico("system")}<div><h3>Custom business management systems</h3><p>Tools shaped around how your business runs, not the other way round.</p></div></div>
      <div class="cap">{ico("loop")}<div><h3>Operational process optimisation</h3><p>Reviewing how work flows and tightening it, again and again as you grow.</p></div></div>
    </div>
  </div>
  {edge("bottom")}
</section>

<section class="section"><div class="wrap split">
  <div><h2 class="h2">How we approach it</h2></div>
  <div>
    <p class="lede">We map how work moves before we automate any of it.</p>
    <p>Automating a broken process only makes it break faster. So we start with how things run today, decide what to simplify, then build systems that connect to your website and to each other.</p>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <h2 class="h2">What it can mean for you</h2>
  <ul class="value-list">
    <li>Fewer enquiries lost and less manual repetition.</li>
    <li>One clearer picture of the business.</li>
    <li>Operations that can take on more without more chaos.</li>
  </ul>
</div></section>
{final_cta("Let's look at how you run.")}
"""
    page("business-operations.html", "ops", "Business Operations | Official Creations",
         "Workflow automation, custom business systems, lead management and process optimisation as connected capabilities.", body)


# ---------- Products ----------
def products():
    cfg = CFG["products"]
    internal = "".join(
        f'<div class="prod"><h3>{esc(w["name"])}</h3><p>{esc(w["text"])}</p><span class="tag">{esc(w["status"])}</span></div>'
        for w in CFG["work"]
    )
    planned = "".join(
        f'<div class="prod planned"><h3>{esc(p["name"])}</h3><div><p>{esc(p["text"])}</p>'
        f'<p class="tie">{esc(p["tie"])}</p></div><span class="tag">{esc(p["status"])}</span></div>'
        for p in cfg
    )
    body = f"""
<section class="page-hero"><div class="wrap">
  <h1>Software built to be reused.</h1>
  <p class="lede">What starts as an internal system can become a product. Everything here is labelled with where it really stands.</p>
</div></section>

<section class="section" style="padding-top:0" id="internal"><div class="wrap">
  <h2 class="h2">Systems we've built</h2>
  <p class="lede" style="margin:1.2rem 0 2rem">Internal tools and automation systems. They connect to Business Operations.</p>
  {internal}
  <div style="border-top:1.5px solid var(--ink)"></div>
</div></section>

<section class="section dark">{edge("top")}
  <div class="wrap">
    <h2 class="h2">On the roadmap</h2>
    <p class="lede" style="margin:1.2rem 0 2rem">Planned products. Not released, and details may change.</p>
    <div class="cols three">
      {''.join(f'<div><h3>{esc(p["name"])}</h3><p>{esc(p["text"])}</p><p class="muted">{esc(p["tie"])}</p><span class="tag">{esc(p["status"])}</span></div>' for p in cfg)}
    </div>
  </div>
  {edge("bottom")}
</section>

<section class="section"><div class="wrap split">
  <h2 class="h2">Room for what comes next</h2>
  <div>
    <p class="lede">Each product plugs into an existing layer of the ecosystem.</p>
    <p>New SaaS products and software solutions will be added here as they're ready, with their status stated plainly.</p>
    <p><a class="link" href="ecosystem.html">See how it connects {ico("arrow")}</a></p>
  </div>
</div></section>
{final_cta("Need something like this for your business?")}
"""
    page("products.html", "products", "Products | Official Creations",
         "Software and SaaS products from Official Creations, labelled by their actual status.", body)


# ---------- About ----------
def about():
    body = f"""
<section class="page-hero"><div class="wrap">
  <h1>A technology partner that grows with you.</h1>
  <p class="lede">Official Creations helps businesses move from traditional operations to modern, technology-driven ones.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap split">
  <div><h2 class="h2">What we're building toward</h2>{founder_block()}</div>
  <div>
    <p class="lede">One partner that can solve a specific problem now and support the next ones as they appear.</p>
    <p>We start small and specific, like a website or a lead system, then grow alongside the business. That's why we build connected foundations instead of one-off projects.</p>
    <p>Scalability is the idea behind everything we do: digital transformation, market reach, operational efficiency and growth.</p>
  </div>
</div></section>

<section class="section dark">{edge("top")}
  <div class="wrap">
    <h2 class="h2">How we work</h2>
    <div class="why">
      <div>{ico("chat")}<h3>Business-first</h3><p>We understand the business before recommending a solution.</p></div>
      <div>{ico("loop")}<h3>Scalability-first</h3><p>We build foundations for long-term growth.</p></div>
      <div>{ico("system")}<h3>Connected solutions</h3><p>We create systems and services that work together.</p></div>
      <div>{ico("eye")}<h3>Long-term partnership</h3><p>We support businesses as their requirements evolve.</p></div>
    </div>
  </div>
  {edge("bottom")}
</section>
{final_cta()}
"""
    page("about.html", "about", "About | Official Creations",
         "Official Creations is a growing technology company helping businesses build scalable digital and operational foundations.", body)


# ---------- Book ----------
def book():
    email = CFG["contact_email"]
    url = CFG["booking_url"].strip()
    sched = (f'<p>{btn("Pick a time online", esc(url), ghost=True)}</p><p class="form-note">Or send the form and we\'ll reply by email.</p>' if url else "")
    body = f"""
<section class="page-hero"><div class="wrap">
  <h1>Let's understand your business first.</h1>
  <p class="lede">A consultation is a conversation about where you are and where you could go. Not a pitch.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap book">
  <div>
    <h2 class="h3" style="margin-bottom:1rem">What we'll cover</h2>
    <ul class="agenda">
      <li>{ico("chat")}<span>How your business works today</span></li>
      <li>{ico("search")}<span>The challenges you're facing right now</span></li>
      <li>{ico("site")}<span>A review of your digital presence</span></li>
      <li>{ico("eye")}<span>Opportunities for growth</span></li>
      <li>{ico("loop")}<span>Where scalability could improve</span></li>
      <li>{ico("system")}<span>Solutions that suit you, if any do</span></li>
    </ul>
  </div>
  <div>
    {sched}
    <form class="consult" id="consult-form" data-to="{esc(email)}">
      <div class="field-row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
      </div>
      <div class="field"><label for="f-business">Business name</label><input id="f-business" name="business" required autocomplete="organization"></div>
      <div class="field"><label for="f-site">Website or social page <span>(optional)</span></label><input id="f-site" name="site"></div>
      <div class="field"><label for="f-interest">What are you looking for?</label>
        <select id="f-interest" name="interest">
          <option>A website or better online presence</option>
          <option>Better systems and automation</option>
          <option>Both</option>
          <option>Not sure yet</option>
        </select></div>
      <div class="field"><label for="f-challenge">What's getting in the way?</label><textarea id="f-challenge" name="challenge" required></textarea></div>
      <button class="btn" type="submit"><span>Request a consultation</span>{ico("arrow")}</button>
      <p class="form-msg" role="status"></p>
      <p class="form-note">Sending opens your email app with this message ready to go.</p>
    </form>
  </div>
</div></section>
"""
    page("book.html", "book", "Book a Consultation | Official Creations",
         "Book a consultation with Official Creations to review your business, your digital presence and where you could scale.", body)


if __name__ == "__main__":
    for fn in (home, ecosystem, digital, ops, products, about, book):
        fn()
    print("Built 7 pages.")
