from google.cloud import storage, bigquery
import os, re
from loblaws_tools import get_week
week = get_week()
current_week = f"{week[0]}_{week[1]:02d}_{week[2]:02d}"

# Constants
BUCKET_NAME = "price-data-storage"
DATASET_ID = "datav1"
TABLE_ID = "prices"
MIN_SIZE_KB = 1
TIMEOUT = 300  

def initialize_clients():
    """Initialize and return Google Cloud Storage and BigQuery clients and bucket."""
    # # # For local development with .env
    # from dotenv import load_dotenv
    # load_dotenv()
    # KEY_PATH = os.getenv("KEY_PATH")
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
    
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    bq_client = bigquery.Client()
    return client, bucket, bq_client

client, bucket, bq_client = initialize_clients()

query = f"""
    SELECT DISTINCT banner, store_id, date
    FROM `{bq_client.project}.{DATASET_ID}.{TABLE_ID}`
"""
existing_combinations = {
    (row["banner"], str(row["store_id"]), row["date"].strftime("%Y-%m-%d"))
    for row in bq_client.query(query).result()
}

csvs = [
    blob for blob in bucket.list_blobs() 
    if blob.name.endswith('.csv') 
    and current_week in blob.name 
    and blob.size >= MIN_SIZE_KB * 1024  # converrt kb to bytes
]

table_ref = bq_client.dataset(DATASET_ID).table(TABLE_ID)

job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1  # skip header row
job_config.autodetect = False
job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

print(f"Found {len(csvs)} CSV files >= {MIN_SIZE_KB}KB")

filename_pattern = re.compile(r"listings_\d{4}_\d{2}_\d{2}/([^/]+)/\1_(\d{4})_(\d{4}_\d{2}_\d{2})\.csv")

for blob in csvs:
    match = filename_pattern.match(blob.name)
    if not match:
        print(f"Skipping {blob.name}: Filename format incorrect")
        continue
    
    banner, store_id, date_str = match.groups()
    formatted_date = date_str.replace("_", "-")
    
    if (banner, str(int(store_id)), formatted_date) in existing_combinations:
        print(f"Skipping {blob.name}: Data already in BigQuery")
        continue

    uri = f"gs://{BUCKET_NAME}/{blob.name}"
    print(f"Loading file: {blob.name} ({blob.size/1024:.1f}KB)")
    
    load_job = bq_client.load_table_from_uri(
        uri,
        table_ref,
        job_config=job_config
    )
    
    load_job.result(timeout=TIMEOUT)
    if load_job.error_result:
        print(f"Error loading {blob.name}: {load_job.error_result}")
        continue
    
    print(f"Successfully loaded {blob.name} ({blob.size/1024:.1f}KB)")