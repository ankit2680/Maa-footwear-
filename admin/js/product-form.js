/*! MAA Footwear — Admin: Add / Edit Product form logic */
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("productForm");
  if (!form) return;

  const params = new URLSearchParams(window.location.search);
  const editId = params.get("id");
  const isEdit = !!editId;
  const uploadedImages = []; // data URLs

  document.getElementById("formTitle").textContent = isEdit ? "Edit Product" : "Add New Product";
  document.getElementById("formSubtitle").textContent = isEdit
    ? "Update the details below and click Update Product to publish your changes."
    : "Fill in the product details below. It will appear on the public website immediately after you click Publish.";
  document.getElementById("submitBtn").textContent = isEdit ? "Update Product" : "Publish Product";

  // Build size chip picker (UK 1–11)
  const sizeWrap = document.getElementById("sizeChipPicker");
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11].forEach((s) => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = s;
    chip.dataset.size = s;
    chip.addEventListener("click", () => chip.classList.toggle("active"));
    sizeWrap.appendChild(chip);
  });

  // Image upload slots
  const imageGrid = document.getElementById("imageUploadGrid");
  function renderImageSlots() {
    imageGrid.innerHTML = "";
    for (let i = 0; i < 4; i++) {
      const slot = document.createElement("div");
      slot.className = "image-slot";
      if (uploadedImages[i]) {
        slot.innerHTML = `<img src="${uploadedImages[i]}" alt="Product image ${i + 1}">`;
      } else {
        slot.innerHTML = `<span>+ Add Image</span><input type="file" accept="image/*" data-slot="${i}">`;
      }
      imageGrid.appendChild(slot);
    }
  }
  renderImageSlots();

  imageGrid.addEventListener("change", function (e) {
    if (e.target.type !== "file") return;
    const slot = Number(e.target.dataset.slot);
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function (ev) {
      uploadedImages[slot] = ev.target.result;
      renderImageSlots();
    };
    reader.readAsDataURL(file);
  });

  // Prefill for edit mode
  if (isEdit) {
    const product = MAA.getProduct(editId);
    if (!product) {
      alert("Product not found.");
      window.location.href = "manage-products.html";
      return;
    }
    form.name.value = product.name;
    form.brand.value = product.brand;
    form.category.value = product.category;
    form.gender.value = product.gender;
    form.material.value = product.material;
    form.mrp.value = product.mrp;
    form.price.value = product.price;
    form.stock.value = product.stock;
    form.description.value = product.description;
    form.colors.value = (product.colors || []).join(", ");
    form.featured.checked = !!product.featured;
    form.bestSeller.checked = !!product.bestSeller;
    form.newArrival.checked = !!product.newArrival;

    (product.sizes || []).forEach((s) => {
      const chip = sizeWrap.querySelector(`[data-size="${s}"]`);
      if (chip) chip.classList.add("active");
    });
    (product.images || []).forEach((img, i) => {
      if (i < 4) uploadedImages[i] = img;
    });
    renderImageSlots();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const sizes = [...sizeWrap.querySelectorAll(".chip.active")].map((c) => Number(c.dataset.size));
    if (!sizes.length) {
      alert("Please select at least one available size.");
      return;
    }
    const images = uploadedImages.filter(Boolean);
    if (!images.length) {
      images.push("../images/products/product-1-1.svg"); // fallback placeholder
    }

    const mrp = Number(form.mrp.value);
    const price = Number(form.price.value);
    if (price > mrp) {
      alert("Selling price cannot be higher than MRP.");
      return;
    }

    const payload = {
      name: form.name.value.trim(),
      brand: form.brand.value.trim(),
      category: form.category.value,
      gender: form.gender.value,
      material: form.material.value.trim(),
      mrp,
      price,
      stock: Number(form.stock.value),
      description: form.description.value.trim(),
      colors: form.colors.value.split(",").map((c) => c.trim()).filter(Boolean),
      sizes,
      images,
      featured: form.featured.checked,
      bestSeller: form.bestSeller.checked,
      newArrival: form.newArrival.checked,
      rating: isEdit ? undefined : 4.3,
    };

    if (isEdit) {
      MAA.updateProduct(editId, payload);
    } else {
      MAA.addProduct(payload);
    }

    document.getElementById("successBanner").style.display = "flex";
    window.scrollTo({ top: 0, behavior: "smooth" });
    setTimeout(() => {
      window.location.href = "manage-products.html";
    }, 1200);
  });
});
