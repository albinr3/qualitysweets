import os
import json
import re
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {"X-Auth-Token": token, "Accept": "application/json"}

# 1. Fetch store info
req_store = urllib.request.Request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/store", headers=headers)
with urllib.request.urlopen(req_store) as resp:
    store = json.loads(resp.read().decode())
    domain = store.get('domain')
    secure_url = store.get('secure_url')
    print(f"Store: {store.get('name')} | Domain: {domain} | Secure URL: {secure_url}")

# 2. Fetch live homepage HTML
home_url = f"https://{domain}/"
print(f"Fetching live homepage HTML from {home_url} ...")
req_home = urllib.request.Request(home_url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

try:
    with urllib.request.urlopen(req_home) as resp:
        home_html = resp.read().decode('utf-8', errors='ignore')
        print(f"Fetched live HTML length: {len(home_html)} bytes")
except Exception as e:
    print(f"Error fetching live homepage: {e}")
    home_html = ""

# 3. Find all <img> tags in live HTML
img_regex = re.compile(r'<img[^>]*>', re.IGNORECASE)
imgs = img_regex.findall(home_html)
print(f"\nTotal <img> tags on LIVE homepage: {len(imgs)}")

with open("scratch/live_home_images.json", "w", encoding="utf-8") as f:
    parsed_imgs = []
    for i, img in enumerate(imgs, 1):
        src = re.search(r'src=["\']([^"\']*)["\']', img, re.IGNORECASE)
        alt = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)
        title = re.search(r'title=["\']([^"\']*)["\']', img, re.IGNORECASE)
        width = re.search(r'width=["\']([^"\']*)["\']', img, re.IGNORECASE)
        height = re.search(r'height=["\']([^"\']*)["\']', img, re.IGNORECASE)
        loading = re.search(r'loading=["\']([^"\']*)["\']', img, re.IGNORECASE)
        fetchp = re.search(r'fetchpriority=["\']([^"\']*)["\']', img, re.IGNORECASE)
        
        item = {
            "index": i,
            "src": src.group(1) if src else "",
            "alt": alt.group(1) if alt else "MISSING",
            "title": title.group(1) if title else "",
            "width": width.group(1) if width else "",
            "height": height.group(1) if height else "",
            "loading": loading.group(1) if loading else "",
            "fetchpriority": fetchp.group(1) if fetchp else "",
            "tag": img
        }
        parsed_imgs.append(item)
        print(f"\n[{i}] ALT: '{item['alt']}'")
        print(f"    SRC: {item['src']}")
        print(f"    DIMS: w={item['width']} h={item['height']} | loading={item['loading']} fetchpriority={item['fetchpriority']}")
    json.dump(parsed_imgs, f, indent=2)

print("\nSaved parsed live home images to scratch/live_home_images.json")
