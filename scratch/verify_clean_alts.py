import os
import json
import re
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {"X-Auth-Token": token, "Accept": "application/json"}

# 1. Check sample products from catalog
url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=10&include=images"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    prods = json.loads(resp.read().decode())['data']
    print("=== CATALOG PRODUCTS SAMPLE ALTS ===")
    for p in prods:
        if p.get('images'):
            print(f"- {p['name']}: '{p['images'][0]['description']}'")

# 2. Check Catering
url_c21 = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21"
req_c = urllib.request.Request(url_c21, headers=headers)
with urllib.request.urlopen(req_c) as resp:
    desc = json.loads(resp.read().decode())['data']['description']
    alts = re.findall(r'alt=["\']([^"\']*)["\']', desc)
    print("\n=== CATERING PAGE ALTS ===")
    for i, a in enumerate(alts, 1):
        print(f" {i}. '{a}'")

# 3. Check Live Homepage
req_home = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_home) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    print("\n=== LIVE HOMEPAGE SAMPLES ===")
    # Find product alts on live homepage
    imgs = re.findall(r'<img[^>]*>', html)
    product_alts = [re.search(r'alt=["\']([^"\']*)["\']', img).group(1) for img in imgs if '/products/' in img and re.search(r'alt=["\']([^"\']*)["\']', img)]
    for a in product_alts[:8]:
        print(f" - '{a}'")
