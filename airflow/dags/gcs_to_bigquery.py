from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator # type: ignore
from helper.gcs_helper import create_gcs_client
from helper.bigquery_helper import create_bq_client, load_csv_bucket_to_bigquery

def gcs_to_bigquery():
    gcs_client = create_gcs_client()
    bq_client = create_bq_client()

    load_csv_bucket_to_bigquery(gcs_client, bq_client, 'icanooo_gcs', 'airbnb_euskadi')
    

with DAG('airbnb_euskadi_bqload',
         start_date=datetime(2024, 11, 8),
         description='DAG to load nba table to Bigquery',
         tags=['airbnb_euskadi'],
         schedule='@weekly',
         catchup=False) as dag:

    load_gcs_csv = PythonOperator(task_id='csv_gcs_to_bigQuery', python_callable=gcs_to_bigquery)

    load_gcs_csv