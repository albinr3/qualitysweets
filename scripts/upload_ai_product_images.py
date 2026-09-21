import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

brain_dir = r"C:\Users\Albin Rodriguez\.gemini\antigravity-ide\brain\88bb73a9-8bb9-49ae-8056-cffa2039bcd2"

images_to_upload = [
    {"key": "samosa_chaat", "file": "samosa_chaat_photo_1789098060133.jpg", "desc": "Samosa & Papri Chaat"},
    {"key": "pani_puri", "file": "pani_puri_photo_1789098074946.jpg", "desc": "Pani Puri Kits To-Go"},
    {"key": "chole_bhatura", "file": "chole_bhatura_photo_1789098088650.jpg", "desc": "Hot Chole Bhatura"},
    {"key": "stuffed_paratha", "file": "stuffed_paratha_photo_1789098102913.jpg", "desc": "Aloo & Gobi Parathas"},
    {"key": "wedding_gift_box", "file": "wedding_gift_box_1789098119353.jpg", "desc": "Wedding Sweets Gift Box"},
    {"key": "temple_prasad", "file": "temple_bulk_prasad_1789098135260.jpg", "desc": "Temple & Mandir Bulk Prasad"},
    {"key": "bulk_samosas", "file": "bulk_samosas_platter_1789098151834.jpg", "desc": "Bulk Fresh Samosas Tray"},
]

upload_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/176/images"
headers = {
    "X-Auth-Token": access_token
}

uploaded_urls = {}

for item in images_to_upload:
    path = os.path.join(brain_dir, item["file"])
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    
    print(f"Uploading {item['desc']}...")
    with open(path, "rb") as f:
        files = {
            "image_file": (item["file"], f, "image/jpeg")
        }
        data = {
            "description": item["desc"],
            "is_thumbnail": False
        }
        resp = requests.post(upload_url, headers=headers, files=files, data=data)
        if resp.status_code in [200, 201]:
            res_json = resp.json()
            cdn_url = res_json.get("data", {}).get("url_standard")
            uploaded_urls[item["key"]] = cdn_url
            print(f"[OK] Uploaded {item['key']}: {cdn_url}")
        else:
            print(f"[ERROR] {resp.status_code}: {resp.text}")

print("\n--- RESULTS JSON ---")
print(json.dumps(uploaded_urls, indent=2))

# Save results to a json file
with open(os.path.join(os.path.dirname(__file__), "uploaded_images.json"), "w") as f:
    json.dump(uploaded_urls, f, indent=2)
