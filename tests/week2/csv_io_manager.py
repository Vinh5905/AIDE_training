from dagster import IOManager, InputContext, OutputContext
import pandas as pd

class CSVIOManager(IOManager):
    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        filename = context.asset_key.path[-1] # path of asset, then -1 is name of last file
        obj.to_csv(f'/tmp/{filename}.csv', index=False)

        # metadata
        num_records = obj.shape[0]
        path = f'/tmp/{filename}.csv'
        context.add_output_metadata({
            'record_count': num_records, 
            'data_path': path
        })
        
    
    def load_input(self, context: InputContext) -> pd.DataFrame:
        filename = context.asset_key.path[-1]
        obj = pd.read_csv(f'/tmp/{filename}.csv')
        return obj