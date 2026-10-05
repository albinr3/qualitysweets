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

img_regex = re.compile(r'<img[^>]*>', re.IGNORECASE)

print("=== 1. CATERING PAGE (/catering/) ===")
cat21 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21")
imgs21 = img_regex.findall(cat21['data']['description'])
print(f"Catering has {len(imgs21)} images:")
for i, img in enumerate(imgs21, 1):
    alt = re.search(r'alt=["\']([^"\']*)["\']', img)
    w = re.search(r'width=["\']([^"\']*)["\']', img)
    h = re.search(r'height=["\']([^"\']*)["\']', img)
    loading = re.search(r'loading=["\']([^"\']*)["\']', img)
    print(f"  {i}. alt: '{alt.group(1) if alt else 'NONE'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'} loading={loading.group(1) if loading else '-'}")

print("\n=== 2. TAKEOUT MENU PAGE (/menu/) ===")
p10 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/10")
imgs10 = img_regex.findall(p10['body'])
for i, img in enumerate(imgs10, 1):
    alt = re.search(r'alt=["\']([^"\']*)["\']', img)
    w = re.search(r'width=["\']([^"\']*)["\']', img)
    h = re.search(r'height=["\']([^"\']*)["\']', img)
    print(f"  {i}. alt: '{alt.group(1) if alt else 'NONE'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'}")

print("\n=== 3. ABOUT US (/about-us) ===")
p6 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/6")
imgs6 = img_regex.findall(p6['body'])
for i, img in enumerate(imgs6, 1):
    alt = re.search(r'alt=["\']([^"\']*)["\']', img)
    w = re.search(r'width=["\']([^"\']*)["\']', img)
    h = re.search(r'height=["\']([^"\']*)["\']', img)
    print(f"  {i}. alt: '{alt.group(1) if alt else 'NONE'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'}")

print("\n=== 4. LOCATION ISELIN (/locations/iselin-nj/) ===")
p15 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15")
imgs15 = img_regex.findall(p15['body'])
for i, img in enumerate(imgs15, 1):
    alt = re.search(r'alt=["\']([^"\']*)["\']', img)
    w = re.search(r'width=["\']([^"\']*)["\']', img)
    h = re.search(r'height=["\']([^"\']*)["\']', img)
    print(f"  {i}. alt: '{alt.group(1) if alt else 'NONE'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'}")

print("\n=== 5. HOME BANNER 5 ===")
b5 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5")
imgs5 = img_regex.findall(b5['content'])
for i, img in enumerate(imgs5, 1):
    alt = re.search(r'alt=["\']([^"\']*)["\']', img)
    print(f"  {i}. alt: '{alt.group(1) if alt else 'NONE'}'")

print("\n=== 6. HOME BANNER 7 ===")
b7 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/7")
imgs7 = img_regex.findall(b7['content'])
for i, img in enumerate(imgs7, 1):
    alt = re.search(r'alt=["\']([^"\']*)["\']', img)
    print(f"  {i}. alt: '{alt.group(1) if alt else 'NONE'}'")
