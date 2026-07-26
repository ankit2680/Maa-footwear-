#!/usr/bin/env python3
from build import wrap, write, head, topbar, navbar, footer, page_header

SITE = "https://www.maafootwear.in/"

# =========================================================
# HOME PAGE
# =========================================================
def size_run():
    items = ""
    for _ in range(2):
        for s in [4, 5, 6, "7", 8, "9", 10, 11, "6", 7, "8", 9, "10", 5, 6, "7"]:
            items += f'<span class="size-run__item">UK <strong>{s}</strong></span>'
    return f"""
<div class="size-run">
  <div class="size-run__track">{items}</div>
</div>
"""


def home_content():
    hero = f"""
<section class="hero">
  <div class="container">
    <div>
      <div class="eyebrow hero__eyebrow">MAA Footwear · Kannauj</div>
      <h1>Footwear That Keeps Up With <em>You</em></h1>
      <p>Browse our full catalog of sports shoes, sneakers, sandals &amp; slippers for men, women and kids — then visit the store or message us on WhatsApp to buy.</p>
      <div class="hero__cta">
        <a href="shop.html" class="btn btn-amber">Shop The Full Range</a>
        <a href="https://wa.me/919876543210" target="_blank" rel="noopener" class="btn btn-outline" style="border-color:#fff;color:#fff;">WhatsApp Us</a>
      </div>
      <div class="hero__stats">
        <div><strong>500+</strong><span>Styles in Store</span></div>
        <div><strong>15+</strong><span>Trusted Brands</span></div>
        <div><strong>4.7★</strong><span>Customer Rating</span></div>
      </div>
    </div>
    <div class="hero__art"><img src="images/site/hero-shoe.svg" alt="Featured MAA Footwear sneaker" width="600" height="400"></div>
  </div>
</section>
{size_run()}
"""

    categories = f"""
<section class="section">
  <div class="container">
    <div class="section__head reveal">
      <div>
        <div class="eyebrow">Shop by Category</div>
        <h2>Find Your Fit</h2>
      </div>
      <a href="shop.html" class="btn btn-ghost">View All Products →</a>
    </div>
    <div class="cat-grid">
      <a class="cat-tile reveal" href="men.html"><img src="images/site/cat-men.svg" alt="Men's Collection"><span class="cat-tile__label">Men <span>→</span></span></a>
      <a class="cat-tile reveal" href="women.html"><img src="images/site/cat-women.svg" alt="Women's Collection"><span class="cat-tile__label">Women <span>→</span></span></a>
      <a class="cat-tile reveal" href="kids.html"><img src="images/site/cat-kids.svg" alt="Kids Collection"><span class="cat-tile__label">Kids <span>→</span></span></a>
      <a class="cat-tile reveal" href="sports-shoes.html"><img src="images/site/cat-sports.svg" alt="Sports Shoes"><span class="cat-tile__label">Sports <span>→</span></span></a>
      <a class="cat-tile reveal" href="sneakers.html"><img src="images/site/cat-sneakers.svg" alt="Sneakers"><span class="cat-tile__label">Sneakers <span>→</span></span></a>
      <a class="cat-tile reveal" href="sandals.html"><img src="images/site/cat-sandals.svg" alt="Sandals"><span class="cat-tile__label">Sandals <span>→</span></span></a>
      <a class="cat-tile reveal" href="slippers.html"><img src="images/site/cat-slippers.svg" alt="Slippers"><span class="cat-tile__label">Slippers <span>→</span></span></a>
      <a class="cat-tile reveal" href="offers.html" style="background:var(--amber);display:flex;align-items:center;justify-content:center;">
        <span style="font-family:var(--font-display);font-size:1.6rem;color:var(--ink);text-align:center;padding:20px;">Seasonal<br>Offers →</span>
      </a>
    </div>
  </div>
</section>
"""

    featured = """
<section class="section section--alt">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">Handpicked</div><h2>Featured Products</h2></div>
    </div>
    <div class="product-grid reveal" id="featuredProducts"></div>
  </div>
</section>
"""

    latest = """
<section class="section">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">Fresh In</div><h2>Latest Arrivals</h2></div>
      <a href="shop.html?sort=newest" class="btn btn-ghost">See All New Arrivals →</a>
    </div>
    <div class="product-grid reveal" id="latestArrivals"></div>
  </div>
</section>
"""

    best = """
<section class="section section--alt">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">Customer Favourites</div><h2>Best Sellers</h2></div>
    </div>
    <div class="product-grid reveal" id="bestSellers"></div>
  </div>
</section>
"""

    newcol = """
<section class="section">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">Just Landed</div><h2>New Collection</h2></div>
      <a href="shop.html" class="btn btn-ghost">Browse Shop →</a>
    </div>
    <div class="product-grid reveal" id="newCollection"></div>
  </div>
</section>
"""

    offers = """
<section class="section section--alt">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">Limited Time</div><h2>Seasonal Offers</h2></div>
      <a href="offers.html" class="btn btn-ghost">View All Offers →</a>
    </div>
    <div class="product-grid reveal" id="seasonalOffers"></div>
  </div>
</section>
"""

    testimonials = """
<section class="section">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">What Customers Say</div><h2>Trusted By The Neighbourhood</h2></div>
    </div>
    <div class="testimonial-grid">
      <div class="testimonial reveal">
        <div class="testimonial__stars">★★★★★</div>
        <p>"Bought running shoes for my son from MAA Footwear — the staff helped us pick the right size after we shortlisted online. Great value for money."</p>
        <div class="testimonial__name">Rajesh Kumar</div>
        <div class="testimonial__role">Kannauj</div>
      </div>
      <div class="testimonial reveal">
        <div class="testimonial__stars">★★★★★</div>
        <p>"I checked the catalog on the website, messaged them on WhatsApp about stock, and picked up my sandals the same evening. So convenient."</p>
        <div class="testimonial__name">Priya Sharma</div>
        <div class="testimonial__role">Kannauj</div>
      </div>
      <div class="testimonial reveal">
        <div class="testimonial__stars">★★★★☆</div>
        <p>"Good collection of sports shoes at fair prices. The website makes it easy to compare styles before visiting the shop."</p>
        <div class="testimonial__name">Amit Verma</div>
        <div class="testimonial__role">Farrukhabad</div>
      </div>
    </div>
  </div>
</section>
"""

    store = """
<section class="section section--alt">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">Visit Us</div><h2>Store Information</h2></div>
    </div>
    <div class="store-grid reveal">
      <div class="store-card">
        <h3>MAA Footwear</h3>
        <ul>
          <li><b>Address</b> Shop No. 14, Station Road Market, Kannauj, Uttar Pradesh 209725</li>
          <li><b>Phone</b> <a href="tel:+919876543210">+91 98765 43210</a></li>
          <li><b>Email</b> <a href="mailto:hello@maafootwear.in">hello@maafootwear.in</a></li>
          <li><b>Hours</b> Mon – Sun: 10:00 AM – 9:00 PM</li>
          <li><b>Payments</b> Cash, UPI, Cards accepted in-store</li>
        </ul>
        <div class="hero__cta" style="margin-top:20px;">
          <a href="tel:+919876543210" class="btn btn-call">📞 Call Shop</a>
          <a href="https://wa.me/919876543210" target="_blank" rel="noopener" class="btn btn-whatsapp">WhatsApp Us</a>
        </div>
      </div>
      <div class="map-wrap">
        <iframe src="https://www.google.com/maps?q=Kannauj,Uttar+Pradesh&output=embed" loading="lazy" title="MAA Footwear store location" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </div>
</section>
"""

    return hero + categories + featured + latest + best + newcol + offers + testimonials + store


