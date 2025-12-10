""" 
Go through every single store and get every single item
Go through each store 5 times in order to get every item inc some that might not show up on the first go around
We will do all stores in Ontario
"""
from loblaws_tools import (
    stores_dict,
    get_week,
    upload_to_bucket,
    get_all_files,
    store_to_csv_data,
)
import time, os
# from dotenv import load_dotenv
# load_dotenv('.env')

API_KEY = os.getenv("NEKREE_API_KEY")

def runner(all_stores, current_week, mode):
    for store_id, store_banner in all_stores.items():
        print('starting', store_id, store_banner)
        start = time.time()

        csv_data = store_to_csv_data(store_banner, store_id, current_week, mode=mode)

        blob_name = f"listings_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}/{store_banner}/{store_banner}_{store_id}_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}.csv"
        result = upload_to_bucket(blob_name, csv_data, key=API_KEY)
        if result == 1:
            print(f"Uploaded {blob_name}")
        if result == 0:
            for _ in range(10):
                result = upload_to_bucket(blob_name, csv_data, key=API_KEY)
                if result == 1:
                    print(f"Uploaded {blob_name}")
                    break
        # print(blob_name)
        print(f"Time taken for store {store_id} is {time.time() - start} seconds")

def main():
    print('starting...')
    
    current_week = [2025,12,9]
    # current_week = get_week()

    # all_stores = {'6720': 'wholesaleclub'} # only do one store for testing
    # all_stores = {'1024': 'superstore'} # only do one store for testing
    # all_stores = {'1095': 'loblaw'} # only do one store for testing
    all_stores = {'6748': 'independent'} # only do one store for testing
    # all_stores = stores_dict()

    done_stores = get_all_files(current_week, key=API_KEY)

    all_stores = {k: v for k, v in all_stores.items() if k not in done_stores}
    print(all_stores)
    print(len(done_stores), 'stores done')
    print(len(all_stores.keys()), 'stores left')

    # runner(all_stores, current_week, 'listings')
    runner(all_stores, current_week, 'search')

if __name__ == "__main__":
    main()