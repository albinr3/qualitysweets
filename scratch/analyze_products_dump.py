import json

with open("scratch/all_products_dump.json", "r", encoding="utf-8") as f:
    products = json.load(f)

print(f"Total products: {len(products)}")
total_imgs = 0
for p in products:
    imgs = p.get('images', [])
    total_imgs += len(imgs)
    for img in imgs:
        print(f"Prod ID {p['id']} ('{p['name']}'): Img ID {img['id']} (thumb: {img['is_thumbnail']}) -> desc: '{img['description']}'")

print(f"\nTotal images: {total_imgs}")
