from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator # type: ignore

dbt_tail = " --profiles-dir /opt/airflow/profiles --project-dir /opt/airflow/airbnb_euskadi"
dbt_1 = "dbt run --models neighbourhoods_table_dim listing_table-dims review_table_facts" + dbt_tail
dbt_2 = "dbt run --models host_table_dims" + dbt_tail

with DAG('dbt_models',
         start_date=datetime(2024, 11, 8),
         description='Using dbt to create models',
         tags=['airbnb_euskadi'],
         schedule='@weekly',
         catchup=False) as dag:
    
    cleansing_dbt = BashOperator(
        task_id='cleansing_tables',
        bash_command=dbt_1
    )

    new_model_dbt = BashOperator(
        task_id='creating models based on cleansed table',
        bash_command=dbt_2
    )


    cleansing_dbt >> new_model_dbt