def build_home():
    content = home_content()
    html = wrap(
        title="MAA Footwear | Sports Shoes, Sneakers, Sandals &amp; Slippers in Kannauj",
        desc="MAA Footwear — your local footwear shop in Kannauj, UP. Browse sports shoes, sneakers, sandals & slippers for men, women and kids online, then visit our store or WhatsApp to buy.",
        active="index.html",
        crumb="Home",
        content=content,
        extra_scripts='<script src="js/home.js"></script>',
        show_page_header=False,
        canonical=SITE,
    )
    write("index.html", html)


# =========================================================
# SHOP + CATEGORY LISTING PAGES
# =========================================================
def shop_layout(intro_html=""):
    return f"""
<section class="section section--tight">
  <div class="container">
    {intro_html}
    <div class="shop-layout">
      <aside class="filters">
        <h4 style="margin-top:0;">Search</h4>
        <input type="search" id="shopSearch" placeholder="Search products…" style="width:100%;padding:10px 12px;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--text);">
        <div id="filterRoot"></div>
      </aside>
      <div>
        <div class="toolbar">
          <span class="result-count" id="resultCount">Loading…</span>
          <select id="sortSelect">
            <option value="popularity">Sort: Popularity</option>
            <option value="newest">Sort: Newest</option>
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
            <option value="discount">Sort: Biggest Discount</option>
          </select>
        </div>
        <div class="product-grid" id="productGrid"></div>
      </div>
    </div>
  </div>
</section>
"""


