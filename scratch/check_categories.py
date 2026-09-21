import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')
url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=250'
req = urllib.request.Request(url, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
with urllib.request.urlopen(req) as res:
    products = json.loads(res.read().decode())['data']

cat3_prods = [p for p in products if 3 in p.get('categories', [])]
cat8_prods = [p for p in products if 8 in p.get('categories', [])]
cat2_prods = [p for p in products if 2 in p.get('categories', [])]
cat22_prods = [p for p in products if 22 in p.get('categories', [])]

print(f'Total products: {len(products)}')
print(f'Products in Cat 3 (All Indian Sweets): {len(cat3_prods)}')
print(f'Products in Cat 8 (Bengali Sweets): {len(cat8_prods)}')
print(f'Products in Cat 2 (Traditional Mithai): {len(cat2_prods)}')
print(f'Products in Cat 22 (Barfi & Kaju Katli): {len(cat22_prods)}')

bengali_not_in_3 = [p for p in cat8_prods if 3 not in p.get('categories', [])]
print(f'\nBengali sweets NOT in Cat 3 ({len(bengali_not_in_3)}):')
for p in bengali_not_in_3:
    print(f"  ID {p['id']}: {p['name']} | Categories: {p['categories']}")

trad_not_in_3 = [p for p in cat2_prods if 3 not in p.get('categories', [])]
print(f'\nTraditional sweets NOT in Cat 3 ({len(trad_not_in_3)}):')
for p in trad_not_in_3:
    print(f"  ID {p['id']}: {p['name']} | Categories: {p['categories']}")

barfi_not_in_3 = [p for p in cat22_prods if 3 not in p.get('categories', [])]
print(f'\nBarfi NOT in Cat 3 ({len(barfi_not_in_3)}):')
for p in barfi_not_in_3:
    print(f"  ID {p['id']}: {p['name']} | Categories: {p['categories']}")
