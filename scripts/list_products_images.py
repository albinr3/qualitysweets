import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=30&include=images",
    headers={"X-Auth-Token": token, "Accept": "application/json"}
)
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())['data']
    for p in data:
        img = p['images'][0]['url_standard'] if p.get('images') else 'No image'
        name = p['name'].encode('ascii', 'replace').decode('ascii')
        url = p.get('custom_url', {}).get('url', '')
        print(f"{p['id']}: {name} -> {url} -> {img}")
