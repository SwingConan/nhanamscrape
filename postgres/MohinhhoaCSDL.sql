-- Tạo bảng categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    subcategory VARCHAR(255)
);

-- Tạo bảng publishing_affiliates
CREATE TABLE publishing_affiliates (
    affiliate_id SERIAL PRIMARY KEY,
    publishing_affiliate VARCHAR(255)
);

-- Tạo bảng sellers
CREATE TABLE sellers (
    seller_id SERIAL PRIMARY KEY,
    seller VARCHAR(255)
);

-- Tạo bảng books với các khóa ngoại
CREATE TABLE books (
    barcode VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    pages INTEGER,
    price FLOAT,
    size VARCHAR(255),
    in_stock INTEGER,
    category_id INTEGER REFERENCES categories(category_id),
    affiliate_id INTEGER REFERENCES publishing_affiliates(affiliate_id),
    seller_id INTEGER REFERENCES sellers(seller_id)
);
