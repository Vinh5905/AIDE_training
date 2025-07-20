--------------------------------- TABLE DATA BRONZE ---------------------------------

DROP TABLE IF EXISTS public.product_category_name_translation CASCADE;
CREATE TABLE public.product_category_name_translation (
    product_category_name text PRIMARY KEY,
    product_category_name_english text
);

DROP TABLE IF EXISTS public.olist_products_dataset CASCADE;
CREATE TABLE public.olist_products_dataset (
    product_id text PRIMARY KEY,
    product_category_name text,
    product_name_lenght integer,
    product_description_lenght integer,
    product_photos_qty integer,
    product_weight_g integer,
    product_length_cm integer,
    product_height_cm integer,
    product_width_cm integer
);

DROP TABLE IF EXISTS public.olist_orders_dataset CASCADE;
CREATE TABLE public.olist_orders_dataset (
    order_id text PRIMARY KEY,
    customer_id text,
    order_status text,
    order_purchase_timestamp text,
    order_approved_at text,
    order_delivered_carrier_date text,
    order_delivered_customer_date text,
    order_estimated_delivery_date text
);

DROP TABLE IF EXISTS public.olist_order_items_dataset CASCADE;
CREATE TABLE public.olist_order_items_dataset (
    order_id text,
    order_item_id integer,
    product_id text,
    seller_id text,
    shipping_limit_date text,
    price real,
    freight_value real,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (order_id, order_item_id, product_id, seller_id),
    FOREIGN KEY (order_id) REFERENCES public.olist_orders_dataset(order_id),
    FOREIGN KEY (product_id) REFERENCES public.olist_products_dataset(product_id)
);

DROP TABLE IF EXISTS public.olist_order_payments_dataset CASCADE;
CREATE TABLE public.olist_order_payments_dataset (
    order_id text,
    payment_sequential integer,
    payment_type text,
    payment_installments integer,
    payment_value real,
    PRIMARY KEY (order_id, payment_sequential)
);


--------------------------------- TABLE DATA GOLD ---------------------------------

CREATE SCHEMA IF NOT EXISTS gold;

DROP TABLE IF EXISTS gold.sales_values_by_category CASCADE;
CREATE TABLE gold.sales_values_by_category (
    monthly text,
    category text,
    sales float8,
    bills int8,
    values_per_bill float8
);