def build_shop_family():
    pages = [
        dict(file="shop.html", title="Shop All Footwear | MAA Footwear",
             desc="Browse the complete MAA Footwear catalog — sports shoes, sneakers, sandals and slippers for men, women & kids.",
             crumb="Shop", h1="Shop All Footwear", preset=None,
             intro="Explore our complete range and filter by category, brand, size or price."),
        dict(file="men.html", title="Men's Footwear Collection | MAA Footwear",
             desc="Shop men's sports shoes, sneakers, sandals and slippers at MAA Footwear, Kannauj.",
             crumb="Men's Collection", h1="Men's Collection", preset=("gender", "men"),
             intro="Sports shoes, sneakers, sandals and slippers built for everyday comfort."),
        dict(file="women.html", title="Women's Footwear Collection | MAA Footwear",
             desc="Shop women's sneakers, flats, sandals and slippers at MAA Footwear, Kannauj.",
             crumb="Women's Collection", h1="Women's Collection", preset=("gender", "women"),
             intro="From everyday flats to festive sandals — styles for every occasion."),
        dict(file="kids.html", title="Kids Footwear Collection | MAA Footwear",
             desc="Shop kids' sports shoes, sneakers, sandals and slippers at MAA Footwear, Kannauj.",
             crumb="Kids Collection", h1="Kids Collection", preset=("gender", "kids"),
             intro="Durable, comfortable footwear built to keep up with playground energy."),
        dict(file="sports-shoes.html", title="Sports Shoes | MAA Footwear",
             desc="Shop sports and running shoes for men, women and kids at MAA Footwear, Kannauj.",
             crumb="Sports Shoes", h1="Sports Shoes", preset=("category", "sports-shoes"),
             intro="Performance-ready trainers and running shoes for every activity."),
        dict(file="sneakers.html", title="Sneakers | MAA Footwear",
             desc="Shop casual sneakers for men, women and kids at MAA Footwear, Kannauj.",
             crumb="Sneakers", h1="Sneakers", preset=("category", "sneakers"),
             intro="Everyday sneakers that pair effortlessly with any outfit."),
        dict(file="sandals.html", title="Sandals | MAA Footwear",
             desc="Shop sandals for men, women and kids at MAA Footwear, Kannauj.",
             crumb="Sandals", h1="Sandals", preset=("category", "sandals"),
             intro="Breathable, comfortable sandals for warm days and outdoor plans."),
        dict(file="slippers.html", title="Slippers | MAA Footwear",
             desc="Shop indoor and outdoor slippers for men, women and kids at MAA Footwear, Kannauj.",
             crumb="Slippers", h1="Slippers", preset=("category", "slippers"),
             intro="Soft, cushioned slippers for everyday comfort at home."),
    ]

    for p in pages:
        intro = f'<div class="reveal" style="max-width:640px;margin-bottom:8px;"><p>{p["intro"]}</p></div>'
        content = shop_layout(intro)
        body_attrs = ""
        if p["preset"]:
            key, val = p["preset"]
            body_attrs = f' data-preset-{key}="{val}"'
        html = wrap(
            title=p["title"], desc=p["desc"], active=p["file"], crumb=p["crumb"],
            content=content, extra_scripts='<script src="js/shop.js"></script>',
            canonical=SITE + p["file"],
        )
        if body_attrs:
            html = html.replace("<body>", f"<body{body_attrs}>", 1)
        write(p["file"], html)


