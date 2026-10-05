import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {
    "X-Auth-Token": token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def get_json(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Inspect 1 product image details
url_p = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=1&include=images"
res = get_json(url_p)
if res and res.get('data'):
    p = res['data'][0]
    print(f"Sample Product: ID={p['id']}, Name={p['name']}")
    if p.get('images'):
        print("Image object keys/values:")
        print(json.dumps(p['images'][0], indent=2))

# Inspect banners
print("\n--- BANNERS ---")
banners = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners")
for b in banners:
    print(f"\nBanner ID: {b.get('id')} - Name: {b.get('name')} - Page: {b.get('page')}")
    content = b.get('content', '')
    # print snippet of content
    print("Content preview:", content[:300])

# Inspect pages
print("\n--- PAGES ---")
pages = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/pages")
for pg in pages.get('data', []):
    print(f"Page ID {pg['id']}: {pg['name']} (URL: {pg.get('url')}, type: {pg.get('type')}) - body length: {len(pg.get('body', ''))}")
