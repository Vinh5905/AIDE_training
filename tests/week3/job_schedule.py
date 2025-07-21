from dagster import op, job, schedule, repository

# Test schedule op, job

@op
def my_op(context):
    context.log.warning('Doing something')

@job
def my_job():
    my_op()

@schedule(
    job=my_job,
    cron_schedule='*/1 * * * *'
)
def my_job_schedule(context):
    return {}

@repository # register all like op, job, schedule, ... into a repository (same to Definitions)
def demo():
    return [
        my_job_schedule
    ]