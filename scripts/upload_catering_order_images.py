"""Upload newly added catering order images to BigCommerce Product 176 (storefront media hub).

Images uploaded:
1. bulk_jalebi_trays: content/catering/images/bulk-jalebi-catering-trays-iselin-nj.jpg
2. bulk_samosa_trays: content/catering/images/bulk-samosa-catering-party-trays-nj.jpg
3. bulk_namkeen_mathri: content/catering/images/bulk-namkeen-savory-snack-order.jpg
4. handcrafted_dough_prep: content/catering/images/handcrafted-mithai-kitchen-preparation.jpg
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

images_to_upload = [
    {
        "key": "bulk_samosa_trays",
        "file": "bulk-samosa-catering-party-trays-nj.jpg",
        "desc": "Freshly fried samosa catering party trays for events at Quality Sweets"
    },
    {
        "key": "bulk_jalebi_trays",
        "file": "bulk-jalebi-catering-trays-iselin-nj.jpg",
        "desc": "Fresh hot jalebi catering trays for live stations and wedding dessert tables"
    },
    {
        "key": "bulk_namkeen_mathri",
        "file": "bulk-namkeen-savory-snack-order.jpg",
        "desc": "Handcrafted spiced mathri and savory namkeen bulk event order"
    },
    {
        "key": "handcrafted_dough_prep",
        "file": "handcrafted-mithai-kitchen-preparation.jpg",
        "desc": "Behind the scenes kitchen preparation of handcrafted mithai dough rolls"
    }
]

def main():
    if not store_hash or not access_token:
        print("[INFO] No API credentials found in .env.")
        print("[INFO] Images are stored locally in content/catering/images/ and assets/catering/.")
        print("[INFO] Using canonical BigCommerce WebDAV image paths in HTML (/product_images/uploaded_images/).")
        return 0

    upload_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/176/images"
    headers = {"X-Auth-Token": access_token}

    uploaded_cache_file = ROOT / "scripts" / "uploaded_images.json"
    uploaded_urls = {}
    if uploaded_cache_file.exists():
        try:
            uploaded_urls = json.loads(uploaded_cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    for item in images_to_upload:
        if item["key"] in uploaded_urls:
            print(f"[SKIP] Already uploaded {item['key']}: {uploaded_urls[item['key']]}")
            continue

        file_path = ROOT / "content" / "catering" / "images" / item["file"]
        if not file_path.exists():
            print(f"[ERROR] File not found: {file_path}")
            continue

        print(f"Uploading {item['file']} ({item['desc']})...")
        with open(file_path, "rb") as f:
            files = {"image_file": (item["file"], f, "image/jpeg")}
            data = {"description": item["desc"], "is_thumbnail": False}
            resp = requests.post(upload_url, headers=headers, files=files, data=data, timeout=40)
            if resp.status_code in [200, 201]:
                res_json = resp.json()
                cdn_url = res_json.get("data", {}).get("url_zoom") or res_json.get("data", {}).get("url_standard")
                uploaded_urls[item["key"]] = cdn_url
                print(f"[OK] Uploaded {item['key']} -> {cdn_url}")
            else:
                print(f"[ERROR] Upload failed ({resp.status_code}): {resp.text}")

    uploaded_cache_file.write_text(json.dumps(uploaded_urls, indent=2), encoding="utf-8")
    print("\n[SUCCESS] Updated scripts/uploaded_images.json")
    return 0

if __name__ == "__main__":
    main()
