from google.cloud import storage, bigquery
import requests, time
from loblaws_tools import get_product_details

BUCKET_NAME = "nutrition-data-storage1"

def initialize_clients():
    """Initialize and return Google Cloud Storage and BigQuery clients and bucket."""
    # # # For local development with .env
    # from dotenv import load_dotenv
    # import os
    # load_dotenv()
    # KEY_PATH = os.getenv("KEY_PATH")
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    bq_client = bigquery.Client()
    return client, bucket, bq_client

client, bucket, bq_client = initialize_clients()

def main():
    holder = [i.name.split('.')[0] for i in bucket.list_blobs()]

    query = f"""
        SELECT id, store_id, banner
        FROM (
        SELECT 
            id, 
            store_id, 
            banner, 
            ROW_NUMBER() OVER (PARTITION BY id ORDER BY date DESC) AS rn
        FROM `{bq_client.project}.datav1.prices`
        )
        WHERE rn = 1
        AND id NOT IN UNNEST({str(holder)})
    """

    result = bq_client.query(query).result()

    for n, i in enumerate(result):
        data = get_product_details(i[0], i[1], i[2])
        if data is not None:
            blob = bucket.blob(f"{i[0]}.json")
            print('uploading', i[0])
            blob.upload_from_string(data, content_type='application/json', timeout=300)
            print('uploaded', i[0])
        else:
            #print('error')
            continue

if __name__ == "__main__":
    main()