import os, json, requests
from datetime import datetime, timedelta
# from dotenv import load_dotenv
# load_dotenv('.env')

API_UPLOAD=os.getenv("NEKREE_API_UPLOAD")
API_FILES = os.getenv("NEKREE_API_FILES")

def get_all_files(key, current_week):
    data = requests.get(f"{API_FILES}?key={key}&date={current_week[0]}-{current_week[1]:02d}-{current_week[2]:02d}&mode=prices&company=empire").json()
    if len(data) == 0:
        return []
    else:
        return [i.split("_")[1] for i in data]

def get_week():
    today = datetime.today()
    offset = (today.weekday() - 3) % 7
    last_thursday = today - timedelta(days=offset)
    return [last_thursday.year, last_thursday.month, last_thursday.day]

def stores_dict():
    headers = {'Referer': 'https://apis.dxp.sobeys.com'}

    params = {"x-algolia-api-key": "0ce0f3a3186b11f7c4b53d7a13e15d43","x-algolia-application-id": "ACSYSHF8AU"}

    data = json.dumps({
        "hitsPerPage": 1000,
        "page": 0,
        "attributesToRetrieve": ["bannerCode"],
        "attributesToHighlight": [],
    })

    r = requests.post('https://acsyshf8au-dsn.algolia.net/1/indexes/dxp_stores/browse',headers=headers,data=data,params=params)
    return {i['objectID']: i['bannerCode'][0] for i in r.json()['hits']}

def upload_to_bucket(filename, data, key):
    try:
        json_data = {
            "key": key,
            "filename": filename,
            "data": data,
        }
        result = requests.post(API_UPLOAD, json=json_data).json()
        return result["success"]
    except:
        print(f"Error uploading {filename}")
        return 0

if __name__ == "__main__":
    print(stores_dict())