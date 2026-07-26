#!/usr/bin/env python3
"""
Static site assembler for MAA Footwear.
Combines shared head/nav/footer with per-page content so every
page ships as plain crawlable HTML (good for SEO) while keeping
one source of truth for the header & footer markup.
Run: python3 build.py
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

NAV_ITEMS = [
    ("index.html", "Home"),
    ("shop.html", "Shop"),
    ("offers.html", "Offers"),
    ("about.html", "About Us"),
    ("contact.html", "Contact Us"),
]

SHOP_DROPDOWN = [
    ("shop.html", "All Products"),
    ("men.html", "Men's Collection"),
    ("women.html", "Women's Collection"),
    ("kids.html", "Kids Collection"),
    ("sports-shoes.html", "Sports Shoes"),
    ("sneakers.html", "Sneakers"),
    ("sandals.html", "Sandals"),
    ("slippers.html", "Slippers"),
]


def head(title, desc, path_prefix="", extra_css="", canonical=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MAA Footwear">
<link rel="icon" href="{path_prefix}images/site/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{path_prefix}css/style.css">
{extra_css}
</head>
<body>
"""


def topbar(prefix=""):
    return f"""
<div class="topbar">
  <div class="container">
    <div class="topbar__left">
      <span>📍 Station Road Market, Kannauj, UP</span>
      <span>🕘 Mon–Sun: 10:00 AM – 9:00 PM</span>
    </div>
    <div class="topbar__left">
      <a href="tel:+919876543210">📞 +91 98765 43210</a>
      <a href="{prefix}contact.html">Store Locator</a>
    </div>
  </div>
</div>
"""


def navbar(active, prefix=""):
    links = ""
    for href, label in NAV_ITEMS:
        cls = "active" if href == active else ""
        if href == "shop.html":
            is_shop_family = active in [x[0] for x in SHOP_DROPDOWN]
            cls = "active" if is_shop_family else ""
            dd = "".join(
                f'<a href="{prefix}{h}">{l}</a>' for h, l in SHOP_DROPDOWN
            )
            links += f"""<div class="nav-dd">
              <a href="{prefix}{href}" class="{cls}">Shop ▾</a>
              <div class="nav-dd__menu">{dd}</div>
            </div>"""
        else:
            links += f'<a href="{prefix}{href}" class="{cls}">{label}</a>'

    mobile_links = "".join(
        f'<a href="{prefix}{h}">{l}</a>' for h, l in NAV_ITEMS
    )
    mobile_shop = "".join(
        f'<a href="{prefix}{h}" style="padding-left:20px;font-weight:500;">{l}</a>'
        for h, l in SHOP_DROPDOWN[1:]
    )

    return f"""
<header class="navbar">
  <div class="container">
    <a href="{prefix}index.html" class="brand">
      <span class="brand__mark">M</span>
      <span class="brand__name">MAA <span>Footwear</span></span>
    </a>
    <nav class="nav-links">{links}</nav>
    <div class="nav-actions">
      <button class="icon-btn" id="searchToggle" aria-label="Search products">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </button>
      <button class="icon-btn" id="themeToggle" aria-label="Toggle dark mode">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
      </button>
      <a class="icon-btn" href="{prefix}admin/login.html" aria-label="Admin Panel" title="Admin Panel">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><path d="M20 21a8 8 0 0 0-16 0"/><circle cx="12" cy="7" r="4"/></svg>
      </a>
      <button class="icon-btn mobile-toggle" id="mobileToggle" aria-label="Open menu">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
      </button>
    </div>
  </div>
  <div class="search-pop" id="searchPop">
    <form action="{prefix}shop.html" method="get">
      <input type="search" name="q" placeholder="Search for shoes, brands, categories…" autocomplete="off" required>
      <button class="btn btn-amber" type="submit">Search</button>
    </form>
  </div>
</header>
<div class="drawer" id="drawer">
  <div class="drawer__overlay" id="drawerOverlay"></div>
  <div class="drawer__panel">
    <button class="icon-btn drawer__close" id="drawerClose" aria-label="Close menu">✕</button>
    <div style="clear:both;height:10px"></div>
    {mobile_links}
    {mobile_shop}
  </div>
</div>
"""


