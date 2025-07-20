from dagster import asset, AssetExecutionContext, AssetIn, Output
import pandas as pd

@asset(
    ins={
        'olist_products_dataset': AssetIn(
            key=['bronze', 'ecom', 'bronze_olist_products_dataset']
        ),
        'product_category_name_translation': AssetIn(
            key=['bronze', 'ecom', 'bronze_product_category_name_translation']
        )
    },
    key_prefix=['silver', 'ecom'],
    io_manager_key='minio_io_manager',
    group_name='silver',
    compute_kind='python'
)
def dim_products(
    context: AssetExecutionContext, 
    olist_products_dataset: pd.DataFrame,
    product_category_name_translation: pd.DataFrame
) -> Output[pd.DataFrame]:
    data = pd.merge(olist_products_dataset, product_category_name_translation, on='product_category_name')
    data_filters = data[['product_id', 'product_category_name_english']].copy()

    return Output(
        data_filters,
        metadata={
            'rows_count': len(data_filters),
            'columns_name': data_filters.columns.to_list()
        }
    )


@asset(
    ins={
        'olist_orders_dataset': AssetIn(
            key=['bronze', 'ecom', 'bronze_olist_orders_dataset']
        ),
        'olist_order_items_dataset': AssetIn(
            key=['bronze', 'ecom', 'bronze_olist_order_items_dataset']
        ),
        'olist_order_payments_dataset': AssetIn(
            key=['bronze', 'ecom', 'bronze_olist_order_payments_dataset']
        )
    },
    key_prefix=['silver', 'ecom'],
    io_manager_key='minio_io_manager',
    group_name='silver',
    compute_kind='python'
)
def fact_sales(
    context: AssetExecutionContext,
    olist_orders_dataset: pd.DataFrame,
    olist_order_items_dataset: pd.DataFrame,
    olist_order_payments_dataset: pd.DataFrame,
) -> Output[pd.DataFrame]:
    data = (
        olist_orders_dataset 
        .merge(olist_order_items_dataset, on='order_id') 
        .merge(olist_order_payments_dataset, on='order_id')
    )
    
    data_filters = data[['order_id', 'customer_id', 'order_purchase_timestamp', 'product_id', 'payment_value', 'order_status']].copy()

    return Output(
        data_filters,
        metadata={
            'rows_count': len(data_filters),
            'columns_name': data_filters.columns.to_list()
        }
    )