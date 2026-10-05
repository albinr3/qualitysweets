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

print("==================================================")
print(" 1. ALL PAGES IN STORE (/v2/pages)")
print("==================================================")
pages = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages?limit=250")
for p in pages:
    p_id = p.get('id')
    name = p.get('name')
    url = p.get('url')
    # Fetch full page body if not present
    body = p.get('body', '')
    if not body:
        full_p = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/{p_id}")
        body = full_p.get('body', '') if full_p else ''
    
    imgs = img_tag_regex.findall(body)
    print(f"\nPage [{p_id}] '{name}' -> URL: {url} | Found {len(imgs)} <img> tags")
    for img in imgs:
        src = src_regex.search(img)
        alt = alt_regex.search(img)
        print(f"   IMG: src={src.group(1) if src else 'NONE'}")
        print(f"        alt='{alt.group(1) if alt else 'NONE'}'")
        print(f"        tag={img}")

print("\n==================================================")
print(" 2. ALL CATEGORIES IN STORE (/v3/catalog/categories)")
print("==================================================")
cats = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories?limit=250")
for c in cats.get('data', []):
    c_id = c.get('id')
    name = c.get('name')
    url = c.get('custom_url', {}).get('url')
    desc = c.get('description', '')
    img_url = c.get('image_url')
    imgs = img_tag_regex.findall(desc)
    if imgs or img_url:
        print(f"\nCategory [{c_id}] '{name}' -> URL: {url}")
        if img_url:
            print(f"   image_url: {img_url}")
        for img in imgs:
            src = src_regex.search(img)
            alt = alt_regex.search(img)
            print(f"   IMG: src={src.group(1) if src else 'NONE'}")
            print(f"        alt='{alt.group(1) if alt else 'NONE'}'")
            print(f"        tag={img}")

print("\n==================================================")
print(" 3. ALL BANNERS IN STORE (/v2/banners)")
print("==================================================")
banners = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners")
for b in banners:
    b_id = b.get('id')
    name = b.get('name')
    page = b.get('page')
    content = b.get('content', '')
    imgs = img_tag_regex.findall(content)
    print(f"\nBanner [{b_id}] '{name}' on page '{page}' | Found {len(imgs)} <img> tags")
    for img in imgs:
        src = src_regex.search(img)
        alt = alt_regex.search(img)
        print(f"   IMG: src={src.group(1) if src else 'NONE'}")
        print(f"        alt='{alt.group(1) if alt else 'NONE'}'")
        print(f"        tag={img}")

print("\n==================================================")
print(" 4. SCRIPTS / SCRIPT MANAGER (/v3/content/scripts)")
print("==================================================")
scripts = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/scripts")
for s in scripts.get('data', []):
    html = s.get('html', '')
    imgs = img_tag_regex.findall(html)
    if imgs:
        print(f"Script [{s.get('uuid')}] '{s.get('name')}' has {len(imgs)} imgs")
