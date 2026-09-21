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

body = open("content/catering/index.html", "r", encoding="utf-8").read()

payload = {
    "name": "Authentic Indian Catering & Bulk Orders",
    "description": body,
    "page_title": "Indian Catering Near Me | Wedding, Temple & Bulk Samosa Orders NJ NY CT",
    "meta_description": "Authentic Indian catering and bulk orders across NJ, NY & CT. Fresh samosa platters, live jalebi stations, temple prasad & custom wedding mithai boxes.",
    "custom_url": {"url": "/catering/", "is_customized": True},
}

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/catalog/categories/21",
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method="PUT",
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("[SUCCESS] Category 21 updated successfully!")
        print("Category custom_url:", res.get("data", {}).get("custom_url"))
except urllib.error.HTTPError as e:
    print("[ERROR]", e.read().decode("utf-8"))
