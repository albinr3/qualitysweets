import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {"X-Auth-Token": token, "Accept": "application/json"}
req = urllib.request.Request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5", headers=headers)
with urllib.request.urlopen(req) as resp:
    b5 = json.loads(resp.read().decode())
    print("Banner 5 Name:", b5['name'])
    print("Banner 5 Page:", b5['page'])
    print("Banner 5 Location:", b5['location'])
    with open("scratch/banner_5_content.html", "w", encoding="utf-8") as f:
        f.write(b5['content'])
    print("Saved Banner 5 content to scratch/banner_5_content.html")
