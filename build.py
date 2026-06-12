#!/usr/bin/env python3
"""Event-Den static site generator. Run once; output is plain HTML."""
import json, os

OUT = "/home/claude/event-den"
DOMAIN = "https://event-den.com"
ADDRESS = "14200 E Alameda Ave, Suite 400, Aurora, CO 80012"
GEO = "39.70929;-104.82171"
MAP_EMBED = ("https://maps.google.com/maps?q=14200%20E%20Alameda%20Ave%20Suite%20400%20Aurora%20CO%2080012"
             "&t=&z=12&ie=UTF8&iwloc=&output=embed")

# Free-licensed Unsplash placeholders (swap with real photos later)
def u(pid, w=1600): return f"https://images.unsplash.com/{pid}?w={w}&q=75&auto=format&fit=crop"
IMG = {
  "hero1": u("photo-1519225421980-715cb0215aed"),   # reception tables, string lights
  "hero2": u("photo-1511795409834-ef04bbd61622"),   # elegant table setting
  "hero3": u("photo-1492684223066-81342ee5ff30"),   # celebration sparklers
  "hero4": u("photo-1505236858219-8359eb29e329"),   # banquet rounds
  "celebrate": u("photo-1530103862676-de8c9debad1d", 900),
  "quince": u("photo-1513151233558-d860c5398176", 900),
  "large": u("photo-1519167758481-83f550bb49b3", 900),
  "gala": u("photo-1464366400600-7168b8af9bc3", 900),
  "cultural": u("photo-1533174072545-7a4b6ad7a6c3", 900),
  "tournament": u("photo-1504450758481-7338eba7524a", 900),
  "corporate": u("photo-1540575467063-178a50c2df87", 900),
  "training": u("photo-1552664730-d307ca884978", 900),
  "retreat": u("photo-1542744173-8e7e53415bb0", 900),
  "catering": u("photo-1555244162-803834f70033", 900),
  "plated": u("photo-1551218808-94e220e084d2", 900),
  "bar": u("photo-1470337458703-46ad1756a187", 900),
  "cocktail": u("photo-1514362545857-3bc16c4c7d1b", 900),
  "rentals": u("photo-1478146896981-b80fe463b330", 900),
  "wedding": u("photo-1519741497674-611481863552", 900),
  "venue": u("photo-1519861531473-9200262188bf", 900),
  "court": u("photo-1546519638-68e109498ffc", 900),
  "lights": u("photo-1478147427282-58a87a120781", 900),
  "crowd": u("photo-1511578314322-379afb476865", 900),
  "dance": u("photo-1529636798458-92182e662485", 900),
  "stage": u("photo-1475721027785-f74eccf877e2", 900),
  "dinner": u("photo-1414235077428-338989a2e8c0", 900),
  "confetti": u("photo-1492684223066-81342ee5ff30", 900),
  "city": u("photo-1546156929-a4c0ac411f47", 900),     # Denver skyline
}
OG_DEFAULT = u("photo-1519225421980-715cb0215aed", 1200)

NAV = [
  ("celebrations.html", "Celebrations"),
  ("large-events.html", "Large Events"),
  ("corporate.html", "Corporate"),
  ("venue.html", "The Space"),
  ("catering.html", "Catering"),
  ("rentals-brokerage.html", "Rentals"),
  ("gallery.html", "Gallery"),
  ("faq.html", "FAQ"),
  ("contact.html", "Contact"),
]

AREA_SERVED = ["Aurora","Denver","Centennial","Greenwood Village","Cherry Hills Village",
  "Cherry Creek","Lone Tree","Castle Pines","Castle Rock","Parker","Highlands Ranch",
  "Washington Park","Denver Tech Center","Littleton"]

BUSINESS_LD = {
  "@context": "https://schema.org",
  "@type": ["EventVenue", "LocalBusiness"],
  "name": "Event-Den",
  "alternateName": "Event Denver",
  "description": "Affordable, flexible event venue and event services for the Denver metro — the middle ground between a backyard party and the downtown convention center.",
  "url": DOMAIN,
  "email": "TODO-confirm@event-den.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "14200 E Alameda Ave, Suite 400",
    "addressLocality": "Aurora",
    "addressRegion": "CO",
    "postalCode": "80012",
    "addressCountry": "US"
  },
  "geo": {"@type": "GeoCoordinates", "latitude": 39.70929, "longitude": -104.82171},
  "hasMap": "https://maps.google.com/?q=14200+E+Alameda+Ave+Suite+400+Aurora+CO+80012",
  "areaServed": [{"@type": "City", "name": c} for c in AREA_SERVED],
  "sameAs": []
}

def head(title, desc, fname, og_image=OG_DEFAULT, extra_ld=None):
    canonical = f"{DOMAIN}/{'' if fname=='index.html' else fname}"
    ld_blocks = [BUSINESS_LD] + (extra_ld or [])
    ld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>'
        for b in ld_blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0d0b09">
<meta name="format-detection" content="telephone=no">
<meta property="og:locale" content="en_US">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:site_name" content="Event-Den">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<meta name="geo.region" content="US-CO">
<meta name="geo.placename" content="Aurora, Colorado">
<meta name="geo.position" content="{GEO}">
<meta name="ICBM" content="{GEO.replace(';', ', ')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">
<link rel="stylesheet" href="assets/css/styles.css">
{ld_html}
</head>
<body>"""

def header(active):
    items = ""
    for f, label in NAV:
        cur = ' aria-current="page"' if f == active else ""
        items += f'<li><a href="{f}"{cur}>{label}</a></li>'
    return f"""
<header class="site-header">
  <nav class="nav" aria-label="Primary">
    <a class="brand" href="index.html">Event<em>·</em>Den<small>Event Denver</small></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Toggle menu">☰</button>
    <ul class="nav-links" id="nav-links">
      {items}
      <li><a class="nav-cta" href="inquiry.html">Request a Quote</a></li>
    </ul>
  </nav>
</header>"""

FOOTER = f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>Event-Den · Event Denver</h4>
        <p>Greater value, fewer frills — the affordable middle ground for Denver events that don't fit, or can't afford, the convention center.</p>
        <p>{ADDRESS}<br>
        <span class="todo-flag">TODO: confirm phone</span> &nbsp;
        <span class="todo-flag">TODO: confirm email</span></p>
      </div>
      <div>
        <h4>Events</h4>
        <ul>
          <li><a href="celebrations.html">Celebration Events</a></li>
          <li><a href="large-events.html">Large Events &amp; Galas</a></li>
          <li><a href="corporate.html">Corporate Events</a></li>
          <li><a href="gallery.html">Gallery</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="catering.html">Catering &amp; Bar</a></li>
          <li><a href="rentals-brokerage.html">Rentals &amp; Brokerage</a></li>
          <li><a href="venue.html">The Space</a></li>
          <li><a href="gallery.html">Gallery</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit</h4>
        <ul>
          <li><a href="inquiry.html">Request a Quote</a></li>
          <li><a href="faq.html">FAQ</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="legal.html#privacy">Privacy</a> · <a href="legal.html#terms">Terms</a> · <a href="legal.html#accessibility">Accessibility</a></li>
        </ul>
      </div>
      <div id="areas" style="grid-column:1/-1;border-top:1px solid rgba(243,236,223,.08);padding-top:1.6rem;">
        <h4><a href="faq.html#metro" style="color:var(--gold-lt);">Serving the Denver Metro</a></h4>
        <p style="font-size:.86rem;letter-spacing:.04em;">Aurora · Denver · Cherry Creek · Denver Tech Center · Greenwood Village · Cherry Hills Village · Centennial · Lone Tree · Castle Pines · Castle Rock · Parker · Highlands Ranch · Washington Park · Littleton</p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> Event-Den. All rights reserved.</span>
      <span>Hosted at FieldhouseUSA Aurora · Partners: The Social Den · Oda Bar &amp; Cafe <span class="todo-flag">verify name</span> · Boomtown Athletics</span>
    </div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>"""

def img_band(triples):
    imgs = "".join(f'<img src="{src}" alt="{alt}" loading="lazy">' for src, alt in triples)
    return f'<section class="img-band reveal" aria-label="Venue photography">{imgs}</section>'

def cta_banner(h, sub, btn="Request a Quote"):
    return f"""
<section class="cta-banner reveal">
  <div class="wrap">
    <span class="eyebrow">Check availability</span>
    <h2>{h}</h2>
    <p style="max-width:60ch;margin:0 auto 2rem;">{sub}</p>
    <div class="btn-row" style="justify-content:center;">
      <a class="btn btn-gold" href="inquiry.html">{btn}</a>
      <a class="btn btn-ghost" href="venue.html">See the Space</a>
    </div>
  </div>
</section>"""

def write(fname, html):
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)
    print("wrote", fname)

PAGES = {}  # fname -> (title, desc, builder)

