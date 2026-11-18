CREATE DATABASE IF NOT EXISTS Shopdb10;
USE Shopdb10;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO users (username, password) VALUES
('admin', 'S3cr3tP4ss_9a21!'),
('guest', '9uestpass123');

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    secret_note VARCHAR(150)
);

INSERT INTO products (name, secret_note) VALUES
('Wireless Mouse', 'Stok terbatas, restock bulan depan'),
('Mechanical Keyboard', 'Promo akhir tahun'),
('USB-C Hub', 'Bundling dengan laptop');

CREATE TABLE config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    flag VARCHAR(100) NOT NULL
);

INSERT INTO config (flag) VALUES
('LKS{b4e8c21f9a7d6035e2f6b8c1d94a7053}');

CREATE USER IF NOT EXISTS 'Storeapp01'@'%' IDENTIFIED BY 'Kj7mPz2qXr';
GRANT SELECT, INSERT, UPDATE, DELETE ON Shopdb10.* TO 'Storeapp01'@'%';
FLUSH PRIVILEGES;
