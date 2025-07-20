from dagster import Definitions
from assets.bronze_layer import olist_order_items_dataset, olist_order_payments_dataset, olist_orders_dataset, olist_products_dataset, product_category_name_translation
from assets.silver_layer import dim_products, fact_sales
from assets.gold_layer import sales_values_by_category
from resources.minio_io_manager import MinIOIOManager
from resources.mysql_io_manager import MySQLIOManager
from resources.psql_io_manager import PostgreSQLIOManager

MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "brazillian_ecommerce",
    "user": "admin",
    "password": "admin123",
}

MINIO_CONFIG = {
    "endpoint_url": "localhost:9000",
    "bucket": "warehouse",
    "aws_access_key_id": "minio",
    "aws_secret_access_key": "minio123",
}

PSQL_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "postgres",
    "user": "admin",
    "password": "admin123",
}

defs = Definitions(
    assets=[
        olist_order_items_dataset,
        olist_order_payments_dataset,
        olist_orders_dataset,
        olist_products_dataset,
        product_category_name_translation,
        dim_products,
        fact_sales,
        sales_values_by_category
    ],
    resources={
        "minio_io_manager": MinIOIOManager(MINIO_CONFIG),
        "mysql_io_manager": MySQLIOManager(MYSQL_CONFIG),
        "psql_io_manager": PostgreSQLIOManager(PSQL_CONFIG),
    }
)