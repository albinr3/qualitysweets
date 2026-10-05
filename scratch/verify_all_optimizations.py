import os
import json
import re
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

print("=== VERIFYING CATALOG PRODUCT IMAGES ===")
page = 1
total_images = 0
empty_alts = 0
populated_alts = 0

while True:
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?page={page}&limit=50&include=images"
    res = get_json(url)
    if not res or not res.get('data'):
        break
    data = res['data']
    for p in data:
        for img in p.get('images', []):
            total_images += 1
            desc = img.get('description', '').strip()
            if not desc:
                empty_alts += 1
                print(f"[MISSING] Prod {p['id']} ({p['name']}) Img {img['id']}")
            else:
                populated_alts += 1
    pagination = res.get('meta', {}).get('pagination', {})
    if page >= pagination.get('total_pages', 1):
        break
    page += 1

print(f"Total product images checked: {total_images}")
print(f"Images with SEO Alt Text: {populated_alts}")
print(f"Images missing Alt Text: {empty_alts}")

print("\n=== VERIFYING PAGES ===")
for p_id in [2, 5, 7]:
    pg = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/{p_id}")
    body = pg.get('body', '')
    imgs = re.findall(r'<img[^>]*>', body)
    print(f"\nPage {p_id} ('{pg.get('name')}'): Found {len(imgs)} images:")
    for img in imgs:
        alt_m = re.search(r'alt=["\']([^"\']*)["\']', img)
        print(f"   alt: '{alt_m.group(1) if alt_m else 'NONE'}'")

print("\n=== VERIFYING BANNER 8 ===")
b8 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/8")
imgs_b8 = re.findall(r'<img[^>]*>', b8.get('content', ''))
for img in imgs_b8:
    alt_m = re.search(r'alt=["\']([^"\']*)["\']', img)
    print(f"   Banner 8 alt: '{alt_m.group(1) if alt_m else 'NONE'}'")

print("\n=== VERIFYING CATEGORY 15 ===")
c15 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/15")
imgs_c15 = re.findall(r'<img[^>]*>', c15.get('data', {}).get('description', ''))
for img in imgs_c15:
    alt_m = re.search(r'alt=["\']([^"\']*)["\']', img)
    print(f"   Category 15 alt: '{alt_m.group(1) if alt_m else 'NONE'}'")
