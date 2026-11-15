"""Homepage sections for the Official Creations site.

build.py calls build(h) with itself as `h`, so this file reuses the shared
helpers (page, ico, btn, shp, par, eco_map, consult_form ...) without importing
build.py back. Each section is its own function. Edit copy here.
"""

# ---------- Hero ----------
BLOB_BLUE = "M20 120C60 40 190 20 300 80C390 130 410 230 340 300C270 370 150 380 80 330C10 280 -20 190 20 120Z"
BLOB_YELLOW = "M30 190C20 100 120 30 230 40C330 50 400 130 380 230C360 330 260 390 160 370C80 350 40 280 30 190Z"
BLOB_ORANGE = "M10 200C10 100 100 20 210 20C320 20 400 100 400 210C400 330 300 400 190 400C90 400 10 320 10 200Z"


def _blob_blue():
    rings = "".join(f'<path d="{BLOB_BLUE}" transform="translate(200 200) scale({k}) translate(-200 -200)" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="1.2"/>'
                    for k in (.92, .84, .76, .68, .6, .52))
    return ('<svg class="blob" viewBox="0 0 400 400" aria-hidden="true"><defs><clipPath id="cb"><path d="%s"/></clipPath></defs>'
            '<g><path d="%s" fill="#2F55DB"/><g clip-path="url(#cb)">%s<circle cx="70" cy="270" r="95" fill="#80E5F2"/></g></g></svg>'
            % (BLOB_BLUE, BLOB_BLUE, rings))


def _blob_yellow():
    return ('<svg class="blob" viewBox="0 0 400 400" aria-hidden="true"><defs><clipPath id="cy"><path d="%s"/></clipPath>'
            '<pattern id="dy" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="8" cy="8" r="2.6" fill="#fff"/></pattern></defs>'
            '<g><path d="%s" fill="#FFD91A"/><g clip-path="url(#cy)"><circle cx="360" cy="40" r="110" fill="#FFF1B8"/>'
            '<circle cx="210" cy="215" r="105" fill="url(#dy)" opacity=".95"/></g></g></svg>' % (BLOB_YELLOW, BLOB_YELLOW))


def _blob_orange():
    return ('<svg class="blob" viewBox="0 0 400 400" aria-hidden="true"><defs><clipPath id="co"><path d="%s"/></clipPath>'
            '<pattern id="do" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="3" fill="#fff"/></pattern></defs>'
            '<g><path d="%s" fill="#FF7B4B"/><g clip-path="url(#co)"><rect x="30" y="30" width="170" height="130" fill="url(#do)"/></g></g></svg>'
            % (BLOB_ORANGE, BLOB_ORANGE))


DASH = ('<svg class="dash" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M-4 84C14 104 34 82 52 66S88 38 104 60" vector-effect="non-scaling-stroke"/></svg>')


def hero(h):
    shapes = (DASH
              + f'<div class="par b-blue" data-par="0.06">{_blob_blue()}</div>'
              + f'<div class="par b-yellow" data-par="0.1">{_blob_yellow()}</div>'
              + f'<div class="par b-orange" data-par="0.05">{_blob_orange()}</div>')
    def hot(href, label):
        return f'<a class="hot" href="{href}" aria-label="{label}"><span aria-hidden="true">+</span><em>{label}</em></a>'
    return f"""
<section class="h-hero">
  <div class="h-shapes" aria-hidden="true">{shapes}</div>
  <div class="wrap h-in">
    <h1><span class="ln"><span>From Offline</span></span><span class="ln"><span>to Online.</span></span><span class="ln"><span>Beyond.</span></span></h1>
    <p class="h-pill">The OC ecosystem</p>
    <p class="lede">Official Creations builds the digital and operational foundations that help businesses move online, run better and keep scaling.</p>
    <div class="cta-row">{h.btn("Book a Consultation")}{h.btn("Explore Our Ecosystem", "ecosystem.html", ghost=True)}</div>
    <div class="h-stage">
      <div class="dev d-left">{_mb(h)}{hot("digital-presence.html", "Digital Presence")}</div>
      <div class="h-card">{h.eco_map()}</div>
      <div class="dev d-right">{_flow(h)}{hot("business-operations.html", "Business Operations")}</div>
    </div>
  </div>
</section>"""


