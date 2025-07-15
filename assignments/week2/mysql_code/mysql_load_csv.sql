LOAD DATA LOCAL INFILE '/tmp/data/olist_order_payments_dataset.csv' 
INTO TABLE olist_order_payments_dataset 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/tmp/data/olist_orders_dataset.csv'
INTO TABLE olist_orders_dataset 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/tmp/data/olist_products_dataset.csv' 
INTO TABLE olist_products_dataset 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/tmp/data/product_category_name_translation.csv' 
INTO TABLE product_category_name_translation 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/tmp/data/olist_order_items_dataset.csv' 
INTO TABLE olist_order_items_dataset 
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
-- Nếu không chỉ rõ column import vào thì postgres không nhận diện được cột để điền default vì nó sẽ điền theo thứ tự (trong /copy)
(order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value);

-- Check table records
SELECT * FROM olist_order_payments_dataset LIMIT 10;
SELECT * FROM olist_orders_dataset LIMIT 10;
SELECT * FROM olist_products_dataset LIMIT 10;
SELECT * FROM product_category_name_translation LIMIT 10;
SELECT * FROM olist_order_items_dataset LIMIT 10;