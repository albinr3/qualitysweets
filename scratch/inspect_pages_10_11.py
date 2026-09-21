import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

print("=== Checking Page 10 (/menu/) ===")
url_p10 = f'https://api.bigcommerce.com/stores/{store_hash}/v3/content/pages/10'
req = urllib.request.Request(url_p10, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    p10 = json.loads(res.read().decode())['data']
    print("Page 10 body snippet:")
    print(p10.get('body', '')[:500])

print("\n=== Checking Page 11 (/menu/chaats/) ===")
url_p11 = f'https://api.bigcommerce.com/stores/{store_hash}/v3/content/pages/11'
req = urllib.request.Request(url_p11, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    p11 = json.loads(res.read().decode())['data']
    print("Page 11 body snippet:")
    print(p11.get('body', '')[:500])

print("\n=== Checking Category 15 (/chaats/) ===")
url_c15 = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/15'
req = urllib.request.Request(url_c15, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    c15 = json.loads(res.read().decode())['data']
    print("Category 15 description snippet:")
    print(c15.get('description', '')[:500])
