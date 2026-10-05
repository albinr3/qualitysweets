import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {"X-Auth-Token": token, "Accept": "application/json"}

endpoints = [
    f"https://api.bigcommerce.com/stores/{store_hash}/v2/carousel",
    f"https://api.bigcommerce.com/stores/{store_hash}/v3/carousel",
    f"https://api.bigcommerce.com/stores/{store_hash}/v2/store/carousel",
    f"https://api.bigcommerce.com/stores/{store_hash}/v2/slides",
    f"https://api.bigcommerce.com/stores/{store_hash}/v2/themes"
]

for url in endpoints:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            print(f"[OK 200] {url}")
            data = resp.read().decode()
            print(data[:300])
    except urllib.error.HTTPError as e:
        print(f"[HTTP {e.code}] {url}")
    except Exception as e:
        print(f"[ERR] {url}: {e}")
