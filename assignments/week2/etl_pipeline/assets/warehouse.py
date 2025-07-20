from dagster import asset, AssetIn, AssetExecutionContext, Output
import pandas as pd

@asset(
    ins={
        'sales_values_by_category': AssetIn(
            key_prefix=['gold', 'ecom']
        )
    },
    io_manager_key='psql_io_manager',
    key_prefix=['gold'],
    group_name='warehouse',
    compute_kind='postgresql'
)
def sales_values_by_category(
    context: AssetExecutionContext,
    sales_values_by_category: pd.DataFrame
) -> Output[pd.DataFrame]:
    data = sales_values_by_category
    context.log.warning(f"Saving {len(data)} rows to PostgreSQL table gold.sales_values_by_category")

    return Output(
        data,
        metadata={
            'rows_count': len(data),
            'columns_name': data.columns.to_list()
        }
    )