# ============================================================ HOME
def page_index():
    body = header("index.html") + f"""
<main>
<section class="hero">
  <div class="hero-slides" aria-hidden="true">
    <div class="hero-slide active" style="background-image:url('{IMG["hero1"]}')"></div>
    <div class="hero-slide" style="background-image:url('{IMG["hero2"]}')"></div>
    <div class="hero-slide" style="background-image:url('{IMG["hero3"]}')"></div>
    <div class="hero-slide" style="background-image:url('{IMG["hero4"]}')"></div>
  </div>
  <div class="hero-veil"></div>
  <canvas id="confetti-canvas" aria-hidden="true"></canvas>
  <div class="bottle-stage" id="champagne" aria-hidden="true">
    <img class="bottle-layer bottle-closed" src="https://images.unsplash.com/photo-1567696911980-2eed69a46042?w=900&q=70&auto=format&fit=crop" alt="" loading="eager" onerror="this.closest('.bottle-stage').classList.add('img-fail')">
    <img class="bottle-layer bottle-open" src="https://images.unsplash.com/photo-1592483648228-b35146a4330c?w=900&q=70&auto=format&fit=crop" alt="" loading="eager" onerror="this.closest('.bottle-stage').classList.add('img-fail')">
    <span class="champagne-hint">move your mouse · pop the bottle</span>
  </div>
  <div class="hero-inner">
    <div class="hero-frame">
      <span class="eyebrow">Event Denver · Aurora, Colorado</span>
      <h1>The events other venues can't hold.</h1>
      <p class="lede">Event-Den is Denver's affordable middle ground — far more room and polish than a small event center, at a fraction of convention-center cost. 70,000 square feet of flexible, finished space for celebrations, cultural gatherings, and corporate events of up to 1,200 guests — and for the occasions that don't fit anyone else's floor.</p>
      <div class="btn-row">
        <a class="btn btn-gold" href="inquiry.html">Request a Quote</a>
        <a class="btn btn-ghost" href="venue.html">See the Space</a>
      </div>
      <div class="hero-stats">
        <div><strong>70,000 sq ft</strong><span>Dedicated event space</span></div>
        <div><strong>35,000 sq ft</strong><span>Largest contiguous floor</span></div>
        <div><strong>1,200</strong><span>Guest capacity</span></div>
        <div><strong>Custom</strong><span>Every quote built to you</span></div>
      </div>
    </div>
  </div>
</section>

<div class="strip" aria-hidden="true">
  <div class="strip-track">
    <span>Celebrations</span><span>Galas</span><span>Cultural Events</span><span>Corporate</span><span>Tournaments</span><span>Weddings</span>
    <span>Celebrations</span><span>Galas</span><span>Cultural Events</span><span>Corporate</span><span>Tournaments</span><span>Weddings</span>
  </div>
</div>

<section class="section-light">
  <div class="wrap">
    <div class="center reveal">
      <span class="eyebrow">Three ways to gather</span>
      <h2>One venue, every occasion</h2>
      <hr class="gold-rule">
    </div>
    <div class="grid grid-3">
      <article class="card reveal">
        <img src="{IMG["celebrate"]}" alt="Birthday celebration with gold balloons and friends raising a toast" loading="lazy">
        <div class="card-body">
          <h3>Celebration Events</h3>
          <p>Milestones of every kind — from first birthdays to family reunions — in a private court or finished event area, on a simple 3-hour block that leaves room in the budget for the fun part.</p>
          <a class="card-link" href="celebrations.html">Plan a celebration</a>
        </div>
      </article>
      <article class="card reveal">
        <img src="{IMG["gala"]}" alt="Formal gala dinner with candlelit tables and elegant place settings" loading="lazy">
        <div class="card-body">
          <h3>Large Events &amp; Galas</h3>
          <p>When the guest list reaches the hundreds, the floor should too. Up to 1,200 guests across wide-open space, with the flexibility for events other venues simply can't hold.</p>
          <a class="card-link" href="large-events.html">Explore large events</a>
        </div>
      </article>
      <article class="card reveal">
        <img src="{IMG["corporate"]}" alt="Corporate conference audience facing a presentation stage" loading="lazy">
        <div class="card-body">
          <h3>Corporate Events</h3>
          <p>From working sessions to company-wide celebrations — weekday daytime is our sweet spot, and the pricing reflects it. Room to think big without big-hotel rates.</p>
          <a class="card-link" href="corporate.html">See corporate options</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section-wood">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Why Event-Den</span>
      <h2>The middle ground Denver was missing</h2>
      <hr class="gold-rule">
      <p>Between a crowded backyard and a downtown convention center, there hasn't been much choice. Small event centers fill up fast and price by the square foot they don't have. Convention space starts in five figures before you've poured a single drink.</p>
      <p><strong>We built Event-Den for the middle.</strong> Hosted inside an upscale, modern athletic facility with a beautifully finished dedicated events area, we offer real scale — 70,000 square feet of event space within a 93,000 sq ft building — 35,000 of it one contiguous floor — with the warmth of a hospitality team, an in-house bar program, and pricing that's honest about what you're getting: greater value, fewer frills.</p>
      <ul class="flourish-list">
        <li><strong>Unique events welcome</strong> — we routinely host the cultural festivals, tournaments, and large-format gatherings other venues turn away</li>
        <li>In-house liquor license and turnkey bar programs</li>
        <li>On-site catering by Oda Bar &amp; Cafe, or bring your own caterer for a fee</li>
        <li>Internal events coordinator available for any program (additional fee)</li>
        <li><a href="rentals-brokerage.html#resources">Event resources</a> — in-house services plus a brokered vendor network, one inquiry away</li>
      </ul>
      <a class="btn btn-ghost" href="inquiry.html">Request a custom quote</a>
    </div>
    <div class="split-img reveal">
      <img src="{IMG["lights"]}" alt="String lights glowing above a warmly lit evening event" loading="lazy">
    </div>
  </div>
</section>

<section class="section-purple">
  <div class="wrap split rev">
    <div class="split-img reveal">
      <img src="{IMG["court"]}" alt="Polished indoor court space ready for transformation into an event floor" loading="lazy">
    </div>
    <div class="reveal">
      <span class="eyebrow">The space</span>
      <h2>From court to ballroom in an afternoon</h2>
      <hr class="gold-rule">
      <p>Our home is FieldhouseUSA Aurora — a large, immaculately maintained facility with a dedicated, fully finished events area, pro-grade courts, and wide-open floor. Draping, lighting, staging, and seating turn the space into whatever your night needs: a gala hall, a wedding reception, a festival floor, a tournament arena.</p>
      <p>It's not a hotel ballroom, and that's the point — you get two to four times the room for the money, with upscale amenities and a team that treats your event like the main attraction.</p>
      <a class="btn btn-gold" href="venue.html">Tour the space</a>
    </div>
  </div>
</section>

<section class="section-light">
  <div class="wrap">
    <div class="center reveal">
      <span class="eyebrow">Recent setups</span>
      <h2>The room, dressed for the occasion</h2>
      <hr class="gold-rule">
    </div>
    <div class="gallery-grid reveal">
      <img src="{IMG["hero2"]}" alt="Elegant gold and white table setting for a formal dinner" loading="lazy">
      <img src="{IMG["dance"]}" alt="Guests dancing under warm lights at a wedding reception" loading="lazy">
      <img src="{IMG["cultural"]}" alt="Crowd celebrating at a vibrant cultural event with stage lighting" loading="lazy">
      <img src="{IMG["plated"]}" alt="Chef-plated entrée from on-site catering" loading="lazy">
      <img src="{IMG["stage"]}" alt="Speaker presenting on stage at a corporate gathering" loading="lazy">
      <img src="{IMG["quince"]}" alt="Confetti falling during a festive celebration" loading="lazy">
    </div>
    <div class="center" style="margin-top:2.4rem;"><a class="btn btn-ghost" href="gallery.html">Full gallery</a></div>
  </div>
</section>

<section class="section-wood">
  <div class="wrap">
    <div class="center reveal">
      <span class="eyebrow">Word of mouth</span>
      <h2>Hosts who found their middle ground</h2>
      <hr class="gold-rule">
    </div>
    <!-- TODO: PLACEHOLDER TESTIMONIALS — replace with real, permissioned client quotes before launch. Do not publish fictional reviews. -->
    <div class="grid grid-3">
      <article class="t-quote reveal" style="background-image:url('{IMG["gala"]}')">
        <div class="t-veil"></div>
        <div class="t-content"><span class="t-tag">Cultural · Lunar New Year Gala</span>
          <p>We needed seating for 600, a stage, and room for the lion dance — every hotel said no. Event-Den asked which entrance the dancers should use.</p>
          <span class="t-name">Mei C. — Gala Committee Chair <span class="todo-flag">placeholder</span></span></div>
      </article>
      <article class="t-quote reveal" style="background-image:url('{IMG["crowd"]}')">
        <div class="t-veil"></div>
        <div class="t-content"><span class="t-tag">Cultural · Community Festival</span>
          <p>Our Ethiopian celebration brought generations together — coffee ceremony, music, dancing past midnight. The team treated our traditions with real care.</p>
          <span class="t-name">Selam T. — Festival Organizer <span class="todo-flag">placeholder</span></span></div>
      </article>
      <article class="t-quote reveal" style="background-image:url('{IMG["dance"]}')">
        <div class="t-veil"></div>
        <div class="t-content"><span class="t-tag">Cultural · Quinceañera</span>
          <p>The waltz, the mariachis, 250 family members, and a dance floor that never emptied. My daughter felt the night was built just for her — because it was.</p>
          <span class="t-name">The Ramirez Family <span class="todo-flag">placeholder</span></span></div>
      </article>
      <article class="t-quote reveal" style="background-image:url('{IMG["stage"]}')">
        <div class="t-veil"></div>
        <div class="t-content"><span class="t-tag">Corporate · Annual All-Hands</span>
          <p>Keynote in the morning, team volleyball after lunch, awards dinner with a hosted bar that night — one venue, one invoice.</p>
          <span class="t-name">Jordan P. — Operations Director <span class="todo-flag">placeholder</span></span></div>
      </article>
      <article class="t-quote reveal" style="background-image:url('{IMG["celebrate"]}')">
        <div class="t-veil"></div>
        <div class="t-content"><span class="t-tag">Celebration · 40th Birthday</span>
          <p>I wanted a party my whole circle could actually fit into. A DJ, a taco bar, and space for the kids to run — nobody wanted to leave.</p>
          <span class="t-name">Tasha W. — Birthday Host <span class="todo-flag">placeholder</span></span></div>
      </article>
      <article class="t-quote reveal" style="background-image:url('{IMG["tournament"]}')">
        <div class="t-veil"></div>
        <div class="t-content"><span class="t-tag">Team · Volleyball Graduation Party</span>
          <p>Our seniors got one last match on a real court, then walked straight into their graduation banquet next door. Parents are still talking about it.</p>
          <span class="t-name">Coach Dana R. — Club Volleyball <span class="todo-flag">placeholder</span></span></div>
      </article>
    </div>
  </div>
</section>
""" + cta_banner("Tell us the occasion. We'll build the room around it.",
                 "Share your date, guest count, and vision — we'll respond with availability and a custom quote, usually within one business day.") + "</main>"
    return head("Event Venue Denver | Affordable Event Space | Event-Den",
        "Flexible Denver event venue. 70,000 sq ft for galas, quinceañeras, weddings, tournaments & corporate events. Up to 1,200 guests. Custom quotes.",
        "index.html") + body + FOOTER

PAGES["index.html"] = page_index