# ---------- Offline to online story (scroll-driven) ----------
def _ly(i, cls, a, b, r, c, z, inner=""):
    """One scene layer. a = shop box (x, y, w, h) and b = website box in a 400x320 space;
    r = corner radius shop/site; c = colour shop/site; z = lift depth when the layers separate."""
    st = (f"--i:{i};--x0:{a[0]};--y0:{a[1]};--w0:{a[2]};--h0:{a[3]};--x1:{b[0]};--y1:{b[1]};--w1:{b[2]};--h1:{b[3]};"
          f"--r0:{r[0]};--r1:{r[1]};--c0:var(--{c[0]});--c1:{c[1]};--z:{z};--zi:{i}")
    return f'<div class="ly {cls}" style="{st}">{inner}</div>'


def _on(cls, box, z, inner="", extra=""):
    st = f"--x:{box[0]};--y:{box[1]};--w:{box[2]};--h:{box[3]};--z:{z}{extra}"
    return f'<div class="on-only {cls}" style="{st}">{inner}</div>'


def _off(cls, box, z, inner=""):
    st = f"--x:{box[0]};--y:{box[1]};--w:{box[2]};--h:{box[3]};--z:{z}"
    return f'<div class="off-only sh {cls}" style="{st}">{inner}</div>'


def _story_stage(h):
    """Layered 3D stage: the shop's parts separate in depth, then become the website's parts."""
    layers = [
        _ly(0, "ly-wall", (60, 120, 280, 170), (40, 60, 320, 230), (3, 14), ("butter", "#fff"),
            0, '<i class="bricks off-only"></i><i class="plinth off-only"></i>'),
        _ly(1, "ly-window", (190, 160, 120, 80), (210, 116, 130, 110), (3, 12), ("sky", "var(--lav)"), 50,
            '<span class="disp off-only"><i class="shelf"></i><i class="pot"></i><i class="leafy"></i><i class="gift"></i>'
            '<i class="jar"></i></span><i class="glare off-only"></i><i class="cross off-only"></i>'),
        _ly(2, "ly-door", (100, 190, 60, 100), (70, 236, 100, 32), (3, 99), ("indigo", "var(--coral)"), 60,
            '<i class="glass off-only"></i><i class="plate off-only"></i><i class="knob off-only"></i>'),
        _ly(3, "ly-awning", (50, 70, 300, 50), (40, 60, 320, 36), (2, 12), ("coral", "var(--indigo)"), 40,
            '<i class="stripes off-only"></i><i class="scallops off-only"></i>'),
        _ly(4, "ly-sign", (130, 28, 140, 30), (100, 70, 200, 16), (4, 99), ("ink", "#fff"), 80,
            '<i class="bulbs off-only"></i><b class="open off-only">OPEN</b>'),
    ]
    shop = [
        _off("chain c1", (150, 58, 2, 12), 76),
        _off("chain c2", (248, 58, 2, 12), 76),
        _off("plant", (66, 232, 28, 58), 8,
             '<i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="pt"></i>'),
        _off("step", (92, 288, 76, 8), 4),
    ]
    online = [
        _on("dots", (52, 74, 40, 8), 95, '<i class="d1"></i><i class="d2"></i><i class="d3"></i>'),
        _on("t1", (60, 118, 120, 14), 55, "", ""),
        _on("t2", (60, 142, 100, 8), 55),
        _on("t3", (60, 158, 80, 8), 55),
        _on("cd cd1", (190, 240, 50, 36), 30),
        _on("cd cd2", (248, 240, 50, 36), 30),
        _on("cd cd3", (306, 240, 40, 36), 30),
    ]
    return ('<div class="stage3d" role="img" aria-label="A shopfront separating into layers and re-forming as a website">'
            '<div class="rig"><div class="ground"></div>' + "".join(layers) + "".join(shop) + "".join(online) + "</div></div>")


def story(h):
    return f"""
<section class="sec s-story"><div class="wrap">
  <div class="panel lav story" data-story>
    <div class="story-grid">
      <div class="story-text">
        <h2 class="h2" data-kinetic>A website is where it starts. It isn't where it ends.</h2>
        <p>Most businesses collect tools one at a time: a site here, a spreadsheet there, a social account nobody has time for. Each piece works alone. Together, they don't.</p>
        <p>OC designs them as one system, so what you build today still fits what you need next year.</p>
      </div>
      <div class="story-scene">
        {_story_stage(h)}
        <div class="story-labels" aria-hidden="true"><span class="off">Offline</span><span class="on">Online</span></div>
        <div class="story-switch" role="group" aria-label="Show offline or online">
          <button type="button" class="sw" data-state="off" aria-pressed="true">Offline</button>
          <button type="button" class="sw" data-state="on" aria-pressed="false">Online</button>
        </div>
      </div>
    </div>
  </div>
</div></section>"""


