import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

for pid in [132, 155]:
    url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/{pid}'
    req = urllib.request.Request(url, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
    with urllib.request.urlopen(req) as res:
        p = json.loads(res.read().decode())['data']
        print(f"Product {pid}: {p['name']}")
        print(f"  Categories: {p.get('categories')}")
