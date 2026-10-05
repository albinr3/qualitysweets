import os
import json
import re
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {"X-Auth-Token": token, "Accept": "application/json"}

def get_json(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

ai_words = ['handcrafted', 'artisan', 'authentic', 'luxury', 'deluxe', 'vibrant', 'showcasing', 'wholesome', 'sweets sweets', 'rich', 'velvety', 'aromatic', 'pure', 'delicate']
ai_regex = re.compile(r'\b(' + '|'.join(ai_words) + r')\b', re.IGNORECASE)

print("=== CHECKING ALL PRODUCTS IMAGES ===")
page = 1
flagged_products = []
while True:
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?page={page}&limit=50&include=images"
    res = get_json(url)
    if not res or not res.get('data'):
        break
    for p in res['data']:
        for img in p.get('images', []):
            desc = img.get('description', '')
            matches = ai_regex.findall(desc)
            if matches:
                flagged_products.append({
                    "product_id": p['id'],
                    "product_name": p['name'],
                    "image_id": img['id'],
                    "description": desc,
                    "matches": matches
                })
    if page >= res.get('meta', {}).get('pagination', {}).get('total_pages', 1):
        break
    page += 1

print(f"Flagged product images: {len(flagged_products)}")
for fp in flagged_products:
    print(f"  P[{fp['product_id']}] Img[{fp['image_id']}]: '{fp['description']}' -> {fp['matches']}")

print("\n=== CHECKING BANNERS ===")
banners = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners")
for b in banners:
    content = b.get('content', '')
    imgs = re.findall(r'<img[^>]*>', content)
    for img in imgs:
        alt_m = re.search(r'alt=["\']([^"\']*)["\']', img)
        if alt_m:
            alt = alt_m.group(1)
            matches = ai_regex.findall(alt)
            if matches:
                print(f"  Banner {b['id']} ({b['name']}): '{alt}' -> {matches}")

print("\n=== CHECKING CATEGORIES ===")
cats = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=100")
for c in cats.get('data', []):
    desc = c.get('description', '')
    imgs = re.findall(r'<img[^>]*>', desc)
    for img in imgs:
        alt_m = re.search(r'alt=["\']([^"\']*)["\']', img)
        if alt_m:
            alt = alt_m.group(1)
            matches = ai_regex.findall(alt)
            if matches:
                print(f"  Category {c['id']} ({c['name']}): '{alt}' -> {matches}")

print("\n=== CHECKING PAGES ===")
pages = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages?limit=100")
for p in pages:
    p_full = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/{p['id']}")
    body = p_full.get('body', '') if p_full else ''
    imgs = re.findall(r'<img[^>]*>', body)
    for img in imgs:
        alt_m = re.search(r'alt=["\']([^"\']*)["\']', img)
        if alt_m:
            alt = alt_m.group(1)
            matches = ai_regex.findall(alt)
            if matches:
                print(f"  Page {p['id']} ({p['name']}): '{alt}' -> {matches}")
