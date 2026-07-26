<?php
/**
 * MAA Footwear — Admin Authentication API
 * ---------------------------------------------------------
 * POST /php/api/auth.php  { "action": "login", "username": "...", "password": "..." }
 * POST /php/api/auth.php  { "action": "logout" }
 * GET  /php/api/auth.php                -> { "loggedIn": true/false }
 *
 * Replace js/store.js's login()/logout()/isLoggedIn() calls with
 * fetch() calls to this file when you deploy the real backend.
 * ---------------------------------------------------------
 */

require_once __DIR__ . '/../config/db.php';
require_once __DIR__ . '/../config/session.php';

header('Content-Type: application/json');

$method = $_SERVER['REQUEST_METHOD'];

if ($method === 'GET') {
    echo json_encode(['loggedIn' => is_admin_logged_in()]);
    exit;
}

if ($method === 'POST') {
    $body = json_input();
    $action = $body['action'] ?? '';

    if ($action === 'login') {
        $username = trim($body['username'] ?? '');
        $password = $body['password'] ?? '';

        if ($username === '' || $password === '') {
            http_response_code(400);
            echo json_encode(['error' => 'Username and password are required.']);
            exit;
        }

        $pdo = getDbConnection();
        $stmt = $pdo->prepare('SELECT id, username, password_hash, full_name FROM admin_users WHERE username = ? LIMIT 1');
        $stmt->execute([$username]);
        $user = $stmt->fetch();

        if ($user && password_verify($password, $user['password_hash'])) {
            session_regenerate_id(true);
            $_SESSION['admin_id'] = $user['id'];
            $_SESSION['admin_username'] = $user['username'];

            $upd = $pdo->prepare('UPDATE admin_users SET last_login = NOW() WHERE id = ?');
            $upd->execute([$user['id']]);

            echo json_encode(['success' => true, 'username' => $user['username'], 'fullName' => $user['full_name']]);
        } else {
            http_response_code(401);
            echo json_encode(['error' => 'Incorrect username or password.']);
        }
        exit;
    }

    if ($action === 'logout') {
        $_SESSION = [];
        session_destroy();
        echo json_encode(['success' => true]);
        exit;
    }

    http_response_code(400);
    echo json_encode(['error' => 'Unknown action.']);
    exit;
}

http_response_code(405);
echo json_encode(['error' => 'Method not allowed.']);
