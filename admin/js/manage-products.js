/*! MAA Footwear — Admin: Manage Products */
document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.getElementById("productsBody");
  const searchInput = document.getElementById("adminSearch");
  const categorySelect = document.getElementById("adminCategoryFilter");
  const countEl = document.getElementById("adminResultCount");

  // populate category filter
  Object.entries(MAA.CATEGORY_LABELS).forEach(([val, label]) => {
    const opt = document.createElement("option");
    opt.value = val;
    opt.textContent = label;
    categorySelect.appendChild(opt);
  });

  function render() {
    const q = (searchInput.value || "").toLowerCase();
    const cat = categorySelect.value;
    let list = MAA.getProducts();
    if (cat) list = list.filter((p) => p.category === cat);
    if (q) list = list.filter((p) => `${p.name} ${p.brand}`.toLowerCase().includes(q));
    list = list.sort((a, b) => b.id - a.id);

    countEl.textContent = `${list.length} product${list.length !== 1 ? "s" : ""}`;

    tbody.innerHTML = list.length
      ? list
          .map((p) => {
            const stock = MAAUI.stockLabel(p.stock);
            return `<tr data-id="${p.id}">
              <td><img src="../${p.images[0]}" alt=""></td>
              <td><b>${p.name}</b><br><span style="color:var(--muted);font-size:.78rem;">${p.brand} · ${p.material}</span></td>
              <td>${MAA.CATEGORY_LABELS[p.category] || p.category}<br><span style="color:var(--muted);font-size:.78rem;">${MAA.GENDER_LABELS[p.gender] || ""}</span></td>
              <td>${MAAUI.money(p.price)}<br><span style="color:var(--muted);font-size:.78rem;text-decoration:line-through;">${MAAUI.money(p.mrp)}</span></td>
              <td>
                <input type="number" min="0" class="stock-input" value="${p.stock}" style="width:64px;padding:5px 7px;border:1px solid var(--border);border-radius:4px;background:var(--bg);color:var(--text);">
                <div><span class="status-pill ${stock.cls}">${stock.text}</span></div>
              </td>
              <td>
                <label style="display:flex;gap:5px;align-items:center;font-size:.78rem;"><input type="checkbox" class="toggle-featured" ${p.featured ? "checked" : ""}> Featured</label>
                <label style="display:flex;gap:5px;align-items:center;font-size:.78rem;"><input type="checkbox" class="toggle-best" ${p.bestSeller ? "checked" : ""}> Best Seller</label>
                <label style="display:flex;gap:5px;align-items:center;font-size:.78rem;"><input type="checkbox" class="toggle-new" ${p.newArrival ? "checked" : ""}> New Arrival</label>
              </td>
              <td class="table-actions">
                <a class="btn btn-ghost btn-sm" href="edit-product.html?id=${p.id}">Edit</a>
                <button class="btn btn-danger btn-sm delete-btn">Delete</button>
              </td>
            </tr>`;
          })
          .join("")
      : `<tr><td colspan="7" style="text-align:center;padding:30px;color:var(--muted);">No products found.</td></tr>`;
  }

  searchInput.addEventListener("input", render);
  categorySelect.addEventListener("change", render);

  tbody.addEventListener("click", function (e) {
    const row = e.target.closest("tr[data-id]");
    if (!row) return;
    const id = row.dataset.id;

    if (e.target.classList.contains("delete-btn")) {
      if (confirm("Delete this product? This cannot be undone.")) {
        MAA.deleteProduct(id);
        showToast("Product deleted");
        render();
      }
    }
  });

  tbody.addEventListener("change", function (e) {
    const row = e.target.closest("tr[data-id]");
    if (!row) return;
    const id = row.dataset.id;

    if (e.target.classList.contains("stock-input")) {
      MAA.updateProduct(id, { stock: Number(e.target.value) });
      showToast("Stock updated");
      render();
    }
    if (e.target.classList.contains("toggle-featured")) {
      MAA.updateProduct(id, { featured: e.target.checked });
      showToast("Homepage featured status updated");
    }
    if (e.target.classList.contains("toggle-best")) {
      MAA.updateProduct(id, { bestSeller: e.target.checked });
      showToast("Best seller status updated");
    }
    if (e.target.classList.contains("toggle-new")) {
      MAA.updateProduct(id, { newArrival: e.target.checked });
      showToast("New arrival status updated");
    }
  });

  render();
});

function showToast(msg) {
  document.querySelectorAll(".toast").forEach((t) => t.remove());
  const el = document.createElement("div");
  el.className = "toast";
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2500);
}
