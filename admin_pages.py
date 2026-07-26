#!/usr/bin/env python3
"""Builds every page under /admin using the same design tokens as the public site."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ADMIN_DIR = os.path.join(ROOT, "admin")

SIDEBAR_LINKS = [
    ("dashboard.html", "📊", "Dashboard"),
    ("manage-products.html", "📦", "Manage Products"),
    ("add-product.html", "➕", "Add New Product"),
    ("enquiries.html", "✉️", "Customer Enquiries"),
]


def admin_head(title, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | MAA Footwear Admin</title>
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="../images/site/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="../css/style.css">
<link rel="stylesheet" href="css/admin.css">
{extra_css}
</head>
<body>
"""


def admin_sidebar(active):
    links = ""
    for href, icon, label in SIDEBAR_LINKS:
        cls = "active" if href == active else ""
        links += f'<a href="{href}" class="{cls}">{icon} {label}</a>'
    return f"""
<aside class="admin-sidebar">
  <a href="dashboard.html" class="brand">
    <span class="brand__mark">M</span>
    <span class="brand__name">MAA <span>Admin</span></span>
  </a>
  <nav class="admin-nav">
    <div class="divider-label">Catalog</div>
    {links}
    <div class="divider-label">Shortcuts</div>
    <a href="../index.html" target="_blank">🌐 View Website</a>
    <a href="#" id="logoutBtn">🚪 Logout</a>
  </nav>
</aside>
"""


def admin_topbar(title, subtitle=""):
    return f"""
<div class="admin-topbar">
  <div>
    <h1>{title}</h1>
    {f'<p style="margin:2px 0 0;font-size:.85rem;">{subtitle}</p>' if subtitle else ""}
  </div>
  <div class="admin-user">
    <button class="icon-btn" id="themeToggle" aria-label="Toggle dark mode">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    </button>
    <div class="admin-user__avatar">A</div>
    <div>
      <div style="font-weight:700;font-size:.9rem;">Admin</div>
      <div style="font-size:.75rem;color:var(--muted);">Website Administrator</div>
    </div>
  </div>
</div>
"""


def admin_wrap(active, title, subtitle, content, extra_scripts=""):
    html = admin_head(title)
    html += '<div class="admin-shell">'
    html += admin_sidebar(active)
    html += '<main class="admin-main">'
    html += admin_topbar(title, subtitle)
    html += f'<div class="admin-content">{content}</div>'
    html += "</main></div>"
    html += """
<script src="../js/products-seed.js"></script>
<script src="../js/store.js"></script>
<script src="../js/main.js"></script>
<script src="js/auth-guard.js"></script>
"""
    html += extra_scripts
    html += "\n</body>\n</html>\n"
    return html


