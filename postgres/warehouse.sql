CREATE TABLE fact_books (
    book_id SERIAL PRIMARY KEY,
    barcode VARCHAR(50),
    price FLOAT,
    in_stock INTEGER,
    category_id INTEGER,
    affiliate_id INTEGER,
    seller_id INTEGER,
    pages INTEGER,
    size VARCHAR(255)
);

CREATE TABLE dim_categories (
    category_id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    subcategory VARCHAR(255)
);

CREATE TABLE dim_affiliates (
    affiliate_id SERIAL PRIMARY KEY,
    publishing_affiliate VARCHAR(255)
);

CREATE TABLE dim_sellers (
    seller_id SERIAL PRIMARY KEY,
    seller VARCHAR(255)
);

CREATE EXTENSION dblink;
SELECT dblink_connect(
    'source_conn',
    'host=localhost dbname=nhanamscrape_db user=postgres password=database1203'
);

INSERT INTO dim_categories (category_id, category, subcategory)
SELECT *
FROM dblink('source_conn', 'SELECT category_id, category, subcategory FROM categories')
AS t(category_id INTEGER, category VARCHAR, subcategory VARCHAR);

INSERT INTO dim_affiliates (affiliate_id, publishing_affiliate)
SELECT *
FROM dblink('source_conn', 'SELECT affiliate_id, publishing_affiliate FROM publishing_affiliates')
AS t(affiliate_id INTEGER, publishing_affiliate VARCHAR);

INSERT INTO dim_sellers (seller_id, seller)
SELECT *
FROM dblink('source_conn', 'SELECT seller_id, seller FROM sellers')
AS t(seller_id INTEGER, seller VARCHAR);

INSERT INTO fact_books (barcode, price, in_stock, category_id, affiliate_id, seller_id, pages, size)
SELECT barcode, price, in_stock, category_id, affiliate_id, seller_id, pages, size
FROM dblink('source_conn', 'SELECT barcode, price, in_stock, category_id, affiliate_id, seller_id, pages, size FROM books')
AS t(barcode VARCHAR, price FLOAT, in_stock INTEGER, category_id INTEGER, affiliate_id INTEGER, seller_id INTEGER, pages INTEGER, size VARCHAR);

select * from fact_books