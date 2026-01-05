import json, time, os, requests
import pandas as pd
from datetime import datetime
from empire_tools import (
    get_all_files,
    get_week,
    stores_dict,
    upload_to_bucket
)
# from dotenv import load_dotenv
# load_dotenv('.env')

API_KEY = os.getenv("NEKREE_API_KEY")
URL = "https://acsyshf8au-dsn.algolia.net/1/indexes/dxp_product_en/browse?x-algolia-api-key=0ce0f3a3186b11f7c4b53d7a13e15d43&x-algolia-application-id=ACSYSHF8AU"

def main():
    print('starting empire...')
    current_timestamp = int(datetime.now().timestamp())
    current_week = [int(i) for i in get_week()]
    json_data = {
        "hitsPerPage": 1000,
        "filters": "isVisible:true AND isMassOffers:false",
        "page": 0,
        "attributesToRetrieve": ["name", "price", "storeId", "updatedAt", "articleNumber", "uom", "brand", "itemAmountValue", "itemAmountUnit", "promotions.startDate", "promotions.endDate", "promotions.source", "promotions.promotionReward.value1Value20.value_1", "upc"],
        "attributesToHighlight": [],
    }
    done_stores = get_all_files(API_KEY, current_week)
    all_stores = stores_dict()

    all_stores = {k: v for k, v in all_stores.items() if k not in done_stores}
    print(all_stores)
    print(len(done_stores), 'stores done')
    print(len(all_stores.keys()), 'stores left')
    
    header = ["id", "brand", "name", "price", "deal_price", "store_id", "banner", "date", "package_size", "upc"]
    for store_id, banner in all_stores.items():
        if store_id in done_stores:
            print(f"done {store_id}")
            continue
        rows = []
        while True:
            json_data['filters'] = f"storeId:{store_id} AND isVisible:true AND isMassOffers:false"
            start = time.time()
            data = json.dumps(json_data)
            r = requests.post(URL,headers={'Referer': 'https://apis.dxp.sobeys.com',},data=data)
            try:
                hits = r.json()['hits']
                for i in hits:
                    row = [f'{i.get("articleNumber")}_{i.get("uom")}', i.get("brand"), i.get("name"), i.get("price"), None, i.get('storeId'), banner, "-".join([str(i) for i in current_week]), f'{i.get("itemAmountValue")} {i.get("itemAmountUnit")}', None if i.get("upc") == None else i.get("upc").split(",")]
                    if i.get('promotions'):
                        for j in i['promotions']:
                            if j.get('startDate') < current_timestamp and j.get('endDate') > current_timestamp and (j.get('source') == 'ZEDL' or j.get('source') == 'VKA0'):
                                row[4] = [k for k in j['promotionReward'][0]['value1Value20'][0].values() if k != ""][0]
                    rows.append(row)
                print("done", json_data['page'])
                json_data['page'] += 1
                json_data['cursor'] = r.json().get('cursor')
            except Exception as e:
                print(e)
                break
            print(time.time() - start)

        df = pd.DataFrame(rows, columns=header)
        print("donedf", store_id)
        df = df.to_csv(index=False)
        blob_name = f"price-data-storage-empire/listings_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}/{banner}/{banner}_{store_id}_{current_week[0]}_{current_week[1]:02d}_{current_week[2]:02d}.csv"
        result = upload_to_bucket(blob_name, df, key=API_KEY)
        if result == 1:
            print(f"Uploaded {blob_name}")
        if result == 0:
            for _ in range(10):
                result = upload_to_bucket(blob_name, df, key=API_KEY)
                if result == 1:
                    print(f"Uploaded {blob_name}")
                    break
        json_data = {
            "hitsPerPage": 1000,
            "filters": "isVisible:true AND isMassOffers:false",
            "page": 0,
            "attributesToRetrieve": ["name", "price", "storeId", "updatedAt", "articleNumber", "uom", "brand", "itemAmountValue", "itemAmountUnit", "promotions.startDate", "promotions.endDate", "promotions.source", "promotions.promotionReward.value1Value20.value_1", "upc"],
            "attributesToHighlight": [],
        }

if __name__ == "__main__":
    main()