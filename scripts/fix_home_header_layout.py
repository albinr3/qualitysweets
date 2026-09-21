"""Publish the header repair through the home-page top banner.

The current API token can manage banners but lacks Script Manager write scope.
Embedding this idempotent style in the home top banner fixes the public home
without changing theme files or the header markup.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request

from dotenv import load_dotenv

from fix_header_layout import HEADER_CSS


STYLE_ID = "qs-home-header-layout"


def content_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def without_header_fix(content: str) -> str:
    pattern = rf'<style\s+id=["\']{re.escape(STYLE_ID)}["\']>.*?</style>\s*'
    return re.sub(pattern, "", content, flags=re.IGNORECASE | re.DOTALL)


def with_header_fix(content: str) -> str:
    return f'<style id="{STYLE_ID}">\n{HEADER_CSS}\n</style>\n{without_header_fix(content)}'


def request_json(url: str, headers: dict[str, str], method: str = "GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="publish the home-header repair")
    args = parser.parse_args()

    load_dotenv()
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    if not store_hash or not access_token:
        print("Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN.", file=sys.stderr)
        return 1

    url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": access_token,
    }
    banner = request_json(url, headers)
    current_content = banner.get("content", "")
    if not current_content:
        print("Banner 5 has no content; refusing to publish an empty replacement.", file=sys.stderr)
        return 1

    updated_content = with_header_fix(current_content)
    print(f"Banner 5 content hash: {content_hash(current_content)}")
    print(f"Repaired content hash: {content_hash(updated_content)}")

    if not args.apply:
        print("Dry run only. Use --apply to publish the home-header repair.")
        return 0

    payload = {
        "name": banner["name"],
        "content": updated_content,
        "page": banner["page"],
        "location": banner["location"],
        "date_type": banner["date_type"],
        "visible": str(banner["visible"]),
    }
    saved_banner = request_json(url, headers, method="PUT", payload=payload)
    if STYLE_ID not in saved_banner.get("content", ""):
        print("BigCommerce accepted the request but the header repair was not retained.", file=sys.stderr)
        return 1

    print("Home header repair published and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
