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
width_regex = re.compile(r'width=["\']([^"\']*)["\']', re.IGNORECASE)
height_regex = re.compile(r'height=["\']([^"\']*)["\']', re.IGNORECASE)
loading_regex = re.compile(r'loading=["\']([^"\']*)["\']', re.IGNORECASE)

print("=== CHECKING CATERING (/catering/ - Category 21) ===")
cat21 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21")
if cat21 and cat21.get('data'):
    desc = cat21['data'].get('description', '')
    imgs = img_tag_regex.findall(desc)
    print(f"Category 21 found {len(imgs)} images:")
    for idx, img in enumerate(imgs, 1):
        s = src_regex.search(img)
        a = alt_regex.search(img)
        w = width_regex.search(img)
        h = height_regex.search(img)
        l = loading_regex.search(img)
        print(f" {idx}. alt='{a.group(1) if a else 'NO_ALT'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'} loading={l.group(1) if l else '-'}\n    src={s.group(1) if s else ''}")

print("\n=== CHECKING ABOUT US (Page 6) ===")
p6 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/6")
if p6:
    body = p6.get('body', '')
    imgs = img_tag_regex.findall(body)
    print(f"Page 6 found {len(imgs)} images:")
    for idx, img in enumerate(imgs, 1):
        s = src_regex.search(img)
        a = alt_regex.search(img)
        w = width_regex.search(img)
        h = height_regex.search(img)
        l = loading_regex.search(img)
        print(f" {idx}. alt='{a.group(1) if a else 'NO_ALT'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'} loading={l.group(1) if l else '-'}\n    src={s.group(1) if s else ''}")

print("\n=== CHECKING LOCATION ISELIN (Page 15) ===")
p15 = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15")
if p15:
    body = p15.get('body', '')
    imgs = img_tag_regex.findall(body)
    print(f"Page 15 found {len(imgs)} images:")
    for idx, img in enumerate(imgs, 1):
        s = src_regex.search(img)
        a = alt_regex.search(img)
        w = width_regex.search(img)
        h = height_regex.search(img)
        l = loading_regex.search(img)
        print(f" {idx}. alt='{a.group(1) if a else 'NO_ALT'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'} loading={l.group(1) if l else '-'}\n    src={s.group(1) if s else ''}")

print("\n=== CHECKING MENU PAGES (Pages 10, 11, 12, 13, 14) ===")
for pid in [10, 11, 12, 13, 14]:
    pg = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/{pid}")
    if pg:
        body = pg.get('body', '')
        imgs = img_tag_regex.findall(body)
        print(f"Page {pid} ('{pg.get('name')}') found {len(imgs)} images:")
        for idx, img in enumerate(imgs, 1):
            s = src_regex.search(img)
            a = alt_regex.search(img)
            w = width_regex.search(img)
            h = height_regex.search(img)
            l = loading_regex.search(img)
            print(f" {idx}. alt='{a.group(1) if a else 'NO_ALT'}' | w={w.group(1) if w else '-'} h={h.group(1) if h else '-'} loading={l.group(1) if l else '-'}\n    src={s.group(1) if s else ''}")
