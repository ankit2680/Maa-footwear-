/*! MAA Footwear — homepage product rails */
document.addEventListener("DOMContentLoaded", function () {
  const products = MAA.getProducts();

  function render(sel, list, emptyMsg) {
    const el = document.querySelector(sel);
    if (!el) return;
    if (!list.length) {
      el.innerHTML = `<p class="empty-state">${emptyMsg}</p>`;
      return;
    }
    el.innerHTML = list.map(MAAUI.productCard).join("");
  }

  render("#featuredProducts", products.filter((p) => p.featured).slice(0, 8), "Featured products will appear here once added in the Admin Panel.");
  render("#latestArrivals", products.filter((p) => p.newArrival).slice(0, 8), "New arrivals will appear here soon.");
  render("#bestSellers", products.filter((p) => p.bestSeller).slice(0, 8), "Best sellers will appear here soon.");
  render("#newCollection", [...products].sort((a, b) => b.id - a.id).slice(0, 8), "Collection coming soon.");

  const dealsEl = document.querySelector("#seasonalOffers");
  if (dealsEl) {
    const deals = [...products]
      .map((p) => Object.assign({}, p, { off: MAAUI.discountPct(p.mrp, p.price) }))
      .filter((p) => p.off >= 25)
      .sort((a, b) => b.off - a.off)
      .slice(0, 4);
    dealsEl.innerHTML = deals.length
      ? deals.map(MAAUI.productCard).join("")
      : `<p class="empty-state">Check back soon for seasonal deals.</p>`;
  }
});
