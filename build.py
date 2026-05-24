#!/usr/bin/env python3
"""
JustFly Affiliate Site Builder
Generates 10 pages styled to match index.html and pushes to GitHub.
Repo: brightlane/justflydeals
"""

import os, base64, requests
from datetime import datetime

AFF       = "https://track.rqqft.com/aff_c?offer_id=25631&aff_id=21885"
SITE_NAME = "FlightDealsPro"
SITE_URL  = "https://brightlane.github.io/justflydeals"
GH_USER   = os.environ.get("GH_USER", "brightlane")
GH_REPO   = os.environ.get("GH_REPO", "justflydeals")
GH_TOKEN  = os.environ.get("GITHUB_TOKEN", "")

HEADERS = {
    "Authorization": f"token {GH_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# ── SHARED CSS (matches index.html exactly) ──────────────────────
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{font-family:'Inter',sans-serif;background:#f7f8fc;color:#1a1a2e;line-height:1.7;}
a{text-decoration:none;color:inherit;}
nav{background:#0a2463;padding:0 1.5rem;display:flex;align-items:center;justify-content:space-between;height:60px;position:sticky;top:0;z-index:100;}
.nav-logo{color:#fff;font-weight:800;font-size:1.15rem;display:flex;align-items:center;gap:6px;}
.nav-logo span{color:#ff6b00;}
.nav-links{display:flex;gap:1.5rem;}
.nav-links a{color:rgba(255,255,255,0.75);font-size:0.85rem;font-weight:600;transition:color 0.2s;}
.nav-links a:hover{color:#fff;}
.nav-book{background:#ff6b00;color:#fff!important;padding:6px 16px;border-radius:50px;font-weight:700!important;}
.hero{background:linear-gradient(135deg,#0a2463 0%,#1a4a8a 60%,#0d3b7a 100%);color:#fff;text-align:center;padding:5rem 1.5rem 4rem;}
.hero-badge{display:inline-block;background:rgba(255,107,0,0.2);border:1px solid rgba(255,107,0,0.5);color:#ffaa66;padding:5px 16px;border-radius:50px;font-size:0.8rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1.5rem;}
.hero h1{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;line-height:1.1;margin-bottom:1rem;}
.hero h1 em{color:#ff6b00;font-style:normal;}
.hero p{font-size:1.1rem;color:rgba(255,255,255,0.75);max-width:520px;margin:0 auto 2rem;}
.btn{display:inline-block;padding:16px 36px;border-radius:8px;font-weight:700;font-size:1rem;transition:transform 0.2s,box-shadow 0.2s;}
.btn-orange{background:#ff6b00;color:#fff;box-shadow:0 6px 24px rgba(255,107,0,0.4);}
.btn-orange:hover{transform:translateY(-3px);box-shadow:0 12px 32px rgba(255,107,0,0.5);}
.btn-ghost{border:2px solid rgba(255,255,255,0.3);color:#fff;margin-left:1rem;}
.btn-ghost:hover{background:rgba(255,255,255,0.1);}
.hero-stats{display:flex;justify-content:center;gap:3rem;margin-top:3.5rem;flex-wrap:wrap;}
.hero-stat-num{font-size:2rem;font-weight:800;}
.hero-stat-label{font-size:0.75rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:0.08em;}
.urgency{background:#fff3e0;border-top:3px solid #ff6b00;text-align:center;padding:0.75rem 1rem;font-weight:600;font-size:0.95rem;color:#7a3300;}
#countdown{color:#ff6b00;font-weight:800;}
.urgency-bar-wrap{height:6px;background:#ffe0b2;margin-top:0.4rem;}
#urgency-bar{height:100%;background:#ff6b00;transition:width 1s linear;}
.section{padding:4rem 1.5rem;}
.section-alt{background:#fff;}
.container{max-width:1100px;margin:0 auto;}
.section-tag{font-size:0.72rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#ff6b00;margin-bottom:0.5rem;}
.section-title{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:800;color:#0a2463;margin-bottom:0.5rem;}
.section-sub{color:#666;margin-bottom:2.5rem;max-width:540px;}
.center{text-align:center;}
.center .section-sub{margin-left:auto;margin-right:auto;}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem;margin-bottom:2rem;}
.card{background:#fff;border-radius:14px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,0.07);border:1px solid #eef0f8;transition:transform 0.25s,box-shadow 0.25s;display:block;}
.card:hover{transform:translateY(-6px);box-shadow:0 12px 36px rgba(10,36,99,0.12);}
.card-icon{font-size:2rem;margin-bottom:1rem;}
.card h3{font-size:1.05rem;font-weight:700;color:#0a2463;margin-bottom:0.5rem;}
.card p{font-size:0.9rem;color:#555;margin-bottom:1rem;}
.card-link{font-size:0.85rem;font-weight:700;color:#ff6b00;}
.dest-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:1rem;margin-bottom:2rem;}
.dest{background:#fff;border-radius:12px;padding:1.2rem;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,0.07);border:1px solid #eef0f8;transition:transform 0.2s;display:block;}
.dest:hover{transform:translateY(-4px);}
.dest-emoji{font-size:2rem;margin-bottom:0.4rem;}
.dest-city{font-weight:700;color:#0a2463;font-size:0.95rem;}
.dest-price{color:#ff6b00;font-weight:700;font-size:0.85rem;margin-top:0.2rem;}
.cta-band{background:linear-gradient(135deg,#0a2463,#1a4a8a);color:#fff;text-align:center;padding:3.5rem 1.5rem;margin:2rem 0;}
.cta-band h2{font-size:clamp(1.4rem,3vw,2rem);font-weight:800;margin-bottom:0.75rem;}
.cta-band p{color:rgba(255,255,255,0.75);margin-bottom:2rem;}
.tips{display:grid;gap:1rem;}
.tip{display:flex;gap:1rem;background:#fff;padding:1.2rem 1.5rem;border-radius:12px;box-shadow:0 2px 12px rgba(0,0,0,0.06);border-left:4px solid #0a2463;}
.tip-n{font-size:1.2rem;font-weight:800;color:#0a2463;min-width:28px;}
.tip-t strong{display:block;font-size:0.95rem;color:#0a2463;margin-bottom:0.2rem;}
.tip-t span{font-size:0.87rem;color:#666;}
.compare-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;margin:1rem 0 2rem;}
th,td{padding:0.9rem 1rem;text-align:left;border-bottom:1px solid #eef0f8;font-size:0.9rem;}
th{background:#f0f4ff;color:#0a2463;font-weight:700;}
tr:hover td{background:#fafbff;}
.yes{color:#16a34a;font-weight:700;}
.no{color:#ccc;}
.best{background:#ff6b00;color:#fff;font-size:0.65rem;font-weight:700;padding:2px 7px;border-radius:50px;margin-left:5px;vertical-align:middle;}
.faqs{display:grid;gap:1rem;}
.faq{background:#fff;border-radius:12px;padding:1.4rem 1.6rem;box-shadow:0 2px 12px rgba(0,0,0,0.06);border:1px solid #eef0f8;}
.faq-q{font-weight:700;color:#0a2463;margin-bottom:0.4rem;}
.faq-a{font-size:0.9rem;color:#555;}
.sticky{position:fixed;bottom:20px;right:20px;background:#ff6b00;color:#fff;padding:14px 24px;border-radius:8px;font-weight:700;font-size:0.9rem;box-shadow:0 6px 20px rgba(255,107,0,0.45);z-index:999;transition:transform 0.2s;}
.sticky:hover{transform:scale(1.05);}
footer{background:#0a2463;color:rgba(255,255,255,0.6);text-align:center;padding:1.5rem;font-size:0.82rem;}
footer a{color:rgba(255,255,255,0.5);}
footer a:hover{color:#fff;}
.disclosure{font-size:0.78rem;color:#999;text-align:center;padding:1rem;border-top:1px solid #eee;}
.fade{opacity:0;transform:translateY(20px);transition:opacity 0.6s ease,transform 0.6s ease;}
.fade.on{opacity:1;transform:none;}
.breadcrumb{font-size:0.82rem;color:#888;padding:0.75rem 0 0;}
.breadcrumb a{color:#ff6b00;}
@media(max-width:768px){.nav-links{display:none;}.hero-stats{gap:1.5rem;}.btn-ghost{display:none;}}
"""

JS = """
const el=document.getElementById('countdown');
const bar=document.getElementById('urgency-bar');
if(el&&bar){
  const total=6*60*60*1000,end=Date.now()+total;
  function tick(){
    const d=end-Date.now();
    if(d<=0){el.textContent='Expired';bar.style.width='0%';return;}
    const h=Math.floor(d/3600000),m=Math.floor((d%3600000)/60000),s=Math.floor((d%60000)/1000);
    el.textContent=h+'h '+m+'m '+s+'s';
    const pct=(d/total)*100;
    bar.style.width=pct+'%';
    bar.style.background=pct>66?'#22c55e':pct>33?'#f59e0b':'#ef4444';
  }
  tick();setInterval(tick,1000);
}
const faders=document.querySelectorAll('.fade');
function check(){faders.forEach(el=>{if(el.getBoundingClientRect().top<window.innerHeight-60)el.classList.add('on');});}
window.addEventListener('scroll',check);
window.addEventListener('load',check);
"""

def nav():
    return f"""<nav>
  <div class="nav-logo">✈ Flight<span>Deals</span>Pro</div>
  <div class="nav-links">
    <a href="index.html">Home</a>
    <a href="flights.html">Flights</a>
    <a href="hotels.html">Hotels</a>
    <a href="destinations.html">Destinations</a>
    <a href="tips.html">Tips</a>
    <a href="comparison.html">Compare</a>
    <a href="faq.html">FAQ</a>
    <a href="{AFF}" class="nav-book">Book Now ✈</a>
  </div>
</nav>"""

STICKY = f'<a href="{AFF}" class="sticky">✈ Book Now on JustFly</a>'

FOOTER = f"""<div class="disclosure">This site contains affiliate links. We earn a commission when you book through our links at no extra cost to you. | aff_id=21885</div>
<footer>
  <p>© 2026 FlightDealsPro | Powered by JustFly.com</p>
  <p style="margin-top:0.4rem;"><a href="about.html">About</a> &nbsp;|&nbsp; <a href="contact.html">Contact</a> &nbsp;|&nbsp; <a href="disclosure.html">Disclosure</a></p>
</footer>"""

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">'

def page(title, desc, slug, body, schema=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="index, follow">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="canonical" href="{SITE_URL}/{slug}">
{FONTS}
{schema}
<style>{CSS}</style>
</head>
<body>
{nav()}
{body}
{FOOTER}
{STICKY}
<script>{JS}</script>
</body>
</html>"""

def urgency():
    return """<div class="urgency">
  ⏰ Limited fares — offer ends in: <span id="countdown">Loading...</span>
  <div class="urgency-bar-wrap"><div id="urgency-bar" style="width:100%;"></div></div>
</div>"""

def cta_band(h2, p):
    return f"""<div class="cta-band fade">
  <div class="container">
    <h2>{h2}</h2>
    <p>{p}</p>
    <a href="{AFF}" class="btn btn-orange" style="font-size:1.1rem;padding:18px 40px;">✈ Find My Cheap Flight on JustFly</a>
  </div>
</div>"""

# ── PAGES ────────────────────────────────────────────────────────

def page_flights():
    body = f"""
<section class="hero">
  <div class="hero-badge">✈ 500+ Airlines Compared</div>
  <h1>Find <em>Cheap Flights</em><br>on JustFly</h1>
  <p>Real-time fares from every major airline. One-way, round-trip, or multi-city.</p>
  <a href="{AFF}" class="btn btn-orange">🔍 Search Flights Now</a>
  <div class="hero-stats">
    <div><div class="hero-stat-num">500+</div><div class="hero-stat-label">Airlines</div></div>
    <div><div class="hero-stat-num">$73</div><div class="hero-stat-label">Avg. Savings</div></div>
    <div><div class="hero-stat-num">4.9★</div><div class="hero-stat-label">Rating</div></div>
  </div>
</section>
{urgency()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Flight Types</div>
    <h2 class="section-title">Every Type of Flight, One Platform</h2>
    <div class="cards fade">
      <a href="{AFF}" class="card"><div class="card-icon">🔄</div><h3>Round-Trip</h3><p>Book outbound and return in one search. JustFly finds the cheapest combination across all airlines.</p><span class="card-link">Search Round-Trip →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">➡️</div><h3>One-Way</h3><p>Mix and match airlines for the cheapest one-way fares on any route.</p><span class="card-link">Search One-Way →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🌐</div><h3>Multi-City</h3><p>Build a custom itinerary visiting multiple cities, optimized for the lowest total fare.</p><span class="card-link">Search Multi-City →</span></a>
    </div>
  </div>
</section>
{cta_band("Prices Drop Daily — Don't Miss Out", "Fares on top routes change every hour. Lock in the lowest price now.")}"""
    return page("Cheap Flights 2026 — JustFly Flight Search | FlightDealsPro",
                "Find the cheapest flights with JustFly. Compare one-way, round-trip, and multi-city fares from 500+ airlines instantly.",
                "flights.html", body)

def page_hotels():
    body = f"""
<section class="hero">
  <div class="hero-badge">🏨 Exclusive Hotel Rates</div>
  <h1>Book <em>Hotels</em> at<br>Unbeatable Rates</h1>
  <p>Bundle your hotel with your flight and save up to 40%.</p>
  <a href="{AFF}" class="btn btn-orange">🏨 Search Hotels on JustFly</a>
</section>
{urgency()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Hotel Perks</div>
    <h2 class="section-title">Why Book Hotels Through JustFly?</h2>
    <div class="cards fade">
      <a href="{AFF}" class="card"><div class="card-icon">💰</div><h3>Bundle &amp; Save</h3><p>Combine your flight + hotel in one booking and unlock exclusive rates not available elsewhere.</p><span class="card-link">Find Bundles →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">🔍</div><h3>Price Comparison</h3><p>Search thousands of hotels and compare rates from multiple booking platforms simultaneously.</p><span class="card-link">Compare Hotels →</span></a>
      <a href="{AFF}" class="card"><div class="card-icon">📅</div><h3>Free Cancellation</h3><p>Filter for hotels with free cancellation. Plans change — your booking should be flexible too.</p><span class="card-link">Free Cancel Hotels →</span></a>
    </div>
    <div style="text-align:center;">
      <a href="{AFF}" class="btn btn-orange">🏨 Find Hotel Deals Now →</a>
    </div>
  </div>
</section>"""
    return page("Cheap Hotel Deals 2026 — Book via JustFly | FlightDealsPro",
                "Find cheap hotel deals and bundle savings on JustFly. Save up to 40% with flight + hotel packages.",
                "hotels.html", body)

def page_destinations():
    dests = [
        ("🗽","New York","NY","$89","The city that never sleeps. World-class dining, Broadway, and iconic skyline views."),
        ("🏰","London","UK","$299","History, culture, and charm. From Big Ben to Borough Market."),
        ("🗼","Paris","France","$319","The City of Light. Art, cuisine, and the Eiffel Tower await."),
        ("🌸","Tokyo","Japan","$549","Futuristic and traditional. Sushi, temples, and neon-lit streets."),
        ("🏖","Cancún","Mexico","$149","White sand beaches and crystal-clear Caribbean waters."),
        ("🌴","Miami","FL","$99","Art Deco, nightlife, and year-round sunshine on South Beach."),
        ("🎰","Las Vegas","NV","$79","Entertainment capital of the world. Shows, dining, and iconic casinos."),
        ("🌉","San Francisco","CA","$119","The Golden Gate, world-class tech scene, and incredible food."),
    ]
    cards = "".join(f"""<a href="{AFF}" class="card">
      <div class="card-icon">{e}</div>
      <h3>{city} <small style="font-weight:400;color:#888;">— {region}</small></h3>
      <p>{desc}</p>
      <span class="card-link">Flights from {price} →</span>
    </a>""" for e,city,region,price,desc in dests)
    body = f"""
<section class="hero">
  <div class="hero-badge">🌍 Top Destinations 2026</div>
  <h1>Where Will You <em>Fly</em><br>This Year?</h1>
  <p>Hot routes with the best fares. Book now before prices rise.</p>
  <a href="{AFF}" class="btn btn-orange">✈ Search All Destinations</a>
</section>
{urgency()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Popular Routes</div>
    <h2 class="section-title">Top Destinations Right Now</h2>
    <p class="section-sub">Fares updated daily. Click any destination to see live prices.</p>
    <div class="cards fade">{cards}</div>
  </div>
</section>"""
    return page("Top Flight Destinations 2026 — Cheap Fares | FlightDealsPro",
                "Browse top travel destinations and find cheap flights via JustFly. Live fares to New York, London, Paris, Tokyo, Cancún, and more.",
                "destinations.html", body)

def page_tips():
    tips = [
        ("Book on Tuesday or Wednesday","Airfare is cheapest mid-week. Avoid Friday–Sunday when prices spike 15–25%."),
        ("Fly early morning or late night","Off-peak departures are 20–30% cheaper with lower cancellation rates."),
        ("Be flexible with dates","Shifting your trip by 1–3 days can save $100–$400, especially around holidays."),
        ("Book domestic 6–8 weeks out","The sweet spot for US flights. Too early or too late costs more."),
        ("Book international 3–6 months out","For transatlantic and transpacific routes, book well in advance."),
        ("Try nearby airports","A secondary airport 60–90 minutes away can cut your fare by up to 40%."),
        ("Set fare alerts on JustFly","Get notified the instant prices drop on your route. Never miss a deal."),
        ("Search in incognito mode","Airlines track repeat searches and raise prices. Always use a private window."),
        ("Bundle flight + hotel","Booking together saves 15–40% over booking separately."),
        ("Consider a one-stop flight","A connecting flight often costs 30–50% less than nonstop."),
    ]
    tip_html = "".join(f'<div class="tip"><div class="tip-n">{str(i+1).zfill(2)}</div><div class="tip-t"><strong>{t}</strong><span>{d}</span></div></div>' for i,(t,d) in enumerate(tips))
    body = f"""
<section class="hero" style="padding:3rem 1.5rem;">
  <div class="hero-badge">💡 Expert Travel Tips</div>
  <h1>How to Find <em>Cheap Flights</em><br>Every Time</h1>
  <p>Proven strategies to cut your airfare by 30–60%.</p>
</section>
{urgency()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Airfare Strategy</div>
    <h2 class="section-title">10 Rules for Cheap Flights</h2>
    <div class="tips fade">{tip_html}</div>
    <div style="text-align:center;margin-top:2rem;">
      <a href="{AFF}" class="btn btn-orange">✈ Apply These Tips — Search JustFly Now</a>
    </div>
  </div>
</section>"""
    return page("10 Tips for Finding Cheap Flights 2026 | FlightDealsPro",
                "Expert tips to find cheap flights every time. Cut airfare by 30–60% using JustFly and flexible booking strategies.",
                "tips.html", body)

def page_comparison():
    body = f"""
<section class="hero" style="padding:3rem 1.5rem;">
  <div class="hero-badge">⚖️ Unbiased Comparison</div>
  <h1>JustFly vs <em>The Competition</em></h1>
  <p>How does JustFly stack up against Expedia, Kayak, and Google Flights?</p>
</section>
{urgency()}
<section class="section section-alt">
  <div class="container">
    <div class="section-tag">Platform Comparison</div>
    <h2 class="section-title">JustFly vs Expedia vs Kayak vs Google Flights</h2>
    <div class="compare-wrap fade">
      <table>
        <tr><th>Feature</th><th>JustFly <span class="best">BEST</span></th><th>Expedia</th><th>Kayak</th><th>Google Flights</th></tr>
        <tr><td>Flight + Hotel Bundles</td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td><td><span class="no">—</span></td><td><span class="no">—</span></td></tr>
        <tr><td>Car Rental Bundling</td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td><td><span class="no">—</span></td><td><span class="no">—</span></td></tr>
        <tr><td>500+ Airlines</td><td><span class="yes">✔</span></td><td><span class="no">—</span></td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td></tr>
        <tr><td>Price Alerts</td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td></tr>
        <tr><td>Flexible Date Search</td><td><span class="yes">✔</span></td><td>Partial</td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td></tr>
        <tr><td>Multi-City Booking</td><td><span class="yes">✔</span></td><td><span class="yes">✔</span></td><td>Partial</td><td><span class="yes">✔</span></td></tr>
        <tr><td>Starting Price</td><td><strong style="color:#ff6b00;">Lowest</strong></td><td>Mid</td><td>Mid</td><td>Variable</td></tr>
      </table>
    </div>
    <div style="text-align:center;">
      <a href="{AFF}" class="btn btn-orange">✈ Book on JustFly — Best Value</a>
    </div>
  </div>
</section>"""
    return page("JustFly vs Expedia vs Kayak vs Google Flights 2026 | FlightDealsPro",
                "Unbiased comparison of JustFly vs Expedia, Kayak, and Google Flights. Features, pricing, and which platform wins.",
                "comparison.html", body)

def page_faq():
    schema = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{"@type":"Question","name":"Is JustFly legit?","acceptedAnswer":{"@type":"Answer","text":"Yes. JustFly is a fully accredited, IATA-certified travel booking platform used by millions of travelers worldwide."}},
{"@type":"Question","name":"Is JustFly cheaper than Expedia?","acceptedAnswer":{"@type":"Answer","text":"JustFly frequently offers lower fares, especially on flight and hotel bundles."}},
{"@type":"Question","name":"What is the cheapest day to book flights?","acceptedAnswer":{"@type":"Answer","text":"Tuesday and Wednesday are historically the cheapest days to book. Avoid weekends when prices spike 15-25%."}},
{"@type":"Question","name":"Can I cancel a JustFly booking?","acceptedAnswer":{"@type":"Answer","text":"Cancellation policies vary by airline. Many fares include a 24-hour free cancellation window."}}
]}</script>"""
    body = f"""
<section class="hero" style="padding:3rem 1.5rem;">
  <div class="hero-badge">❓ FAQ</div>
  <h1>JustFly — Your Questions <em>Answered</em></h1>
  <p>Everything you need to know before booking.</p>
</section>
{urgency()}
<section class="section section-alt">
  <div class="container">
    <div class="faqs fade">
      <div class="faq"><div class="faq-q">Is JustFly legit?</div><div class="faq-a">Yes. JustFly is a fully accredited, IATA-certified booking platform used by millions of travelers. It partners with 500+ airlines worldwide.</div></div>
      <div class="faq"><div class="faq-q">Is JustFly cheaper than Expedia?</div><div class="faq-a">JustFly frequently offers lower fares, especially on flight + hotel bundles. It compares hundreds of airlines simultaneously to find the lowest rate.</div></div>
      <div class="faq"><div class="faq-q">What is the cheapest day to book flights?</div><div class="faq-a">Tuesday and Wednesday are historically cheapest. Avoid weekends when prices spike 15–25%.</div></div>
      <div class="faq"><div class="faq-q">Can I cancel a JustFly booking?</div><div class="faq-a">Policies vary by airline and fare type. Many fares include a 24-hour free cancellation window. Always check fare rules before booking.</div></div>
      <div class="faq"><div class="faq-q">Does JustFly compare all airlines?</div><div class="faq-a">JustFly compares 500+ airlines including all major carriers and many budget airlines.</div></div>
      <div class="faq"><div class="faq-q">How far ahead should I book?</div><div class="faq-a">Domestic: 6–8 weeks ahead. International: 3–6 months ahead. Use price alerts to catch fare drops.</div></div>
    </div>
    <div style="text-align:center;margin-top:2rem;">
      <a href="{AFF}" class="btn btn-orange">✈ Book on JustFly Now →</a>
    </div>
  </div>
</section>"""
    return page("JustFly FAQ 2026 — Is It Legit? Fees, Cancellation & More | FlightDealsPro",
                "Answers to common JustFly questions. Is JustFly legit? How does it compare? Cancellation, fees, and booking tips.",
                "faq.html", body, schema)

def page_about():
    body = f"""
<section class="section" style="padding-top:3rem;">
  <div class="container" style="max-width:720px;">
    <h1 class="section-title">About FlightDealsPro</h1>
    <p style="margin-bottom:1.5rem;">FlightDealsPro was built to help everyday travelers find the cheapest flights without spending hours searching. We compare platforms, review booking sites, and share expert tips so you can travel more for less.</p>
    <h2 class="section-title" style="font-size:1.3rem;text-align:left;margin-top:2rem;">Why JustFly?</h2>
    <p style="margin-bottom:2rem;">After testing every major flight booking platform, JustFly consistently delivered the lowest fares across the widest range of routes — especially on bundle deals.</p>
    <div style="text-align:center;">
      <a href="{AFF}" class="btn btn-orange">✈ Try JustFly Now →</a>
    </div>
  </div>
</section>"""
    return page("About FlightDealsPro — JustFly Travel Reviews",
                "About FlightDealsPro. We review and compare travel booking platforms to help you find the cheapest flights.",
                "about.html", body)

def page_contact():
    body = """
<section class="section" style="padding-top:3rem;">
  <div class="container" style="max-width:720px;">
    <h1 class="section-title">Contact Us</h1>
    <p>Questions, corrections, or partnership inquiries? Reach us at:</p>
    <p style="margin-top:1.5rem;font-size:1.1rem;font-weight:700;">contact [at] flightdealspro [dot] info</p>
    <p style="margin-top:1rem;color:#666;">For partnership inquiries, include "Partnership" in your subject line.</p>
  </div>
</section>"""
    return page("Contact FlightDealsPro",
                "Contact the FlightDealsPro team with questions or partnership inquiries.",
                "contact.html", body)

def page_disclosure():
    body = f"""
<section class="section" style="padding-top:3rem;">
  <div class="container" style="max-width:720px;">
    <h1 class="section-title">Affiliate Disclosure</h1>
    <p style="color:#888;margin-bottom:1.5rem;">Last updated: 2026</p>
    <p>FlightDealsPro participates in affiliate marketing programs. We earn a commission when you book through our links — at no extra cost to you.</p>
    <h2 class="section-title" style="font-size:1.3rem;text-align:left;margin-top:2rem;">Our Affiliate Relationship</h2>
    <p>We have an affiliate relationship with JustFly.com via rqqft.com (offer ID: 25631, affiliate ID: 21885).</p>
    <h2 class="section-title" style="font-size:1.3rem;text-align:left;margin-top:2rem;">Our Commitment</h2>
    <p>Commission rates do not influence our recommendations. We only promote JustFly because we believe it offers genuine value.</p>
    <div style="text-align:center;margin-top:2rem;">
      <a href="{AFF}" class="btn btn-orange">✈ Book on JustFly →</a>
    </div>
  </div>
</section>"""
    return page("Affiliate Disclosure — FlightDealsPro",
                "FlightDealsPro affiliate disclosure. We earn commissions from JustFly bookings at no extra cost to you.",
                "disclosure.html", body)

# ── SITEMAP + ROBOTS ─────────────────────────────────────────────

def all_pages():
    return {
        "flights.html":     page_flights(),
        "hotels.html":      page_hotels(),
        "destinations.html":page_destinations(),
        "tips.html":        page_tips(),
        "comparison.html":  page_comparison(),
        "faq.html":         page_faq(),
        "about.html":       page_about(),
        "contact.html":     page_contact(),
        "disclosure.html":  page_disclosure(),
    }

def sitemap(pages):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    urls = [f"  <url><loc>{SITE_URL}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>"]
    for slug in pages:
        urls.append(f"  <url><loc>{SITE_URL}/{slug}</loc><lastmod>{today}</lastmod><priority>0.8</priority></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>"

def robots():
    return f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"

def gh_put(path, content, msg):
    url = f"https://api.github.com/repos/{GH_USER}/{GH_REPO}/contents/{path}"
    r = requests.get(url, headers=HEADERS)
    sha = r.json().get("sha") if r.status_code == 200 else None
    payload = {"message": msg, "content": base64.b64encode(content.encode()).decode()}
    if sha:
        payload["sha"] = sha
    resp = requests.put(url, headers=HEADERS, json=payload)
    icon = "✅" if resp.status_code in (200, 201) else "❌"
    print(f"{icon} {path} ({resp.status_code})")

if __name__ == "__main__":
    pages = all_pages()
    print(f"Building {len(pages)} pages for {SITE_NAME}...")
    for slug, html in pages.items():
        gh_put(slug, html, f"Site update: {slug}")
    gh_put("sitemap.xml", sitemap(pages), "Site update: sitemap.xml")
    gh_put("robots.txt",  robots(),       "Site update: robots.txt")
    print(f"\nDone! {len(pages)+2} files pushed to {GH_REPO}.")
