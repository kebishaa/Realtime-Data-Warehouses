from random import choice, randint
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

start_date = datetime(2025, 3, 18)
default_args = {
    'owner': 'kebishaa',
    'depends_on_past': False,
    'backfill': False,
}

num_rows = 50
output_file = './account_dim_large_data.csv'

# Lists to store generated data
account_ids = []
account_types = []
statuses = []
customer_ids = []
balances = []
opening_dates = []

def generate_random_data(row_num):
    account_id = f'A{row_num:05d}'
    account_type = choice(['SAVINGS', 'CHECKING'])
    status = choice(['ACTIVE', 'INACTIVE'])
    customer_id = f'C{randint(1, 1000):05d}'
    balance = round(randint(10000, 100000) / 100, 2)

    now = datetime.now()
    random_date = now - timedelta(days=randint(0, 365))
    opening_date_millis = int(random_date.timestamp() * 1000)

    return account_id, account_type, status, customer_id, balance, opening_date_millis

def generate_account_dim_data():
    for row_num in range(1, num_rows + 1):
        account_id, account_type, status, customer_id, balance, opening_date_millis = generate_random_data(row_num)
        account_ids.append(account_id)
        account_types.append(account_type)
        statuses.append(status)
        customer_ids.append(customer_id)
        balances.append(balance)
        opening_dates.append(opening_date_millis)

    # Create a DataFrame and save to CSV
    df = pd.DataFrame({
        'account_id': account_ids,
        'account_type': account_types,
        'status': statuses,
        'customer_id': customer_ids,
        'balance': balances,
        'opening_date': opening_dates
    })
    df.to_csv(output_file, index=False)
    print(f'CSV file {output_file} with {num_rows} rows has been generated successfully!')

# Define the DAG
with DAG(
    'account_dim_generator',  # The name of the DAG
    default_args=default_args,
    schedule_interval=timedelta(days=1),  
    start_date=start_date,
    catchup=False,
) as dag:

    start_task = EmptyOperator(
        task_id='start_task'
    )

    generate_task = PythonOperator(
        task_id='generate_account_dim_data',
        python_callable=generate_account_dim_data
    )

    # Set task dependencies
    start_task >> generate_task
