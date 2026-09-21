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
    "is_visible": True,
    "page_title": "Indian Catering Near Me | Wedding, Temple & Bulk Samosa Orders NJ NY CT",
    "meta_description": "Authentic Indian catering and bulk orders across NJ, NY & CT. Fresh samosa platters, live jalebi stations, temple prasad & custom wedding mithai boxes.",
}

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/categories/21",
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method="PUT",
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print("[SUCCESS v2] Category 21 updated successfully!")
    print("Is Visible:", res.get("is_visible"))
    print("Category URL:", res.get("url"))