def page_header(title, crumb, prefix=""):
    return f"""
<section class="page-header">
  <div class="container">
    <div class="breadcrumb"><a href="{prefix}index.html">Home</a> / {crumb}</div>
    <h1>{title}</h1>
  </div>
</section>
"""


def footer(prefix=""):
    return f"""
<footer class="footer">
  <div class="container">
    <div>
      <h5>MAA Footwear</h5>
      <p>Your neighbourhood footwear store for the whole family — sports shoes, sneakers, sandals and slippers, picked for comfort and value. Browse online, buy in-store.</p>
      <div class="footer__social">
        <a href="#" aria-label="Facebook">f</a>
        <a href="#" aria-label="Instagram">◎</a>
        <a href="https://wa.me/919876543210" aria-label="WhatsApp">✆</a>
      </div>
    </div>
    <div>
      <h5>Shop</h5>
      <ul>
        <li><a href="{prefix}men.html">Men's Collection</a></li>
        <li><a href="{prefix}women.html">Women's Collection</a></li>
        <li><a href="{prefix}kids.html">Kids Collection</a></li>
        <li><a href="{prefix}sports-shoes.html">Sports Shoes</a></li>
        <li><a href="{prefix}sneakers.html">Sneakers</a></li>
        <li><a href="{prefix}sandals.html">Sandals</a></li>
        <li><a href="{prefix}slippers.html">Slippers</a></li>
      </ul>
    </div>
    <div>
      <h5>Company</h5>
      <ul>
        <li><a href="{prefix}about.html">About Us</a></li>
        <li><a href="{prefix}offers.html">Offers</a></li>
        <li><a href="{prefix}contact.html">Contact Us</a></li>
        <li><a href="{prefix}admin/login.html">Admin Login</a></li>
      </ul>
    </div>
    <div>
      <h5>Visit The Store</h5>
      <p>Shop No. 14, Station Road Market,<br>Kannauj, Uttar Pradesh 209725</p>
      <p>📞 <a href="tel:+919876543210">+91 98765 43210</a><br>✉️ <a href="mailto:hello@maafootwear.in">hello@maafootwear.in</a></p>
    </div>
  </div>
  <div class="container footer__bottom">
    <span>© 2026 MAA Footwear. All rights reserved.</span>
    <span>Designed &amp; maintained by your website developer.</span>
  </div>
</footer>
<a class="wa-float" href="https://wa.me/919876543210?text=Hi%20MAA%20Footwear%2C%20I%20have%20a%20question" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
  <svg viewBox="0 0 32 32" fill="currentColor"><path d="M16.02 3C9.4 3 4 8.4 4 15.02c0 2.5.72 4.83 1.97 6.8L4 29l7.36-1.93a11.9 11.9 0 0 0 4.66.95h.01c6.62 0 12.02-5.4 12.02-12.02C28.05 8.4 22.65 3 16.02 3zm7.02 17.1c-.3.85-1.72 1.62-2.38 1.7-.6.08-1.36.11-2.2-.14-.5-.15-1.15-.37-1.98-.72-3.48-1.5-5.75-5.02-5.93-5.26-.17-.24-1.42-1.9-1.42-3.62s.9-2.57 1.22-2.92c.32-.35.7-.43.93-.43h.67c.21 0 .5-.08.78.6.3.7 1 2.44 1.09 2.62.09.18.15.4.03.64-.12.24-.18.4-.36.6-.18.2-.38.46-.54.62-.18.18-.37.37-.16.72.21.35.94 1.55 2.02 2.5 1.39 1.24 2.56 1.63 2.92 1.81.36.18.57.15.78-.09.21-.24.9-1.05 1.14-1.4.24-.36.48-.3.8-.18.33.12 2.06.97 2.41 1.15.36.18.6.27.68.42.09.15.09.85-.2 1.7z"/></svg>
</a>
<script src="{prefix}js/products-seed.js"></script>
<script src="{prefix}js/store.js"></script>
<script src="{prefix}js/main.js"></script>
"""


def wrap(title, desc, active, crumb, content, extra_scripts="", extra_css="", show_page_header=True, canonical=""):
    html = head(title, desc, extra_css=extra_css, canonical=canonical)
    html += topbar()
    html += navbar(active)
    if show_page_header:
        html += page_header(title.split("|")[0].strip(), crumb)
    html += content
    html += footer()
    html += extra_scripts
    html += "\n</body>\n</html>\n"
    return html


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)