# ============================================================ CELEBRATIONS
def page_celebrations():
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":"How much does a celebration at Event-Den cost?",
       "acceptedAnswer":{"@type":"Answer","text":"Every event is custom quoted based on space, date, guest count, and services. Send an inquiry with your details and we'll respond with a tailored quote, typically within one business day."}},
      {"@type":"Question","name":"Can I bring my own food to a celebration?",
       "acceptedAnswer":{"@type":"Answer","text":"Yes. On-site catering by Oda Bar & Cafe is available, and outside catering is welcome for a fee."}},
      {"@type":"Question","name":"What kinds of celebrations does Event-Den host?",
       "acceptedAnswer":{"@type":"Answer","text":"Birthdays, graduations, reunions, quinceañeras, bar and bat mitzvahs, sports-team celebrations, and other private parties."}}]}
    body = header("celebrations.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["celebrate"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Celebration Events</nav>
    <span class="eyebrow">Celebration Events</span>
    <h1>Celebrate big without spending big</h1>
    <p class="lede" style="max-width:58ch;">Birthdays, graduations, reunions, quinceañeras, bar &amp; bat mitzvahs, team parties — a private court or finished event area, a simple 3-hour block, and pricing tailored to exactly what you need.</p>
    <a class="btn btn-gold" href="inquiry.html">Check availability</a>
  </div>
</section>

<section class="section-light">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">What it's for</span>
      <h2>Every milestone deserves real room</h2>
      <hr class="gold-rule">
      <p>Home parties run out of space. Restaurant back rooms run out of patience. Our celebration spaces give you a private court or a finished event area with room for games, dancing, a dessert table, and every cousin who shows up unannounced.</p>
      <p>If it's worth gathering for, it fits here — coming-of-age traditions, milestone years, family reunions, and team celebrations alike. Active parties take the court; dressier occasions take the finished event area; the biggest take both.</p>
      <p><a href="faq.html#events">See the full range of events we host →</a></p>
    </div>
    <div class="split-img reveal"><img src="{IMG["quince"]}" alt="Confetti and celebration at a festive party" loading="lazy"></div>
  </div>
</section>

<section class="section-wood">
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">Space options</span><h2>Pick your room</h2><hr class="gold-rule"></div>
    <div class="grid grid-3">
      <article class="card reveal"><img src="{IMG["court"]}" alt="Indoor court available for private party rental" loading="lazy"><div class="card-body"><h3>Private Court</h3><p>A full basketball/volleyball court for active parties — games first, cake after. A favorite for kids' birthdays and team celebrations.</p></div></article>
      <article class="card reveal"><img src="{IMG["hero2"]}" alt="Finished event area set with elegant tables" loading="lazy"><div class="card-body"><h3>Finished Event Area</h3><p>Our dedicated, nicely finished event room — tables, ambiance, and a polished setting for quinceañeras, mitzvahs, and dinners.</p></div></article>
      <article class="card reveal"><img src="{IMG["lights"]}" alt="Open event space under string lights" loading="lazy"><div class="card-body"><h3>Combination Setups</h3><p>Blend court time and event-area dining in one booking. <span class="todo-flag">TODO: confirm capacities per area</span></p></div></article>
    </div>
  </div>
</section>

<section>
  <div class="wrap split rev">
    <div class="split-img reveal"><img src="{IMG["catering"]}" alt="Buffet spread prepared by on-site catering" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">What's included</span>
      <h2>Add as much, or as little, as you like</h2>
      <hr class="gold-rule">
      <ul class="flourish-list">
        <li><strong>Catering</strong> — on-site menus by Oda Bar &amp; Cafe, or bring your own caterer for a fee</li>
        <li><strong>Bar</strong> — we hold our own liquor license; turnkey bar packages priced to your guest list</li>
        <li><strong>Rentals</strong> — tables, linens, décor, and event equipment</li>
        <li><strong>Coordination</strong> — our internal events coordinator can run your program for an additional fee</li>
      </ul>
      <h3 style="margin-top:2rem;color:var(--gold-lt);">How pricing works</h3>
      <p>Our signature 3-hour celebration block — 30 minutes setup, 2 hours of event, 30 minutes cleanup — is the simplest way to host. Every booking is <strong>custom quoted</strong> to your space, date, and add-ons, so you only pay for what your party actually needs.</p>
      <div class="btn-row"><a class="btn btn-gold" href="inquiry.html">Request a Quote</a></div>
    </div>
  </div>
</section>

<section class="section-light">
  <div class="wrap" style="max-width:840px;">
    <div class="center reveal"><span class="eyebrow">Good to know</span><h2>Celebration FAQs</h2><hr class="gold-rule"></div>
    <details class="reveal"><summary>What does the 3-hour block include?</summary><p>30 minutes to set up, 2 hours of party, 30 minutes to clean up — in your choice of space. Food, bar, rentals, and coordination are optional add-ons, all wrapped into one custom quote.</p></details>
    <details class="reveal"><summary>Can we bring our own food and decorations?</summary><p>Yes. Outside catering is welcome for a fee, and most décor is fine — we'll confirm specifics (open flames, confetti, wall fixings) when you book.</p></details>
    <details class="reveal"><summary>Do you host quinceañeras and mitzvahs?</summary><p>Proudly and often. Multicultural celebrations are at the heart of what we do — tell us your traditions and we'll shape the room around them.</p></details>
  </div>
</section>
""" + cta_banner("Pick a date. We'll hold the room.",
                 "Send your guest count and occasion — we'll confirm availability and a tailored price for your celebration.") + "</main>"
    return head("Birthday & Quinceañera Venue Aurora | Event-Den",
        "Affordable party venue in Aurora & Denver. Birthdays, quinceañeras, bar mitzvahs & reunions. Private court or finished event area — custom quotes.",
        "celebrations.html", IMG["celebrate"], [faq_ld]) + body + FOOTER

PAGES["celebrations.html"] = page_celebrations

# ============================================================ LARGE EVENTS
def page_large():
    body = header("large-events.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["large"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Large Events</nav>
    <span class="eyebrow">Large Events &amp; Galas</span>
    <h1>Up to 1,200 guests. One remarkable floor.</h1>
    <p class="lede" style="max-width:58ch;">Galas, cultural festivals, tournaments, rallies, weddings and receptions — 70,000 square feet of event space, 35,000 of it contiguous, for gatherings of up to 1,200 guests.</p>
    <a class="btn btn-gold" href="inquiry.html">Start a custom quote</a>
  </div>
</section>

<section class="section-light">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">What it's for</span>
      <h2>Events that outgrow ordinary venues</h2>
      <hr class="gold-rule">
      <p>Most Denver venues top out around 150 guests — and the ones that don't start at convention-center prices. Event-Den fills that gap with genuinely large, flexible floor space, an in-house team to dress it, and a habit of saying yes to the unique, large-format events other venues turn away.</p>
      <p>Galas and cultural celebrations are the heart of our calendar — alongside tournaments on convertible pro-grade courts under 40-foot ceilings, civic gatherings that need real capacity, and weddings whose guest lists refuse to shrink.</p>
      <p><a href="faq.html#events">Every event type we host, answered →</a></p>
    </div>
    <div class="split-img reveal"><img src="{IMG["cultural"]}" alt="Large crowd celebrating at a vibrant cultural festival" loading="lazy"></div>
  </div>
</section>

<section class="section-purple">
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">The scale</span><h2>What a true fieldhouse floor gets you</h2><hr class="gold-rule"></div>
    <div class="grid grid-4">
      <div class="price-card reveal"><span class="tier">Total space</span><div class="amount">70,000</div><div class="qualifier">square feet of event space</div></div>
      <div class="price-card feature reveal"><span class="tier">Contiguous floor</span><div class="amount">35,000</div><div class="qualifier">square feet, uninterrupted</div></div>
      <div class="price-card reveal"><span class="tier">Capacity</span><div class="amount">1,200</div><div class="qualifier">guests at full scale</div></div>
      <div class="price-card reveal"><span class="tier">Configurations</span><div class="amount">∞</div><div class="qualifier">staging, draping, dance floor, courts</div></div>
    </div>
    <p class="center" style="max-width:70ch;margin:2rem auto 0;font-size:.9rem;">Every large event is a custom build — venue, catering, bar, production, and coordination quoted together as one clear number. <span class="todo-flag">TODO: confirm capacities by configuration</span></p>
  </div>
</section>

""" + img_band([(IMG["cultural"],"Vibrant cultural festival with stage lighting"),(IMG["gala"],"Formal gala dinner service"),(IMG["confetti"],"Celebration confetti over a crowd")]) + f"""
<section class="section-wood">
  <div class="wrap split rev">
    <div class="split-img reveal"><img src="{IMG["wedding"]}" alt="Wedding reception with long banquet tables and floral décor" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">What's included</span>
      <h2>Built out, poured, and coordinated</h2>
      <hr class="gold-rule">
      <ul class="flourish-list">
        <li><strong>Catering</strong> — Oda Bar &amp; Cafe and select vendors; outside catering allowed for a fee</li>
        <li><strong>Bar programs</strong> — our own liquor license, turnkey service scaled to hundreds</li>
        <li><strong>Equipment rental</strong> — staging, tables, linens, wedding &amp; event equipment</li>
        <li><strong>Internal events coordinator</strong> — available for any program at an additional fee</li>
        <li><strong>Planner referrals</strong> — full wedding &amp; event planning is referred to trusted partners through our brokerage (connections we facilitate, not guarantee)</li>
      </ul>
      <div class="btn-row"><a class="btn btn-gold" href="inquiry.html">Request a custom build</a><a class="btn btn-ghost" href="catering.html">Catering &amp; bar</a></div>
    </div>
  </div>
</section>
""" + cta_banner("A gala-sized vision deserves a gala-sized floor.",
                 "Custom builds start with a conversation. Tell us the date, headcount, and the feeling you're after.") + "</main>"
    return head("Gala & Large Event Venue Denver | 1,200 Guests | Event-Den",
        "Large event space in the Denver metro. Galas, cultural events, tournaments, weddings & rallies. 70,000 sq ft, up to 1,200 guests. Custom quotes.",
        "large-events.html", IMG["large"]) + body + FOOTER

PAGES["large-events.html"] = page_large

# ============================================================ CORPORATE
def page_corporate():
    body = header("corporate.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["corporate"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Corporate Events</nav>
    <span class="eyebrow">Corporate Events</span>
    <h1>Room to think bigger than the conference room</h1>
    <p class="lede" style="max-width:58ch;">Trainings, retreats, team-building, holiday parties, and corporate galas — typically weekday daytime, always flexible, and priced well below hotel and convention space.</p>
    <a class="btn btn-gold" href="inquiry.html">Request a corporate quote</a>
  </div>
</section>

<section class="section-light">
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">Formats</span><h2>Programs we host weekly</h2><hr class="gold-rule"></div>
    <div class="grid grid-3">
      <article class="card reveal"><img src="{IMG["training"]}" alt="Team collaborating around a table during a training session" loading="lazy"><div class="card-body"><h3>Trainings &amp; Off-sites</h3><p>Classroom, theater, or workshop layouts with space to break out — minus the per-person hotel markup.</p></div></article>
      <article class="card reveal"><img src="{IMG["retreat"]}" alt="Colleagues presenting and planning at a company retreat" loading="lazy"><div class="card-body"><h3>Retreats &amp; Team-Building</h3><p>Full sports options — basketball, volleyball, open play — turn an agenda into an experience: strategy in the morning, team tournament in the afternoon.</p></div></article>
      <article class="card reveal"><img src="{IMG["dinner"]}" alt="Elegant dinner setting for a corporate gala" loading="lazy"><div class="card-body"><h3>Parties &amp; Corporate Galas</h3><p>Holiday parties, milestone dinners, and awards nights with in-house catering and a licensed bar.</p></div></article>
    </div>
  </div>
</section>

<section class="section-wood">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Why companies choose us</span>
      <h2>Weekday daytime is our sweet spot</h2>
      <hr class="gold-rule">
      <p>Most of our space is quiet on weekday daytimes — which means availability, flexibility, and pricing your finance team will actually approve. Evening and weekend corporate events are absolutely on the table too.</p>
      <ul class="flourish-list">
        <li>All-day formats with built-in activity options (courts, open space)</li>
        <li>On-site catering &amp; coffee service by Oda Bar &amp; Cafe</li>
        <li>Licensed bar for evening receptions</li>
        <li>Internal events coordinator available at an additional fee</li>
        <li>A/V, staging, and rentals arranged through our broker network</li>
      </ul>
      <p><strong>Pricing:</strong> corporate programs are custom builds — share your headcount, hours, and format and we'll return a clear, itemized quote.</p>
      <div class="btn-row"><a class="btn btn-gold" href="inquiry.html">Get a quote</a><a class="btn btn-ghost" href="venue.html">See the space</a></div>
    </div>
    <div class="split-img reveal"><img src="{IMG["stage"]}" alt="Presenter on stage addressing a corporate audience" loading="lazy"></div>
  </div>
</section>
""" + cta_banner("Your next off-site, minus the hotel invoice.",
                 "Tell us the format and headcount — we'll send availability and an itemized corporate quote.") + "</main>"
    return head("Corporate Event Space Denver | Retreats | Event-Den",
        "Corporate event venue near Denver & DTC. Trainings, retreats, team-building & company galas. Weekday-friendly, flexible space at honest prices.",
        "corporate.html", IMG["corporate"]) + body + FOOTER

PAGES["corporate.html"] = page_corporate

# ============================================================ CATERING & BAR
def page_catering():
    body = header("catering.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["catering"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Catering &amp; Bar</nav>
    <span class="eyebrow">Catering &amp; Bar</span>
    <h1>Fed well, poured properly</h1>
    <p class="lede" style="max-width:58ch;">On-site catering by Oda Bar &amp; Cafe <span class="todo-flag">TODO: verify name — "Oda Bar &amp; Cafe" vs "Oda Up"</span>, a house liquor license, and turnkey bar programs sized to your guest list.</p>
  </div>
</section>

<section class="section-light">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">On-site kitchen</span>
      <h2>Oda Bar &amp; Cafe, in the house</h2>
      <hr class="gold-rule">
      <p>Our in-house culinary partner builds menus for the occasion — plated dinners for galas, buffets for reunions, stations for festivals, coffee and lunch service for corporate days. For specialized cuisines, we bring in trusted vendor partners.</p>
      <p><strong>Prefer your own caterer?</strong> Outside catering is welcome for a fee — a fair trade for kitchen access and cleanup support, and far cheaper than venues that forbid it outright.</p>
    </div>
    <div class="split-img reveal"><img src="{IMG["plated"]}" alt="Chef-plated entrée with refined presentation" loading="lazy"></div>
  </div>
</section>

<section class="section-purple">
  <div class="wrap split rev">
    <div class="split-img reveal"><img src="{IMG["bar"]}" alt="Bartender preparing craft cocktails at an event bar" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">Licensed bar</span>
      <h2>Our license. Your party.</h2>
      <hr class="gold-rule">
      <p>Event-Den holds its own liquor license — no outside permits to chase, no gray areas. We run turnkey bar programs at a clear price:</p>
      <ul class="flourish-list">
        <li>Hosted &amp; cash-bar formats, beer/wine or full spirits</li>
        <li>Signature-cocktail menus for galas and weddings</li>
        <li>Licensed, insured bartenders and responsible-service staffing</li>
        <li>Per-person or consumption-based pricing, quoted with your event</li>
      </ul>
      <div class="btn-row"><a class="btn btn-gold" href="inquiry.html">Quote food &amp; bar</a></div>
    </div>
  </div>
</section>
""" + img_band([(IMG["plated"],"Chef-plated entrée"),(IMG["dinner"],"Elegant dinner service"),(IMG["cocktail"],"Signature cocktail being poured")]) + cta_banner("Menus and bar packages are built per event.",
                 "Tell us guest count and style — plated, buffet, stations, hosted bar — and we'll price it clearly.") + "</main>"
    return head("Event Catering & Bar Service Denver | Event-Den",
        "On-site catering by Oda Bar & Cafe plus in-house licensed bar programs for Denver events. Outside catering welcome for a fee.",
        "catering.html", IMG["catering"]) + body + FOOTER

PAGES["catering.html"] = page_catering

# ============================================================ RENTALS & BROKERAGE
def page_rentals():
    body = header("rentals-brokerage.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["rentals"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Rentals &amp; Brokerage</nav>
    <span class="eyebrow">Rentals &amp; Brokerage</span>
    <h1>Everything your event needs — sourced, not stressed</h1>
    <p class="lede" style="max-width:58ch;">In-house wedding &amp; event rentals — on-site or pickup — plus an event-resource network of vendors we host or broker, from planners to partner venues.</p>
  </div>
</section>

<section class="section-light">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Equipment rental</span>
      <h2>Wedding &amp; event equipment, on hand</h2>
      <hr class="gold-rule">
      <ul class="flourish-list">
        <li>Tables, chairs, and linens in banquet and cocktail formats</li>
        <li>Staging, draping, and dance-floor sections</li>
        <li>Arches, backdrops, and ceremony pieces</li>
        <li>Basic A/V and lighting — more through partner vendors</li>
      </ul>
      <p>Renting where you host means one delivery, one invoice, and no truck-scheduling roulette.</p>
    </div>
    <div class="split-img reveal"><img src="{IMG["wedding"]}" alt="Decorated wedding ceremony arch and seating" loading="lazy"></div>
  </div>
</section>

<section class="section-wood">
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">Wedding rental catalog</span><h2>Rent it here — use it here, or take it with you</h2><hr class="gold-rule">
    <p style="max-width:66ch;margin:0 auto;">Our specialty wedding and event pieces are available for your event on-site — or for <strong>pickup rental</strong> at off-site venues. Reserve through the inquiry form.</p></div>
    <div class="grid grid-3">
      <article class="card reveal"><img src="{IMG["wedding"]}" alt="Decorated ceremony arch with florals" loading="lazy"><div class="card-body"><h3>Ceremony Arches</h3><p>Round, hexagon, and classic frames ready for florals and draping — the photo backdrop of the day.</p></div></article>
      <article class="card reveal"><img src="{IMG["bar"]}" alt="Rolling bar cart set for cocktail service" loading="lazy"><div class="card-body"><h3>Rolling Bars</h3><p>Mobile bar carts that bring cocktail hour anywhere on the floor — or to your backyard reception.</p></div></article>
      <article class="card reveal"><img src="{IMG["lights"]}" alt="String lights and uplighting at an evening event" loading="lazy"><div class="card-body"><h3>Lighting &amp; Drape</h3><p>String lights, uplights, pipe-and-drape, and backdrop kits that turn any room romantic.</p></div></article>
      <article class="card reveal"><img src="{IMG["hero2"]}" alt="Banquet tables with linens and place settings" loading="lazy"><div class="card-body"><h3>Tables, Chairs &amp; Linens</h3><p>Banquet rounds, cocktail talls, and linens in event-ready condition, by the piece or by the room.</p></div></article>
      <article class="card reveal"><img src="{IMG["dance"]}" alt="Guests on a dance floor at a reception" loading="lazy"><div class="card-body"><h3>Dance Floor Sections</h3><p>Modular flooring that scales from first-dance intimate to full-floor party.</p></div></article>
      <article class="card reveal"><img src="{IMG["stage"]}" alt="Stage and A/V setup for a program" loading="lazy"><div class="card-body"><h3>Staging &amp; Basic A/V</h3><p>Risers, podiums, and essential sound — larger production sourced through our network.</p></div></article>
    </div>
    <p class="center" style="margin-top:2rem;font-size:.9rem;"><span class="todo-flag">TODO: confirm rental inventory list, pickup terms &amp; deposit policy</span></p>
  </div>
</section>

<section class="section-light" id="resources">
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">Event resources</span><h2>Hosted by us, or brokered through us</h2><hr class="gold-rule">
    <p style="max-width:66ch;margin:0 auto;">One inquiry reaches our whole network — in-house services we deliver ourselves, and trusted vendors we connect you with directly.</p></div>
    <div class="grid grid-3">
      <article class="card res-card reveal"><div class="card-body"><span class="res-chip">In-House</span><h3>Catering &amp; Bar</h3><p>Oda Bar &amp; Cafe menus and turnkey licensed bar programs, delivered by our own team.</p><a class="card-link" href="catering.html">Catering &amp; bar</a></div></article>
      <article class="card res-card reveal"><div class="card-body"><span class="res-chip">In-House</span><h3>Events Coordinator</h3><p>Our internal coordinator runs timelines, vendors, and day-of logistics for any program — available at an additional fee.</p><a class="card-link" href="inquiry.html">Add coordination</a></div></article>
      <article class="card res-card reveal"><div class="card-body"><span class="res-chip">In-House</span><h3>Equipment Rental</h3><p>The wedding and event catalog above — on-site or pickup.</p><a class="card-link" href="inquiry.html">Reserve pieces</a></div></article>
      <article class="card res-card reveal"><div class="card-body"><span class="res-chip">Brokered</span><h3>Planners &amp; Designers</h3><p>Full wedding and event planning referred to trusted partner planners who know our floor.</p><a class="card-link" href="inquiry.html">Request an intro</a></div></article>
      <article class="card res-card reveal"><div class="card-body"><span class="res-chip">Brokered</span><h3>Entertainment, A/V &amp; Photo</h3><p>DJs, live music, production, photographers, and videographers from our vendor network.</p><a class="card-link" href="inquiry.html">Request an intro</a></div></article>
      <article class="card res-card reveal"><div class="card-body"><span class="res-chip">Brokered</span><h3>Florals, Décor &amp; Partner Venues</h3><p>Specialty décor, florists, rental companies — and other venues when ours isn't the fit.</p><a class="card-link" href="inquiry.html">Request an intro</a></div></article>
    </div>
    <p class="center" style="margin-top:2rem;font-size:.85rem;">Brokered vendors and venues are independent businesses — introductions we facilitate, not services we guarantee.</p>
  </div>
</section>

<section class="section-wood">
  <div class="wrap split rev">
    <div class="split-img reveal"><img src="{IMG["dinner"]}" alt="Coordinated dinner event with polished service" loading="lazy"></div>
    <div class="reveal">
      <span class="eyebrow">Concierge brokerage</span>
      <h2>Our network, your shortcut</h2>
      <hr class="gold-rule">
      <p>Need a wedding planner, a specialty rental company, an event organizer — or a different venue entirely? We broker introductions across our metro network, including partner venues, so the right fit finds you faster.</p>
      <p><strong>Coordination in-house:</strong> for any program hosted with us, our internal events coordinator is available at an additional fee to run timelines, vendors, and day-of logistics. Full wedding and event planning is referred out to trusted partner planners.</p>
      <p style="border:1px dashed var(--gold);padding:1rem 1.2rem;border-radius:6px;background:rgba(75,46,107,.18);"><strong>Honest disclaimer:</strong> third-party venues, planners, and vendors are connections we facilitate — we cannot guarantee their availability, pricing, or performance. Your contracts with them are direct.</p>
      <a class="btn btn-gold" href="inquiry.html">Ask the concierge</a>
    </div>
  </div>
</section>
""" + cta_banner("One ask, many doors.",
                 "Tell us what you're missing — equipment, a planner, even another venue — and we'll make the introductions.") + "</main>"
    return head("Event Rentals & Vendor Brokerage Denver | Event-Den",
        "Wedding & event equipment rental plus concierge brokerage in Denver. We connect you to planners, rentals & partner venues — introductions, not guarantees.",
        "rentals-brokerage.html", IMG["rentals"]) + body + FOOTER

PAGES["rentals-brokerage.html"] = page_rentals

# ============================================================ VENUE
def page_venue():
    body = header("venue.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["venue"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / The Space</nav>
    <span class="eyebrow">The Space</span>
    <h1>An imperfect venue, perfected for value</h1>
    <p class="lede" style="max-width:58ch;">We'll say it plainly: we're not a downtown hotel ballroom. We're 70,000 square feet of clean, upscale, endlessly configurable event space inside FieldhouseUSA Aurora — and that honesty is exactly why the value works.</p>
  </div>
</section>

<section class="section-light">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">The finished event area</span>
      <h2>Polished where it counts</h2>
      <hr class="gold-rule">
      <p>The heart of Event-Den is a dedicated, nicely finished events area — warm, presentable, and ready for dinners, receptions, and programs without heavy production. Beyond it, pro-grade courts and wide-open floor scale up to festival- and gala-sized footprints.</p>
      <p>FieldhouseUSA is a modern facility with genuinely upscale amenities — immaculate floors, high ceilings, ample restrooms, and free on-site parking — so the "fieldhouse" part reads as scale and quality, not compromise.</p>
      <ul class="flourish-list">
        <li>Dedicated finished event area for dinners &amp; receptions</li>
        <li>Basketball/volleyball courts for parties &amp; tournaments</li>
        <li>70,000 sq ft of dedicated event space in a 93,000 sq ft building — up to 1,200 guests</li>
        <li>35,000 sq ft contiguous floor, plus 25,000 and 10,000 sq ft flexible areas</li>
        <li>Convertible courts under 40-foot ceilings — volleyball, basketball, pickleball &amp; open play for team bonding</li>
        <li>Draping, lighting &amp; staging transform court to ballroom</li>
        <li>The Social Den — our in-house lounge, workspace &amp; meetings hall — adjoins for breakouts and VIP rooms</li>
      </ul>
      <p><span class="todo-flag">TODO: confirm max occupancy — full facility, half facility, each event area, court configs</span></p>
    </div>
    <div class="split-img reveal"><img src="{IMG["court"]}" alt="High-ceiling indoor court with polished flooring" loading="lazy"></div>
  </div>
</section>

<section class="section-light">
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">Configurations</span><h2>One building, many rooms</h2><hr class="gold-rule"></div>
    <table>
      <thead><tr><th scope="col">Space</th><th scope="col">Best for</th><th scope="col">Scale</th></tr></thead>
      <tbody>
        <tr><td>Main contiguous floor</td><td>Galas, festivals, tournaments, weddings</td><td>35,000 sq ft</td></tr>
        <tr><td>Secondary open area</td><td>Large receptions &amp; expos</td><td>25,000 sq ft</td></tr>
        <tr><td>Finished event area &amp; flex space</td><td>Dinners, mitzvahs, corporate sessions</td><td>10,000 sq ft</td></tr>
        <tr><td>Convertible courts</td><td>Parties, team bonding, tournaments</td><td>10 volleyball · 4 basketball · 12 pickleball <span class="todo-flag">confirm</span></td></tr>
        <tr><td>Full-scale capacity</td><td>Maximum-format events</td><td>Up to 1,200 guests</td></tr>
      </tbody>
    </table>
    <p style="font-size:.85rem;">93,000 sq ft building total; roughly 70,000 sq ft is dedicated event space (the remainder is administration, walls, and circulation).</p>
  </div>
</section>

""" + img_band([(IMG["lights"],"String lights over an evening event setup"),(IMG["hero1"],"Reception tables dressed for a gala"),(IMG["dance"],"Guests dancing at a reception")]) + f"""
<section>
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">Find us</span><h2>Central to the whole metro</h2><hr class="gold-rule">
    <p style="max-width:64ch;margin:0 auto 2rem;">{ADDRESS} — minutes from I-225, central to Aurora, Denver, the Tech Center, and the southeast suburbs.</p></div>
    <div class="map-frame reveal">
      <iframe src="{MAP_EMBED}" title="Map to Event-Den at FieldhouseUSA, 14200 E Alameda Ave, Aurora CO" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>
""" + cta_banner("Walk it before you book it.",
                 "Schedule a tour — see the event area, the courts, and exactly how your night fits the floor.", "Schedule a Tour") + "</main>"
    return head("The Space | 70,000 Sq Ft Event Venue Aurora | Event-Den",
        "Tour Event-Den at FieldhouseUSA Aurora: finished event area, courts & 70,000 sq ft for up to 1,200 guests. Free parking, easy I-225 access.",
        "venue.html", IMG["venue"]) + body + FOOTER

PAGES["venue.html"] = page_venue

# ============================================================ PRICING
def page_pricing():
    offer_ld = {"@context":"https://schema.org","@type":"Service",
      "name":"Event venue rental","provider":{"@type":"LocalBusiness","name":"Event-Den"},
      "areaServed":"Denver metro, Colorado",
      "offers":[
        {"@type":"Offer","name":"Small-event 3-hour block","price":"400","priceCurrency":"USD",
         "description":"30 min setup + 2 hr event + 30 min cleanup; space only, no food. Starting/illustrative price."},
        {"@type":"Offer","name":"Large-event evening (illustrative)","priceCurrency":"USD",
         "priceSpecification":{"@type":"PriceSpecification","minPrice":"6000","maxPrice":"8000","priceCurrency":"USD"},
         "description":"Full-scale evening for 300–400 guests across up to 20,000 sq ft. Custom quoted."}]}
    body = header("pricing.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["hero2"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Pricing</nav>
    <span class="eyebrow">Pricing</span>
    <h1>Honest numbers, before you even ask</h1>
    <p class="lede" style="max-width:58ch;">Every figure here is a starting point, not a locked quote — but unlike most venues, we'd rather you see the ballpark up front.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="grid grid-3 price-cards">
      <div class="price-card reveal">
        <span class="tier">Celebrations</span>
        <div class="amount">from $400</div>
        <div class="qualifier">3-hour block · space only, no food</div>
        <ul class="flourish-list" style="text-align:left;">
          <li>30 min setup + 2 hr event + 30 min cleanup</li>
          <li>Private court or finished event area</li>
          <li>Catering, bar &amp; rentals quoted as add-ons</li>
        </ul>
        <a class="btn btn-ghost" href="celebrations.html">Celebration details</a>
      </div>
      <div class="price-card feature reveal">
        <span class="tier">Large Events &amp; Galas</span>
        <div class="amount">$6,000–8,000</div>
        <div class="qualifier">illustrative per evening · 300–400 guests</div>
        <ul class="flourish-list" style="text-align:left;">
          <li>Up to 20,000 sq ft of open space</li>
          <li>Compare: similar-capacity metro venues often run far higher</li>
          <li>Catering, bar, production &amp; coordination custom quoted</li>
        </ul>
        <a class="btn btn-gold" href="inquiry.html">Start a custom build</a>
      </div>
      <div class="price-card reveal">
        <span class="tier">Corporate</span>
        <div class="amount">Custom</div>
        <div class="qualifier">itemized quotes · weekday-friendly</div>
        <ul class="flourish-list" style="text-align:left;">
          <li>Trainings, retreats, parties &amp; galas</li>
          <li>Daytime availability = better rates</li>
          <li>Coordinator available at additional fee</li>
        </ul>
        <a class="btn btn-ghost" href="corporate.html">Corporate details</a>
      </div>
    </div>
    <p class="center" style="max-width:72ch;margin:2.5rem auto 0;">Add-ons priced with your quote: Oda Bar &amp; Cafe catering, outside-catering fee, licensed bar packages, equipment rental, and our internal events coordinator (additional fee for all internal programs). <span class="todo-flag">TODO: confirm published "starting at" ranges per category, or keep inquiry-only</span></p>
  </div>
</section>

<section class="section-wood">
  <div class="wrap" style="max-width:840px;">
    <div class="center reveal"><span class="eyebrow">How quoting works</span><h2>Three steps to a real number</h2><hr class="gold-rule"></div>
    <ul class="flourish-list reveal">
      <li><strong>1 · Tell us the event</strong> — date, guest count, occasion, and any food/bar wishes via the inquiry form.</li>
      <li><strong>2 · We scope it</strong> — space, hours, services, and a clear itemized estimate, typically within one business day.</li>
      <li><strong>3 · You decide</strong> — adjust the build until the number fits. No pressure, no hidden lines.</li>
    </ul>
    <div class="center"><a class="btn btn-gold" href="inquiry.html">Request a Quote</a></div>
  </div>
</section>
</main>"""
    return head("Event Venue Pricing Denver | From $400 | Event-Den",
        "Transparent Denver event venue pricing: 3-hr celebration blocks from $400; large-event evenings $6,000–$8,000 for 300–400 guests. Custom quotes for all builds.",
        "pricing.html", IMG["hero2"], [offer_ld]) + body + FOOTER

# pricing page removed — all pricing is by custom quote via inquiry

# ============================================================ GALLERY
def page_gallery():
    shots = [
      (IMG["hero1"], "Reception tables glowing under string lights"),
      (IMG["hero2"], "Gold-accented formal table setting"),
      (IMG["gala"], "Candlelit gala dinner service"),
      (IMG["dance"], "Guests dancing at a wedding reception"),
      (IMG["cultural"], "Cultural celebration with vibrant stage lighting"),
      (IMG["quince"], "Confetti moment at a milestone celebration"),
      (IMG["court"], "Court space prepared for an active party"),
      (IMG["tournament"], "Indoor tournament play on a pro-grade court"),
      (IMG["corporate"], "Corporate audience at a keynote session"),
      (IMG["training"], "Workshop teams collaborating at a retreat"),
      (IMG["catering"], "Catering spread by the on-site kitchen"),
      (IMG["bar"], "Craft cocktails from the licensed house bar"),
      (IMG["wedding"], "Wedding banquet tables dressed in florals"),
      (IMG["lights"], "Warm string lights over an evening event"),
      (IMG["stage"], "Speaker on stage at a large gathering"),
    ]
    imgs = "\n".join(f'<img src="{s}" alt="{a}" loading="lazy">' for s, a in shots)
    body = header("gallery.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["dance"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Gallery</nav>
    <span class="eyebrow">Gallery</span>
    <h1>The room, a hundred ways</h1>
    <p class="lede" style="max-width:58ch;">Setups, celebrations, and transformations. <em>Images below are licensed placeholders — photography of our own events is being added.</em></p>
  </div>
</section>
<section class="section-light">
  <div class="wrap">
    <div class="gallery-grid reveal">
{imgs}
    </div>
  </div>
</section>
""" + cta_banner("Picture your event here.", "Send the vision — we'll show you how the floor becomes it.") + "</main>"
    return head("Event Gallery | Denver Venue Setups | Event-Den",
        "See Event-Den setups: galas, quinceañeras, weddings, tournaments & corporate events across our 20,000 sq ft Aurora event space.",
        "gallery.html", IMG["dance"]) + body + FOOTER

PAGES["gallery.html"] = page_gallery

# ============================================================ LOCATIONS
LOCS = [
 dict(slug="aurora", city="Aurora", drive="You're already here — we sit at E Alameda Ave & I-225, in the heart of Aurora",
  kw="affordable event space Aurora", h1="Aurora's hometown event venue",
  intro="Event-Den isn't near Aurora — it <strong>is</strong> Aurora. Our home at FieldhouseUSA on East Alameda Avenue puts 20,000 square feet of flexible event space minutes from every Aurora neighborhood, from Del Mar to Southlands.",
  body="Aurora is one of the most culturally rich cities in Colorado, and our calendar shows it: quinceañeras, Ethiopian and Korean community celebrations, church gatherings, youth-sports banquets, and tournaments fill our courts and event areas year-round. For Aurora families, we're the answer between a crowded backyard on Chambers Road and a downtown Denver venue with downtown Denver parking.",
  fits=["Quinceañeras & family milestone parties","Cultural & faith community events","Youth and adult sports tournaments","Neighborhood association & civic gatherings"]),
 dict(slug="denver", city="Denver", drive="≈15–20 minutes from downtown Denver via 6th Ave or Colfax; free on-site parking when you arrive",
  kw="event venue Denver", h1="Denver's convention-center alternative",
  intro="When a Denver event outgrows the brewery taproom but the convention center quote arrives with a comma too many, Event-Den is the metro's middle ground — genuinely large, genuinely affordable, fifteen minutes east of downtown.",
  body="Galas, cultural festivals, weddings, and corporate programs that need 200–400 guests have shockingly few Denver options under five figures. We host them across up to half our facility, with an in-house licensed bar and on-site catering — and your guests park free instead of circling LoDo.",
  fits=["Galas & fundraisers priced out of downtown","Weddings & receptions with big guest lists","Cultural festivals & community celebrations","Company parties escaping hotel pricing"]),
 dict(slug="centennial", city="Centennial", drive="≈20 minutes north via I-25 → I-225 or Parker Rd; an easy reverse-commute drive",
  kw="corporate retreat space Centennial", h1="Centennial's room to grow",
  intro="Centennial households plan generous events — graduation parties that invite the whole cul-de-sac, corporate teams along the Arapahoe corridor that need real off-site space. Event-Den gives Centennial that room, twenty minutes up I-225.",
  body="South-suburban venues tend to be small and booked solid. Our finished event area handles the dinners and milestone parties; our open floor handles the company all-hands and team-building days that the office park conference room never could.",
  fits=["Graduation & milestone parties","Corporate trainings & retreats for Arapahoe-corridor firms","Club & league banquets","Anniversary & reunion dinners"]),
 dict(slug="greenwood-village", city="Greenwood Village", drive="≈18 minutes via I-25 → I-225; straight shot from the DTC's north end",
  kw="affordable gala venue near Greenwood Village", h1="Greenwood Village galas, without the gala markup",
  intro="Greenwood Village knows what a polished event should look like — and what hotel ballrooms charge for it. Event-Den offers an alternative eighteen minutes away: gala-scale space, licensed bar, white-tablecloth catering, at a fraction of the rate.",
  body="Nonprofit boards and corporate hosts from the Village use us for fundraising galas, awards dinners, and holiday parties where the budget should go to the cause or the team — not the room. Our illustrative $6,000–$8,000 evenings for 300–400 guests routinely undercut comparable south-metro ballrooms.",
  fits=["Fundraising & awards galas","Corporate holiday parties","Board dinners that grew into banquets","Charity events maximizing net proceeds"]),
 dict(slug="cherry-hills-village", city="Cherry Hills Village", drive="≈20 minutes via Hampden Ave (US-285) east to I-225 north",
  kw="private event venue near Cherry Hills Village", h1="Cherry Hills celebrations, scaled up",
  intro="Cherry Hills Village hosts beautifully at home — until the guest list passes a hundred. For the milestone birthdays, receptions, and family galas that outgrow even a generous backyard, Event-Den is twenty unhurried minutes east.",
  body="We offer what private estates can't: 300–400-guest capacity, a licensed in-house bar, professional catering, free parking, and no cleanup crew to hire at midnight. The room dresses up or down — draping and lighting included in your build — so the evening feels intentional, not improvised.",
  fits=["Large family celebrations & receptions","Milestone anniversaries & birthday galas","Charity dinners hosted by Village families","Graduation parties beyond backyard scale"]),
 dict(slug="cherry-creek", city="Cherry Creek", drive="≈12 minutes east on E Alameda Ave — our address is on the same street as the shopping district",
  kw="event space near Cherry Creek Denver", h1="Cherry Creek style, Alameda Avenue value",
  intro="Here's a secret hiding in plain sight: Event-Den sits on East Alameda Avenue — the very road that runs through Cherry Creek. Twelve minutes east of the shopping district, the boutique-venue aesthetic gives way to 20,000 square feet of possibility.",
  body="Cherry Creek hosts know small-and-stylish; we add big-and-flexible. Engagement parties, fashion and brand events, receptions, and milestone dinners that need more floor than a Creek restaurant's private room land here — with valet-free parking and a bar program we run on our own license.",
  fits=["Engagement parties & receptions","Brand launches & pop-up events","Milestone dinners beyond private-room capacity","Galas with a designer's eye and a realist's budget"]),
 dict(slug="lone-tree", city="Lone Tree", drive="≈25 minutes north via I-25 → I-225, against traffic most evenings",
  kw="event venue near Lone Tree", h1="Lone Tree's large-format option",
  intro="Lone Tree has entertainment, dining, and the Lincoln corridor's corporate energy — but precious little large, affordable event space. Event-Den fills that gap twenty-five minutes up the highway.",
  body="South-metro companies headquartered near Sky Ridge and RidgeGate use our weekday-friendly floor for trainings and team days; Lone Tree families book courts and the finished event area for parties that Park Meadows restaurants can't seat. Either way, the quote stays sane.",
  fits=["Corporate trainings for Lincoln-corridor companies","Team celebrations & sports banquets","Family parties beyond restaurant capacity","Community organization events"]),
 dict(slug="castle-rock", city="Castle Pines & Castle Rock", drive="≈35 minutes north on I-25 → I-225 — a familiar drive, with free parking at the end",
  kw="large event venue near Castle Rock", h1="Worth the drive from the Castles",
  intro="Castle Pines and Castle Rock are growing faster than their event infrastructure. When a wedding, gala, or tournament outgrows Douglas County's venues, Event-Den's 20,000 square feet are thirty-five minutes up the interstate.",
  body="We regularly host Douglas County weddings and receptions of 300+, regional tournaments that need multiple courts, and company events for firms whose teams span the whole south metro. The drive buys you double the space at a fraction of resort-venue rates.",
  fits=["Weddings & receptions of 300+ guests","Regional sports tournaments","South-metro company gatherings","Large community & church events"]),
 dict(slug="parker", city="Parker", drive="≈25 minutes via Parker Rd (CO-83) north to I-225 — one road, door to door",
  kw="party venue near Parker CO", h1="Parker's one-road party venue",
  intro="From downtown Parker, one road — Parker Road — runs straight to our front door. Twenty-five minutes, no highway maze, and suddenly your event has more space than anything in town.",
  body="Parker's family-first community keeps our celebration calendar busy: birthday courts, graduation parties, team banquets for the town's packed youth-sports leagues, and receptions that Mainstreet venues can't hold. The 3-hour celebration block from ~$400 is a Parker-parent favorite.",
  fits=["Kids' & teens' birthday parties on a private court","Youth-sports team banquets","Graduation & reunion parties","Receptions beyond Mainstreet capacity"]),
 dict(slug="highlands-ranch", city="Highlands Ranch", drive="≈30 minutes via C-470 → I-25 → I-225, or Quebec/Havana surface route",
  kw="event space near Highlands Ranch", h1="Highlands Ranch, meet your bigger backyard",
  intro="Highlands Ranch perfected the community rec center — but rec centers cap your guest list, your hours, and your bar. Event-Den is the next size up: thirty minutes away, 20,000 square feet, and a liquor license of our own.",
  body="HR families and HOAs book us for the celebrations that exceed rec-center rules: quinceañeras with a real dance floor, adult milestone parties with a hosted bar, large reunions, and tournaments. You get the community-center price instinct with grown-up amenities.",
  fits=["Milestone parties with a licensed bar","Quinceañeras & sweet sixteens","HOA & community celebrations","Reunions & multi-family gatherings"]),
 dict(slug="wash-park", city="Washington Park", drive="≈15 minutes east via E Alameda Ave or Leetsdale — our street starts in your neighborhood",
  kw="event venue near Wash Park Denver", h1="Wash Park's indoor plan B (and A)",
  intro="Wash Park residents host outdoors by instinct — until the guest list, the weather, or the city permit says otherwise. Fifteen minutes east on Alameda, Event-Den is the indoor venue with picnic-in-the-park pricing instincts.",
  body="Engagement parties, wedding receptions, fundraisers, and big birthdays move from pavilion to polished floor without losing their warmth: string lighting, open space, our own bar license, and room for 300+ if the whole neighborhood's invited.",
  fits=["Wedding receptions & engagement parties","Fundraisers for neighborhood causes","Weather-proof milestone birthdays","Community & school celebrations"]),
 dict(slug="dtc", city="Denver Tech Center (DTC)", drive="≈15 minutes north on I-225 from the I-25 interchange — reverse commute, every time",
  kw="event space Denver Tech Center", h1="The DTC's off-site, off the clock",
  intro="The Tech Center has towers full of teams and almost nowhere to gather them. Event-Den is fifteen reverse-commute minutes up I-225: a corporate-scale floor without corporate-hotel pricing.",
  body="DTC companies use our weekday-daytime sweet spot for all-hands, trainings, product launches, and team-building days that mix strategy sessions with court time. Evening holiday parties get the licensed bar and catering by our in-house kitchen — itemized, predictable, finance-approved.",
  fits=["All-hands & quarterly meetings","Trainings, workshops & launches","Team-building days with court activities","Holiday parties & corporate galas"]),
 dict(slug="littleton", city="Littleton", drive="≈30 minutes via US-285/Hampden east to I-225 north",
  kw="affordable event venue near Littleton", h1="Littleton's big-event answer",
  intro="Historic downtown Littleton charms at small scale; for the events that need ten times the floor, Event-Den is thirty minutes northeast with space to spare.",
  body="Littleton weddings, school and booster-club fundraisers, dance and sports events, and big family parties book our courts and finished event area when Main Street venues max out. Honest starting prices — celebration blocks from ~$400, large evenings from $6,000 — keep the budget conversation short.",
  fits=["Weddings & receptions","School, booster & club fundraisers","Dance showcases & sports events","Large family celebrations"]),
]

def page_location(L):
    fname = f"events-{L['slug']}.html"
    def b():
        body = header("locations.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["hero1"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <a href="locations.html">Locations</a> / {L['city']}</nav>
    <span class="eyebrow">Serving {L['city']}</span>
    <h1>{L['h1']}</h1>
    <p class="lede" style="max-width:58ch;">{L['intro']}</p>
    <a class="btn btn-gold" href="inquiry.html">Check availability for {L['city']}</a>
  </div>
</section>

<section>
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Why {L['city']} books Event-Den</span>
      <h2>Made for how {L['city']} gathers</h2>
      <hr class="gold-rule">
      <p>{L['body']}</p>
      <h3 style="color:var(--gold-lt);margin-top:1.6rem;">A natural fit for</h3>
      <ul class="flourish-list">{''.join(f'<li>{f}</li>' for f in L['fits'])}</ul>
      <div class="btn-row">
        <a class="btn btn-gold" href="inquiry.html">Request a Quote</a>
        <a class="btn btn-ghost" href="venue.html">See the Space</a>
      </div>
    </div>
    <div class="reveal">
      <div class="split-img"><img src="{IMG["lights"]}" alt="Evening event under warm string lights at Event-Den" loading="lazy"></div>
      <div class="card" style="margin-top:28px;"><div class="card-body">
        <h3>Getting here from {L['city']}</h3>
        <p>{L['drive']}. Destination: {ADDRESS}.</p>
      </div></div>
    </div>
  </div>
</section>

<section class="section-tint">
  <div class="wrap">
    <div class="center reveal"><span class="eyebrow">The drive</span><h2>From {L['city']} to the front door</h2><hr class="gold-rule"></div>
    <div class="map-frame reveal">
      <iframe src="{MAP_EMBED}" title="Map from {L['city']} area to Event-Den, 14200 E Alameda Ave, Aurora CO" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>
""" + cta_banner(f"Hosting from {L['city']}? Let's hold your date.",
                 "Tell us your occasion and guest count — we'll reply with availability and a quote built for your event.") + "</main>"
        title = f"{L['kw'].title()} | Event-Den"
        if len(title) > 60: title = f"Event Venue Near {L['city']} | Event-Den"
        desc = (f"{L['city']} event venue alternative: 20,000 sq ft for galas, parties, weddings & corporate events. "
                f"Celebration blocks from $400. Minutes from {L['city']}.")[:155]
        return head(title, desc, fname, IMG["hero1"]) + body + FOOTER
    return fname, b

# Location landing pages removed for now — cities listed in footer (#areas).
# LOCS data retained above for future re-activation.

def page_locations_hub():
    cards = "\n".join(
      f'''<article class="card reveal"><div class="card-body"><h3>{L["city"]}</h3>
      <p>{L["intro"].split(".")[0].replace("<strong>","").replace("</strong>","")}.</p>
      <a class="card-link" href="events-{L["slug"]}.html">Events near {L["city"]}</a></div></article>'''
      for L in LOCS)
    body = header("locations.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["city"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Locations</nav>
    <span class="eyebrow">Areas we serve</span>
    <h1>One central venue, the whole metro invited</h1>
    <p class="lede" style="max-width:58ch;">Centrally located at I-225 and Alameda, Event-Den serves communities across the Denver metro. Find yours below.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="grid grid-3">
{cards}
    </div>
  </div>
</section>
""" + cta_banner("Wherever you're hosting from, the answer is twenty-some minutes away.",
                 "Send your date and headcount — we'll handle the rest.") + "</main>"
    return head("Denver Metro Event Venue Locations | Event-Den",
        "Event-Den serves Aurora, Denver, Cherry Creek, DTC, Greenwood Village, Highlands Ranch, Parker, Castle Rock & more — one central venue for the whole metro.",
        "locations.html", IMG["city"]) + body + FOOTER

# locations hub removed

# ============================================================ INQUIRY / CONTACT / LEGAL
def page_inquiry():
    body = header("inquiry.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["hero3"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Request a Quote</nav>
    <span class="eyebrow">Inquiry</span>
    <h1>Request a quote, check a date</h1>
    <p class="lede" style="max-width:58ch;">Tell us the occasion, the date, and the guest count. We typically respond within one business day with availability and an itemized starting quote.</p>
  </div>
</section>
<section class="section-light">
  <div class="wrap" style="max-width:880px;">
    <div class="card reveal"><div class="card-body" style="text-align:center;padding:60px 30px;">
      <h3>Inquiry form</h3>
      <p><span class="todo-flag">TODO: embed Google Form here — replace this block with the &lt;iframe&gt; once the form URL is confirmed</span></p>
      <p style="font-size:.9rem;">Form is hosted off-domain (Google Forms) so no personal data is stored on this website. Until it's live, email us directly:</p>
      <p><span class="todo-flag">TODO: confirm public Event-Den email</span> &nbsp; <span class="todo-flag">TODO: confirm phone</span></p>
      <!-- TODO: <iframe src="GOOGLE_FORM_URL" title="Event-Den inquiry form" loading="lazy" style="width:100%;height:1200px;border:0;"></iframe> -->
    </div></div>
    <div class="grid grid-3" style="margin-top:40px;">
      <div class="reveal"><h3 style="color:var(--gold-lt);">What to include</h3><p style="font-size:.92rem;">Date(s), guest count, event type, and whether you'd like catering, bar, rentals, or coordination.</p></div>
      <div class="reveal"><h3 style="color:var(--gold-lt);">What you'll get</h3><p style="font-size:.92rem;">Availability confirmation and a clear, itemized starting quote — no obligation.</p></div>
      <div class="reveal"><h3 style="color:var(--gold-lt);">Prefer to talk?</h3><p style="font-size:.92rem;">Schedule a tour via the <a href="contact.html">contact page</a> and walk the floor first.</p></div>
    </div>
  </div>
</section>
""" + img_band([(IMG["hero2"],"Gold-accented formal table setting"),(IMG["bar"],"Craft cocktails at the licensed house bar"),(IMG["lights"],"Warm string lights over an evening event")]) + """
</main>"""
    return head("Request a Quote | Book Event Space Denver | Event-Den",
        "Check availability and request a custom quote for your Denver event. Celebrations to 1,200-guest galas. Replies within 1 business day.",
        "inquiry.html", IMG["hero3"]) + body + FOOTER

PAGES["inquiry.html"] = page_inquiry

def page_contact():
    body = header("contact.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["venue"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Contact</nav>
    <span class="eyebrow">Contact</span>
    <h1>Find us, call us, tour the floor</h1>
  </div>
</section>
<section class="section-light">
  <div class="wrap split">
    <div class="reveal">
      <h2>Event-Den · Event Denver</h2>
      <hr class="gold-rule">
      <ul class="flourish-list">
        <li><strong>Address:</strong> {ADDRESS} (inside FieldhouseUSA)</li>
        <li><strong>Phone:</strong> <span class="todo-flag">TODO: real phone — current placeholder 123-456-7890 must be replaced</span></li>
        <li><strong>Email:</strong> <span class="todo-flag">TODO: confirm public inbox (own domain vs admin@boomtownvb.com)</span></li>
        <li><strong>Hours:</strong> Tours by appointment; events scheduled seven days a week <span class="todo-flag">TODO: confirm office hours</span></li>
        <li><strong>Parking:</strong> Free on-site lot</li>
        <li><strong>Social:</strong> <span class="todo-flag">TODO: real FB/IG links or omit (current Wix placeholders)</span></li>
      </ul>
      <div class="btn-row"><a class="btn btn-gold" href="inquiry.html">Request a Quote</a></div>
    </div>
    <div class="map-frame reveal">
      <iframe src="{MAP_EMBED}" title="Map to Event-Den at 14200 E Alameda Ave, Suite 400, Aurora CO 80012" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>
</main>"""
    return head("Contact Event-Den | Aurora CO Event Venue",
        "Contact Event-Den at 14200 E Alameda Ave, Suite 400, Aurora, CO 80012. Tours by appointment, free parking, events seven days a week.",
        "contact.html", IMG["venue"]) + body + FOOTER

PAGES["contact.html"] = page_contact

def page_legal():
    body = header("legal.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["hero4"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Legal</nav>
    <span class="eyebrow">Legal</span>
    <h1>Privacy, terms &amp; accessibility</h1>
    <p class="lede"><span class="todo-flag">Boilerplate pending counsel review</span></p>
  </div>
</section>
<section class="section-light">
  <div class="wrap" style="max-width:840px;">
    <h2 id="privacy">Privacy Policy</h2>
    <hr class="gold-rule">
    <p>Event-Den ("we") does not collect or store personal information on this website. Our inquiry form is hosted by Google Forms; information you submit there is processed under <a href="https://policies.google.com/privacy" rel="noopener" target="_blank">Google's privacy policy</a> and used by us solely to respond to your inquiry. Embedded services (Google Maps, Google Fonts, image CDN) may set their own cookies or receive standard request data (such as IP address) under their respective policies. We do not sell personal information. Questions: contact us via the details on our <a href="contact.html">contact page</a>.</p>

    <h2 id="terms" style="margin-top:3rem;">Terms of Use</h2>
    <hr class="gold-rule">
    <p>Content on event-den.com is provided for general information. Prices shown are illustrative starting points, not binding offers; all bookings are governed by a written event agreement. Third-party venues, planners, and vendors referenced through our brokerage are independent businesses: we facilitate introductions but do not guarantee their availability, pricing, or performance, and your contracts with them are direct. We may update this site at any time without notice.</p>

    <h2 id="accessibility" style="margin-top:3rem;">Accessibility</h2>
    <hr class="gold-rule">
    <p>We aim to meet WCAG 2.1 AA on this website — semantic structure, keyboard navigability, descriptive alternative text, and reduced-motion support. Our venue offers accessible parking, entrances, and restrooms. If you encounter a barrier on this site or have accessibility needs for an event, contact us and we will work to accommodate you.</p>
    <p style="margin-top:2rem;"><span class="todo-flag">TODO: counsel review before launch — confirm entity name, governing law, and venue-accessibility specifics</span></p>
  </div>
</section>
</main>"""
    return head("Privacy, Terms & Accessibility | Event-Den",
        "Event-Den legal information: privacy policy, terms of use, and accessibility statement for event-den.com and our Aurora, Colorado venue.",
        "legal.html", IMG["hero4"]) + body + FOOTER

PAGES["legal.html"] = page_legal

# ============================================================ FAQ (events + metro Denver)
EVENT_FAQS = [
 ("What types of events can Event-Den host in Denver?",
  "Almost anything that needs real space: private celebrations, galas and fundraisers, cultural and community festivals, weddings and receptions, corporate programs, sports tournaments, expos, and large-format gatherings of up to 1,200 guests. If your event doesn't fit a typical venue, it's probably a fit for ours."),
 ("Do you host quinceañeras, bar mitzvahs, and bat mitzvahs?",
  "Yes — coming-of-age celebrations are a specialty. Our finished event area suits the ceremony and dinner, while courts and open space give younger guests room to play. We work with your family's traditions, from the quinceañera waltz to mitzvah party games."),
 ("Can Event-Den host cultural festivals and community galas?",
  "Proudly and often — cultural events are at the heart of our calendar, including Asian galas, heritage festivals, faith gatherings, and community celebrations across the Denver metro's many cultures. Large open floors, flexible staging, and in-house catering and bar make multicultural programming straightforward."),
 ("Can we hold a wedding or reception at Event-Den?",
  "Yes. Couples choose us when the guest list outgrows traditional venues — we host receptions for several hundred guests with draping, lighting, and staging that transform the floor. Full wedding planning is referred to trusted partner planners; our internal events coordinator is available for day-of logistics at an additional fee."),
 ("Do you host sports tournaments and team events?",
  "Yes — we're built for them. Convertible volleyball, basketball, and pickleball courts under 40-foot ceilings host ethnic and specialized sports tournaments, league play, and matches, with the event area available for banquets and award ceremonies alongside."),
 ("What corporate events does Event-Den accommodate?",
  "Trainings, retreats, team-building days, product launches, holiday parties, and corporate galas. Weekday daytime is our most available window, which works in your favor on both scheduling and price. Court access turns an off-site into an experience."),
 ("Do you host birthday and graduation parties?",
  "Yes — on a simple 3-hour block (30 minutes setup, 2 hours of event, 30 minutes cleanup) in a private court or the finished event area. Availability for court-based parties is strongest on weekends; ask early for popular dates."),
 ("Can you host unusual or large-format events other venues turn away?",
  "That's our niche. Rallies, expos, filming, large rehearsals, multi-court competitions, and one-of-a-kind formats that need 35,000 contiguous square feet — tell us the idea before assuming it can't be done."),
 ("How does pricing work at Event-Den?",
  "Every event is custom quoted — space, hours, catering, bar, rentals, and coordination are scoped together into one clear number based on your needs, date, and market availability. Send an inquiry and we'll typically respond within one business day."),
]
METRO_FAQS = [
 ("Where is Event-Den located?",
  "Inside FieldhouseUSA at 14200 E Alameda Ave, Suite 400, Aurora, CO 80012 — just off I-225 at Alameda, with free on-site parking. The location is central to the entire Denver metro."),
 ("How far is Event-Den from downtown Denver?",
  "About 15–20 minutes east via 6th Avenue or Alameda. Guests trade downtown traffic and paid garages for a straight drive and a free parking lot."),
 ("Is Event-Den close to Denver International Airport?",
  "Yes — roughly 25–30 minutes via I-225 and Peña Boulevard, which makes us practical for tournaments, conferences, and celebrations with out-of-town guests. Hotels cluster nearby along I-225."),
 ("Is Event-Den accessible by public transit?",
  "The RTD R-Line runs through Aurora near the I-225 corridor, with stations a short ride from the venue. Most guests drive — parking is free on-site."),
 ("Which Denver metro communities does Event-Den serve?",
  "All of them — hosts come to us from Aurora, Denver, Cherry Creek, the Denver Tech Center, Greenwood Village, Cherry Hills Village, Centennial, Lone Tree, Castle Pines, Castle Rock, Parker, Highlands Ranch, Washington Park, and Littleton. Our I-225 location keeps the drive reasonable from every direction."),
 ("Why choose an Aurora venue for a Denver-area event?",
  "Space and value. Aurora's central east-metro position means more square footage for the money than downtown, easy interstate access from the south suburbs and DIA, and free parking — without giving up catering, bar service, or polish."),
 ("Is there parking for large events?",
  "Yes — a free on-site lot sized for a major sports facility, which means even 1,200-guest events park without valet lines or garage fees."),
]

def page_faq():
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
        for q,a in EVENT_FAQS+METRO_FAQS]}
    ev = "\n".join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q,a in EVENT_FAQS)
    me = "\n".join(f'<details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q,a in METRO_FAQS)
    body = header("faq.html") + f"""
<main>
<section class="page-hero" style="background-image:url('{IMG["crowd"]}')">
  <div class="hero-veil"></div>
  <div class="wrap">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / FAQ</nav>
    <span class="eyebrow">Questions &amp; Answers</span>
    <h1>Everything hosts ask us</h1>
    <p class="lede" style="max-width:58ch;">The events we host, and how to reach us from anywhere in the metro. Don't see your question? <a href="inquiry.html">Ask us directly.</a></p>
  </div>
</section>

<section id="events">
  <div class="wrap" style="max-width:880px;">
    <div class="center reveal"><span class="eyebrow">Events we host</span><h2>From milestone parties to 1,200-guest galas</h2><hr class="gold-rule"></div>
    {ev}
  </div>
</section>

<section class="section-light" id="metro">
  <div class="wrap" style="max-width:880px;">
    <div class="center reveal"><span class="eyebrow">Serving Metro Denver</span><h2>Getting here from anywhere in the metro</h2><hr class="gold-rule"></div>
    {me}
    <div class="map-frame reveal" style="margin-top:2.5rem;">
      <iframe src="{MAP_EMBED}" title="Map to Event-Den, 14200 E Alameda Ave, Aurora CO" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>
""" + cta_banner("Asked everything? Ask for a date.",
                 "Send your occasion and guest count — we'll answer with availability and a custom quote.") + "</main>"
    return head("Event & Venue FAQ | Denver Metro | Event-Den",
        "Answers on hosting galas, quinceañeras, weddings, tournaments & corporate events at Event-Den — plus directions and access from across Metro Denver.",
        "faq.html", IMG["crowd"], [faq_ld]) + body + FOOTER

PAGES["faq.html"] = page_faq

# ============================================================ BUILD ALL
if __name__ == "__main__":
    for fname, builder in PAGES.items():
        html = builder()
        if fname == "index.html":
            html = html.replace('<link rel="icon"',
                f'<link rel="preload" as="image" href="{IMG["hero1"]}">\n<link rel="icon"')
        write(fname, html)

    # sitemap.xml
    urls = "\n".join(
        f"  <url><loc>{DOMAIN}/{'' if f=='index.html' else f}</loc></url>"
        for f in PAGES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + urls + "\n</urlset>\n")
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print("sitemap, robots, .nojekyll written —", len(PAGES), "pages")

