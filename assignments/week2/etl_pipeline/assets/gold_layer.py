from dagster import asset, AssetExecutionContext, AssetIn, Output
import pandas as pd

@asset(
    ins={
        'fact_sales': AssetIn(
            key_prefix=['silver', 'ecom']
        ),
        'dim_products': AssetIn(
            key_prefix=['silver', 'ecom']
        )
    },
    io_manager_key='minio_io_manager',
    key_prefix=['gold', 'ecom'],
    group_name='gold',
    compute_kind='minio'
)
def sales_values_by_category(
    context: AssetExecutionContext,
    fact_sales: pd.DataFrame,
    dim_products: pd.DataFrame
) -> Output[pd.DataFrame]:
    # Convert order_purchase_timestamp to proper datetime format
    fact_sales["order_purchase_timestamp"] = pd.to_datetime(fact_sales["order_purchase_timestamp"])

    # Keep only rows where order_status is 'delivered'
    delivered_sales = fact_sales[fact_sales["order_status"] == "delivered"]

    # Aggregate daily sales per product
    daily_sales_products = (
        delivered_sales
        .assign(daily=lambda df: df["order_purchase_timestamp"].dt.date)
        .groupby(["daily", "product_id"], as_index=False)
        .agg(
            sales=("payment_value", lambda x: round(x.astype(float).sum(), 2)),
            bills=("order_id", "nunique")
        )
    )

    # Join product categories
    daily_sales_categories = (
        daily_sales_products
        .merge(dim_products[["product_id", "product_category_name_english"]], on="product_id", how="left")
        .rename(columns={"product_category_name_english": "category"})
        .assign(
            monthly=lambda df: pd.to_datetime(df["daily"]).dt.to_period("M").astype(str),
            values_per_bills=lambda df: df["sales"] / df["bills"]
        )
    )

    # Compute sales per category
    sales_values_by_category = (
        daily_sales_categories
        .groupby(["monthly", "category"], as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            total_bills=("bills", "sum")
        )
        .assign(
            values_per_bills=lambda df: df["total_sales"] / df["total_bills"]
        )
    )

    final_data = sales_values_by_category.copy()

    context.log.info(final_data.head(5).to_string())

    return Output(
        final_data,
        metadata={
            'rows_count': len(final_data),
            'columns_name': final_data.columns.to_list()
        }
    )