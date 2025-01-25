import requests

def get_all_stores():
    r = requests.get('https://www.loblaws.ca/api/pickup-locations')
    return r.json()

if __name__ == '__main__':
    print(len(get_all_stores()))