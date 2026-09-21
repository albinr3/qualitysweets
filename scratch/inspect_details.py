import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

# Inspect specific products
target_ids = [77, 90, 140, 162, 139, 154, 98, 104, 138, 155, 168, 169, 167, 170, 158, 141, 142]

results = []
for pid in target_ids:
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/{pid}?include=modifiers,options,custom_fields"
    req = urllib.request.Request(url, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req) as res:
            p = json.loads(res.read().decode())['data']
            results.append({
                'id': p['id'],
                'name': p['name'],
                'price': p['price'],
                'retail_price': p.get('retail_price'),
                'weight': p.get('weight'),
                'description': p.get('description', '')[:200],
                'custom_url': p.get('custom_url', {}).get('url'),
                'custom_fields': p.get('custom_fields', []),
                'modifiers': p.get('modifiers', []),
                'options': p.get('options', [])
            })
    except Exception as e:
        print(f"Error for {pid}:", e)

with open("scratch/product_details.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(f"Fetched details for {len(results)} products.")
