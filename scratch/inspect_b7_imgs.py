import os
import json
import re
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {"X-Auth-Token": token, "Accept": "application/json"}
req = urllib.request.Request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/7", headers=headers)
with urllib.request.urlopen(req) as resp:
    b7 = json.loads(resp.read().decode())
    imgs = re.findall(r'<img[^>]*>', b7['content'])
    for i, img in enumerate(imgs, 1):
        print(f"B7 [{i}]: {img}\n")
