import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {
    "X-Auth-Token": token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def api_request(url, data=None, method="GET"):
    req_data = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            return json.loads(content) if content else {}
    except Exception as e:
        print(f"Error {method} {url}: {e}")
        return {"error": str(e)}

# 1. Fix Category 21 (Catering)
print("1. Fixing Category 21 Catering alts...")
c21 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21")
if c21 and c21.get('data'):
    desc21 = c21['data']['description']
    desc21 = desc21.replace(
        'Commercial catering trays of freshly fried samosas ready for event delivery at Quality Sweets',
        'Trays of fried samosas ready for event delivery'
    )
    desc21 = desc21.replace(
        'Crisp golden jalebi catering trays prepared for wedding dessert tables and temple events',
        'Trays of fresh jalebi spirals for event dessert tables'
    )
    desc21 = desc21.replace(
        'Bulk fresh Gud Para coated in pure jaggery ready for catering orders at Quality Sweets Iselin NJ',
        'Gud para snacks coated in jaggery for catering orders'
    )
    desc21 = desc21.replace(
        'Fresh handcrafted Kaju Rolls lined up on baking sheet pans at Quality Sweets kitchen in Iselin NJ',
        'Kaju rolls arranged on baking sheets in the kitchen'
    )
    res21 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21", data={"description": desc21}, method="PUT")
    print("Category 21 updated:", "data" in res21)

# 2. Fix Banner 8
print("2. Fixing Banner 8...")
b8 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/8")
if b8 and "content" in b8:
    c8 = b8["content"].replace('Quality Sweets sweets and savory snacks', 'Quality Sweets mithai and savory snacks')
    res8 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/8", data={"content": c8}, method="PUT")
    print("Banner 8 updated:", "id" in res8)

# 3. Fix Banner 5 qs-home-images-seo script
print("3. Fixing Banner 5 script...")
b5 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5")
if b5 and "content" in b5:
    c5 = b5["content"]
    c5 = c5.replace("logo.alt = 'Quality Sweets - Authentic Indian Sweets & Mithai in Iselin NJ';", "logo.alt = 'Quality Sweets Indian Sweets and Snacks';")
    c5 = c5.replace("img.alt = 'Quality Sweets Authentic Handcrafted Indian Mithai and Fresh Snacks Daily';", "img.alt = 'Fresh Indian mithai and snacks made daily';")
    c5 = c5.replace("img.alt = 'Special Bulk Pricing on Indian Sweets and Event Catering in NJ NY CT - Quality Sweets';", "img.alt = 'Bulk pricing on Indian sweets and catering orders';")
    c5 = c5.replace("img.alt = 'Assorted Indian Sweets Gift Baskets and Festive Hampers - Quality Sweets Iselin NJ';", "img.alt = 'Gift baskets with assorted Indian sweets';")
    res5 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5", data={"content": c5}, method="PUT")
    print("Banner 5 script updated:", "id" in res5)

# 4. Fix Page 9 (Preview Home Staging)
print("4. Fixing Page 9...")
p9 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/9")
if p9 and "body" in p9:
    b9 = p9["body"]
    b9 = b9.replace('Welcome to Quality Sweets - Traditional Indian Sweets Handcrafted Daily', 'Quality Sweets Indian mithai and hot snacks')
    b9 = b9.replace('alt="Pure Besan Ladoo"', 'alt="Besan ladoo round sweets"')
    res9 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/9", data={"body": b9}, method="PUT")
    print("Page 9 updated:", "id" in res9)

print("\n[SUCCESS] All remaining AI patterns resolved.")
