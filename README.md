# MAA Footwear — Website & Admin Panel

A complete, responsive footwear catalog website for **MAA Footwear** (Kannauj, UP). Customers browse products online; the shop owner sends you (the developer) new stock, and you publish it through the Admin Panel.

This package ships as a **fully working demo** (HTML/CSS/JS, data stored in the browser via `localStorage`) plus the **complete PHP + MySQL backend code** so you can go live on real hosting whenever you're ready. Both versions share the same design, pages, and admin UI.

---

## 1. What's inside

```
MAA-Footwear/
├── index.html, shop.html, product.html, about.html, contact.html, offers.html
├── men.html, women.html, kids.html, sports-shoes.html, sneakers.html, sandals.html, slippers.html
├── admin/
│   ├── login.html, dashboard.html, manage-products.html
│   ├── add-product.html, edit-product.html, enquiries.html
│   ├── css/admin.css
│   └── js/  (auth-guard.js, login.js, dashboard.js, manage-products.js, product-form.js, enquiries.js)
├── css/style.css                 # shared design system (light + dark theme)
├── js/
│   ├── store.js                  # demo "database" (localStorage) — swap for API calls to go live
│   ├── products-seed.js          # demo product data, loaded once into the store
│   ├── main.js                   # nav, theme toggle, product card rendering, WhatsApp/call links
│   ├── home.js, shop.js, product.js, offers.js, contact.js
├── data/products.json            # source-of-truth demo catalog (also mirrored in products-seed.js)
├── images/                       # placeholder product photos, hero art, category tiles, logo
├── uploads/                       # where admin-uploaded photos will live in production
├── database/schema.sql           # full MySQL schema + sample rows
├── php/
│   ├── config/db.php, config/session.php
│   ├── api/auth.php, api/products.php, api/enquiries.php, api/upload.php
│   └── import_json_to_mysql.php  # one-time script to load the full demo catalog into MySQL
├── build.py, pages.py, admin_pages.py   # the generator scripts used to build every HTML page
└── README.md
```

`build.py` / `pages.py` / `admin_pages.py` are the Python scripts that assembled the HTML files from shared header/footer/sidebar templates. **You don't need Python to run the site** — the generated `.html` files are the actual website. Keep the scripts if you want to regenerate pages after changing the shared template (see §6).

---

## 2. Running the demo (no server needed)

The demo version works by simply opening the files, but for the admin image uploads and `fetch()`-free JS to behave consistently in every browser, serve the folder with any static server:

```bash
cd MAA-Footwear
python3 -m http.server 8080
# then visit http://localhost:8080/index.html
```

**Admin Panel demo login:** `admin/login.html`
- Username: `admin`
- Password: `maa@2026`

Change these in `js/store.js` (search for `DEFAULT_ADMIN`) before sharing the demo with anyone else.

> The demo "database" lives in your browser's `localStorage`. Editing, adding, or deleting a product in the Admin Panel updates it instantly on the public pages, in that same browser. Clearing browser data resets it back to the seed catalog in `js/products-seed.js`.

---

## 3. How to upload a new product (Admin Panel)

1. Go to `admin/login.html` and sign in.
2. Click **Add New Product** in the sidebar.
3. Upload up to 4 photos (first photo becomes the main thumbnail).
4. Fill in Name, Brand, Category, Collection (Men/Women/Kids), Material, Colours (comma-separated), and tick every available Size.
5. Enter **MRP** and **Selling Price** — the discount badge and "% OFF" label are calculated automatically.
6. Enter Stock Quantity. Stock ≤ 5 shows "Only X left"; 0 shows "Out of Stock" and disables purchase-intent styling.
7. Write a short Description.
8. Toggle **Featured / Best Seller / New Arrival** to control which homepage rails the product appears in.
9. Click **Publish Product** — it's live on the public site immediately.

## 4. Editing stock, price, or details

- **Quick stock/tag changes:** `admin/manage-products.html` lets you edit the stock number and the Featured/Best Seller/New Arrival checkboxes directly in the table — no need to open the full form.
- **Full edit:** click **Edit** on any row to open the same form used for adding a product, pre-filled with its current data.
- **Deleting a product:** click **Delete** in Manage Products. In the PHP version this is a soft-delete (`is_active = 0`), so the record and any of its past customer enquiries are preserved.

## 5. Managing categories & offers

- **Categories** are the 4 fixed catalog types (Sports Shoes, Sneakers, Sandals, Slippers) plus 3 audience collections (Men, Women, Kids), matching the site's navigation and dedicated pages. To add a brand-new category (e.g. "Formal Shoes"), you'll need to add it in three places: `MAA.CATEGORY_LABELS` in `js/store.js`, the `<select>` in the product form (`admin_pages.py` → `product_form_content()`), and a new category page (copy an existing one, e.g. `sandals.html`, and change its `data-preset-category` attribute and page title). Then re-run `python3 pages.py` if you're using the generator, or hand-edit the new HTML file directly.
- **Offers** aren't a separate list to manage — any product whose Selling Price is lower than its MRP automatically appears on `offers.html`, sorted by biggest discount. To put a product on sale, just lower its Selling Price in Manage Products or the edit form.

