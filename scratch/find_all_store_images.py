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

img_tag_regex = re.compile(r'<img[^>]*>', re.IGNORECASE)
src_regex = re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE)
alt_regex = re.compile(r'alt=["\']([^"\']*)["\']', re.IGNORECASE)
title_regex = re.compile(r'title=["\']([^"\']*)["\']', re.IGNORECASE)

print("=== 1. CHECKING PAGES (/v2/pages) ===")
pages = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages?limit=250")
page_images = []
if pages:
    for pg in pages:
        body = pg.get('body', '') or ''
        imgs = img_tag_regex.findall(body)
        if imgs:
            print(f"Page ID {pg['id']}: '{pg['name']}' ({pg.get('url')}) - Found {len(imgs)} images")
            for img in imgs:
                src_m = src_regex.search(img)
                alt_m = alt_regex.search(img)
                src = src_m.group(1) if src_m else 'No src'
                alt = alt_m.group(1) if alt_m else 'NO ALT ATTRIBUTE'
                print(f"   [IMG]: src={src}\n          alt='{alt}'\n          tag={img}")
                page_images.append({
                    "page_id": pg['id'],
                    "page_name": pg['name'],
                    "page_url": pg.get('url'),
                    "src": src,
                    "alt": alt,
                    "tag": img
                })

print(f"\nTotal page images found: {len(page_images)}")

print("\n=== 2. CHECKING BANNERS (/v2/banners) ===")
banners = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners")
banner_images = []
if banners:
    for b in banners:
        content = b.get('content', '') or ''
        imgs = img_tag_regex.findall(content)
        if imgs:
            print(f"Banner ID {b['id']}: '{b['name']}' (Page: {b.get('page')}) - Found {len(imgs)} images")
            for img in imgs:
                src_m = src_regex.search(img)
                alt_m = alt_regex.search(img)
                src = src_m.group(1) if src_m else 'No src'
                alt = alt_m.group(1) if alt_m else 'NO ALT ATTRIBUTE'
                print(f"   [IMG]: src={src}\n          alt='{alt}'\n          tag={img}")
                banner_images.append({
                    "banner_id": b['id'],
                    "banner_name": b['name'],
                    "src": src,
                    "alt": alt,
                    "tag": img
                })

print(f"\nTotal banner images found: {len(banner_images)}")

print("\n=== 3. CHECKING CATEGORIES (/v3/catalog/categories) ===")
cats = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=250")
cat_images = []
if cats and cats.get('data'):
    for c in cats['data']:
        desc = c.get('description', '') or ''
        img_url = c.get('image_url') or ''
        imgs_in_desc = img_tag_regex.findall(desc)
        if img_url or imgs_in_desc:
            print(f"Category ID {c['id']}: '{c['name']}' (URL: {c.get('custom_url', {}).get('url')})")
            if img_url:
                print(f"   Category image_url: {img_url}")
            for img in imgs_in_desc:
                src_m = src_regex.search(img)
                alt_m = alt_regex.search(img)
                print(f"   Desc IMG: src={src_m.group(1) if src_m else ''} alt={alt_m.group(1) if alt_m else ''}")

print("\n=== 4. CHECKING ALL PRODUCTS ===")
# Fetch all products with images
all_products = []
page = 1
while True:
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?page={page}&limit=50&include=images"
    res = get_json(url)
    if not res or not res.get('data'):
        break
    all_products.extend(res['data'])
    pagination = res.get('meta', {}).get('pagination', {})
    if page >= pagination.get('total_pages', 1):
        break
    page += 1

print(f"Total products fetched: {len(all_products)}")
prod_img_count = sum(len(p.get('images', [])) for p in all_products)
print(f"Total product images: {prod_img_count}")

with open("scratch/all_products_dump.json", "w", encoding="utf-8") as f:
    json.dump([{
        "id": p["id"],
        "name": p["name"],
        "sku": p.get("sku", ""),
        "categories": p.get("categories", []),
        "custom_url": p.get("custom_url", {}).get("url", ""),
        "images": [{
            "id": img["id"],
            "description": img.get("description", ""),
            "is_thumbnail": img.get("is_thumbnail", False),
            "sort_order": img.get("sort_order", 0),
            "url_standard": img.get("url_standard", "")
        } for img in p.get("images", [])]
    } for p in all_products], f, indent=2)

print("Saved product image summary to scratch/all_products_dump.json")
