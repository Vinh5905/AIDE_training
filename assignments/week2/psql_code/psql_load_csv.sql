\copy olist_order_payments_dataset FROM '/tmp/data/olist_order_payments_dataset.csv' DELIMITER ',' CSV HEADER;
\copy olist_orders_dataset FROM '/tmp/data/olist_orders_dataset.csv' DELIMITER ',' CSV HEADER;
\copy olist_products_dataset FROM '/tmp/data/olist_products_dataset.csv' DELIMITER ',' CSV HEADER;
\copy product_category_name_translation FROM '/tmp/data/product_category_name_translation.csv' DELIMITER ',' CSV HEADER;
-- Nếu không chỉ rõ column import vào thì postgres không nhận diện được cột để điền default vì nó sẽ điền theo thứ tự (trong /copy)
\copy olist_order_items_dataset (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value) FROM '/tmp/data/olist_order_items_dataset.csv' DELIMITER ',' CSV HEADER;

-- Check table records
SELECT * FROM olist_order_payments_dataset LIMIT 10;
SELECT * FROM olist_orders_dataset LIMIT 10;
SELECT * FROM olist_products_dataset LIMIT 10;
SELECT * FROM product_category_name_translation LIMIT 10;
SELECT * FROM olist_order_items_dataset LIMIT 10;