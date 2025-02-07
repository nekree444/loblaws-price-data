import requests, datetime

def get_all_stores():
    r = requests.get('https://www.loblaws.ca/api/pickup-locations')
    return r.json()

def get_product_grid(pages):
    if not pages:
        return None

    layout = pages.get('layout')
    if not layout:
        return None

    sections = layout.get('sections')
    if not sections:
        return None

    product_listing_section = sections.get('productListingSection')
    if not product_listing_section:
        return None

    components = product_listing_section.get('components')
    if not components:
        return None

    data = components[0].get('data')
    if not data:
        return None

    product_grid = data.get('productGrid')
    if not product_grid:
        return None

    product_tiles = product_grid.get('productTiles')
    if not product_tiles:
        return None

    if product_tiles:
        return True

def get_product_grid_search(pages):
    if not pages:
        return None

    layout = pages.get('layout')
    if not layout:
        return None

    sections = layout.get('sections')
    if not sections:
        return None

    product_listing_section = sections.get('mainContentCollection')
    if not product_listing_section:
        return None

    components = product_listing_section.get('components')
    if not components:
        return None

    data = components[0].get('data')
    if not data:
        return None

    product_tiles = data.get('productTiles')
    if not product_tiles:
        return None

    if product_tiles:
        return True

def get_listings_data(num_listings, page_num, store_id, store_banner):
    # Constants
    API_URL = 'https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/27985'
    HEADERS = {
        'User-Agent': 'PC%20Express/202408011329 CFNetwork/1474 Darwin/23.0.0',
        'Accept-Language': 'en',
        'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
        'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
        'x-application-type': 'Web',
        # 'x-application-type': 'ios',
    }


    json_data = {
            'cart': {
                'cartId': '7e853d0b-15d4-4947-b3f7-204a91491f4e',
            },
            'fulfillmentInfo': {
                'storeId': None,
                'pickupType': 'STORE',
                'offerType': 'OG',
                'date': '01012025',
                'timeSlot': None,
            },
            'listingInfo': {
                'filters': {},
                'sort': {},
                'pagination': {
                    'from': None,
                    'size': None,
                },
                'includeFiltersInResponse': True,
            },
            'banner': None,
            'userData': {
                'domainUserId': 'e716d4b1-1b04-4828-9ed8-f28fa19fc34b',
                'sessionId': '266369e4-c959-4a5d-abd9-fd84707c1a32',
            },
        }
    
    # script

    json_data['listingInfo']['pagination']['size'] = num_listings
    json_data['listingInfo']['pagination']['from'] = page_num
    json_data['fulfillmentInfo']['storeId'] = store_id
    json_data['banner'] = store_banner
    # start = time.time()
    try:
        r = requests.post(API_URL, headers=HEADERS, json=json_data)
        return r.json()
    except:
        return ['errors']

def get_listings_data_search(num_listings, page_num, store_id, store_banner):
    # Constants
    API_URL = 'https://api.pcexpress.ca/pcx-bff/api/v2/products/search'
    HEADERS = {
        'User-Agent': 'PC%20Express/202408011329 CFNetwork/1474 Darwin/23.0.0',
        'Accept-Language': 'en',
        'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
        'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
        'x-application-type': 'Web',
        # 'x-application-type': 'ios',
    }


    json_data = {
            'cart': {
                'cartId': '7e853d0b-15d4-4947-b3f7-204a91491f4e',
            },
            'fulfillmentInfo': {
                'storeId': None,
                'pickupType': 'STORE',
                'offerType': 'OG',
                'date': '01012025',
                'timeSlot': None,
            },
            'listingInfo': {
                'filters': {
                    'category': [
                        '27985',
                    ],
                },
                'pagination': {
                    'from': None,
                    'size': None,
                },
                'includeFiltersInResponse': True,
            },
            'banner': None,
            'userData': {
                'domainUserId': 'e716d4b1-1b04-4828-9ed8-f28fa19fc34b',
                'sessionId': '266369e4-c959-4a5d-abd9-fd84707c1a32',
            },
            'searchRelatedInfo': {
                'term': 'food',
            },
        }
    
    # script

    json_data['listingInfo']['pagination']['size'] = num_listings
    json_data['listingInfo']['pagination']['from'] = page_num
    json_data['fulfillmentInfo']['storeId'] = store_id
    json_data['banner'] = store_banner
    # start = time.time()
    try:
        r = requests.post(API_URL, headers=HEADERS, json=json_data)
        return r.json()
    except:
        return ['errors']

def upload_to_bucket(blob_name, file_data, bucket):
    """Uploads a string data as a file to the Google Cloud Storage bucket."""
    try:
        blob = bucket.blob(blob_name)
        blob.upload_from_string(file_data.getvalue(), content_type='text/csv')
        print(f"Uploaded {blob_name}")
    except:
        print(f"Error uploading {blob_name}")

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

def get_all_files(client, bucket_name, current_week):
    blobs = client.list_blobs(bucket_name)
    temp = [i.name.split('/')[-1].split('_')[1] for i in blobs if f"listings_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}" in i.name]
    return temp