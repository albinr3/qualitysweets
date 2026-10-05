import os
import requests
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ['BIGCOMMERCE_STORE_HASH']
token = os.environ['BIGCOMMERCE_ACCESS_TOKEN']
headers = {'X-Auth-Token': token, 'Accept': 'application/json'}

res = requests.get(f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15', headers=headers)
data = res.json()

for k, v in data.items():
    if isinstance(v, str):
        if 'whatsapp' in v.lower() or '803' in v:
            print(f"Key '{k}' contains match!")