## 6. Regenerating pages after a design change

If you edit the shared header, footer, or navigation in `build.py`, or add a new page in `pages.py` / `admin_pages.py`, rebuild the static HTML with:

```bash
python3 build.py     # defines the shared templates (no output by itself)
python3 pages.py      # rewrites all public pages
python3 admin_pages.py  # rewrites all admin pages
```

This keeps every page's header/footer/sidebar in sync from one source of truth instead of hand-editing 19 HTML files individually.

---

## 7. Going live with PHP + MySQL

The demo is intentionally self-contained so it works anywhere instantly, but the real backend code is included and ready:

### Step 1 — Create the database
```bash
mysql -u root -p < database/schema.sql
```
This creates the `maa_footwear` database, all tables, and 3 sample products. To load the **full 18-product demo catalog**, also run:
```bash
php php/import_json_to_mysql.php
```

### Step 2 — Configure the connection
Edit `php/config/db.php` and set your real `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS` (most shared hosting control panels like cPanel show these after you create a MySQL database there).

### Step 3 — Set a real admin password
The schema ships with a **placeholder** password hash. Generate a real one:
```bash
php -r "echo password_hash('your-new-password', PASSWORD_BCRYPT);"
```
Then update the `admin_users` row in MySQL with that hash (via phpMyAdmin or `UPDATE admin_users SET password_hash = '...' WHERE username = 'admin';`).

### Step 4 — Point the front-end at the API
Right now, `js/store.js` reads/writes `localStorage`. To use the real database instead, replace the body of each function in `js/store.js` with a `fetch()` call to the matching endpoint — the function names and return shapes were designed to match 1:1, so no other file needs to change:

| `js/store.js` function | Replace with a call to |
|---|---|
| `getProducts()` | `GET php/api/products.php` (supports `?category=`, `?gender=`, `?featured=1`, `?q=`) |
| `getProduct(id)` | `GET php/api/products.php?id=5` |
| `addProduct(data)` | `POST php/api/products.php` |
| `updateProduct(id, patch)` | `PUT php/api/products.php?id=5` |
| `deleteProduct(id)` | `DELETE php/api/products.php?id=5` |
| `getEnquiries()` | `GET php/api/enquiries.php` (admin only) |
| `addEnquiry(data)` | `POST php/api/enquiries.php` (public) |
| `login(user, pass)` | `POST php/api/auth.php` with `{ "action": "login", ... }` |
| `isLoggedIn()` | `GET php/api/auth.php` → `{ loggedIn: true/false }` |
| `logout()` | `POST php/api/auth.php` with `{ "action": "logout" }` |

Product photo uploads: send each selected file to `POST php/api/upload.php` (admin only, `multipart/form-data`, field name `image`), which saves it into `uploads/products/` and returns its path — collect the returned paths into the `images` array you send to `products.php`.

### Step 5 — Server requirements
- PHP 8.0+
- MySQL 5.7+ / MariaDB 10.3+
- `uploads/products/` must be writable by the web server (`chmod 755` and confirm ownership matches the PHP process user)
- Enable HTTPS, then uncomment `'secure' => true` in `php/config/session.php`

---

## 8. SEO notes

- Every page ships as static, crawlable HTML with a unique `<title>`, meta description, and canonical URL (edit `SITE` in `pages.py` to your real domain and rebuild).
- Product names, prices, and descriptions render directly into the page for JS-off crawlers to see once the store is fed server-side (the demo renders product grids client-side for simplicity — the PHP version can render the grid server-side in PHP for full crawlability if desired).
- Update `data/products.json` / your MySQL data with real, unique descriptions per product — duplicate boilerplate text hurts search ranking.
- Add your Google Business listing and replace the placeholder map embed URL (`site_settings.map_embed_url` / `MAA.getSettings().mapEmbed`) with your real store's Google Maps embed link.

---

## 9. Roadmap / where to extend next

The codebase is deliberately modular so these can be added later without a rewrite:
- **Shopping cart & online payments** — add a `cart.js` using the same `localStorage`-then-API pattern as `store.js`, and a Razorpay/UPI payment API route under `php/api/`.
- **Customer accounts** — extend `admin_users`-style tables with a `customers` table and a public login/register flow.
- **Order tracking** — add an `orders` table (FK to `products`, `customers`) and an order-status page.
- **Inventory automation / barcode scanning** — the `stock` column and `manage-products.html` quick-edit are ready to be driven by a barcode scanner input (most USB scanners type + Enter like a keyboard, so a plain `<input>` with a `keydown` listener for Enter is often all that's needed).
- **GST invoicing** — add an `invoices` table and a PDF generation script (e.g. with `tecnickcom/tcpdf` or `dompdf/dompdf` via Composer).
- **Analytics dashboard** — the `admin/dashboard.html` stat cards already read live data; wire in page-view tracking (e.g. a simple `page_views` table logged from each page's JS) to extend it.

---

## 10. Support

This site was built and is maintained by your website developer. For code-level questions, refer to the inline comments in `js/store.js` (data layer) and `php/api/*.php` (backend) — every function explains its role and how the pieces connect.
