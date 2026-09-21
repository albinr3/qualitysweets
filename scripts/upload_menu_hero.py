"""Upload the menu hero image to the Quality Sweets BigCommerce CDN."""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

store_hash = os.environ["BIGCOMMERCE_STORE_HASH"]
access_token = os.environ["BIGCOMMERCE_ACCESS_TOKEN"]
image_path = Path("content/menu/samosa-chaat-menu-hero.jpg")

# Product 176 is the established media container for shared storefront imagery.
endpoint = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/176/images"
with image_path.open("rb") as image_file:
    response = requests.post(
        endpoint,
        headers={"X-Auth-Token": access_token},
        files={"image_file": ("samosa-chaat-menu-hero.jpg", image_file, "image/jpeg")},
        data={
            "description": "Samosa chaat with chickpeas, yogurt and chutneys for the Quality Sweets takeout menu",
            "is_thumbnail": False,
        },
        timeout=30,
    )

response.raise_for_status()
print(response.json()["data"]["url_zoom"])
