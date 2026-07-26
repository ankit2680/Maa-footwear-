<?php
/**
 * MAA Footwear — Products API
 * ---------------------------------------------------------
 * GET    /php/api/products.php                 -> list all active products (public)
 * GET    /php/api/products.php?id=5            -> single product with images/sizes/colors
 * GET    /php/api/products.php?category=sneakers&gender=men&featured=1&q=running
 * POST   /php/api/products.php                 -> create product (admin only, JSON body)
 * PUT    /php/api/products.php?id=5            -> update product (admin only, JSON body)
 * DELETE /php/api/products.php?id=5            -> delete product (admin only)
 *
 * This mirrors the shape used by js/store.js so the front-end
 * JS only needs its data-fetching functions swapped from
 * localStorage to fetch() calls against this file.
 * ---------------------------------------------------------
 */

require_once __DIR__ . '/../config/db.php';
require_once __DIR__ . '/../config/session.php';

header('Content-Type: application/json');
$pdo = getDbConnection();
$method = $_SERVER['REQUEST_METHOD'];

function fetch_full_product(PDO $pdo, int $id): ?array {
    $stmt = $pdo->prepare('
        SELECT p.*, c.slug AS category, c.name AS category_name
        FROM products p JOIN categories c ON c.id = p.category_id
        WHERE p.id = ? AND p.is_active = 1
    ');
    $stmt->execute([$id]);
    $product = $stmt->fetch();
    if (!$product) return null;

    $imgs = $pdo->prepare('SELECT image_path FROM product_images WHERE product_id = ? ORDER BY sort_order');
    $imgs->execute([$id]);
    $product['images'] = array_map(fn($r) => UPLOAD_URL . basename($r['image_path']), $imgs->fetchAll());

    $sizes = $pdo->prepare('SELECT size_uk FROM product_sizes WHERE product_id = ? ORDER BY size_uk');
    $sizes->execute([$id]);
    $product['sizes'] = array_map(fn($r) => (float) $r['size_uk'], $sizes->fetchAll());

    $colors = $pdo->prepare('SELECT color_name FROM product_colors WHERE product_id = ?');
    $colors->execute([$id]);
    $product['colors'] = array_map(fn($r) => $r['color_name'], $colors->fetchAll());

    return $product;
}

/* ---------------------------- GET ---------------------------- */
if ($method === 'GET') {
    if (isset($_GET['id'])) {
        $product = fetch_full_product($pdo, (int) $_GET['id']);
        if (!$product) {
            http_response_code(404);
            echo json_encode(['error' => 'Product not found.']);
            exit;
        }
        echo json_encode($product);
        exit;
    }

    $sql = 'SELECT p.*, c.slug AS category FROM products p JOIN categories c ON c.id = p.category_id WHERE p.is_active = 1';
    $params = [];

    if (!empty($_GET['category'])) { $sql .= ' AND c.slug = ?'; $params[] = $_GET['category']; }
    if (!empty($_GET['gender']))   { $sql .= ' AND p.gender = ?'; $params[] = $_GET['gender']; }
    if (!empty($_GET['featured'])) { $sql .= ' AND p.is_featured = 1'; }
    if (!empty($_GET['bestSeller'])) { $sql .= ' AND p.is_best_seller = 1'; }
    if (!empty($_GET['newArrival'])) { $sql .= ' AND p.is_new_arrival = 1'; }
    if (!empty($_GET['q'])) {
        $sql .= ' AND (p.name LIKE ? OR p.brand LIKE ?)';
        $like = '%' . $_GET['q'] . '%';
        $params[] = $like; $params[] = $like;
    }
    $sql .= ' ORDER BY p.created_at DESC';

    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $products = $stmt->fetchAll();

    // attach images/sizes/colors in bulk (avoids N+1 queries)
    $ids = array_column($products, 'id');
    if ($ids) {
        $in = implode(',', array_fill(0, count($ids), '?'));

        $imgStmt = $pdo->prepare("SELECT product_id, image_path FROM product_images WHERE product_id IN ($in) ORDER BY sort_order");
        $imgStmt->execute($ids);
        $imagesByProduct = [];
        foreach ($imgStmt->fetchAll() as $row) {
            $imagesByProduct[$row['product_id']][] = UPLOAD_URL . basename($row['image_path']);
        }

        $sizeStmt = $pdo->prepare("SELECT product_id, size_uk FROM product_sizes WHERE product_id IN ($in) ORDER BY size_uk");
        $sizeStmt->execute($ids);
        $sizesByProduct = [];
        foreach ($sizeStmt->fetchAll() as $row) {
            $sizesByProduct[$row['product_id']][] = (float) $row['size_uk'];
        }

        $colorStmt = $pdo->prepare("SELECT product_id, color_name FROM product_colors WHERE product_id IN ($in)");
        $colorStmt->execute($ids);
        $colorsByProduct = [];
        foreach ($colorStmt->fetchAll() as $row) {
            $colorsByProduct[$row['product_id']][] = $row['color_name'];
        }

        foreach ($products as &$p) {
            $p['images'] = $imagesByProduct[$p['id']] ?? [];
            $p['sizes'] = $sizesByProduct[$p['id']] ?? [];
            $p['colors'] = $colorsByProduct[$p['id']] ?? [];
        }
        unset($p);
    }

    echo json_encode($products);
    exit;
}

/* ------------------- POST / PUT / DELETE need auth ------------------- */
require_admin();

function category_id_from_slug(PDO $pdo, string $slug): ?int {
    $stmt = $pdo->prepare('SELECT id FROM categories WHERE slug = ?');
    $stmt->execute([$slug]);
    $row = $stmt->fetch();
    return $row ? (int) $row['id'] : null;
}

function save_product_relations(PDO $pdo, int $productId, array $body): void {
    $pdo->prepare('DELETE FROM product_images WHERE product_id = ?')->execute([$productId]);
    $pdo->prepare('DELETE FROM product_sizes WHERE product_id = ?')->execute([$productId]);
    $pdo->prepare('DELETE FROM product_colors WHERE product_id = ?')->execute([$productId]);

    $imgStmt = $pdo->prepare('INSERT INTO product_images (product_id, image_path, sort_order) VALUES (?,?,?)');
    foreach (($body['images'] ?? []) as $i => $path) {
        $imgStmt->execute([$productId, basename($path), $i]);
    }

    $sizeStmt = $pdo->prepare('INSERT INTO product_sizes (product_id, size_uk) VALUES (?,?)');
    foreach (($body['sizes'] ?? []) as $size) {
        $sizeStmt->execute([$productId, $size]);
    }

    $colorStmt = $pdo->prepare('INSERT INTO product_colors (product_id, color_name) VALUES (?,?)');
    foreach (($body['colors'] ?? []) as $color) {
        $colorStmt->execute([$productId, $color]);
    }
}

/* ---------------------------- POST (create) ---------------------------- */
if ($method === 'POST') {
    $body = json_input();
    $required = ['name', 'brand', 'category', 'gender', 'mrp', 'price', 'stock'];
    foreach ($required as $field) {
        if (!isset($body[$field]) || $body[$field] === '') {
            http_response_code(400);
            echo json_encode(['error' => "Missing required field: $field"]);
            exit;
        }
    }

    $categoryId = category_id_from_slug($pdo, $body['category']);
    if (!$categoryId) {
        http_response_code(400);
        echo json_encode(['error' => 'Unknown category.']);
        exit;
    }

    $stmt = $pdo->prepare('
        INSERT INTO products
          (name, brand, category_id, gender, material, mrp, price, stock, description, is_featured, is_best_seller, is_new_arrival)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    ');
    $stmt->execute([
        $body['name'], $body['brand'], $categoryId, $body['gender'],
        $body['material'] ?? '', $body['mrp'], $body['price'], $body['stock'],
        $body['description'] ?? '',
        !empty($body['featured']) ? 1 : 0,
        !empty($body['bestSeller']) ? 1 : 0,
        !empty($body['newArrival']) ? 1 : 0,
    ]);
    $productId = (int) $pdo->lastInsertId();
    save_product_relations($pdo, $productId, $body);

    echo json_encode(fetch_full_product($pdo, $productId));
    exit;
}

/* ---------------------------- PUT (update) ---------------------------- */
if ($method === 'PUT') {
    $id = (int) ($_GET['id'] ?? 0);
    if (!$id) { http_response_code(400); echo json_encode(['error' => 'Missing product id.']); exit; }

    $body = json_input();
    $fields = [];
    $params = [];

    $map = [
        'name' => 'name', 'brand' => 'brand', 'gender' => 'gender', 'material' => 'material',
        'mrp' => 'mrp', 'price' => 'price', 'stock' => 'stock', 'description' => 'description',
    ];
    foreach ($map as $key => $col) {
        if (array_key_exists($key, $body)) { $fields[] = "$col = ?"; $params[] = $body[$key]; }
    }
    if (array_key_exists('category', $body)) {
        $categoryId = category_id_from_slug($pdo, $body['category']);
        if ($categoryId) { $fields[] = 'category_id = ?'; $params[] = $categoryId; }
    }
    if (array_key_exists('featured', $body))   { $fields[] = 'is_featured = ?';    $params[] = $body['featured'] ? 1 : 0; }
    if (array_key_exists('bestSeller', $body)) { $fields[] = 'is_best_seller = ?'; $params[] = $body['bestSeller'] ? 1 : 0; }
    if (array_key_exists('newArrival', $body)) { $fields[] = 'is_new_arrival = ?'; $params[] = $body['newArrival'] ? 1 : 0; }

    if ($fields) {
        $params[] = $id;
        $sql = 'UPDATE products SET ' . implode(', ', $fields) . ' WHERE id = ?';
        $pdo->prepare($sql)->execute($params);
    }
    if (isset($body['images']) || isset($body['sizes']) || isset($body['colors'])) {
        save_product_relations($pdo, $id, $body);
    }

    $updated = fetch_full_product($pdo, $id);
    if (!$updated) { http_response_code(404); echo json_encode(['error' => 'Product not found.']); exit; }
    echo json_encode($updated);
    exit;
}

/* ---------------------------- DELETE ---------------------------- */
if ($method === 'DELETE') {
    $id = (int) ($_GET['id'] ?? 0);
    if (!$id) { http_response_code(400); echo json_encode(['error' => 'Missing product id.']); exit; }

    // Soft delete keeps the row (and any linked enquiries) for records.
    $pdo->prepare('UPDATE products SET is_active = 0 WHERE id = ?')->execute([$id]);
    echo json_encode(['success' => true]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed.']);
