from gcs_helper import create_gcs_client, download_files_from_gcs
from bigquery_helper import create_client, gcs_to_bigquery

gcs_client = create_gcs_client()
bq_client = create_client()

gcs_uri = "gs://icanooo_gcs/neigbourhoods.csv"

result = gcs_to_bigquery(bq_client, gcs_uri, 'airbnb_bangkok', 'neighbourhood_test')
