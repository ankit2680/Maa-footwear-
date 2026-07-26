-- =========================================================
--  MAA Footwear — MySQL Database Schema
--  Import this file in phpMyAdmin / MySQL CLI to create the
--  production database used by the php/ backend.
--  Charset: utf8mb4 (safe for ₹ symbol and all text)
-- =========================================================

CREATE DATABASE IF NOT EXISTS maa_footwear CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE maa_footwear;

-- ---------------------------------------------------------
-- Admin users (the IT developer / shop owner logins)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS admin_users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,   -- store with password_hash(), never plain text
  full_name VARCHAR(100) DEFAULT NULL,
  role ENUM('admin','editor') NOT NULL DEFAULT 'admin',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP NULL
) ENGINE=InnoDB;

-- Default admin — CHANGE THIS PASSWORD before going live.
-- Generated with password_hash('maa@2026', PASSWORD_BCRYPT)
INSERT INTO admin_users (username, password_hash, full_name, role) VALUES
('admin', '$2y$10$k8H1r7GxlxWq4l6P1lQwHu5oQ9d5r0M1c8yQeQ2s5wq9m0ZfR8n1e', 'Site Administrator', 'admin');

-- ---------------------------------------------------------
-- Categories (Sports Shoes, Sneakers, Sandals, Slippers …)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  slug VARCHAR(60) NOT NULL UNIQUE,      -- e.g. 'sports-shoes'
  name VARCHAR(100) NOT NULL,            -- e.g. 'Sports Shoes'
  sort_order INT DEFAULT 0,
  is_active TINYINT(1) DEFAULT 1
) ENGINE=InnoDB;

INSERT INTO categories (slug, name, sort_order) VALUES
('sports-shoes', 'Sports Shoes', 1),
('sneakers', 'Sneakers', 2),
('sandals', 'Sandals', 3),
('slippers', 'Slippers', 4);

-- ---------------------------------------------------------
-- Products
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  brand VARCHAR(100) NOT NULL,
  category_id INT NOT NULL,
  gender ENUM('men','women','kids') NOT NULL,
  material VARCHAR(150) DEFAULT NULL,
  mrp DECIMAL(10,2) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  description TEXT,
  is_featured TINYINT(1) DEFAULT 0,
  is_best_seller TINYINT(1) DEFAULT 0,
  is_new_arrival TINYINT(1) DEFAULT 0,
  is_active TINYINT(1) DEFAULT 1,        -- soft-delete / hide from site
  rating DECIMAL(2,1) DEFAULT 4.0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES categories(id)
) ENGINE=InnoDB;

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_gender ON products(gender);
CREATE INDEX idx_products_featured ON products(is_featured);

-- ---------------------------------------------------------
-- Product images (multiple images per product)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS product_images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  image_path VARCHAR(255) NOT NULL,      -- e.g. uploads/products/12-1.jpg
  sort_order INT DEFAULT 0,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Product sizes (many-to-many: a product has many sizes)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS product_sizes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  size_uk DECIMAL(3,1) NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  UNIQUE KEY unique_product_size (product_id, size_uk)
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Product colors
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS product_colors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  color_name VARCHAR(50) NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Customer enquiries (from Product Details + Contact forms)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS enquiries (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT DEFAULT NULL,
  customer_name VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(150) DEFAULT NULL,
  message TEXT NOT NULL,
  status ENUM('new','read','closed') DEFAULT 'new',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- Site settings (store info shown in footer / contact / map)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS site_settings (
  setting_key VARCHAR(60) PRIMARY KEY,
  setting_value TEXT
) ENGINE=InnoDB;

INSERT INTO site_settings (setting_key, setting_value) VALUES
('store_name', 'MAA Footwear'),
('phone', '+91 98765 43210'),
('whatsapp', '919876543210'),
('email', 'hello@maafootwear.in'),
('address', 'Shop No. 14, Station Road Market, Kannauj, Uttar Pradesh 209725'),
('hours', 'Mon – Sun: 10:00 AM – 9:00 PM'),
('map_embed_url', 'https://www.google.com/maps?q=Kannauj,Uttar+Pradesh&output=embed');

-- ---------------------------------------------------------
-- Sample product data (mirrors data/products.json — 3 rows shown,
-- see data/products.json + php/import_json_to_mysql.php for a
-- script that imports the FULL demo catalog automatically)
-- ---------------------------------------------------------
INSERT INTO products (id, name, brand, category_id, gender, material, mrp, price, stock, description, is_featured, is_best_seller, is_new_arrival, rating) VALUES
(1, 'Air Stride Runner', 'Nova Sport', 1, 'men', 'Mesh & EVA Sole', 3499.00, 2399.00, 18, 'A lightweight daily trainer built for long runs and gym days. Breathable knit upper, cushioned midsole and a grippy rubber outsole keep every stride comfortable.', 1, 1, 0, 4.6),
(2, 'Urban Court Sneaker', 'Cityfeet', 2, 'men', 'Canvas & Rubber Sole', 2999.00, 2199.00, 24, 'Classic low-top silhouette with a padded collar and vulcanised rubber sole.', 1, 0, 1, 4.4),
(5, 'Blossom Ballet Flat', 'Elira', 2, 'women', 'Soft PU', 1899.00, 1349.00, 22, 'A soft, rounded-toe ballet flat with cushioned insole.', 1, 1, 0, 4.7);

INSERT INTO product_images (product_id, image_path, sort_order) VALUES
(1, 'uploads/products/1-1.jpg', 0), (1, 'uploads/products/1-2.jpg', 1),
(2, 'uploads/products/2-1.jpg', 0), (2, 'uploads/products/2-2.jpg', 1),
(5, 'uploads/products/5-1.jpg', 0), (5, 'uploads/products/5-2.jpg', 1);

INSERT INTO product_sizes (product_id, size_uk) VALUES
(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),
(2,7),(2,8),(2,9),(2,10),(2,11),
(5,4),(5,5),(5,6),(5,7),(5,8);

INSERT INTO product_colors (product_id, color_name) VALUES
(1,'Amber'),(1,'Black'),
(2,'White'),(2,'Rust'),
(5,'Blush Pink'),(5,'Black');
