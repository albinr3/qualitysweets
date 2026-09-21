import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

req = urllib.request.Request(
    f'https://api.bigcommerce.com/stores/{store_hash}/v2/banners',
    headers={'X-Auth-Token': token, 'Accept': 'application/json'}
)
with urllib.request.urlopen(req) as res:
    banners = json.loads(res.read().decode())
    for b in banners:
        name = b['name'].encode('ascii', 'replace').decode('ascii')
        print(f"ID: {b['id']}, Name: {name}, Page: {b['page']}, Location: {b['location']}")
        print(b['content'])
        print("="*60)
