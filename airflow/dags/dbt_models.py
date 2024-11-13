from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator # type: ignore

dbt_tail = " --profiles-dir /opt/airflow/profiles --project-dir /opt/airflow/airbnb_euskadi"
dbt_1 = "dbt run --models neighbourhoods_table_dim listings_table_dim reviews_table_fct" + dbt_tail
dbt_2 = "dbt run --models host_table_dim" + dbt_tail
dbt_3 = "dbt run --models neighbourhood_reviews_mart" + dbt_tail

# I use nvim btw
# Sometimes

with DAG('dbt_models',
         start_date=datetime(2024, 11, 12),
         description='Using dbt to create models',
         tags=['airbnb_euskadi'],
         schedule='@weekly',
         catchup=False) as dag:
    
    cleansing_dbt = BashOperator(
        task_id='cleansing_tables',
        bash_command=dbt_1
    )

    new_model_dbt = BashOperator(
        task_id='creating_new_models',
        bash_command=dbt_2
    )

    mart = BashOperator(
        task_id='creating_data_marts',
        bash_command=dbt_3
    )


    [new_model_dbt, mart]