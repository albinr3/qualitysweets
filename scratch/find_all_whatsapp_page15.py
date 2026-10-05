import os
import requests
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ['BIGCOMMERCE_STORE_HASH']
token = os.environ['BIGCOMMERCE_ACCESS_TOKEN']
headers = {'X-Auth-Token': token, 'Accept': 'application/json'}

res = requests.get(f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15', headers=headers)
body = res.json()['body']

lines = body.split('\n')
print("Lines containing whatsapp or 803:")
for i, l in enumerate(lines, 1):
    if 'whatsapp' in l.lower() or '803' in l:
        print(f"Line {i}: {l.strip()}")
