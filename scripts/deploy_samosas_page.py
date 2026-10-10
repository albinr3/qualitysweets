"""Deploy the dedicated Fresh Samosas & Samosa Chaat page to BigCommerce.

Source of truth: content/menu/samosas.html
Target URL: /menu/samosas/
Operational mode: Takeout & Counter Pickup Only (No dine-in, no postal shipping)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
HTML_PATH = BASE_DIR / "content" / "menu" / "samosas.html"
BACKUP_DIR = BASE_DIR / "scripts" / "backups"

PAGE_URL = "/menu/samosas/"
PAGE_NAME = "Fresh Samosas & Samosa Chaat - Oak Tree Rd Iselin NJ Takeout"
PAGE_META_TITLE = "Fresh Samosas & Samosa Chaat | Quality Sweets Iselin NJ"
PAGE_META_DESCRIPTION = (
    "Fresh, never-frozen hot samosas ($1.75) & samosa chaat ($8) at Quality Sweets "
    "on Oak Tree Rd, Iselin, NJ. Walk-in takeout & party trays. Call (732) 283-3799."
)
PAGE_SEARCH_KEYWORDS = "samosas near me, samosa chaat near me, fresh samosas iselin nj, oak tree road samosa, bulk samosas nj"


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
    return values


ENV = load_env()
STORE_HASH = ENV.get("BIGCOMMERCE_STORE_HASH") or os.getenv("BIGCOMMERCE_STORE_HASH")
ACCESS_TOKEN = ENV.get("BIGCOMMERCE_ACCESS_TOKEN") or os.getenv("BIGCOMMERCE_ACCESS_TOKEN")
API_ROOT = f"https://api.bigcommerce.com/stores/{STORE_HASH}" if STORE_HASH else ""


def get_headers() -> dict[str, str]:
    return {
        "X-Auth-Token": ACCESS_TOKEN or "",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def fetch_all_pages() -> list[dict]:
    request = urllib.request.Request(f"{API_ROOT}/v2/pages", headers=get_headers())
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy dedicated Samosas page to BigCommerce.")
    parser.add_argument("--dry-run", action="store_true", help="Inspect intended changes without calling BigCommerce.")
    args = parser.parse_args()

    if not STORE_HASH or not ACCESS_TOKEN:
        print("Error: Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN in environment / .env", file=sys.stderr)
        return 1

    if not HTML_PATH.exists():
        print(f"Error: HTML template not found at {HTML_PATH}", file=sys.stderr)
        return 1

    body_html = HTML_PATH.read_text(encoding="utf-8")

    payload = {
        "name": PAGE_NAME,
        "type": "page",
        "url": PAGE_URL,
        "body": body_html,
        "is_visible": True,
        "meta_title": PAGE_META_TITLE,
        "meta_description": PAGE_META_DESCRIPTION,
        "search_keywords": PAGE_SEARCH_KEYWORDS,
    }

    print(f"Checking existing pages in BigCommerce store {STORE_HASH}...")
    pages = fetch_all_pages()
    existing_page = next((p for p in pages if p.get("url") == PAGE_URL), None)

    if existing_page:
        action = "UPDATE"
        endpoint = f"{API_ROOT}/v2/pages/{existing_page['id']}"
        method = "PUT"
        print(f"Found existing page ID {existing_page['id']} for URL {PAGE_URL}")
    else:
        action = "CREATE"
        endpoint = f"{API_ROOT}/v2/pages"
        method = "POST"
        print(f"No existing page found for URL {PAGE_URL}. Will create a new page.")

    if args.dry_run:
        print(f"\n[DRY RUN] Intended Action: {action}")
        print(f"Endpoint: {method} {endpoint}")
        print(f"Name: {payload['name']}")
        print(f"URL: {payload['url']}")
        print(f"Meta Title: {payload['meta_title']} ({len(payload['meta_title'])} chars)")
        print(f"Meta Description: {payload['meta_description']} ({len(payload['meta_description'])} chars)")
        print(f"Body size: {len(payload['body'])} characters")
        print("\nDry run completed successfully. No changes made.")
        return 0

    # Create backup directory if needed
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"samosas_page_{action.lower()}_backup_{timestamp}.json"
    backup_file.write_text(
        json.dumps({"existing_page": existing_page, "payload_metadata": {k: v for k, v in payload.items() if k != "body"}}, indent=2),
        encoding="utf-8"
    )
    print(f"Backup created at {backup_file}")

    print(f"Executing {method} {endpoint}...")
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers(),
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"BigCommerce API Error ({e.code}): {error_body}", file=sys.stderr)
        return 1

    print("\nSuccessfully deployed Samosas page to BigCommerce!")
    print(json.dumps({
        "id": result.get("id"),
        "name": result.get("name"),
        "url": f"https://qualitysweetsnj.com{result.get('url')}",
        "is_visible": result.get("is_visible"),
        "meta_title": result.get("meta_title"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
