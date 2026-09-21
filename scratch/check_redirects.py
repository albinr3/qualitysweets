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

# Try v3 storefront redirects
try:
    req = urllib.request.Request(
        f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/storefront/redirects?limit=250",
        headers=HEADERS,
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        redirects = data.get("data", [])
        print(f"Total v3 redirects: {len(redirects)}")
        for r in redirects:
            from_path = r.get("from_path", "")
            to_url = r.get("to", {}).get("url", "") if isinstance(r.get("to"), dict) else str(r.get("to"))
            if "catering" in from_path or "catering" in to_url or "bulk" in from_path:
                print(f"ID {r.get('id')}: {from_path} -> {to_url}")
except Exception as e:
    print("v3 Redirects error:", e)

# Try v2 redirects
try:
    req = urllib.request.Request(
        f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/redirects?limit=250",
        headers=HEADERS,
    )
    with urllib.request.urlopen(req) as resp:
        redirects_v2 = json.loads(resp.read().decode("utf-8"))
        print(f"Total v2 redirects: {len(redirects_v2)}")
        for r in redirects_v2:
            path = r.get("path", "")
            target = r.get("target", "") or r.get("url", "")
            if "catering" in path or "catering" in str(target) or "bulk" in path:
                print(f"v2 ID {r.get('id')}: {path} -> {target}")
except Exception as e:
    print("v2 Redirects error:", e)