def write_admin(path, html):
    full = os.path.join(ADMIN_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote admin/" + path)


# =========================================================
# LOGIN PAGE (no sidebar / no auth guard)
# =========================================================
def build_login():
    content = f"""
<div class="login-shell">
  <div class="login-card">
    <a href="../index.html" class="brand"><span class="brand__mark">M</span><span class="brand__name" style="color:var(--ink);">MAA <span>Footwear</span></span></a>
    <h1>Admin Login</h1>
    <p class="sub" style="text-align:center;color:var(--muted);">Sign in to manage products, offers &amp; enquiries.</p>
    <form id="loginForm">
      <div class="field"><label for="username">Username</label><input id="username" name="username" required autocomplete="username"></div>
      <div class="field"><label for="password">Password</label><input id="password" name="password" type="password" required autocomplete="current-password"></div>
      <p id="loginError" style="display:none;color:var(--danger);font-size:.85rem;margin:-6px 0 14px;">Incorrect username or password.</p>
      <button type="submit" class="btn btn-primary btn-block">Login</button>
    </form>
    <div class="login-hint">
      <b>Demo credentials</b><br>Username: <code>admin</code> &nbsp; Password: <code>maa@2026</code><br>
      Change these in <code>js/store.js</code> before going live, and replace with the real PHP session login in <code>php/api/auth.php</code>.
    </div>
  </div>
</div>
"""
    html = admin_head("Admin Login")
    html += content
    html += """
<script src="../js/products-seed.js"></script>
<script src="../js/store.js"></script>
<script src="../js/main.js"></script>
<script src="js/login.js"></script>
</body>
</html>
"""
    write_admin("login.html", html)


# =========================================================
# DASHBOARD
# =========================================================
def build_dashboard():
    content = """
<div class="stat-cards">
  <div class="admin-card stat-card"><div class="label">Total Products</div><div class="value" id="statTotalProducts">0</div><div class="trend up">Live on website</div></div>
  <div class="admin-card stat-card"><div class="label">Total Units In Stock</div><div class="value" id="statTotalStock">0</div><div class="trend up">Across all products</div></div>
  <div class="admin-card stat-card"><div class="label">Low Stock (≤5)</div><div class="value" id="statLowStock">0</div><div class="trend warn">Needs restocking</div></div>
  <div class="admin-card stat-card"><div class="label">Out of Stock</div><div class="value" id="statOutStock">0</div><div class="trend warn">Hidden from "in stock" filter</div></div>
  <div class="admin-card stat-card"><div class="label">Customer Enquiries</div><div class="value" id="statEnquiries">0</div><div class="trend up"><span id="statNewEnquiries">0</span> new</div></div>
  <div class="admin-card stat-card"><div class="label">Featured Products</div><div class="value" id="statFeatured">0</div><div class="trend up">Shown on homepage</div></div>
  <div class="admin-card stat-card"><div class="label">Categories</div><div class="value" id="statCategories">0</div><div class="trend up">Active categories</div></div>
  <div class="admin-card stat-card"><div class="label">Quick Action</div><div style="margin-top:8px;"><a href="add-product.html" class="btn btn-amber btn-block btn-sm">+ Add Product</a></div></div>
</div>

<div class="admin-card">
  <div class="admin-card__head">
    <h3 style="margin:0;">Recently Added Products</h3>
    <a href="manage-products.html" class="btn btn-ghost btn-sm">Manage All →</a>
  </div>
  <div style="overflow-x:auto;">
    <table class="admin-table">
      <thead><tr><th></th><th>Product</th><th>Category</th><th>Price</th><th>Stock</th></tr></thead>
      <tbody id="recentProductsBody"></tbody>
    </table>
  </div>
</div>

<div class="admin-card">
  <div class="admin-card__head">
    <h3 style="margin:0;">Recent Customer Enquiries</h3>
    <a href="enquiries.html" class="btn btn-ghost btn-sm">View All →</a>
  </div>
  <div style="overflow-x:auto;">
    <table class="admin-table">
      <thead><tr><th>Name</th><th>Phone</th><th>Product</th><th>Date</th><th>Status</th></tr></thead>
      <tbody id="recentEnquiriesBody"></tbody>
    </table>
  </div>
</div>
"""
    html = admin_wrap("dashboard.html", "Dashboard", "An overview of your catalog and customer activity.", content, '<script src="js/dashboard.js"></script>')
    write_admin("dashboard.html", html)


# =========================================================
# MANAGE PRODUCTS
# =========================================================
def build_manage_products():
    content = """
<div class="admin-card">
  <div class="admin-card__head">
    <h3 style="margin:0;">All Products</h3>
    <a href="add-product.html" class="btn btn-amber btn-sm">+ Add New Product</a>
  </div>
  <div class="toolbar" style="margin-bottom:16px;">
    <input type="search" id="adminSearch" placeholder="Search by name or brand…" style="flex:1;min-width:220px;padding:10px 12px;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--text);">
    <select id="adminCategoryFilter" style="padding:9px 12px;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--text);">
      <option value="">All Categories</option>
    </select>
    <span class="result-count" id="adminResultCount"></span>
  </div>
  <div style="overflow-x:auto;">
    <table class="admin-table">
      <thead><tr><th></th><th>Product</th><th>Category</th><th>Price</th><th>Stock</th><th>Homepage Tags</th><th>Actions</th></tr></thead>
      <tbody id="productsBody"></tbody>
    </table>
  </div>
</div>
"""
    html = admin_wrap("manage-products.html", "Manage Products", "Search, filter, edit stock and control what appears on the homepage.", content, '<script src="js/manage-products.js"></script>')
    write_admin("manage-products.html", html)


# =========================================================
# ADD / EDIT PRODUCT FORM (shared markup)
# =========================================================
def product_form_content():
    return """
<div class="admin-card" id="successBanner" style="display:none;background:#E4EEE1;border-color:var(--success);align-items:center;gap:10px;">
  ✅ <span>Product published! Redirecting to Manage Products…</span>
</div>
<div class="admin-card">
  <h3 id="formTitle" style="margin-top:0;">Add New Product</h3>
  <p id="formSubtitle" style="color:var(--muted);"></p>
  <form id="productForm">
    <h4 style="text-transform:uppercase;font-size:.8rem;letter-spacing:1px;color:var(--muted);">Product Images</h4>
    <div class="image-upload-grid" id="imageUploadGrid"></div>
    <p><small>Upload up to 4 images. First image is used as the primary thumbnail.</small></p>

    <div class="divider"></div>

    <div class="form-grid">
      <div class="field"><label for="pName">Product Name</label><input id="pName" name="name" required placeholder="e.g. Air Stride Runner"></div>
      <div class="field"><label for="pBrand">Brand</label><input id="pBrand" name="brand" required placeholder="e.g. Nova Sport"></div>
      <div class="field">
        <label for="pCategory">Category</label>
        <select id="pCategory" name="category" required>
          <option value="sports-shoes">Sports Shoes</option>
          <option value="sneakers">Sneakers</option>
          <option value="sandals">Sandals</option>
          <option value="slippers">Slippers</option>
        </select>
      </div>
      <div class="field">
        <label for="pGender">Collection</label>
        <select id="pGender" name="gender" required>
          <option value="men">Men</option>
          <option value="women">Women</option>
          <option value="kids">Kids</option>
        </select>
      </div>
      <div class="field"><label for="pMaterial">Material</label><input id="pMaterial" name="material" required placeholder="e.g. Mesh & EVA Sole"></div>
      <div class="field"><label for="pColors">Available Colours</label><input id="pColors" name="colors" required placeholder="e.g. Black, Amber (comma separated)"></div>
    </div>

    <h4 style="text-transform:uppercase;font-size:.8rem;letter-spacing:1px;color:var(--muted);">Available Sizes (UK)</h4>
    <div class="chip-group" id="sizeChipPicker" style="margin-bottom:18px;"></div>

    <div class="form-grid">
      <div class="field"><label for="pMrp">MRP (₹)</label><input id="pMrp" name="mrp" type="number" min="0" required></div>
      <div class="field"><label for="pPrice">Selling Price (₹)</label><input id="pPrice" name="price" type="number" min="0" required></div>
      <div class="field"><label for="pStock">Stock Quantity</label><input id="pStock" name="stock" type="number" min="0" required></div>
    </div>

    <div class="field">
      <label for="pDescription">Product Description</label>
      <textarea id="pDescription" name="description" rows="4" required placeholder="Short, honest description of the product…"></textarea>
    </div>

    <div class="divider"></div>

    <h4 style="text-transform:uppercase;font-size:.8rem;letter-spacing:1px;color:var(--muted);">Homepage Visibility</h4>
    <div class="toggle-row">
      <span>Featured Product <br><small style="color:var(--muted);">Shows in the homepage "Featured Products" section</small></span>
      <label class="switch"><input type="checkbox" name="featured"><span class="slider"></span></label>
    </div>
    <div class="toggle-row">
      <span>Best Seller <br><small style="color:var(--muted);">Shows in the homepage "Best Sellers" section</small></span>
      <label class="switch"><input type="checkbox" name="bestSeller"><span class="slider"></span></label>
    </div>
    <div class="toggle-row" style="border-bottom:none;">
      <span>New Arrival <br><small style="color:var(--muted);">Shows in the homepage "Latest Arrivals" section</small></span>
      <label class="switch"><input type="checkbox" name="newArrival"><span class="slider"></span></label>
    </div>

    <div class="divider"></div>
    <div style="display:flex;gap:12px;">
      <button type="submit" class="btn btn-primary" id="submitBtn">Publish Product</button>
      <a href="manage-products.html" class="btn btn-ghost">Cancel</a>
    </div>
  </form>
</div>
"""


def build_add_product():
    html = admin_wrap("add-product.html", "Add New Product", "New products go live on the public website immediately after publishing.", product_form_content(), '<script src="js/product-form.js"></script>')
    write_admin("add-product.html", html)


def build_edit_product():
    html = admin_wrap("manage-products.html", "Edit Product", "Update product details, images, price or stock.", product_form_content(), '<script src="js/product-form.js"></script>')
    write_admin("edit-product.html", html)


# =========================================================
# CUSTOMER ENQUIRIES
# =========================================================
def build_enquiries():
    content = """
<div class="admin-card">
  <div class="admin-card__head">
    <h3 style="margin:0;">Customer Enquiries</h3>
    <span class="result-count" id="enqCount"></span>
  </div>
  <p style="color:var(--muted);">Enquiries submitted from the Product Details page and Contact page appear here.</p>
  <div style="overflow-x:auto;">
    <table class="admin-table">
      <thead><tr><th>Date</th><th>Name</th><th>Phone</th><th>Product</th><th>Message</th><th>Status</th><th>Actions</th></tr></thead>
      <tbody id="enquiriesBody"></tbody>
    </table>
  </div>
</div>
"""
    html = admin_wrap("enquiries.html", "Customer Enquiries", "Follow up with customers who asked about a product or the store.", content, '<script src="js/enquiries.js"></script>')
    write_admin("enquiries.html", html)


if __name__ == "__main__":
    build_login()
    build_dashboard()
    build_manage_products()
    build_add_product()
    build_edit_product()
    build_enquiries()
