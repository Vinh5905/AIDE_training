from dagster import AssetIn, Definitions, asset
import pandas as pd
from dagster_test_csv_io_manager import CSVIOManager

@asset(
    name='my_2nd_asset', # set name
    key_prefix=['demo', 'fde'], # path of asset
    metadata={ 
        'owner': 'abc@abc.vn',
        'priority': 'high'
    },
    compute_kind='minio', # compute engine
    group_name='demo', # show in same group
    io_manager_key='csv_io_manager' # name of io_manager want to use
)
def my_asset_2(context):
    pd_data = pd.DataFrame({
        'a': [1, 2, 3],
        'b': ['x', 'y', 'z']
    })

    return pd_data


@asset(
    ins={'my_asset_2': AssetIn(key=['demo', 'fde', 'my_2nd_asset'])}, # key is prefix + name, if asset hasn't have 'name' then use key_prefix=['demo', 'fde']
    io_manager_key='csv_io_manager'
)
def asset_2_downstream(context, my_asset_2):
    context.log.info(f'Shape of data: {my_asset_2.shape}')
    return my_asset_2.head(1)


defs = Definitions(
    assets=[my_asset_2, asset_2_downstream],
    resources={
        'csv_io_manager': CSVIOManager()
    }
)