/*!
 * MAA Footwear — Demo Data Store
 * ---------------------------------------------------------
 * This file simulates the MySQL database using localStorage,
 * so the whole site (public pages + Admin Panel) works as a
 * live, editable demo without needing PHP/MySQL running.
 *
 * When you deploy the real backend, replace the calls in this
 * file with fetch() calls to php/api/products.php etc. Every
 * function keeps the same name and return shape so the rest of
 * the site does not need to change. See README.md.
 * ---------------------------------------------------------
 */
(function (global) {
  const LS_PRODUCTS = "maa_products";
  const LS_ENQUIRIES = "maa_enquiries";
  const LS_ADMIN = "maa_admin_session";
  const LS_SETTINGS = "maa_settings";

  const DEFAULT_SETTINGS = {
    storeName: "MAA Footwear",
    tagline: "Step Out In Style",
    phone: "+91 98765 43210",
    whatsapp: "919876543210",
    email: "hello@maafootwear.in",
    address: "Shop No. 14, Station Road Market, Kannauj, Uttar Pradesh 209725",
    hours: "Mon – Sun: 10:00 AM – 9:00 PM",
    mapEmbed: "https://www.google.com/maps?q=Kannauj,Uttar+Pradesh&output=embed",
    heroHeadline: "Footwear That Keeps Up With You",
    heroSub: "Browse the full MAA Footwear catalog online — sports shoes, sneakers, sandals & slippers for the whole family. Visit our store or message us to buy.",
  };

  function seedIfEmpty() {
    if (!localStorage.getItem(LS_PRODUCTS)) {
      localStorage.setItem(LS_PRODUCTS, JSON.stringify(global.MAA_SEED_PRODUCTS || []));
    }
    if (!localStorage.getItem(LS_ENQUIRIES)) {
      localStorage.setItem(LS_ENQUIRIES, JSON.stringify([]));
    }
    if (!localStorage.getItem(LS_SETTINGS)) {
      localStorage.setItem(LS_SETTINGS, JSON.stringify(DEFAULT_SETTINGS));
    }
  }

  function getProducts() {
    seedIfEmpty();
    try {
      return JSON.parse(localStorage.getItem(LS_PRODUCTS)) || [];
    } catch (e) {
      return [];
    }
  }

  function saveProducts(list) {
    localStorage.setItem(LS_PRODUCTS, JSON.stringify(list));
  }

  function getProduct(id) {
    return getProducts().find((p) => String(p.id) === String(id));
  }

  function nextId(list) {
    return list.reduce((max, p) => Math.max(max, Number(p.id) || 0), 0) + 1;
  }

  function addProduct(product) {
    const list = getProducts();
    product.id = nextId(list);
    list.unshift(product);
    saveProducts(list);
    return product;
  }

  function updateProduct(id, patch) {
    const list = getProducts();
    const idx = list.findIndex((p) => String(p.id) === String(id));
    if (idx === -1) return null;
    list[idx] = Object.assign({}, list[idx], patch);
    saveProducts(list);
    return list[idx];
  }

  function deleteProduct(id) {
    const list = getProducts().filter((p) => String(p.id) !== String(id));
    saveProducts(list);
  }

  function getSettings() {
    seedIfEmpty();
    try {
      return JSON.parse(localStorage.getItem(LS_SETTINGS)) || DEFAULT_SETTINGS;
    } catch (e) {
      return DEFAULT_SETTINGS;
    }
  }

  function saveSettings(settings) {
    localStorage.setItem(LS_SETTINGS, JSON.stringify(settings));
  }

  function getEnquiries() {
    seedIfEmpty();
    try {
      return JSON.parse(localStorage.getItem(LS_ENQUIRIES)) || [];
    } catch (e) {
      return [];
    }
  }

  function addEnquiry(enq) {
    const list = getEnquiries();
    enq.id = Date.now();
    enq.date = new Date().toISOString();
    enq.status = "new";
    list.unshift(enq);
    localStorage.setItem(LS_ENQUIRIES, JSON.stringify(list));
    return enq;
  }

  function updateEnquiry(id, patch) {
    const list = getEnquiries();
    const idx = list.findIndex((e) => String(e.id) === String(id));
    if (idx === -1) return;
    list[idx] = Object.assign({}, list[idx], patch);
    localStorage.setItem(LS_ENQUIRIES, JSON.stringify(list));
  }

  function deleteEnquiry(id) {
    const list = getEnquiries().filter((e) => String(e.id) !== String(id));
    localStorage.setItem(LS_ENQUIRIES, JSON.stringify(list));
  }

  /* ---------------- Admin auth (demo only) ----------------
     Default credentials: admin / maa@2026
     In production this MUST be replaced by php/api/auth.php
     with hashed passwords + server-side sessions. See README. */
  const DEFAULT_ADMIN = { username: "admin", password: "maa@2026" };

  function login(username, password) {
    if (username === DEFAULT_ADMIN.username && password === DEFAULT_ADMIN.password) {
      sessionStorage.setItem(LS_ADMIN, JSON.stringify({ username, at: Date.now() }));
      return true;
    }
    return false;
  }

  function isLoggedIn() {
    return !!sessionStorage.getItem(LS_ADMIN);
  }

  function logout() {
    sessionStorage.removeItem(LS_ADMIN);
  }

  function requireAuth() {
    if (!isLoggedIn()) {
      window.location.href = "login.html";
    }
  }

  const CATEGORY_LABELS = {
    "sports-shoes": "Sports Shoes",
    sneakers: "Sneakers",
    sandals: "Sandals",
    slippers: "Slippers",
  };

  const GENDER_LABELS = { men: "Men", women: "Women", kids: "Kids" };

  global.MAA = {
    getProducts,
    saveProducts,
    getProduct,
    addProduct,
    updateProduct,
    deleteProduct,
    getSettings,
    saveSettings,
    getEnquiries,
    addEnquiry,
    updateEnquiry,
    deleteEnquiry,
    login,
    isLoggedIn,
    logout,
    requireAuth,
    CATEGORY_LABELS,
    GENDER_LABELS,
  };
})(window);
