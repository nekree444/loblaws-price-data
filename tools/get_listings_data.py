import requests
import time

def get_listings_data(num_listings, page_num, store_id, store_banner):
    # Constants
    API_URL = 'https://api.pcexpress.ca/pcx-bff/api/v2/listingPage/27985'
    HEADERS = {
        'Accept-Language': 'en',
        'User-Agent': 'PC%20Express/202408011329 CFNetwork/1474 Darwin/23.0.0',
        'x-apikey': 'C1xujSegT5j3ap3yexJjqhOfELwGKYvz',
        'x-application-type': 'Web',
        'x-loblaw-tenant-id': 'ONLINE_GROCERIES',
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


if __name__ == '__main__':
    test = get_listings_data(5, 1, '1080', 'superstore')
    # print(test)

    print(test['layout']['sections']['productListingSection']['components'][0]['data']['productGrid'].keys())