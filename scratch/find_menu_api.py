import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

print("=== 1. Checking Content Pages (/v3/content/pages) ===")
url_pages = f'https://api.bigcommerce.com/stores/{store_hash}/v3/content/pages?limit=250'
req = urllib.request.Request(url_pages, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    pages = json.loads(res.read().decode())['data']

for p in pages:
    print(f"Page ID {p['id']} | URL: {p.get('url')} | Name: {p.get('name')} | Type: {p.get('type')}")

print("\n=== 2. Checking Categories for Menu / Chaats ===")
url_cats = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=250'
req = urllib.request.Request(url_cats, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    cats = json.loads(res.read().decode())['data']

for c in cats:
    if any(k in c.get('name', '').lower() or k in c.get('custom_url', {}).get('url', '').lower() for k in ['menu', 'chaat', 'takeout']):
        print(f"Cat ID {c['id']} | URL: {c.get('custom_url', {}).get('url')} | Name: {c.get('name')}")
        if 'description' in c:
            print(f"  Description snippet: {c['description'][:150]}...")
