import json

with open("scratch/all_products_dump.json", "r", encoding="utf-8") as f:
    products = json.load(f)

for p in products:
    if p['id'] <= 80:
        imgs = p.get('images', [])
        for img in imgs:
            print(f"ID:{p['id']}|IMG_ID:{img['id']}|THUMB:{img['is_thumbnail']}|NAME:{p['name']}|URL:{p.get('custom_url')}|FILE:{img.get('url_standard', '').split('/')[-1]}")
