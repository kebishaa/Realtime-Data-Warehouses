from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from kafka_operator import KafkaProduceOperator  # Ensure this is correctly implemented

start_date = datetime(2025, 3, 18)

default_args = {
    'owner': 'kebishaa',
    'depends_on_past': False,
    'start_date': start_date,
    'retries': 1,  # Retry once if the task fails
    'retry_delay': timedelta(minutes=5)  # Wait 5 minutes before retrying
}

with DAG(
        dag_id='transaction-facts_generator',
        default_args=default_args,
        description='Transaction fact data generator into Kafka',
        schedule_interval=timedelta(days=1),  # Fixed the schedule parameter
        tags=['fact_data']
) as dag:
    start = EmptyOperator(
        task_id='start_task'
    )

    generate_txn_data = KafkaProduceOperator(
        task_id='generate_txn_fact_data',
        kafka_broker='kafka_broker:9092',
        kafka_topic='transaction_facts',
        num_records=1000
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_txn_data >> end  # Space after `>>` for readability