# ---------- Ecosystem: four layers as tilted cards ----------
CONSTELLATION_LINKS = {0: [1], 1: [0, 3, 2], 2: [3, 1], 3: [1, 2]}
_TOOTH = '<circle class="ln" cx="{x}" cy="{y}" r="{r}" stroke-width="6" stroke-dasharray="4.2 4.2"/>'
ILLS = [
    ("#E6DEF7", '''<path class="fi sk" d="M20 46V34a10 10 0 0 1 10-10h100a10 10 0 0 1 10 10v12z"/>
<path class="fw sk" d="M20 46h120v62a10 10 0 0 1-10 10H30a10 10 0 0 1-10-10z"/>
<circle class="fw" cx="33" cy="35" r="2.8"/><circle class="fw" cx="42" cy="35" r="2.8"/><circle class="fw" cx="51" cy="35" r="2.8"/>
<rect class="fk" x="30" y="56" width="50" height="9" rx="4.5"/><rect class="fg" x="30" y="71" width="62" height="6" rx="3"/><rect class="fg" x="30" y="82" width="54" height="6" rx="3"/>
<rect class="fc sk" x="30" y="95" width="32" height="12" rx="6"/><circle class="fs sk" cx="116" cy="74" r="19"/>
<path class="fk" stroke="#fff" stroke-width="2.5" stroke-linejoin="round" d="M112 88v27l8-7 6 13 6-3-6-12h11z"/>'''),
    ("#D4EFE0", '''<path class="ln" stroke-dasharray="1 6" d="M80 84v14"/>
<path class="ln" d="M49 56h14M107 56h-4"/><path class="ln" d="M60 52l5 4-5 4M100 52l5 4-5 4"/>
<circle class="fi sk" cx="34" cy="56" r="15"/><rect class="fw sk" x="63" y="40" width="34" height="32" rx="9"/>
<circle class="fl sk" cx="126" cy="56" r="15"/><path class="ln" style="stroke:#fff;stroke-width:3.5" d="M119 56l5 5 9-10"/>
<path class="ln" style="stroke:#fff;stroke-width:3" d="M70 52h20M70 60h12" />
''' + _TOOTH.format(x=80, y=106, r=13) + '''<circle class="fs sk" cx="80" cy="106" r="11"/><circle class="fw sk" cx="80" cy="106" r="4"/>'''),
    ("#F8D9D2", '''<path class="fs sk" d="M80 26l36 20-36 20-36-20z"/><path class="fc sk" d="M44 46l36 20v44L44 90z"/><path class="fi sk" d="M80 66l36-20v44l-36 20z"/>
<path class="fw sk" d="M62 84l8 4v10l-8-4zM94 90l16-9v10l-16 9z" opacity=".95"/>
<path class="fk" d="M132 24l2.6 6.4 6.4 2.6-6.4 2.6-2.6 6.4-2.6-6.4-6.4-2.6 6.4-2.6zM26 100l1.8 4.2 4.2 1.8-4.2 1.8-1.8 4.2-1.8-4.2-4.2-1.8 4.2-1.8z"/>'''),
    ("#FBEBB8", '''<rect class="fk sk" x="20" y="26" width="104" height="74" rx="10"/>
<circle class="fc" cx="33" cy="38" r="3"/><circle class="fs" cx="43" cy="38" r="3"/><circle class="fl" cx="53" cy="38" r="3"/>
<path class="ln" style="stroke:#2BD68A;stroke-width:4" d="M34 60l11 8-11 8"/><path class="ln" style="stroke:#fff;stroke-width:4" d="M54 78h24"/><path class="ln" style="stroke:#8C84B8;stroke-width:4" d="M54 62h34"/>
''' + _TOOTH.format(x=122, y=96, r=17) + '''<circle class="fs sk" cx="122" cy="96" r="14"/><circle class="fw sk" cx="122" cy="96" r="5"/>'''),
]


