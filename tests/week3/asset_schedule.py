from dagster import (
    asset, 
    define_asset_job, 
    AssetSelection, 
    ScheduleDefinition, 
    DailyPartitionsDefinition,
    Definitions
)
from datetime import datetime

@asset
def my_asset(context):
    context.log.warning('Doing something')

# Change asset to job
my_asset_job = define_asset_job(
    name='my_asset_job',
    selection=AssetSelection.assets(my_asset),
)

# Set schedule for job
my_scheduled_asset = ScheduleDefinition(
    job=my_asset_job,
    cron_schedule='*/1 * * * *'
)

defs = Definitions(
    assets=[my_asset],
    schedules=[my_scheduled_asset]
)
