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

url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/76/images/270"
payload = {
    "description": "Matka Kaju handcrafted cashew sweet in decorative mini pot - Quality Sweets Iselin NJ"
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method="PUT")

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("Status:", resp.status)
        print("Updated Image:", json.dumps(res, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
