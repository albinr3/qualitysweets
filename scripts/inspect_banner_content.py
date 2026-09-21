import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

headers = {
    "X-Auth-Token": access_token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

url_v2 = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners"
req = urllib.request.Request(url_v2, headers=headers)

with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    for b in data:
        print(f"=== BANNER ID: {b.get('id')} | NAME: {b.get('name')} | PAGE: {b.get('page')} | LOC: {b.get('location')} ===")
        print(b.get("content"))
        print("\n" + "="*50 + "\n")
