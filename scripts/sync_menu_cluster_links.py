"""Sync internal cluster links from content/menu/ to BigCommerce for pages 10, 11, and 12."""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                values[k.strip()] = v.strip().strip('"').strip("'")
    return values

ENV = load_env()
STORE_HASH = ENV.get("BIGCOMMERCE_STORE_HASH") or os.getenv("BIGCOMMERCE_STORE_HASH")
TOKEN = ENV.get("BIGCOMMERCE_ACCESS_TOKEN") or os.getenv("BIGCOMMERCE_ACCESS_TOKEN")

if not STORE_HASH or not TOKEN:
    print("Missing BigCommerce credentials.", file=sys.stderr)
    sys.exit(1)

API_ROOT = f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/pages"
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

UPDATES = [
    (10, BASE_DIR / "content" / "menu" / "index.html", "/menu/"),
    (11, BASE_DIR / "content" / "menu" / "chaats.html", "/menu/chaats/"),
    (12, BASE_DIR / "content" / "menu" / "street-food-snacks.html", "/menu/street-food-snacks/"),
    (22, BASE_DIR / "content" / "menu" / "samosas.html", "/menu/samosas/"),
    (23, BASE_DIR / "content" / "menu" / "pani-puri.html", "/menu/pani-puri/"),
]

for page_id, file_path, url in UPDATES:
    if not file_path.exists():
        print(f"Skipping {file_path}, does not exist.")
        continue
    content = file_path.read_text(encoding="utf-8")
    payload = json.dumps({"body": content}).encode("utf-8")
    req = urllib.request.Request(f"{API_ROOT}/{page_id}", data=payload, headers=HEADERS, method="PUT")
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode("utf-8"))
        print(f"Updated Page {page_id} ({url}): HTTP {res.status} - {data.get('name')}")

print("\nAll cluster pages successfully synchronized with new Samosas internal links!")