def constellation(h):
    nodes = []
    for i, (bg, art) in enumerate(ILLS):
        title, text, href, link, *_ = h.MAP_NODES[i]
        links = ",".join(str(x) for x in CONSTELLATION_LINKS[i])
        nodes.append(
            f'<button type="button" class="cnode" data-i="{i}" data-links="{links}" '
            f'data-title="{h.esc(title)}" data-text="{h.esc(text)}" data-href="{href}" data-link="{h.esc(link)}">'
            f'<svg class="ill" viewBox="0 0 160 134" aria-hidden="true"><rect width="160" height="134" fill="{bg}"/>{art}</svg>'
            f'<span class="clabel">{h.esc(title)}</span></button>'
        )
    return f"""
<section class="sec s-eco slide-over"><div class="wrap">
  <div class="panel paper slide" data-const>
    <div class="cstage">
      <div class="ccenter">
        <span class="eco-pill">Four layers &middot; one system</span>
        <h2 class="h2" data-kinetic>One ecosystem, four layers.</h2>
        <p class="handoff">A website captures an enquiry. A lead system keeps track of it. A workflow follows it up.</p>
        <div class="cdetail" aria-live="polite">
          <h3>Four layers, one system</h3>
          <p>Select a card to see what it holds and what it connects to.</p>
          <a class="link" href="ecosystem.html">How the layers connect {h.ico("arrow")}</a>
        </div>
      </div>
      {''.join(nodes)}
    </div>
  </div>
</div></section>"""


# ---------- What we do: two scene panels ----------
def _mb(h):
    return f"""<div class="mb">
    <div class="mb-bar"><i class="d1"></i><i class="d2"></i><i class="d3"></i><b>yourbusiness.com</b></div>
    <div class="mb-body">
      <div class="mb-nav"><span class="logo-b"></span><span></span><span></span><span></span></div>
      <div class="mb-hero">
        <div class="mb-text"><p class="t1"></p><p class="t2"></p><p class="t3"></p><span class="mb-btn"></span></div>
        <div class="mb-art">{h.shp("circ", "indigo")}</div>
      </div>
      <div class="mb-cards"><i></i><i></i><i></i></div>
    </div>
  </div>"""


def _scene_dp(h):
    return f"""<div class="scene sc-dp" aria-hidden="true">{_mb(h)}
  <div class="chip k1">{h.ico("site")}<span>Website design</span></div>
  <div class="chip k2">{h.ico("search")}<span>Search</span></div>
</div>"""


def _flow(h):
    return f"""<div class="flow">
    <div class="fnode"><span class="fdot coral"></span><b>Enquiry</b><span class="fbar"></span></div>
    <span class="fline"></span>
    <div class="fnode wide"><b>Lead list</b><div class="frows"><span></span><span></span><span></span></div></div>
    <span class="fline"></span>
    <div class="fnode"><span class="fdot leaf"></span><b>Follow-up</b><span class="fbar"></span></div>
  </div>"""


def _scene_bo(h):
    return f"""<div class="scene sc-bo" aria-hidden="true">{_flow(h)}
  <div class="chip k1">{h.ico("flow")}<span>Workflow</span></div>
  <div class="chip k2">{h.ico("funnel")}<span>Lead system</span></div>
</div>"""


def pillars(h):
    def caps(items):
        out = []
        for i, (icon, label) in enumerate(items):
            out.append(f'<li class="{"main" if i == 0 else ""}">{h.ico(icon)}<span>{label}</span></li>')
        return "".join(out)

    dp = caps([("site", "Website design and development"), ("search", "Search engine optimisation"),
               ("identity", "Digital identity"), ("eye", "Online visibility"), ("social", "Social media management")])
    bo = caps([("flow", "Workflow automation"), ("system", "Custom business management systems"),
               ("funnel", "Lead generation and management"), ("loop", "Operational process optimisation")])
    return f"""
<section class="sec" id="what-we-do"><div class="wrap">
  <h2 class="h2" data-kinetic style="max-width:16ch">Two pillars. One foundation.</h2>
  <div class="pillars2">
    <article class="spanel lav tilt-l">
      <div class="sp-text"><h3>Digital Presence</h3><p>Help your business be found, understood and trusted online.</p></div>
      {_scene_dp(h)}
      <ul class="caps2">{dp}</ul>
      <a class="link stretch" href="digital-presence.html">Explore Digital Presence {h.ico("arrow")}</a>
    </article>
    <article class="spanel mint tilt-r">
      <div class="sp-text"><h3>Business Operations</h3><p>Run the business on connected systems instead of scattered tools.</p></div>
      {_scene_bo(h)}
      <ul class="caps2">{bo}</ul>
      <a class="link stretch" href="business-operations.html">Explore Business Operations {h.ico("arrow")}</a>
    </article>
  </div>
</div></section>"""


