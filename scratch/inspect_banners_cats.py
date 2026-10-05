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

# Check all banners
print("=== BANNERS DETAIL ===")
banners = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners")
for b in banners:
    content = b.get('content', '')
    img_matches = re.findall(r'<img[^>]*>', content)
    print(f"\nBanner {b['id']} - Name: {b['name']} - Page: {b['page']} - Total imgs: {len(img_matches)}")
    for img in img_matches:
        print(f"   {img}")

# Check all categories
print("\n=== CATEGORIES DETAIL ===")
cats = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=250")
for c in cats.get('data', []):
    desc = c.get('description', '')
    img_matches = re.findall(r'<img[^>]*>', desc)
    if img_matches or c.get('image_url'):
        print(f"\nCategory {c['id']} - Name: {c['name']} - URL: {c.get('custom_url', {}).get('url')}")
        if c.get('image_url'):
            print(f"   image_url: {c['image_url']}")
        for img in img_matches:
            print(f"   desc img: {img}")
