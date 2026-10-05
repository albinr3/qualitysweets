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

banners = get_json(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners")
for b in banners:
    content = b.get('content', '')
    imgs = img_tag_regex.findall(content)
    if imgs:
        print(f"\n==========================================")
        print(f"BANNER [{b['id']}] {b['name']} ({len(imgs)} imgs)")
        print(f"==========================================")
        for i, img in enumerate(imgs, 1):
            print(f"{i}. {img}\n")
