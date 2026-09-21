import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

with open('scratch/about_page_new.html', 'r', encoding='utf-8') as f:
    new_html = f.read()

payload = {
    "name": "About Us",
    "meta_title": "About Quality Sweets | Handcrafted Indian Mithai Since 2003 | Iselin NJ",
    "meta_description": "Quality Sweets has been handcrafting authentic Bengali mithai and traditional Indian sweets on Oak Tree Road in Iselin, NJ since 2003. Takeout, catering, and nationwide shipping.",
    "search_keywords": "quality sweets about us, indian sweets iselin nj, bengali sweets oak tree road, indian sweets since 2003",
    "is_visible": True,
    "body": new_html
}

url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/pages/6"
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={
        'X-Auth-Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    method='PUT'
)

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        print("Update Success!")
        print("Updated page ID:", result.get('data', {}).get('id'))
        print("Meta Title:", result.get('data', {}).get('meta_title'))
        print("Meta Description:", result.get('data', {}).get('meta_description'))
        print("Body length:", len(result.get('data', {}).get('body', '')))
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code} - {e.reason}")
    print(e.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