# =========================================================
# PRODUCT DETAILS PAGE
# =========================================================
def build_product_page():
    content = """
<section class="section section--tight">
  <div class="container" id="productRoot"></div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="section__head reveal">
      <div><div class="eyebrow">You Might Also Like</div><h2>Related Products</h2></div>
    </div>
    <div class="product-grid reveal" id="relatedProducts"></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="store-grid">
      <div class="form-card reveal">
        <h3>Ask About This Product</h3>
        <p>Have a question about size, colour or availability? Send us a quick note and we'll get back to you.</p>
        <form id="enquiryForm">
          <div class="field"><label for="eqName">Full Name</label><input id="eqName" name="name" required></div>
          <div class="field"><label for="eqPhone">Phone Number</label><input id="eqPhone" name="phone" type="tel" required></div>
          <div class="field"><label for="eqMsg">Message</label><textarea id="eqMsg" name="message" rows="4" placeholder="I'd like to know if this is available in size 9…" required></textarea></div>
          <button type="submit" class="btn btn-primary btn-block">Send Enquiry</button>
        </form>
      </div>
      <div class="map-wrap reveal">
        <iframe src="https://www.google.com/maps?q=Kannauj,Uttar+Pradesh&output=embed" loading="lazy" title="MAA Footwear store location" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </div>
</section>
"""
    html = wrap(
        title="Product Details | MAA Footwear",
        desc="View full product details, sizes, colours and availability at MAA Footwear.",
        active="shop.html", crumb="Product", content=content,
        extra_scripts='<script src="js/product.js"></script>',
        show_page_header=False,
        canonical=SITE + "product.html",
    )
    write("product.html", html)


# =========================================================
# OFFERS PAGE
# =========================================================
def build_offers_page():
    content = """
<section class="section section--tight">
  <div class="container">
    <div class="reveal" style="max-width:640px;margin-bottom:28px;">
      <p>Every product below is currently discounted from its MRP. Offers are updated regularly by our team — check back often or follow up on WhatsApp for the latest deals.</p>
    </div>
    <div class="toolbar">
      <span class="result-count" id="resultCount">Loading…</span>
    </div>
    <div class="product-grid" id="productGrid"></div>
  </div>
</section>
"""
    html = wrap(
        title="Offers &amp; Discounts | MAA Footwear",
        desc="Browse the latest seasonal offers and discounted footwear at MAA Footwear, Kannauj.",
        active="offers.html", crumb="Offers", content=content,
        extra_scripts='<script src="js/offers.js"></script>',
        canonical=SITE + "offers.html",
    )
    write("offers.html", html)


