import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/176/images"
headers = {"X-Auth-Token": token}

uploads = [
    {
        "key": "gift_baskets",
        "file": r"C:\Users\Albin Rodriguez\.gemini\antigravity-ide\brain\88bb73a9-8bb9-49ae-8056-cffa2039bcd2\.user_uploaded\media_1789173111974.jpg",
        "filename": "hero_gift_baskets_banner.jpg",
        "desc": "Assorted Sweets Gift Baskets Hero Banner"
    },
    {
        "key": "bulk_pricing",
        "file": r"C:\Users\Albin Rodriguez\.gemini\antigravity-ide\brain\88bb73a9-8bb9-49ae-8056-cffa2039bcd2\.user_uploaded\media_1789173111925.jpg",
        "filename": "hero_bulk_pricing_banner.jpg",
        "desc": "Special Bulk Pricing Indian Sweets Hero Banner"
    }
]

results = {
    "welcome": "https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/405/hero_welcome_banner__81442.1789173185.1280.1280.jpg?c=2"
}

for item in uploads:
    with open(item["file"], "rb") as f:
        files = {"image_file": (item["filename"], f, "image/jpeg")}
        data = {"description": item["desc"], "is_thumbnail": False}
        res = requests.post(url, headers=headers, files=files, data=data)
        if res.status_code in [200, 201]:
            d = res.json().get("data", {})
            results[item["key"]] = d.get("url_zoom")
            print(f"Uploaded {item['key']}: {d.get('url_zoom')}")
        else:
            print(f"Error uploading {item['key']}: {res.status_code} {res.text}")

with open("scripts/hero_banner_urls.json", "w") as out:
    json.dump(results, out, indent=2)

print("Finished successfully! URLs:")
print(json.dumps(results, indent=2))
