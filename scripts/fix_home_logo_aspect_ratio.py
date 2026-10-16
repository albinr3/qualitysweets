"""Repair the logo dimensions in the published home image optimization script.

The store's original logo is 226x233, but banner 5 injected 240x50 image
attributes. The header fits a 160x165 rendering at the same aspect ratio.
Run without --apply to inspect; --apply backs up the banner and replaces only
the two logo dimension statements.
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


BANNER_ID = 5
WRONG_WIDTH = "if (!logo.getAttribute('width')) logo.setAttribute('width', '240');"
WRONG_HEIGHT = "if (!logo.getAttribute('height')) logo.setAttribute('height', '50');"
INTERIM_WIDTH = "logo.setAttribute('width', '226');"
INTERIM_HEIGHT = "logo.setAttribute('height', '233');"
NEW_WIDTH = "logo.setAttribute('width', '160');"
NEW_HEIGHT = "logo.setAttribute('height', '165');"


def request_json(url, token, method="GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Auth-Token": token,
        },
        method=method,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    if not store_hash or not token:
        print("Missing BigCommerce credentials.", file=sys.stderr)
        return 1

    url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/{BANNER_ID}"
    banner = request_json(url, token)
    content = banner.get("content", "")
    if banner.get("page") != "home_page" or banner.get("location") != "top":
        print("Banner 5 is no longer the home top banner; stopped.", file=sys.stderr)
        return 1

    if NEW_WIDTH in content and NEW_HEIGHT in content and WRONG_WIDTH not in content and WRONG_HEIGHT not in content and INTERIM_WIDTH not in content and INTERIM_HEIGHT not in content:
        print("Logo dimensions are already correct in banner 5.")
        return 0
    previous = None
    for width, height, label in (
        (WRONG_WIDTH, WRONG_HEIGHT, "240x50"),
        (INTERIM_WIDTH, INTERIM_HEIGHT, "226x233"),
    ):
        if content.count(width) == 1 and content.count(height) == 1:
            previous = (width, height, label)
            break
    if previous is None:
        print("Expected logo statements were not found exactly once; stopped.", file=sys.stderr)
        return 1

    old_width, old_height, label = previous
    updated = content.replace(old_width, NEW_WIDTH).replace(old_height, NEW_HEIGHT)
    print(f"Banner 5 logo: {label} -> 160x165 (source aspect ratio, scaled to fit header).")
    if not args.apply:
        print("Dry run. Use --apply to publish.")
        return 0

    backup_dir = Path(__file__).parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    backup_file = backup_dir / f"banner-5-before-logo-fix-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
    backup_file.write_text(json.dumps(banner, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Backup: {backup_file}")

    payload = {
        "name": banner["name"],
        "content": updated,
        "page": banner["page"],
        "location": banner["location"],
        "date_type": banner["date_type"],
        "visible": str(banner["visible"]),
    }
    request_json(url, token, method="PUT", payload=payload)
    saved = request_json(url, token)
    if saved.get("content") != updated:
        print("BigCommerce did not retain the exact updated banner content.", file=sys.stderr)
        return 1
    print("Published and verified through the BigCommerce API.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
