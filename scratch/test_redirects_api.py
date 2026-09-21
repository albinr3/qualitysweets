import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

STORE_HASH = os.getenv("BIGCOMMERCE_STORE_HASH")
ACCESS_TOKEN = os.getenv("BIGCOMMERCE_ACCESS_TOKEN")

headers_v2 = {
    "X-Auth-Token": ACCESS_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

headers_v3 = {
    "X-Auth-Token": ACCESS_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print("=== Testing Redirects API ===")
# Try v3 redirects list or v2 redirects list
v3_url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/storefront/redirects"
res = requests.get(v3_url, headers=headers_v3)
print(f"V3 Redirects Status: {res.status_code}")
if res.status_code == 200:
    print("V3 Data:", res.json().get("data", [])[:2])
else:
    print("V3 Error:", res.text)

v2_url = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/redirects"
res_v2 = requests.get(v2_url, headers=headers_v2)
print(f"V2 Redirects Status: {res_v2.status_code}")
if res_v2.status_code == 200:
    print("V2 Data count:", len(res_v2.json()))
else:
    print("V2 Error:", res_v2.text)
