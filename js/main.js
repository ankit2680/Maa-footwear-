/*! MAA Footwear — shared UI behaviour for every public page */
(function () {
  "use strict";

  /* ---------------- Theme (light/dark) ---------------- */
  const THEME_KEY = "maa_theme";
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
  }
  (function initTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved) applyTheme(saved);
  })();
  document.addEventListener("click", (e) => {
    if (e.target.closest("#themeToggle")) {
      const current = document.documentElement.getAttribute("data-theme") || "light";
      applyTheme(current === "light" ? "dark" : "light");
    }
  });

  /* ---------------- Search popover ---------------- */
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("#searchToggle");
    const pop = document.getElementById("searchPop");
    if (!pop) return;
    if (btn) {
      pop.classList.toggle("open");
      const input = pop.querySelector("input");
      if (pop.classList.contains("open") && input) setTimeout(() => input.focus(), 50);
      return;
    }
    if (!e.target.closest(".search-pop") && !e.target.closest("#searchToggle")) {
      pop.classList.remove("open");
    }
  });

  /* ---------------- Mobile drawer ---------------- */
  const drawer = document.getElementById("drawer");
  document.addEventListener("click", (e) => {
    if (e.target.closest("#mobileToggle")) drawer && drawer.classList.add("open");
    if (e.target.closest("#drawerClose") || e.target.closest("#drawerOverlay")) drawer && drawer.classList.remove("open");
  });

  /* ---------------- Reveal on scroll ---------------- */
  function initReveal() {
    const els = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || !els.length) {
      els.forEach((el) => el.classList.add("in"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    els.forEach((el) => io.observe(el));
  }
  document.addEventListener("DOMContentLoaded", initReveal);

  /* ---------------- Helpers shared across pages ---------------- */
  const Settings = window.MAA ? window.MAA.getSettings() : {};

  function money(n) {
    return "₹" + Number(n).toLocaleString("en-IN");
  }

  function discountPct(mrp, price) {
    if (!mrp || mrp <= price) return 0;
    return Math.round(((mrp - price) / mrp) * 100);
  }

  function stockLabel(stock) {
    if (stock <= 0) return { cls: "out", text: "Out of Stock" };
    if (stock <= 5) return { cls: "low", text: `Only ${stock} left` };
    return { cls: "in", text: "In Stock" };
  }

  function waLink(product) {
    const phone = Settings.whatsapp || "919876543210";
    const text = product
      ? `Hi MAA Footwear, I'm interested in "${product.name}" (${window.MAA.CATEGORY_LABELS[product.category] || product.category}, Brand: ${product.brand}). Is it available?`
      : "Hi MAA Footwear, I have a question about a product.";
    return `https://wa.me/${phone}?text=${encodeURIComponent(text)}`;
  }

  function callLink() {
    return `tel:${(Settings.phone || "+919876543210").replace(/\s/g, "")}`;
  }

  function badgesFor(p) {
    let html = "";
    if (p.stock <= 0) html += `<span class="badge badge-out">Sold Out</span>`;
    if (p.newArrival) html += `<span class="badge badge-new">New</span>`;
    if (p.bestSeller) html += `<span class="badge badge-best">Best Seller</span>`;
    return html;
  }

  function productCard(p) {
    const off = discountPct(p.mrp, p.price);
    const stock = stockLabel(p.stock);
    const img1 = (p.images && p.images[0]) || "images/products/product-1-1.svg";
    const img2 = (p.images && p.images[1]) || img1;
    return `
    <article class="product-card">
      <a href="product.html?id=${p.id}" class="product-card__media" aria-label="${p.name}">
        ${off > 0 ? `<span class="product-card__tag">-${off}%</span>` : ""}
        <div class="product-card__badges">${badgesFor(p)}</div>
        <img class="main" src="${img1}" alt="${p.name} — ${p.brand}" loading="lazy" width="400" height="400">
        <img class="alt" src="${img2}" alt="" loading="lazy" width="400" height="400">
      </a>
      <div class="product-card__body">
        <div class="product-card__brand">${p.brand}</div>
        <h3 class="product-card__name"><a href="product.html?id=${p.id}">${p.name}</a></h3>
        <div class="product-card__meta">
          <span>${window.MAA.CATEGORY_LABELS[p.category] || p.category}</span>
          <span>${window.MAA.GENDER_LABELS[p.gender] || ""}</span>
          <span>${p.material}</span>
        </div>
        <div class="product-card__price">
          <span class="price-now">${money(p.price)}</span>
          ${p.mrp > p.price ? `<span class="price-mrp">${money(p.mrp)}</span><span class="price-off">${off}% OFF</span>` : ""}
        </div>
        <div class="stock-line ${stock.cls}">${stock.text}</div>
        <div class="product-card__actions">
          <a href="product.html?id=${p.id}" class="btn btn-outline btn-sm btn-block">View Details</a>
          <div class="row">
            <a href="${callLink()}" class="btn btn-call btn-sm">📞 Call Shop</a>
            <a href="${waLink(p)}" target="_blank" rel="noopener" class="btn btn-whatsapp btn-sm">WhatsApp</a>
          </div>
        </div>
      </div>
    </article>`;
  }

  window.MAAUI = { money, discountPct, stockLabel, waLink, callLink, badgesFor, productCard, Settings };
})();