# ---------- Approach: a path that draws itself ----------
STOPS = [(50, 12.5, "circ", "coral"), (24, 37.5, "diamond", "sun"), (76, 62.5, "semi", "leaf"), (30, 87.5, "tri", "indigo")]
STEPS = [
    ("Discover", "We start with how your business earns, where it's stuck and what your customers actually do."),
    ("Strategise", "We decide what to fix first, what can wait, and how the pieces will connect."),
    ("Build", "We build in working stages, so you see progress along the way."),
    ("Evolve", "As your business changes, the foundations change with it."),
]


def approach(h):
    stops = "".join(
        f'<span class="pstop" style="--x:{x}%;--y:{y}%">{h.shp(k, c)}</span>' for x, y, k, c in STOPS
    )
    steps = "".join(
        f'<div class="pstep"><div class="pstep-in"><h3>{t}</h3><p>{d}</p></div></div>' for t, d in STEPS
    )
    return f"""
<section class="sec"><div class="wrap">
  <div class="panel butter">
    <h2 class="h2" data-kinetic style="max-width:18ch">We understand the business before we build anything.</h2>
    <div class="ppath" data-draw>
      <div class="pcol" aria-hidden="true">
        <svg viewBox="0 0 100 100" preserveAspectRatio="none">
          <defs><clipPath id="ppclip" clipPathUnits="userSpaceOnUse"><rect class="pclip" x="-5" y="-1" width="110" height="102"/></clipPath></defs>
          <path class="pp-base" d="M50 0C50 6 50 8 50 12.5C50 24 24 26 24 37.5C24 50 76 50 76 62.5C76 75 30 75 30 87.5C30 95 50 96 50 100" vector-effect="non-scaling-stroke"/>
          <path class="pp" clip-path="url(#ppclip)" d="M50 0C50 6 50 8 50 12.5C50 24 24 26 24 37.5C24 50 76 50 76 62.5C76 75 30 75 30 87.5C30 95 50 96 50 100" vector-effect="non-scaling-stroke"/>
        </svg>
        {stops}
      </div>
      {steps}
    </div>
  </div>
</div></section>"""


# ---------- Selected work: pastel tiles with illustrative previews ----------
def _prev_leads():
    rows = "".join('<div class="lr"><i></i><span></span><span class="s"></span><b></b></div>' for _ in range(4))
    return f'<div class="pv pv-leads" aria-hidden="true"><div class="pv-head"><span></span><b></b></div>{rows}</div>'


def _prev_social():
    cells = []
    marks = {2: "coral", 5: "indigo", 9: "leaf", 12: "sun", 16: "coral", 19: "indigo"}
    for i in range(21):
        c = marks.get(i)
        cells.append(f'<span class="cell{" has" if c else ""}">{f"<i class=c-{c}></i>" if c else ""}</span>')
    return f'<div class="pv pv-social" aria-hidden="true"><div class="pv-head"><span></span><b></b></div><div class="cal">{"".join(cells)}</div></div>'


def _prev_site():
    return ('<div class="pv pv-site" aria-hidden="true">'
            '<div class="pg a"><div class="bar"></div><div class="blk"></div><div class="ln"></div><div class="ln s"></div></div>'
            '<div class="pg b"><div class="bar"></div><div class="blk"></div><div class="ln"></div><div class="ln s"></div></div>'
            '<span class="tag-s">Simple</span><span class="tag-p">Premium</span></div>')


def work(h):
    previews = [_prev_leads(), _prev_social(), _prev_site()]
    tones = ["lav", "mint", "blush"]
    tiles = []
    for i, w in enumerate(h.CFG["work"]):
        tiles.append(
            f'<article class="wtile {tones[i % 3]} w{i + 1}">{previews[i % 3]}'
            f'<div class="wt-text"><span class="tag">{h.esc(w["status"])}</span><h3>{h.esc(w["name"])}</h3><p>{h.esc(w["text"])}</p></div></article>'
        )
    return f"""
<section class="sec"><div class="wrap">
  <h2 class="h2" data-kinetic>Selected work</h2>
  <p class="lede" style="margin-top:1.2rem">The systems we've built and are building. Real work, labelled honestly.</p>
  <div class="work2">{''.join(tiles)}</div>
  <p class="note">The previews are illustrations, not screenshots. More will appear here as projects are ready to share. <a class="link" href="products.html">See Products {h.ico("arrow")}</a></p>
</div></section>"""


