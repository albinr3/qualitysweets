import os
import json
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

url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    cat = json.loads(resp.read().decode())['data']
    print("Category 21 Name:", cat['name'])
    print("Description length:", len(cat['description']))
    with open("scratch/category_21_desc.html", "w", encoding="utf-8") as f:
        f.write(cat['description'])
    print("Saved description to scratch/category_21_desc.html")
