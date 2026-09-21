import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners",
    headers={"X-Auth-Token": token, "Accept": "application/json"}
)

with urllib.request.urlopen(req) as res:
    banners = json.loads(res.read().decode("utf-8"))

backup_file = "scripts/production_banners_backup_before_rollout.json"
with open(backup_file, "w", encoding="utf-8") as f:
    json.dump(banners, f, indent=2, ensure_ascii=False)

print(f"Banners backed up successfully to {backup_file}!")
for b in banners:
    print(f"ID: {b['id']}, Name: {b['name']}, Page: {b['page']}, Location: {b['location']}")