# =========================================================
# ABOUT PAGE
# =========================================================
def build_about_page():
    content = """
<section class="section">
  <div class="container">
    <div class="store-grid reveal">
      <div>
        <div class="eyebrow">Our Story</div>
        <h2>Footwear For The Whole Family, Since Day One</h2>
        <p>MAA Footwear started as a small family-run shoe shop in Kannauj with one goal: stock footwear that's genuinely comfortable and fairly priced, and know every customer by name. Years on, that hasn't changed — we've simply added a website so you can browse before you visit.</p>
        <p>Every pair on this site is physically in our store. We photograph, price and list each style ourselves, so what you see online is exactly what you'll find on the shelf.</p>
      </div>
      <div class="map-wrap" style="min-height:280px;">
        <img src="images/site/hero-shoe.svg" alt="Inside MAA Footwear store" style="width:100%;height:100%;object-fit:cover;">
      </div>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="section__head reveal"><div><div class="eyebrow">Why Shop With Us</div><h2>What Sets Us Apart</h2></div></div>
    <div class="testimonial-grid">
      <div class="testimonial reveal"><h3>Try Before You Buy</h3><p>Browse online, then try the exact pair in-store — no surprises on fit or finish.</p></div>
      <div class="testimonial reveal"><h3>Honest Pricing</h3><p>MRP and offer price are listed upfront on every product, no hidden mark-ups.</p></div>
      <div class="testimonial reveal"><h3>Real Local Support</h3><p>Call or WhatsApp us directly — a real person from the shop will reply, not a bot.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section__head reveal"><div><div class="eyebrow">Our Reach</div><h2>MAA Footwear In Numbers</h2></div></div>
    <div class="hero__stats reveal" style="color:var(--text);">
      <div><strong style="color:var(--text);">10+</strong><span>Years Serving Kannauj</span></div>
      <div><strong style="color:var(--text);">500+</strong><span>Styles In Stock</span></div>
      <div><strong style="color:var(--text);">15+</strong><span>Brands Stocked</span></div>
      <div><strong style="color:var(--text);">10,000+</strong><span>Happy Customers</span></div>
    </div>
  </div>
</section>
"""
    html = wrap(
        title="About Us | MAA Footwear",
        desc="Learn about MAA Footwear — a family-run footwear shop in Kannauj, Uttar Pradesh, serving customers with quality shoes for the whole family.",
        active="about.html", crumb="About Us", content=content,
        canonical=SITE + "about.html",
    )
    write("about.html", html)


# =========================================================
# CONTACT PAGE
# =========================================================
def build_contact_page():
    content = """
<section class="section">
  <div class="container">
    <div class="store-grid">
      <div class="form-card reveal">
        <h3 class="mt-0">Send Us a Message</h3>
        <p>Have a question about a product, stock, or store hours? Fill in the form and we'll get back to you — or reach us directly below.</p>
        <form id="contactForm">
          <div class="form-grid">
            <div class="field"><label for="cName">Full Name</label><input id="cName" name="name" required></div>
            <div class="field"><label for="cPhone">Phone Number</label><input id="cPhone" name="phone" type="tel" required></div>
          </div>
          <div class="field"><label for="cEmail">Email (optional)</label><input id="cEmail" name="email" type="email"></div>
          <div class="field"><label for="cMsg">Message</label><textarea id="cMsg" name="message" rows="5" required placeholder="Tell us what you're looking for…"></textarea></div>
          <button type="submit" class="btn btn-primary btn-block">Send Message</button>
        </form>
      </div>
      <div>
        <div class="store-card reveal" style="margin-bottom:20px;">
          <h3 class="mt-0">Store Details</h3>
          <ul>
            <li><b>Address</b> Shop No. 14, Station Road Market, Kannauj, Uttar Pradesh 209725</li>
            <li><b>Phone</b> <a href="tel:+919876543210">+91 98765 43210</a></li>
            <li><b>Email</b> <a href="mailto:hello@maafootwear.in">hello@maafootwear.in</a></li>
            <li><b>Hours</b> Mon – Sun: 10:00 AM – 9:00 PM</li>
          </ul>
          <div class="hero__cta" style="margin-top:16px;">
            <a href="tel:+919876543210" class="btn btn-call">📞 Call Shop</a>
            <a href="https://wa.me/919876543210" target="_blank" rel="noopener" class="btn btn-whatsapp">WhatsApp Us</a>
          </div>
        </div>
        <div class="map-wrap reveal">
          <iframe src="https://www.google.com/maps?q=Kannauj,Uttar+Pradesh&output=embed" loading="lazy" title="MAA Footwear store location" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    html = wrap(
        title="Contact Us | MAA Footwear",
        desc="Get in touch with MAA Footwear — call, WhatsApp, or visit our store in Kannauj, Uttar Pradesh.",
        active="contact.html", crumb="Contact Us", content=content,
        extra_scripts='<script src="js/contact.js"></script>',
        canonical=SITE + "contact.html",
    )
    write("contact.html", html)


if __name__ == "__main__":
    build_home()
    build_shop_family()
    build_product_page()
    build_offers_page()
    build_about_page()
    build_contact_page()
