""" 
now we go through every document within every folder within listings
we get the nutritional data as a json for each product and save the data to the nutrition data oflder
if the product already has a json file we skip it 
"""
import requests, os, json, csv

# constants
HEADERS = {
    'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
    'User-Agent': 'PC%20Express/202408011329 CFNetwork/1474 Darwin/23.0.0',
}

s = requests.Session()

params = {
    'lang': 'en',
    'date': '01012025',
    'storeId': None,
    'banner': None,
    'pickupType': 'STORE',
}

os.makedirs('nutrition_data', exist_ok=True)

def get_nutrition_data(product_id, store_id, store_banner):
    params['storeId'] = str(store_id)
    params['banner'] = str(store_banner)
    r = requests.get(f'https://api.pcexpress.ca/pcx-bff/api/v1/products/{product_id}', params=params, headers=HEADERS)
    if 'nutritionFacts' in r.json().keys():
        with open(f"nutrition_data/{product_id}.json", "w", encoding="utf-8") as f:
            json.dump(r.json()['nutritionFacts'], f, ensure_ascii=False, indent=4)
            print(f"wrote {product_id}")

for root, dirs, files in os.walk('listings'):
    for file in files:
        if file.endswith('.csv'):
            store_banner, store_id, *_ = file.split('_')
            with open(os.path.join(root, file), newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    product_id = row['id']
                    if not os.path.exists(f'nutrition_data/{product_id}.json'):
                        get_nutrition_data(product_id, store_id, store_banner)
                    else:
                        print(f"Skipping {product_id}, already exists.")