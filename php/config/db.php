<?php
/**
 * MAA Footwear — Database Connection
 * ---------------------------------------------------------
 * Update the constants below with your hosting provider's
 * MySQL credentials, then require this file from any API
 * script: require_once __DIR__ . '/../config/db.php';
 * ---------------------------------------------------------
 */

define('DB_HOST', 'localhost');
define('DB_NAME', 'maa_footwear');
define('DB_USER', 'root');          // change in production
define('DB_PASS', '');              // change in production
define('DB_CHARSET', 'utf8mb4');

function getDbConnection(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
        $options = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ];
        try {
            $pdo = new PDO($dsn, DB_USER, DB_PASS, $options);
        } catch (PDOException $e) {
            http_response_code(500);
            header('Content-Type: application/json');
            echo json_encode(['error' => 'Database connection failed. Check php/config/db.php credentials.']);
            exit;
        }
    }
    return $pdo;
}

/** Uploaded product image storage (relative to project root) */
define('UPLOAD_DIR', __DIR__ . '/../../uploads/products/');
define('UPLOAD_URL', '/uploads/products/');
define('MAX_UPLOAD_BYTES', 5 * 1024 * 1024); // 5MB per image
define('ALLOWED_IMAGE_TYPES', ['image/jpeg', 'image/png', 'image/webp']);
