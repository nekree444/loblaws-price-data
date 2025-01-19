from google.cloud import storage
import os

BUCKET_NAME = "price-data-storage"
KEY_PATH = "my_key.json"  # Path to your Google Cloud key

# Initialize Google Cloud Storage client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def get_folder_sizes(bucket_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = client.list_blobs(bucket_name)

    folder_sizes = {}

    for blob in blobs:
        folder_path = os.path.dirname(blob.name)
        if folder_path not in folder_sizes:
            folder_sizes[folder_path] = 0
        folder_sizes[folder_path] += blob.size

    for folder, size in folder_sizes.items():
        print(f"Folder: {folder}, Size: {size / (1024 * 1024):.2f} MB")

get_folder_sizes(BUCKET_NAME)