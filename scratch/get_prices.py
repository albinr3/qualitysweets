import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

page = 1
all_products = []
while True:
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products?limit=250&page={page}&include=variants"
    req = urllib.request.Request(url, headers={'X-Auth-Token': token, 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            prods = data.get('data', [])
            all_products.extend(prods)
            pagination = data.get('meta', {}).get('pagination', {})
            total_pages = pagination.get('total_pages', 1)
            if page >= total_pages or not prods:
                break
            page += 1
    except Exception as e:
        print('Error:', e)
        break

print(f"Total products found: {len(all_products)}")
output_lines = []
for p in sorted(all_products, key=lambda x: x['name']):
    pid = p['id']
    name = p['name']
    price = p.get('price')
    sale_price = p.get('sale_price')
    retail_price = p.get('retail_price')
    variants = p.get('variants', [])
    v_info = []
    for v in variants:
        v_price = v.get('price')
        v_opt = [f"{o.get('display_name')}:{o.get('label')}" for o in v.get('option_values', [])]
        if v_price is not None or v_opt:
            v_info.append(f"[{','.join(v_opt)}: ${v_price}]")
    line = f"{pid} | {name} | Price: ${price} | Sale: ${sale_price} | Retail: ${retail_price}"
    if v_info:
        line += f" | Variants: {' '.join(v_info[:3])}"
    output_lines.append(line)

with open("scratch/products_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Saved {len(output_lines)} products to scratch/products_list.txt")
