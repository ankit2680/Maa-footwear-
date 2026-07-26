<?php
/**
 * MAA Footwear — Customer Enquiries API
 * ---------------------------------------------------------
 * POST /php/api/enquiries.php   -> public: submit an enquiry (no login needed)
 *   { "name": "...", "phone": "...", "email": "...", "message": "...", "productId": 5 }
 *
 * GET    /php/api/enquiries.php               -> admin only: list all enquiries
 * PUT    /php/api/enquiries.php?id=3          -> admin only: update status
 * DELETE /php/api/enquiries.php?id=3          -> admin only: delete
 * ---------------------------------------------------------
 */

require_once __DIR__ . '/../config/db.php';
require_once __DIR__ . '/../config/session.php';

header('Content-Type: application/json');
$pdo = getDbConnection();
$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'POST') {
    $body = json_input();
    $name = trim($body['name'] ?? '');
    $phone = trim($body['phone'] ?? '');
    $message = trim($body['message'] ?? '');

    if ($name === '' || $phone === '' || $message === '') {
        http_response_code(400);
        echo json_encode(['error' => 'Name, phone and message are required.']);
        exit;
    }

    $stmt = $pdo->prepare('INSERT INTO enquiries (product_id, customer_name, phone, email, message) VALUES (?,?,?,?,?)');
    $stmt->execute([
        !empty($body['productId']) ? (int) $body['productId'] : null,
        $name, $phone, $body['email'] ?? null, $message,
    ]);

    echo json_encode(['success' => true, 'id' => (int) $pdo->lastInsertId()]);
    exit;
}

require_admin();

if ($method === 'GET') {
    $stmt = $pdo->query('
        SELECT e.*, p.name AS product_name
        FROM enquiries e LEFT JOIN products p ON p.id = e.product_id
        ORDER BY e.created_at DESC
    ');
    echo json_encode($stmt->fetchAll());
    exit;
}

if ($method === 'PUT') {
    $id = (int) ($_GET['id'] ?? 0);
    $body = json_input();
    if (!$id || empty($body['status'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing id or status.']);
        exit;
    }
    $pdo->prepare('UPDATE enquiries SET status = ? WHERE id = ?')->execute([$body['status'], $id]);
    echo json_encode(['success' => true]);
    exit;
}

if ($method === 'DELETE') {
    $id = (int) ($_GET['id'] ?? 0);
    if (!$id) { http_response_code(400); echo json_encode(['error' => 'Missing id.']); exit; }
    $pdo->prepare('DELETE FROM enquiries WHERE id = ?')->execute([$id]);
    echo json_encode(['success' => true]);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed.']);