# ---------- Why OC ----------
def why(h):
    items = [
        ("chat", "Business-first", "We ask before we recommend. Sometimes the right answer is a simpler site, not a bigger system."),
        ("loop", "Scalability-first", "We choose foundations that can grow, so growth doesn't mean starting over."),
        ("system", "Connected solutions", "Your site, leads and workflows share information instead of living in separate places."),
        ("eye", "Long-term partnership", "The first project is the start of a working relationship, not the end of one."),
    ]
    cells = "".join(f'<div class="why-i"><span class="why-ico">{h.ico(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)
    deco = h.par("quarter", "coral", "left:-1.4rem;bottom:-1.4rem", "clamp(3.4rem,7vw,6.5rem)", 0)
    return f"""
<section class="sec"><div class="wrap">
  <div class="panel blush">
    <div aria-hidden="true">{deco}</div>
    <h2 class="h2" data-kinetic>Why OC</h2>
    <div class="why2">{cells}</div>
  </div>
</div></section>"""


# ---------- About ----------
def about(h):
    return f"""
<section class="sec"><div class="wrap split">
  <div>
    <h2 class="h2" data-kinetic>About OC</h2>
    {h.founder_block()}
  </div>
  <div>
    <p class="lede">OC is a growing technology company working with businesses that are moving from traditional operations to digital ones.</p>
    <p>We're building toward a single partner that can solve one problem today and support the next ones as they appear.</p>
    <p><a class="link" href="about.html">More about OC {h.ico("arrow")}</a></p>
  </div>
</div></section>"""


# ---------- FAQ ----------
def faq_section(h):
    art = (h.par("arch", "indigo", "left:4%;top:8%", "34%", 0)
           + h.par("circ", "coral", "left:38%;top:42%", "24%", 0)
           + h.par("quarter", "sun", "left:6%;top:56%", "22%", 0)
           + h.par("semi", "leaf", "left:46%;top:8%", "30%", 0))
    return f"""
<section class="sec"><div class="wrap faq-grid">
  <div class="faq-head">
    <h2 class="h2" data-kinetic>Questions</h2>
    <div class="faq-art" aria-hidden="true">{art}</div>
  </div>
  {h.faq(h.FAQ_HOME)}
</div></section>"""


# ---------- Closing: scrolling headline + mini form ----------
# PLACEHOLDER: the scrolling headline text is temporary. Replace MARQUEE_TEXT with the final words.
MARQUEE_TEXT = "Tell us about your business."


def closing(h):
    unit = f'<span>{MARQUEE_TEXT}</span><i class="mq-dot" aria-hidden="true"></i>'
    half = unit * 3
    quick = h.pick_link() + h.chat_link()
    email = h.CFG["contact_email"]
    email_line = "" if "REPLACE_ME" in email else f'<p class="form-note">Prefer email? <a class="link" href="mailto:{h.esc(email)}">Email us</a></p>'
    return f"""
<section class="sec"><div class="wrap">
  <div class="panel mint close">
    <h2 class="sr">{MARQUEE_TEXT}</h2>
    <div class="marquee" aria-hidden="true"><div class="mq-track"><div class="mq-half">{half}</div><div class="mq-half">{half}</div></div></div>
    <div class="close-grid">
      <div>
        <p class="lede">A first conversation to understand where your business is and where it could go. Not a sales pitch.</p>
        <div class="cta-row">{quick}</div>
        {email_line}
      </div>
      {h.consult_form("c", mini=True)}
    </div>
  </div>
</div></section>"""


def build(h):
    body = "".join([hero(h), story(h), constellation(h), pillars(h), approach(h), work(h), why(h), about(h), faq_section(h), closing(h)])
    h.page("index.html", "home", "Official Creations | From Offline to Online. Beyond.",
           "Official Creations builds connected digital and operational foundations that help businesses move online, run better and keep scaling.",
           body, home=True)
