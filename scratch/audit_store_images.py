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

# 1. Check all products and their images
print("--- FETCHING PRODUCTS ---")
page = 1
total_products = 0
products_with_images = 0
total_images = 0
images_without_alt = 0
products_list = []

while True:
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?page={page}&limit=50&include=images"
    res = get_json(url)
    if not res or not res.get('data'):
        break
    data = res['data']
    for p in data:
        total_products += 1
        imgs = p.get('images', [])
        if imgs:
            products_with_images += 1
            for img in imgs:
                total_images += 1
                desc = img.get('description', '') or ''
                if not desc.strip():
                    images_without_alt += 1
                products_list.append({
                    "product_id": p['id'],
                    "product_name": p['name'],
                    "image_id": img['id'],
                    "is_thumbnail": img.get('is_thumbnail', False),
                    "description": desc,
                    "url_standard": img.get('url_standard', '')
                })
    pagination = res.get('meta', {}).get('pagination', {})
    if page >= pagination.get('total_pages', 1):
        break
    page += 1

print(f"Total Products: {total_products}")
print(f"Products with images: {products_with_images}")
print(f"Total product images: {total_images}")
print(f"Images without alt text / description: {images_without_alt}")

# 2. Check categories
print("\n--- FETCHING CATEGORIES ---")
url_cat = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=100"
cats_res = get_json(url_cat)
if cats_res:
    for c in cats_res.get('data', []):
        img_url = c.get('image_url')
        if img_url:
            print(f"Category {c['id']}: {c['name']} -> Image: {img_url}")

# 3. Check pages
print("\n--- FETCHING PAGES ---")
url_pages = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/pages?limit=100"
pages_res = get_json(url_pages)
if pages_res:
    for pg in pages_res.get('data', []):
        body = pg.get('body', '')
        if '<img' in body:
            print(f"Page {pg['id']}: {pg['name']} ({pg.get('url')}) has <img> tags in body")

# 4. Check banners
print("\n--- FETCHING BANNERS ---")
url_banners = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners"
banners_res = get_json(url_banners)
if banners_res:
    for b in banners_res:
        content = b.get('content', '')
        if '<img' in content:
            print(f"Banner {b.get('id')}: {b.get('name')} has <img> tags")
