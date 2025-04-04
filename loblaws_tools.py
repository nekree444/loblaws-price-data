import requests, datetime

def get_product_grid(pages, mode):
    """validates product grid of either listings or search

    Args:
        pages (dict): json data of the call
        mode (str): search or listings

    Returns:
        True if product grid is present, None otherwise
    """
    if mode == 'listings':
        if not pages:
            return None
        
        if type(pages) != dict:
            print(pages)
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
    elif mode == 'search':
        if not pages:
            return None
        
        if type(pages) != dict:
            print(pages)
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

def get_listings_data(num_listings, page_num, store_id, store_banner, mode):
    """get the json data of listings/search for all food

    Args:
        num_listings (int): number of listings per page
        page_num (int): page number offset
        store_id (str/int): store id
        store_banner (str): store banner
        mode (str): search or listings

    Returns:
        dict: json data of listings/search for all food
    """
    if mode == 'listings':
        API_URL = 'https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/27985'
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
    
    elif mode == 'search':
        API_URL = 'https://api.pcexpress.ca/pcx-bff/api/v2/products/search'
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
    
    # Constants
    HEADERS = {
        'User-Agent': 'PC%20Express/202408011329 CFNetwork/1474 Darwin/23.0.0',
        'Accept-Language': 'en',
        'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
        'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
        'x-application-type': 'Web',
        # 'x-application-type': 'ios',
    }
    # script
    json_data['listingInfo']['pagination']['size'] = num_listings
    json_data['listingInfo']['pagination']['from'] = page_num
    json_data['fulfillmentInfo']['storeId'] = str(store_id)
    json_data['banner'] = store_banner
    try:
        r = requests.post(API_URL, headers=HEADERS, json=json_data)
        return r.json()
    except:
        return ['errors']

def upload_to_bucket(blob_name, file_data, bucket):
    """uploads file to bucket

    Args:
        blob_name (str): name of the blob inc path
        file_data (str): csv data of file to be uploaded
        bucket (bucket): bucket object
    """
    try:
        blob = bucket.blob(blob_name)
        blob.upload_from_string(file_data.getvalue(), content_type='text/csv')
        print(f"Uploaded {blob_name}")
    except:
        print(f"Error uploading {blob_name}")

def stores_dict():
    """get all loblaws brand stores in Ontario that are shoppable

    Returns:
        dict: store_id: store_banner
    """
    temp = requests.get('https://www.loblaws.ca/api/pickup-locations').json()
    temp = [i for i in temp if i['address']['region'] == 'Ontario' and i['isShoppable'] == True]
    unique_stores = {i['storeId']: i['storeBannerId'] for i in temp}
    return unique_stores # in format {store_id: store_banner}

def get_week():
    """gets the current week

    Returns:
        list: [year, month, day] of the current week ints
    """
    today = datetime.datetime.today()
    offset = (today.weekday() - 3) % 7  # 3 corresponds to Thursday
    last_thursday = today - datetime.timedelta(days=offset)
    return [last_thursday.year, last_thursday.month, last_thursday.day]

def get_all_files(client, bucket_name, current_week):
    """get all files in the bucket that are for the current week (used for checking if a store has already been scraped)

    Args:
        client (client): client object
        bucket_name (str): name of the bucket
        current_week (list): [year, month, day] of the current week ints (current_week fcn)

    Returns:
        list: list of store banners that have already been scraped
    """
    blobs = client.list_blobs(bucket_name)
    temp = [i.name.split('/')[-1].split('_')[1] for i in blobs if f"listings_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}" in i.name]
    return temp

def get_products_list(data, mode):
    """get the list of products from the json data (listings or search)

    Args:
        data (dict): json data of the call
        mode (str): search or listings

    Returns:
        dict: list of products or None
    """
    if mode == 'listings':
        return data['layout']['sections']['productListingSection']['components'][0]['data']['productGrid']['productTiles']
    elif mode == 'search':
        components = data['layout']['sections']['mainContentCollection']['components']
        if len(components) == 4:  # Two sections of products
            products = components[0]['data']['productTiles']
            products.extend(components[2]['data']['productTiles'])
            return products
        else:
            return None
        
def process_product_data(product, holder, store_banner, store_id, current_week):
    """processes one product and returns a row for the csv

    Args:
        product (dict): json data of the product
        holder (list): list of product ids that have already been scraped
        store_banner (str): store banner
        store_id (str): store id
        current_week (list): [year, month, day] of the current week ints (current_week fcn)

    Returns:
        list: row for the csv or None if the product has already been scraped
    """
    if product['productId'] in holder:
        return None
        
    # Determine pricing (regular vs deal price)
    package_size = None
    if 'packageSizing' in product:
        package_size = product['packageSizing']
    if product['pricing']['wasPrice'] is None:
        price = product['pricing']['price']
        deal_price = None
    else:
        price = product['pricing']['wasPrice']
        deal_price = product['pricing']['price']
    
    holder.append(product['productId'])
    # print('skipped')
    return [product['productId'], product['brand'], product['title'], price, deal_price, store_id, store_banner, f"{current_week[0]}-{current_week[1]:02d}-{current_week[2]:02d}", package_size]
