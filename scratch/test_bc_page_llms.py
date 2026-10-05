import os
import json
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

# Test 1: Try creating a raw page with url "/llms.txt"
payload = {
    "name": "llms.txt",
    "type": "raw",
    "body": "# Quality Sweets LLMS test",
    "url": "/llms.txt",
    "is_visible": False
}

print("Attempting to test creating page with /llms.txt via v2 API...")
req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/pages",
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print("Success! Created page:")
        data = json.loads(resp.read().decode("utf-8"))
        print(data)
        page_id = data.get("id")
        print(f"Page ID is {page_id}")
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
