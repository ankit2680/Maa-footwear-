<?php
/**
 * MAA Footwear — Session bootstrap + auth helpers
 * Include at the top of every protected admin API script:
 *   require_once __DIR__ . '/../config/session.php';
 *   require_admin(); // stops execution with 401 if not logged in
 */

if (session_status() === PHP_SESSION_NONE) {
    session_set_cookie_params([
        'httponly' => true,
        'samesite' => 'Lax',
        // 'secure' => true, // enable once the site is served over HTTPS
    ]);
    session_start();
}

function is_admin_logged_in(): bool {
    return !empty($_SESSION['admin_id']);
}

function require_admin(): void {
    if (!is_admin_logged_in()) {
        http_response_code(401);
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Not authenticated. Please log in again.']);
        exit;
    }
}

function json_input(): array {
    $raw = file_get_contents('php://input');
    $data = json_decode($raw, true);
    return is_array($data) ? $data : [];
}
