CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    nama_barang VARCHAR(100) NOT NULL,
    kategori VARCHAR(50),
    harga_beli DECIMAL(10, 2) NOT NULL,
    harga_jual DECIMAL(10, 2) NOT NULL,
    stok INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active TINYINT(1) DEFAULT 1
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role varchar(50) not null,
    nama_lengkap VARCHAR(100)
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no_invoice VARCHAR(20) UNIQUE NOT NULL,
    total_harga DECIMAL(10, 2) NOT NULL,
    bayar DECIMAL(10, 2) NOT NULL,
    kembali DECIMAL(10, 2) NOT NULL,
    user_id INT, -- Siapa kasir yang bertugas
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE transaction_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT,
    product_id INT,
    qty INT NOT NULL,
    harga_jual DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE stock_adjustments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    qty_sebelum INT,
    qty_sesudah INT,
    selisih INT,
    keterangan TEXT,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);


INSERT INTO products (sku, nama_barang, kategori, harga_beli, harga_jual, stok) VALUES
('BRG001', 'Beras Ramos 5kg', 'Sembako', 62000.00, 68000.00, 20),
('BRG002', 'Minyak Goreng 2L', 'Sembako', 28000.00, 32000.00, 15),
('BRG003', 'Gula Pasir 1kg', 'Sembako', 13500.00, 15000.00, 3), -- Stok menipis
('BRG004', 'Mie Instan Goreng', 'Makanan', 2500.00, 3100.00, 100),
('BRG005', 'Kopi Sachet (Isi 10)', 'Minuman', 12000.00, 15000.00, 2), -- Stok menipis
('BRG006', 'Sabun Mandi Cair', 'Kesehatan', 18000.00, 22500.00, 12),
('BRG007', 'Susu UHT 1L', 'Minuman', 16000.00, 19000.00, 8),
('BRG008', 'Tepung Terigu 1kg', 'Sembako', 10000.00, 12500.00, 25);

INSERT INTO users (username, password, role, nama_lengkap) VALUES
('admin', 'scrypt:32768:8:1$OIAOJyx9yVlhueEe$fbd3a81ba754b5a1d8e1b4cb5264c47cdf875decf3cea6b719dceef320e7d2ee5f8b25334aa7db7d88ffb45d65b7e275e2ffd6a54bd85333e6d4db03d4d82f0e', 'admin', 'ADMIN SM')
;