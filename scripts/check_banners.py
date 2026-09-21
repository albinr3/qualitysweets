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

# Check banners v2
url_v2 = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners"
req = urllib.request.Request(url_v2, headers=headers)

try:
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        print("Banners found:", len(data))
        for b in data:
            print("Banner:", b.get("name"), "Page:", b.get("page"), "Location:", b.get("location"), "Visible:", b.get("visible"))
except Exception as e:
    print("Error fetching banners:", e)
