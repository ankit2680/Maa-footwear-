/*! MAA Footwear — Offers page logic */
document.addEventListener("DOMContentLoaded", function () {
  const grid = document.getElementById("productGrid");
  if (!grid) return;
  const deals = MAA.getProducts()
    .map((p) => Object.assign({}, p, { off: MAAUI.discountPct(p.mrp, p.price) }))
    .filter((p) => p.off > 0)
    .sort((a, b) => b.off - a.off);

  document.getElementById("resultCount").textContent = `${deals.length} product${deals.length !== 1 ? "s" : ""} on offer`;
  grid.innerHTML = deals.length
    ? deals.map(MAAUI.productCard).join("")
    : `<div class="empty-state"><h3>No active offers right now</h3><p>Check back soon — new deals are added regularly.</p></div>`;
});
