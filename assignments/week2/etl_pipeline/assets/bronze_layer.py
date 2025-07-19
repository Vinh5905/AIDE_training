from dagster import asset, OutputContext, Output
import pandas as pd
from resources.mysql_io_manager import MySQLIOManager

# Ingest list of tables from MySQL -> MinIO (bronze/ecom/<table_name>)
ls_tables = [
    "olist_order_items_dataset",
    "olist_order_payments_dataset",
    "olist_orders_dataset",
    "olist_products_dataset",
    "product_category_name_translation",
]

def create_bronze_asset(table_name):
    @asset(
        name=f'bronze_{table_name}',
        required_resource_keys={'mysql_io_manager'},
        key_prefix=['bronze', 'ecom'],
        compute_kind='mysql',
        group_name='bronze',
        io_manager_key='minio_io_manager'
    )
    def bronze_asset(context: OutputContext) -> Output[pd.DataFrame]:
        sql_request = f'SELECT * FROM {table_name}'
        pd_data = context.resources.mysql_io_manager.extract_data(sql_request)
        context.log.warning(f'Extracted {len(pd_data)} rows successfully from {table_name}!!')
        return Output(
            pd_data,
            metadata={
                'table': table_name,
                'rows_count': len(pd_data)
            }
        )
    
    return bronze_asset

# Bronze datasets
olist_order_items_dataset = create_bronze_asset('olist_order_items_dataset')
olist_order_payments_dataset = create_bronze_asset('olist_order_payments_dataset')
olist_orders_dataset = create_bronze_asset('olist_orders_dataset')
olist_products_dataset = create_bronze_asset('olist_products_dataset')
product_category_name_translation = create_bronze_asset('product_category_name_translation')