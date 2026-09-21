import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

def update_product_categories(pid, new_categories):
    url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/{pid}'
    data = json.dumps({"categories": new_categories}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'X-Auth-Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }, method='PUT')
    with urllib.request.urlopen(req) as res:
        updated = json.loads(res.read().decode())['data']
        print(f"Success! Product {pid} '{updated['name']}' categories now: {updated['categories']}")

# Update 132: Khoya Kalakand -> [3, 8]
update_product_categories(132, [3, 8])

# Update 155: Sweets Basket Assortment -> [3, 8, 14, 20]
update_product_categories(155, [3, 8, 14, 20])
