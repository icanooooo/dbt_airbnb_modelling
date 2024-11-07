from google.cloud import storage

def create_gcs_client():
    client = storage.Client()

    return client

def download_files_from_gcs(client, bucket, blob, filename):
    gcs_bucket = client.bucket(bucket)

    gcs_blob = gcs_bucket.blob(blob)

    gcs_blob.download_to_filename(filename)

    print(f"Downloaded {gcs_blob} as {filename}")

