/*! MAA Footwear — Admin dashboard stats */
document.addEventListener("DOMContentLoaded", function () {
  const products = MAA.getProducts();
  const enquiries = MAA.getEnquiries();

  const totalStock = products.reduce((s, p) => s + Number(p.stock || 0), 0);
  const lowStock = products.filter((p) => p.stock > 0 && p.stock <= 5).length;
  const outStock = products.filter((p) => p.stock <= 0).length;
  const newEnquiries = enquiries.filter((e) => e.status === "new").length;

  document.getElementById("statTotalProducts").textContent = products.length;
  document.getElementById("statTotalStock").textContent = totalStock;
  document.getElementById("statLowStock").textContent = lowStock;
  document.getElementById("statOutStock").textContent = outStock;
  document.getElementById("statEnquiries").textContent = enquiries.length;
  document.getElementById("statNewEnquiries").textContent = newEnquiries;
  document.getElementById("statFeatured").textContent = products.filter((p) => p.featured).length;
  document.getElementById("statCategories").textContent = new Set(products.map((p) => p.category)).size;

  // Recent products
  const recentBody = document.getElementById("recentProductsBody");
  const recent = [...products].sort((a, b) => b.id - a.id).slice(0, 6);
  recentBody.innerHTML = recent
    .map((p) => {
      const stock = MAAUI.stockLabel(p.stock);
      return `<tr>
        <td><img src="../${p.images[0]}" alt=""></td>
        <td>${p.name}<br><span style="color:var(--muted);font-size:.78rem;">${p.brand}</span></td>
        <td>${MAA.CATEGORY_LABELS[p.category] || p.category}</td>
        <td>${MAAUI.money(p.price)}</td>
        <td><span class="status-pill ${stock.cls}">${stock.text}</span></td>
      </tr>`;
    })
    .join("");

  // Recent enquiries
  const enqBody = document.getElementById("recentEnquiriesBody");
  const recentEnq = enquiries.slice(0, 6);
  enqBody.innerHTML = recentEnq.length
    ? recentEnq
        .map(
          (e) => `<tr>
        <td>${e.name}</td>
        <td>${e.phone}</td>
        <td>${e.productName || "General"}</td>
        <td>${new Date(e.date).toLocaleDateString("en-IN")}</td>
        <td><span class="status-pill ${e.status === "new" ? "new" : "read"}">${e.status}</span></td>
      </tr>`
        )
        .join("")
    : `<tr><td colspan="5" style="text-align:center;color:var(--muted);padding:20px;">No enquiries yet.</td></tr>`;
});
