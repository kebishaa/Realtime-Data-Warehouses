import random
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from pinot_schema_operator import PinotSchemaSubmitOperator

start_date = datetime(2025, 3, 18)

default_args = {
    'owner': 'kebishaa',
    'depends_on_past': False,
    'start_date': start_date
}

with DAG(
        dag_id='schema_dag',
        default_args=default_args,
        description='A DAG to submit all schema in a folder to Apache Pinot',
        schedule_interval=timedelta(days=1),
        tags=['schema']
) as dag:
    start = EmptyOperator(task_id='start_task')

    submit_schema = PinotSchemaSubmitOperator(
        task_id='submit_schemas',
        folder_path='/opt/airflow/dags/schemas',
        pinot_url='http://pinot-controller:9000/schemas'  # Use HTTP unless HTTPS is explicitly configured
    )

    end = EmptyOperator(task_id='end_task')

    start >> submit_schema >> end
