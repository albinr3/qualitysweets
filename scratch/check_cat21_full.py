import json
import os
import urllib.request
from pathlib import Path


def load_env():
    env_vars = {}
    env_path = Path(".env")
    if env_path.exists():
        with env_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars


env = load_env()
STORE_HASH = env["BIGCOMMERCE_STORE_HASH"]
TOKEN = env["BIGCOMMERCE_ACCESS_TOKEN"]
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/categories/21",
    headers=HEADERS,
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    print("Category 21 data:")
    print("ID:", data.get("id"))
    print("Name:", data.get("name"))
    print("URL:", data.get("url"))
    print("Is Visible:", data.get("is_visible"))
    print("Parent ID:", data.get("parent_id"))
    print("Page Title:", data.get("page_title"))
