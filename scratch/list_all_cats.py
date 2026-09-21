import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')
url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=250'
req = urllib.request.Request(url, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    products = json.loads(res.read().decode())['data']

for p in sorted(products, key=lambda x: x['name']):
    cats = p.get('categories', [])
    vis = p.get('is_visible')
    print(f"ID: {p['id']:3d} | Vis: {str(vis):<5} | Cats: {str(cats):<16} | Name: {p['name']}")
