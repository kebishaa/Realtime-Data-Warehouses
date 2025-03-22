import glob
import requests
from typing import Any
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.context import Context
from sqlalchemy import table


class PinotTableSubmitOperator(BaseOperator):
    @apply_defaults
    def __init__(self, folder_path: str, pinot_url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.folder_path = folder_path
        self.pinot_url = pinot_url

    def execute(self, context: Context) -> Any:
        try:
            table_files = glob.glob(self.folder_path + '/*.json')
            for table_file in table_files:
                with open(table_file, 'r') as file:
                    table_data = file.read()

                # Define headers and submit the request to Pinot
                headers = {'Content-Type': 'application/json'}
                response = requests.post(self.pinot_url, headers=headers, data=table_data)

                if response.status_code == 200:
                    self.log.info(f'Table successfully submitted to Apache Pinot: {table_file}')
                else:
                    self.log.error(f'Failed to submit table: {response.status_code} - {response.text}')
                    raise Exception(f'Table submission failed with status code {response.status_code}')
        except Exception as e:
            self.log.error(f'An error occurred: {str(e)}')
            raise
