from google.cloud import bigquery
from google.auth import default
import pandas as pd
from helper.gcs_helper import get_file_list
import re

#Creating client
def create_bq_client():
    scopes=["https://www.googleapis.com/auth/cloud-platform"]

    credentials, _ = default(scopes=scopes)

    client = bigquery.Client(credentials=credentials)

    return client

#reading data from bigquery
def read_bigquery(client, what_to_query):
    df = client.query(what_to_query).result().to_dataframe()

    return df

# Function to help to create schema based on pandas column datatype
def create_schema(dataframe):
    schema = []
    for col in dataframe.columns:
        dtype = dataframe[col].dtype

        if pd.api.types.is_integer_dtype(dtype):
            field_type = "INT64"
        elif pd.api.types.is_float_dtype(dtype):
            field_type = "FLOAT64"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            field_type = "TIMESTAMP"         

        mode = "REQUIRED" if dataframe[col].notna().all() else "NULLABLE"

        if pd.api.types.is_object_dtype(dtype):
            field_type = "STRING"

            mode = "NULLABLE"

        schema.append(bigquery.SchemaField(col, field_type, mode=mode))

    return schema


# Creating table
def create_table(client, table_id, schema, partition_col=None):
    try:
        table = bigquery.Table(table_ref=table_id, schema=schema)

        if partition_col:
            table.time_partitioning = bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field=partition_col
            )            

        client.create_table(table)
        print("Loaded table to bigQuery! ")
    except:
        client.get_table(table_id)
        print(f"Table `{table_id}` already exist")


# Loading data to bigQuery
def load_bigquery(client, dataframe, table_id, mode, partition_field=None):
    # Akan print table already exist jika ada
    create_table(client, table_id, create_schema(dataframe), partition_field)

    job_config = bigquery.LoadJobConfig(
        schema = create_schema(dataframe),
        write_disposition=mode,
    )

    if partition_field:
        job_config.time_partitioning = bigquery.TimePartitioning(
            field=partition_field
        )

    job = client.load_table_from_dataframe(
        dataframe, table_id, job_config=job_config
    )
    job.result()

# functions to drop table
def drop_table(client, table_id):
    client.delete_table(table_id, not_found_ok=True)

    print(f"Deleted table `{table_id}`.")

def gcs_to_bigquery(client, gcs_uri, dataset_id, table):
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        skip_leading_rows=1,
        max_bad_records=500
    )

    load_job = client.load_table_from_uri(
        gcs_uri, dataset_id + '.' + table, job_config=job_config
    )

    result = load_job.result()

    print(f"Succesfully load to {gcs_uri} to bigquery")

    return result

def load_csv_bucket_to_bigquery(gcs_client, bq_client, gcs_bucket, dataset_id):
    filelist = get_file_list(gcs_client, gcs_bucket)

    for filename in filelist:
        if '.csv' in filename:
            gcs_uri = f"gs://{gcs_bucket}/{filename}"

            match = re.search(r'([^\/]+)(?=\.[^.]+$)', filename)
            table = match.group(0)
            table_id = table + '_table_source'

            gcs_to_bigquery(bq_client, gcs_uri, dataset_id, table_id)


