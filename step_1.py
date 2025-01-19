""" 
Go through every single store and get every single item
Go through each store 5 times in order to get every item inc some that might not show up on the first go around
We will do all stores in Ontario
'nofrills', 'valumart', 'independent', 'loblaw', 'wholesaleclub', 'rapid', 'zehrs', 'fortinos', 'independentcitymarket', 'extrafoods', 'superstore', 'provigo'
"""

from tools.loblaws_tools import get_product_grid
from tools.get_listings_data import get_listings_data
from tools.all_stores_getter import get_all_stores
import time, datetime, csv, io, os
from google.cloud import storage

# Constants
LISTINGS_NUM = 275
BUCKET_NAME = os.getenv("BUCKET_NAME")
# KEY_PATH = os.getenv("GCP_SA_KEY")  # Path to your Google Cloud key

# Initialize Google Cloud Storage client
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_PATH
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

def upload_to_bucket(blob_name, file_data):
    """Uploads a string data as a file to the Google Cloud Storage bucket."""
    blob = bucket.blob(blob_name)
    blob.upload_from_string(file_data.getvalue(), content_type='text/csv')
    print(f"Uploaded {blob_name}")

def stores_dict():
    temp = get_all_stores()
    temp = [i for i in temp if i['address']['region'] == 'Ontario']
    unique_stores = {i['storeId']: i['storeBannerId'] for i in temp}
    return unique_stores # in format {store_id: store_banner}

def get_week():
    today = datetime.datetime.today()
    offset = (today.weekday() - 3) % 7  # 3 corresponds to Thursday
    last_thursday = today - datetime.timedelta(days=offset)
    return [last_thursday.year, last_thursday.month, last_thursday.day]

if __name__ == "__main__":
    print('updated succesffuly')

    # for store_id, store_banner in all_stores.items():
    # all_stores = stores_dict()

    # # all_stores = {'1080': 'superstore'} # only do one store for testing

    # current_week = get_week()

    # for store_id, store_banner in all_stores.items():
    #     print('starting', store_id, store_banner)
    #     start = time.time()
    #     csv_data = io.StringIO()
    #     writer = csv.writer(csv_data)
    #     writer.writerow(['id', 'brand', 'name', 'price', 'dealPrice'])
    #     holder = []  # this is for repeat product ids
    #     continues = 0  # tracks how many times there's an error or empty page; the fifth time we break
    #     for i in range(1, 500):  # no store has more than 500 pages of products
    #         errors = 0  # tracks how many times there was an error; if it goes over 3, we break
    #         while True:  # this loop is for catching errors
    #             data = get_listings_data(LISTINGS_NUM, i, store_id, store_banner)
    #             if 'errors' in data:
    #                 print("Error occurred, retrying...")
    #                 time.sleep(1)
    #                 errors += 1
    #                 if errors > 3:
    #                     break
    #             else:
    #                 break
    #         if get_product_grid(data):  # if there are products on the page
    #             for j in data['layout']['sections']['productListingSection']['components'][0]['data']['productGrid']['productTiles']:
    #                 if j['productId'] in holder:  # checks for duplicates
    #                     continue
    #                 if j['pricing']['wasPrice'] is None:  # deal pricing
    #                     price = j['pricing']['price']
    #                     dealPrice = None
    #                 else:
    #                     price = j['pricing']['wasPrice']
    #                     dealPrice = j['pricing']['price']

    #                 holder.append(j['productId']) 
    #                 writer.writerow([j['productId'], j['brand'], j['title'], price, dealPrice])  # write to memory
    #             # print('wrote', i, 'holder length is', len(holder))
    #         else:  # if the data is invalid
    #             # print('continuing...', str(data)[0:30])
    #             continues += 1
    #             if continues > 5:  # at 5 continues
    #                 break  # break if we've reached the max page
    #             continue  # otherwise, continue

    #     # Upload the CSV data to the Google Cloud Storage bucket
    #     blob_name = f"listings_{current_week[0]}_{current_week[1]}_{current_week[2]}/{store_banner}/{store_banner}_{store_id}_{current_week[0]}_{current_week[1]}_{current_week[2]}.csv"
    #     upload_to_bucket(blob_name, csv_data)
    #     print(f"Time taken for store {store_id} is {time.time() - start} seconds")