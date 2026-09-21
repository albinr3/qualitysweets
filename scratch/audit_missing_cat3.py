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

url_cat = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=250'
req_cat = urllib.request.Request(url_cat, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req_cat) as res:
    categories = {c['id']: c['name'] for c in json.loads(res.read().decode())['data']}

print("Categories mapping:", categories)
print("\n=== Products without Category 3 (All Indian Sweets) ===")
for p in sorted(products, key=lambda x: x['name']):
    cats = p.get('categories', [])
    if 3 not in cats:
        cat_names = [f"{c}:{categories.get(c, 'Unknown')}" for c in cats]
        print(f"ID {p['id']:3d} | Vis: {str(p.get('is_visible')):<5} | Cats: {str(cat_names):<45} | Name: {p['name']}")
