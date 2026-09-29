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

url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    for c in data.get("data", []):
        print(f"ID: {c['id']}, Parent: {c['parent_id']}, Name: '{c['name']}', URL: '{c.get('custom_url', {}).get('url')}', Visible: {c['is_visible']}, Sort: {c['sort_order']}")
