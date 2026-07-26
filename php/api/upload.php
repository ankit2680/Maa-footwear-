<?php
/**
 * MAA Footwear — Product Image Upload API
 * ---------------------------------------------------------
 * POST /php/api/upload.php   (multipart/form-data, field name "image")
 * Admin only. Returns { "path": "uploads/products/xxxx.jpg" } which
 * the admin form then sends to products.php as part of "images": [...].
 * ---------------------------------------------------------
 */

require_once __DIR__ . '/../config/db.php';
require_once __DIR__ . '/../config/session.php';

header('Content-Type: application/json');
require_admin();

if ($_SERVER['REQUEST_METHOD'] !== 'POST' || empty($_FILES['image'])) {
    http_response_code(400);
    echo json_encode(['error' => 'No image uploaded.']);
    exit;
}

$file = $_FILES['image'];

if ($file['error'] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    echo json_encode(['error' => 'Upload failed. Please try a different file.']);
    exit;
}
if ($file['size'] > MAX_UPLOAD_BYTES) {
    http_response_code(400);
    echo json_encode(['error' => 'Image is too large. Maximum size is 5MB.']);
    exit;
}

$finfo = finfo_open(FILEINFO_MIME_TYPE);
$mime = finfo_file($finfo, $file['tmp_name']);
finfo_close($finfo);

if (!in_array($mime, ALLOWED_IMAGE_TYPES, true)) {
    http_response_code(400);
    echo json_encode(['error' => 'Only JPEG, PNG or WEBP images are allowed.']);
    exit;
}

if (!is_dir(UPLOAD_DIR)) {
    mkdir(UPLOAD_DIR, 0755, true);
}

$ext = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp'][$mime];
$filename = bin2hex(random_bytes(8)) . '.' . $ext;
$destination = UPLOAD_DIR . $filename;

if (!move_uploaded_file($file['tmp_name'], $destination)) {
    http_response_code(500);
    echo json_encode(['error' => 'Could not save the uploaded file. Check folder permissions on uploads/products/.']);
    exit;
}

echo json_encode(['path' => 'uploads/products/' . $filename]);
