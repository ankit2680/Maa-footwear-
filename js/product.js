/*! MAA Footwear — Product Details page logic */
document.addEventListener("DOMContentLoaded", function () {
  const root = document.getElementById("productRoot");
  if (!root) return;

  const params = new URLSearchParams(window.location.search);
  const id = params.get("id");
  const product = MAA.getProduct(id);

  if (!product) {
    root.innerHTML = `<div class="empty-state">
      <h3>Product not found</h3>
      <p>This product may have been removed or is no longer available.</p>
      <a href="shop.html" class="btn btn-primary">Back to Shop</a>
    </div>`;
    return;
  }

  document.title = `${product.name} — ${product.brand} | MAA Footwear`;
  const metaDesc = document.querySelector('meta[name="description"]');
  if (metaDesc) metaDesc.setAttribute("content", product.description.slice(0, 155));

  const off = MAAUI.discountPct(product.mrp, product.price);
  const stock = MAAUI.stockLabel(product.stock);
  const images = product.images && product.images.length ? product.images : ["images/products/product-1-1.svg"];

  root.innerHTML = `
    <div class="pdp-grid">
      <div class="pdp-gallery">
        <div class="pdp-gallery__main" id="zoomBox">
          <img id="mainImg" src="${images[0]}" alt="${product.name}">
          ${off > 0 ? `<span class="product-card__tag">-${off}%</span>` : ""}
        </div>
        <div class="pdp-gallery__thumbs">
          ${images
            .map(
              (img, i) =>
                `<button class="pdp-thumb ${i === 0 ? "active" : ""}" data-src="${img}"><img src="${img}" alt="${product.name} view ${i + 1}"></button>`
            )
            .join("")}
        </div>
        <p class="pdp-hint">🔍 Hover the main image to zoom</p>
      </div>
      <div class="pdp-info">
        <div class="product-card__brand">${product.brand}</div>
        <h1>${product.name}</h1>
        <div class="product-card__meta" style="margin-bottom:10px;">
          <span>${MAA.CATEGORY_LABELS[product.category] || product.category}</span>
          <span>${MAA.GENDER_LABELS[product.gender] || ""}</span>
          ${MAAUI.badgesFor(product)}
        </div>
        <div class="product-card__price" style="font-size:1.1em;">
          <span class="price-now">${MAAUI.money(product.price)}</span>
          ${product.mrp > product.price ? `<span class="price-mrp">${MAAUI.money(product.mrp)}</span><span class="price-off">${off}% OFF</span>` : ""}
        </div>
        <div class="stock-line ${stock.cls}" style="margin-bottom:14px;">${stock.text}</div>
        <p>${product.description}</p>

        <div class="pdp-option">
          <h4>Select Size (UK)</h4>
          <div class="chip-group" id="sizeChips">
            ${product.sizes.map((s) => `<span class="chip" data-size="${s}">${s}</span>`).join("")}
          </div>
        </div>
        <div class="pdp-option">
          <h4>Select Colour</h4>
          <div class="chip-group" id="colorChips">
            ${product.colors.map((c) => `<span class="chip" data-color="${c}">${c}</span>`).join("")}
          </div>
        </div>

        <table class="spec-table">
          <tr><th>Material</th><td>${product.material}</td></tr>
          <tr><th>Available Sizes</th><td>${product.sizes.join(", ")}</td></tr>
          <tr><th>Available Colours</th><td>${product.colors.join(", ")}</td></tr>
          <tr><th>Brand</th><td>${product.brand}</td></tr>
          <tr><th>Category</th><td>${MAA.CATEGORY_LABELS[product.category] || product.category}</td></tr>
        </table>

        <div class="pdp-actions">
          <a href="${MAAUI.callLink()}" class="btn btn-call">📞 Call Shop</a>
          <a id="pdpWaLink" href="${MAAUI.waLink(product)}" target="_blank" rel="noopener" class="btn btn-whatsapp">WhatsApp Inquiry</a>
        </div>
      </div>
    </div>
  `;

  // Thumb switching
  root.addEventListener("click", (e) => {
    const thumb = e.target.closest(".pdp-thumb");
    if (thumb) {
      root.querySelectorAll(".pdp-thumb").forEach((t) => t.classList.remove("active"));
      thumb.classList.add("active");
      document.getElementById("mainImg").src = thumb.dataset.src;
    }
    const chip = e.target.closest("#sizeChips .chip, #colorChips .chip");
    if (chip) {
      chip.parentElement.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      updateWaLink();
    }
  });

  function updateWaLink() {
    const size = root.querySelector("#sizeChips .chip.active");
    const color = root.querySelector("#colorChips .chip.active");
    let text = `Hi MAA Footwear, I'm interested in "${product.name}" (${product.brand}).`;
    if (size) text += ` Size: UK ${size.dataset.size}.`;
    if (color) text += ` Colour: ${color.dataset.color}.`;
    text += " Is it available?";
    document.getElementById("pdpWaLink").href = `https://wa.me/${MAAUI.Settings.whatsapp || "919876543210"}?text=${encodeURIComponent(text)}`;
  }

  // Simple zoom on hover
  const zoomBox = document.getElementById("zoomBox");
  const mainImg = document.getElementById("mainImg");
  zoomBox.addEventListener("mousemove", (e) => {
    const rect = zoomBox.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    mainImg.style.transformOrigin = `${x}% ${y}%`;
    mainImg.style.transform = "scale(1.9)";
  });
  zoomBox.addEventListener("mouseleave", () => {
    mainImg.style.transform = "scale(1)";
  });

  // Related products
  const related = MAA.getProducts()
    .filter((p) => p.id !== product.id && (p.category === product.category || p.gender === product.gender))
    .slice(0, 4);
  const relatedEl = document.getElementById("relatedProducts");
  if (relatedEl) {
    relatedEl.innerHTML = related.length
      ? related.map(MAAUI.productCard).join("")
      : `<p class="empty-state">No related products yet.</p>`;
  }

  // Enquiry form
  const form = document.getElementById("enquiryForm");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      MAA.addEnquiry({
        name: data.name,
        phone: data.phone,
        message: data.message,
        productId: product.id,
        productName: product.name,
      });
      form.innerHTML = `<div class="empty-state"><h3>Thank you, ${data.name.split(" ")[0]}!</h3><p>Your enquiry about <b>${product.name}</b> has been received. Our team will contact you shortly, or reach us directly on WhatsApp.</p></div>`;
    });
  }
});
