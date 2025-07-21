from dagster import (
    asset, 
    define_asset_job, 
    build_schedule_from_partitioned_job,
    AssetSelection, 
    ScheduleDefinition, 
    DailyPartitionsDefinition,
    Definitions
)
from datetime import datetime

# Create partitioned asset
@asset(
    partitions_def=DailyPartitionsDefinition(start_date=datetime(2025, 7, 16)) # set partition
)
def my_asset(context):
    context.log.warning('Doing something')


# Change asset to job
my_asset_job = define_asset_job(
    name='my_asset_job',
    selection=AssetSelection.assets(my_asset),
    partitions_def=DailyPartitionsDefinition(start_date=datetime(2025, 7, 16)) # set partition for schedule
)

my_scheduled_job_partition = build_schedule_from_partitioned_job(job=my_asset_job)

defs = Definitions(
    assets=[my_asset],
    schedules=[my_scheduled_job_partition]
)
