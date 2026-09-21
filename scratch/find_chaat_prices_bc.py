import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

print("=== Checking all v2/pages for Chaat prices ===")
url_pages = f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages'
req = urllib.request.Request(url_pages, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    pages = json.loads(res.read().decode())

for p in pages:
    body = p.get('body', '')
    if '$8.50' in body or '$7.99' in body or 'Samosa Chaat' in body:
        print(f"Match in Page ID {p['id']} | Name: {p.get('name')} | URL: {p.get('url')}")

print("\n=== Checking all categories for Chaat prices ===")
url_cats = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=250'
req = urllib.request.Request(url_cats, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    cats = json.loads(res.read().decode())['data']

for c in cats:
    desc = c.get('description', '')
    if '$8.50' in desc or '$7.99' in desc or 'Samosa Chaat' in desc:
        print(f"Match in Category ID {c['id']} | Name: {c.get('name')} | URL: {c.get('custom_url', {}).get('url')}")
