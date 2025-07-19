import os
from contextlib import contextmanager
from datetime import datetime
from typing import Union

import pandas as pd
from dagster import IOManager, OutputContext, InputContext
from minio import Minio

@contextmanager
def connect_minio(config):
    client = Minio(
        endpoint=config.get("endpoint_url"),
        access_key=config.get("aws_access_key_id"),
        secret_key=config.get("aws_secret_access_key"),
        secure=False,
    )
    try:
        yield client
    except Exception:
        raise

class MinIOIOManager(IOManager):
    def __init__(self, config):
        self._config = config

    def _get_path(self, context: Union[InputContext, OutputContext]):
        layer, schema, table = context.asset_key.path
        key = "/".join([layer, schema, table.replace(f"{layer}_", "")])
        tmp_file_path = "/tmp/file-{}-{}.parquet".format(
            datetime.today().strftime("%Y%m%d%H%M%S"),
            "-".join(context.asset_key.path)
        )
        
        return f"{key}.parquet", tmp_file_path
    
    def _check_and_create_bucket(self, client: Minio, bucket: str):
        if not client.bucket_exists(bucket):
            print(f'Create bucket {bucket}')
            client.make_bucket(bucket)
        else:
            print(f"Bucket {bucket} already exists")

    # TODO: your code here
    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        # convert to parquet format
        key_name, tmp_file_path = self._get_path(context)
        context.log.warning(self._get_path(context))

        layer, object_name = key_name.split(sep='/', maxsplit=1)
        context.log.warning(f'Layer: {layer} ---- Object_name: {object_name}')

        try:
            # save data in file first
            obj.to_parquet(tmp_file_path, index=False)

            # upload to MinIO
            with connect_minio(self._config) as client:
                self._check_and_create_bucket(client, layer)
                client.fput_object(layer, object_name, tmp_file_path)
                context.log.warning(f"Uploaded file to {layer}/{object_name}")

            # clean up tmp file
            if os.path.exists(tmp_file_path):
                context.log.warning('File exists -> Remove')
                os.remove(tmp_file_path)
            
            context.log.warning('Done handle output!!')

        except Exception:
            raise

    # TODO: your code here
    def load_input(self, context: InputContext) -> pd.DataFrame:
        key_name, tmp_file_path = self._get_path(context)

        layer, object_name = key_name.split(sep='/', maxsplit=1)

        try:
            with connect_minio(self._config) as client:
                client.fget_object(layer, object_name, tmp_file_path)
                data = pd.read_parquet(tmp_file_path)
                
            return data
        except Exception:
            raise