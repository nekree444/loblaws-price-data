""" 
Go through every single store and get every single item
Go through each store 5 times in order to get every item inc some that might not show up on the first go around
We will do all stores in Ontario
"""
from loblaws_tools import (
    stores_dict,
    get_product_grid,
    get_listings_data,
    get_week,
    upload_to_bucket,
    get_all_files,
    get_products_list,
    process_product_data
)
import time, csv, io, os
from google.cloud import storage


# Constants
LISTINGS_NUM = 250
BUCKET_NAME = "price-data-storage1"
MAX_RETRIES = 3
MAX_PAGES = 500
PASSES_PER_STORE = 5

def initialize_storage_client():
    """Initialize and return Google Cloud Storage client and bucket."""
    # Uncomment for local development with .env
    # from dotenv import load_dotenv
    # load_dotenv()
    # KEY_PATH = os.getenv("KEY_PATH")
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
    
    client = storage.Client()
    return client, client.bucket(BUCKET_NAME)

client, bucket = initialize_storage_client()

def runner(all_stores, current_week, mode):
    for store_id, store_banner in all_stores.items():
        print('starting', store_id, store_banner)
        start = time.time()

        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['id', 'brand', 'name', 'price', 'deal_price', 'store_id', 'banner', 'date', 'package_size'])
        holder = [] # this is for repeat product ids
        for _ in range(PASSES_PER_STORE):
            empty_page_count = 0  # tracks how many times there's an error or empty page; the fifth time we break
            for i in range(1, MAX_PAGES):  # no store has more than 500 pages of products
                # print(i) # testing
                errors = 0  # tracks how many times there was an error; if it goes over 3, we break
                while True:  # this loop is for catching errors
                    if store_banner == 'rapid':
                        data = get_listings_data(225, i, store_id, store_banner, mode=mode)
                    else:
                        data = get_listings_data(LISTINGS_NUM, i, store_id, store_banner, mode=mode)
                    if 'errors' in data:
                        print("Error occurred, retrying...")
                        time.sleep(1)
                        errors += 1
                        if errors > MAX_RETRIES:
                            break
                    else:
                        break
                if not get_product_grid(data, mode=mode):
                    empty_page_count += 1
                    if empty_page_count > 5:
                        break
                    continue
                
                # Check if there are multiple product sections
                products = get_products_list(data, mode=mode)
                
                if products == None:
                    break
                
                for product in products:
                    row = process_product_data(product, holder, store_banner, store_id, current_week)
                    if row:
                        # print(row[2]) # testing
                        writer.writerow(row)

        # Upload the CSV data to the Google Cloud Storage bucket
        blob_name = f"listings_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}/{store_banner}/{store_banner}_{store_id}_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}.csv"
        upload_to_bucket(blob_name, csv_data, bucket)
        # print(blob_name)
        print(f"Time taken for store {store_id} is {time.time() - start} seconds")

def main():
    print('starting...')
    
    # current_week = [2025,4,7]
    current_week = get_week()

    # all_stores = {'6720': 'wholesaleclub'} # only do one store for testing
    # all_stores = {'1024': 'superstore'} # only do one store for testing
    # all_stores = {'1095': 'loblaw'} # only do one store for testing
    all_stores = stores_dict()

    done_stores = get_all_files(client, BUCKET_NAME, current_week)

    all_stores = {k: v for k, v in all_stores.items() if k not in done_stores}
    print(all_stores)
    print(len(done_stores), 'stores done')
    print(len(all_stores.keys()), 'stores left')

    runner(all_stores, current_week, 'listings')
    # runner(all_stores, current_week, 'search')

if __name__ == "__main__":
    main()