import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ['BIGCOMMERCE_STORE_HASH']
token = os.environ['BIGCOMMERCE_ACCESS_TOKEN']
headers = {
    'X-Auth-Token': token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# 1. Fetch current page data from BigCommerce API v2
res = requests.get(f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15', headers=headers)
if res.status_code != 200:
    print(f"Error fetching page 15: {res.status_code} - {res.text}")
    exit(1)

page_data = res.json()
old_body = page_data['body']

target = '<a class="qs-btn qs-btn--gold" href="https://wa.me/17328037617" target="_blank" rel="noopener">Order for Counter Pickup on WhatsApp</a>'

if target not in old_body:
    print("ERROR: Target button not found in page body!")
    exit(1)

print("Target button found!")
new_body = old_body.replace(target, '')

# 2. Update page 15 via BigCommerce API
payload = {'body': new_body}
put_res = requests.put(f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15', headers=headers, json=payload)
print(f"PUT response status: {put_res.status_code}")

if put_res.status_code == 200:
    updated = put_res.json()
    print("Page updated successfully!")
    print(f"Old body length: {len(old_body)}, New body length: {len(updated.get('body', ''))}")
    print(f"Target still in body: {target in updated.get('body', '')}")
else:
    print(f"Failed to update page: {put_res.text}")
