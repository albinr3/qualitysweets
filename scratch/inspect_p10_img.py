import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {"X-Auth-Token": token, "Accept": "application/json"}
req = urllib.request.Request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/10", headers=headers)
with urllib.request.urlopen(req) as resp:
    p10 = json.loads(resp.read().decode())
    print("Page 10 name:", p10['name'])
    import re
    imgs = re.findall(r'<img[^>]*>', p10['body'])
    for img in imgs:
        print("Page 10 IMG:", img)
