from gcs_helper import create_gcs_client, download_files_from_gcs, get_file_list
from bigquery_helper import create_client, gcs_to_bigquery, load_csv_bucket_to_bigquery
import re

gcs_client = create_gcs_client()
bq_client = create_client()

# gcs_uri = "gs://icanooo_gcs/neighbourhoods.csv"

# result = gcs_to_bigquery(bq_client, gcs_uri, 'airbnb_bangkok', 'neighbourhood_test')

load_csv_bucket_to_bigquery(gcs_client, bq_client, 'icanooo_gcs', 'airbnb_bangkok')