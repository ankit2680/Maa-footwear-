/*! MAA Footwear — Shop / category listing logic */
document.addEventListener("DOMContentLoaded", function () {
  const grid = document.getElementById("productGrid");
  if (!grid) return;

  const params = new URLSearchParams(window.location.search);
  const body = document.body;
  const presetCategory = body.dataset.presetCategory || "";
  const presetGender = body.dataset.presetGender || "";

  const all = MAA.getProducts();
  const brands = [...new Set(all.map((p) => p.brand))].sort();
  const maxPrice = Math.max(...all.map((p) => p.mrp), 5000);

  const state = {
    q: params.get("q") || "",
    categories: presetCategory ? [presetCategory] : params.getAll("category"),
    genders: presetGender ? [presetGender] : params.getAll("gender"),
    brands: params.getAll("brand"),
    sizes: params.getAll("size").map(Number),
    maxPrice: Number(params.get("max")) || maxPrice,
    sort: params.get("sort") || "popularity",
  };

  /* ---------------- Build filter sidebar ---------------- */
  const filterRoot = document.getElementById("filterRoot");
  if (filterRoot) {
    const catBox = !presetCategory
      ? `<div class="filter-group" id="catFilters">
          <h4>Category</h4>
          ${Object.entries(MAA.CATEGORY_LABELS)
            .map(
              ([val, label]) => `
            <label><input type="checkbox" value="${val}" ${state.categories.includes(val) ? "checked" : ""}> ${label}</label>`
            )
            .join("")}
        </div>`
      : "";

    const genderBox = !presetGender
      ? `<div class="filter-group" id="genderFilters">
          <h4>Gender</h4>
          ${Object.entries(MAA.GENDER_LABELS)
            .map(
              ([val, label]) => `
            <label><input type="checkbox" value="${val}" ${state.genders.includes(val) ? "checked" : ""}> ${label}</label>`
            )
            .join("")}
        </div>`
      : "";

    filterRoot.innerHTML = `
      ${catBox}
      ${genderBox}
      <div class="filter-group" id="brandFilters">
        <h4>Brand</h4>
        ${brands
          .map(
            (b) => `<label><input type="checkbox" value="${b}" ${state.brands.includes(b) ? "checked" : ""}> ${b}</label>`
          )
          .join("")}
      </div>
      <div class="filter-group" id="sizeFilters">
        <h4>Size (UK)</h4>
        <div class="chip-group">
          ${[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            .map((s) => `<span class="chip ${state.sizes.includes(s) ? "active" : ""}" data-size="${s}">${s}</span>`)
            .join("")}
        </div>
      </div>
      <div class="filter-group">
        <h4>Max Price</h4>
        <div class="range-row">
          <input type="range" id="priceRange" min="0" max="${maxPrice}" step="100" value="${state.maxPrice}">
        </div>
        <div class="range-row"><span id="priceRangeLabel">${MAAUI.money(state.maxPrice)}</span></div>
      </div>
      <button class="btn btn-ghost btn-block btn-sm" id="clearFilters">Clear Filters</button>
    `;
  }

  function readCheckedValues(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return [];
    return [...el.querySelectorAll("input:checked")].map((i) => i.value);
  }

  function applyFilters() {
    if (!presetCategory) state.categories = readCheckedValues("catFilters");
    if (!presetGender) state.genders = readCheckedValues("genderFilters");
    state.brands = readCheckedValues("brandFilters");
    render();
  }

  filterRoot &&
    filterRoot.addEventListener("change", (e) => {
      if (e.target.id === "priceRange") {
        state.maxPrice = Number(e.target.value);
        document.getElementById("priceRangeLabel").textContent = MAAUI.money(state.maxPrice);
        render();
        return;
      }
      applyFilters();
    });

  filterRoot &&
    filterRoot.addEventListener("click", (e) => {
      const chip = e.target.closest(".chip");
      if (chip) {
        const size = Number(chip.dataset.size);
        const idx = state.sizes.indexOf(size);
        if (idx > -1) state.sizes.splice(idx, 1);
        else state.sizes.push(size);
        chip.classList.toggle("active");
        render();
      }
      if (e.target.id === "clearFilters") {
        state.brands = [];
        state.sizes = [];
        state.maxPrice = maxPrice;
        if (!presetCategory) state.categories = [];
        if (!presetGender) state.genders = [];
        state.q = "";
        const searchBox = document.getElementById("shopSearch");
        if (searchBox) searchBox.value = "";
        buildFiltersAgain();
      }
    });

  function buildFiltersAgain() {
    // simplest: reload without query params but keep preset page
    window.location.href = window.location.pathname;
  }

  /* ---------------- Toolbar: search + sort ---------------- */
  const searchBox = document.getElementById("shopSearch");
  if (searchBox) {
    searchBox.value = state.q;
    searchBox.addEventListener("input", () => {
      state.q = searchBox.value;
      render();
    });
  }
  const sortSelect = document.getElementById("sortSelect");
  if (sortSelect) {
    sortSelect.value = state.sort;
    sortSelect.addEventListener("change", () => {
      state.sort = sortSelect.value;
      render();
    });
  }

  /* ---------------- Filtering + rendering ---------------- */
  function matches(p) {
    if (state.categories.length && !state.categories.includes(p.category)) return false;
    if (state.genders.length && !state.genders.includes(p.gender)) return false;
    if (state.brands.length && !state.brands.includes(p.brand)) return false;
    if (state.sizes.length && !state.sizes.some((s) => p.sizes.includes(s))) return false;
    if (p.price > state.maxPrice) return false;
    if (state.q) {
      const hay = `${p.name} ${p.brand} ${p.material} ${p.category}`.toLowerCase();
      if (!hay.includes(state.q.toLowerCase())) return false;
    }
    return true;
  }

  function sortList(list) {
    const arr = [...list];
    switch (state.sort) {
      case "price-asc":
        return arr.sort((a, b) => a.price - b.price);
      case "price-desc":
        return arr.sort((a, b) => b.price - a.price);
      case "discount":
        return arr.sort((a, b) => MAAUI.discountPct(b.mrp, b.price) - MAAUI.discountPct(a.mrp, a.price));
      case "newest":
        return arr.sort((a, b) => b.id - a.id);
      default:
        return arr.sort((a, b) => (b.bestSeller === true) - (a.bestSeller === true) || b.rating - a.rating);
    }
  }

  function render() {
    const filtered = sortList(all.filter(matches));
    const countEl = document.getElementById("resultCount");
    if (countEl) countEl.textContent = `${filtered.length} product${filtered.length !== 1 ? "s" : ""} found`;
    grid.innerHTML = filtered.length
      ? filtered.map(MAAUI.productCard).join("")
      : `<div class="empty-state"><h3>No products match your filters</h3><p>Try clearing some filters or search with a different keyword.</p></div>`;
  }

  render();
});
