""" 
Go through every single store and get every single item
Go through each store 5 times in order to get every item inc some that might not show up on the first go around
We will do all stores in Ontario
'nofrills', 'valumart', 'independent', 'loblaw', 'wholesaleclub', 'rapid', 'zehrs', 'fortinos', 'independentcitymarket', 'extrafoods', 'superstore', 'provigo'
"""

from loblaws_tools import get_all_stores, get_product_grid, get_listings_data, stores_dict, get_week, upload_to_bucket, get_product_grid_search, get_listings_data_search, get_all_files
import time, csv, io, os
# from dotenv import load_dotenv
from google.cloud import storage


# Constants
LISTINGS_NUM = 275
BUCKET_NAME = "price-data-storage"

# Initialize Google Cloud Storage client
# load_dotenv()
# KEY_PATH = os.getenv("KEY_PATH")  # Path to your Google Cloud key
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def listings_runner(all_stores, current_week):
    for store_id, store_banner in all_stores.items():
        print('starting', store_id, store_banner)
        start = time.time()
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['id', 'brand', 'name', 'price', 'dealPrice'])
        holder = []  # this is for repeat product ids
        for _ in range(5):
            continues = 0  # tracks how many times there's an error or empty page; the fifth time we break
            for i in range(1, 500):  # no store has more than 500 pages of products
                errors = 0  # tracks how many times there was an error; if it goes over 3, we break
                while True:  # this loop is for catching errors
                    data = get_listings_data(LISTINGS_NUM, i, store_id, store_banner)
                    if 'errors' in data:
                        print("Error occurred, retrying...")
                        time.sleep(1)
                        errors += 1
                        if errors > 3:
                            break
                    else:
                        break
                if get_product_grid(data):  # if there are products on the page
                    for j in data['layout']['sections']['productListingSection']['components'][0]['data']['productGrid']['productTiles']:
                        if j['productId'] in holder:  # checks for duplicates
                            continue
                        if j['pricing']['wasPrice'] is None:  # deal pricing
                            price = j['pricing']['price']
                            dealPrice = None
                        else:
                            price = j['pricing']['wasPrice']
                            dealPrice = j['pricing']['price']

                        holder.append(j['productId']) 
                        writer.writerow([j['productId'], j['brand'], j['title'], price, dealPrice])  # write to memory
                    # print('wrote', i, 'holder length is', len(holder))
                else:  # if the data is invalid
                    # print('continuing...', str(data)[0:30])
                    continues += 1
                    if continues > 5:  # at 5 continues
                        break  # break if we've reached the max page
                    continue  # otherwise, continue

        # Upload the CSV data to the Google Cloud Storage bucket
        blob_name = f"listings_{current_week[0]}_{current_week[1]}_{current_week[2]}/{store_banner}/{store_banner}_{store_id}_{current_week[0]}_{current_week[1]}_{current_week[2]}.csv"
        upload_to_bucket(blob_name, csv_data, bucket)
        print(f"Time taken for store {store_id} is {time.time() - start} seconds")

def search_runner(all_stores, current_week):
    for store_id, store_banner in all_stores.items():
        print('starting', store_id, store_banner)
        start = time.time()
        csv_data = io.StringIO()
        writer = csv.writer(csv_data)
        writer.writerow(['id', 'brand', 'name', 'price', 'dealPrice'])
        holder = []  # this is for repeat product ids
        for _ in range(5):
            continues = 0  # tracks how many times there's an error or empty page; the fifth time we break
            for i in range(1, 500):  # no store has more than 500 pages of products
                errors = 0  # tracks how many times there was an error; if it goes over 3, we break
                while True:  # this loop is for catching errors
                    data = get_listings_data_search(LISTINGS_NUM, i, store_id, store_banner)
                    if 'errors' in data:
                        print("Error occurred, retrying...")
                        time.sleep(1)
                        errors += 1
                        if errors > 3:
                            break
                    else:
                        break
                if get_product_grid_search(data):  # if there are products on the page
                    if len(data['layout']['sections']['mainContentCollection']['components']) == 4:  # if there are 2 sections of products
                        product_tiles = data['layout']['sections']['mainContentCollection']['components'][0]['data']['productTiles']
                        product_tiles.extend(data['layout']['sections']['mainContentCollection']['components'][2]['data']['productTiles'])
                        for j in product_tiles:
                            if j['productId'] in holder:  # checks for duplicates
                                continue
                            if j['pricing']['wasPrice'] is None:  # deal pricing
                                price = j['pricing']['price']
                                dealPrice = None
                            else:
                                price = j['pricing']['wasPrice']
                                dealPrice = j['pricing']['price']

                            holder.append(j['productId']) 
                            writer.writerow([j['productId'], j['brand'], j['title'], price, dealPrice])  # write to memory
                        # print('wrote', i, 'holder length is', len(holder))
                    else:  # if there is only 1 section of products
                        break
                else:  # if the data is invalid
                    # print('continuing...', str(data)[0:30])
                    continues += 1
                    if continues > 5:  # at 5 continues
                        break  # break if we've reached the max page
                    continue  # otherwise, continue

        # Upload the CSV data to the Google Cloud Storage bucket
        blob_name = f"listings_{current_week[0]}_{current_week[1]}_{current_week[2]}/{store_banner}/{store_banner}_{store_id}_{current_week[0]}_{current_week[1]}_{current_week[2]}.csv"
        upload_to_bucket(blob_name, csv_data, bucket)
        print(f"Time taken for store {store_id} is {time.time() - start} seconds")

def ios_listings_runner():
    pass

def ios_search_runner():
    pass

if __name__ == "__main__":
    print('updated succesffuly')
    
    current_week = get_week()

    # all_stores = {'6720': 'wholesaleclub'} # only do one store for testing
    # all_stores = {'1080': 'superstore'} # only do one store for testing
    all_stores = stores_dict()

    done_stores = get_all_files(client, BUCKET_NAME, current_week)

    all_stores = {k: v for k, v in all_stores.items() if k not in done_stores}
    print(all_stores)

    # listings_runner(all_stores, current_week)

    search_runner(all_stores, current_week)