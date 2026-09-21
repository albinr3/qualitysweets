import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

# 1. Update content/menu/index.html
index_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'menu', 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Replace prices in chaats section
# Samosa Chaat: $8.50 -> $8.00
# Others: $7.99 -> $8.00
# Note: $7.99 and $8.50 only appear in the chaats section of index.html
updated_index = index_content.replace('<p class="price">$8.50</p>', '<p class="price">$8.00</p>')
updated_index = updated_index.replace('<p class="price">$7.99</p>', '<p class="price">$8.00</p>')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(updated_index)
print("Updated local content/menu/index.html")

# 2. Update content/menu/chaats.html
chaats_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'menu', 'chaats.html')
with open(chaats_path, 'r', encoding='utf-8') as f:
    chaats_content = f.read()

updated_chaats = chaats_content.replace('<p class="price">$8.50</p>', '<p class="price">$8.00</p>')
updated_chaats = updated_chaats.replace('<p class="price">$7.99</p>', '<p class="price">$8.00</p>')

with open(chaats_path, 'w', encoding='utf-8') as f:
    f.write(updated_chaats)
print("Updated local content/menu/chaats.html")

# 3. Deploy to BigCommerce API for Page 10 (/menu/)
url_p10 = f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/10'
payload_p10 = json.dumps({"body": updated_index}).encode('utf-8')
req_p10 = urllib.request.Request(url_p10, data=payload_p10, headers={
    'X-Auth-Token': token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}, method='PUT')

with urllib.request.urlopen(req_p10) as res:
    resp_p10 = json.loads(res.read().decode('utf-8'))
    print(f"API Success for Page 10 ({resp_p10.get('name')})! Body updated, status: {res.status}")

# 4. Deploy to BigCommerce API for Page 11 (/menu/chaats/)
url_p11 = f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/11'
payload_p11 = json.dumps({"body": updated_chaats}).encode('utf-8')
req_p11 = urllib.request.Request(url_p11, data=payload_p11, headers={
    'X-Auth-Token': token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}, method='PUT')

with urllib.request.urlopen(req_p11) as res:
    resp_p11 = json.loads(res.read().decode('utf-8'))
    print(f"API Success for Page 11 ({resp_p11.get('name')})! Body updated, status: {res.status}")
