from dagster import asset
import random

@asset(config_schema={
    'api_endpoint': str
})
def my_asset1(context):
    context.log.info('INFO: my 1st asset')
    context.log.warning('WARNING: you see this but do not care=))')
    context.log.error('ERROR: my error:<')
    context.log.critical('CRITICAL: omgggg!!')

    api_endpoint = context.op_config.get('api_endpoint', 'no endpoint')
    context.log.info(f'API: {api_endpoint}')

    random_num = random.randint(1, 10)
    context.add_output_metadata({
        'row_count': random_num
    })
    return 1