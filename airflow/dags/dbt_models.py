from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator # type: ignore

with DAG('dbt_models',
         start_date=datetime(2024, 11, 8),
         description='Using dbt to create models',
         tags=['airbnb_euskadi'],
         schedule='@weekly',
         catchup=False) as dag:
    
    dimensional_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='dbt run --models neighbourhoods_table_dim --profiles-dir /opt/airflow/profiles --project-dir /opt/airflow/airbnb_euskadi'
    )

    dimensional_dbt