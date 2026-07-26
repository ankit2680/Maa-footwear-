<?php
/**
 * MAA Footwear — One-time import: data/products.json -> MySQL
 * ---------------------------------------------------------
 * Run this ONCE from the command line after creating the database
 * with database/schema.sql, to load the full 18-product demo
 * catalog (the schema.sql file only inserts 3 sample rows).
 *
 *   php php/import_json_to_mysql.php
 *
 * Safe to re-run: it skips products whose id already exists.
 * ---------------------------------------------------------
 */

require_once __DIR__ . '/config/db.php';

$jsonPath = __DIR__ . '/../data/products.json';
if (!file_exists($jsonPath)) {
    fwrite(STDERR, "Could not find data/products.json\n");
    exit(1);
}

$products = json_decode(file_get_contents($jsonPath), true);
if (!is_array($products)) {
    fwrite(STDERR, "data/products.json is not valid JSON\n");
    exit(1);
}

$pdo = getDbConnection();
$catCache = [];
function categoryId(PDO $pdo, array &$cache, string $slug): ?int {
    if (isset($cache[$slug])) return $cache[$slug];
    $stmt = $pdo->prepare('SELECT id FROM categories WHERE slug = ?');
    $stmt->execute([$slug]);
    $row = $stmt->fetch();
    return $cache[$slug] = $row ? (int) $row['id'] : null;
}

$inserted = 0;
$skipped = 0;

foreach ($products as $p) {
    $exists = $pdo->prepare('SELECT id FROM products WHERE id = ?');
    $exists->execute([$p['id']]);
    if ($exists->fetch()) { $skipped++; continue; }

    $catId = categoryId($pdo, $catCache, $p['category']);
    if (!$catId) { fwrite(STDERR, "Unknown category '{$p['category']}' for product {$p['id']}, skipping.\n"); continue; }

    $stmt = $pdo->prepare('
        INSERT INTO products
          (id, name, brand, category_id, gender, material, mrp, price, stock, description, is_featured, is_best_seller, is_new_arrival, rating)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ');
    $stmt->execute([
        $p['id'], $p['name'], $p['brand'], $catId, $p['gender'], $p['material'],
        $p['mrp'], $p['price'], $p['stock'], $p['description'],
        !empty($p['featured']) ? 1 : 0, !empty($p['bestSeller']) ? 1 : 0, !empty($p['newArrival']) ? 1 : 0,
        $p['rating'] ?? 4.0,
    ]);

    $imgStmt = $pdo->prepare('INSERT INTO product_images (product_id, image_path, sort_order) VALUES (?,?,?)');
    foreach (($p['images'] ?? []) as $i => $path) {
        $imgStmt->execute([$p['id'], basename($path), $i]);
    }
    $sizeStmt = $pdo->prepare('INSERT INTO product_sizes (product_id, size_uk) VALUES (?,?)');
    foreach (($p['sizes'] ?? []) as $size) {
        $sizeStmt->execute([$p['id'], $size]);
    }
    $colorStmt = $pdo->prepare('INSERT INTO product_colors (product_id, color_name) VALUES (?,?)');
    foreach (($p['colors'] ?? []) as $color) {
        $colorStmt->execute([$p['id'], $color]);
    }

    $inserted++;
}

echo "Import complete: $inserted inserted, $skipped skipped (already existed).\n";
echo "Note: product images referenced here (product-N-1.svg) are the demo placeholders.\n";
echo "Upload real photos through the Admin Panel to replace them.\n";
