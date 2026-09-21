"""Remove the duplicate editorial ``Current Top Sellers`` block from Banner 7.

This operates on the live banner content so it never replaces unrelated storefront
changes with a stale local copy.  It is deliberately idempotent: a second run
does not publish anything after the duplicate is gone.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


BANNER_ID = 7
START_MARKER = "<!-- SECTION 5: CURRENT TOP SELLERS (CAROUSEL MATCHING FEATURED PRODUCTS) -->"
END_MARKER = "<!-- SECTION 6: REGIONAL CATERING, WEDDINGS & MANDIRS TRI-STATE -->"
BACKUP_DIRECTORY = Path(__file__).with_name("backups")


def request_json(url, headers, method="GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def remove_duplicate_top_sellers(content):
    pattern = re.escape(START_MARKER) + r".*?(?=" + re.escape(END_MARKER) + r")"
    updated, replacements = re.subn(pattern, "", content, count=1, flags=re.DOTALL)
    if replacements > 1:
        raise RuntimeError("More than one editorial Top Sellers block matched; refusing to publish.")
    return updated, replacements


def save_backup(banner):
    BACKUP_DIRECTORY.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIRECTORY / f"banner-{BANNER_ID}-before-heading-repair-{timestamp}.json"
    backup_path.write_text(json.dumps(banner, ensure_ascii=False, indent=2), encoding="utf-8")
    return backup_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="publish the repair")
    args = parser.parse_args()

    load_dotenv()
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    if not store_hash or not token:
        print("Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN.", file=sys.stderr)
        return 1

    url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/{BANNER_ID}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": token,
    }
    banner = request_json(url, headers)
    content = banner.get("content", "")
    updated_content, replacements = remove_duplicate_top_sellers(content)

    print(f"Banner {BANNER_ID} current hash: {hashlib.sha256(content.encode()).hexdigest()[:12]}")
    print(f"Duplicate editorial block matches: {replacements}")
    if replacements == 0:
        print("No duplicate editorial block is present. No change needed.")
        return 0
    print(f"Banner {BANNER_ID} repaired hash: {hashlib.sha256(updated_content.encode()).hexdigest()[:12]}")

    if not args.apply:
        print("Dry run only. Use --apply to publish the repair.")
        return 0

    backup_path = save_backup(banner)
    payload = {
        "name": banner["name"],
        "content": updated_content,
        "page": banner["page"],
        "location": banner["location"],
        "date_type": banner["date_type"],
        "visible": str(banner["visible"]),
    }
    saved_banner = request_json(url, headers, method="PUT", payload=payload)
    saved_content = saved_banner.get("content", "")
    if START_MARKER in saved_content or END_MARKER not in saved_content:
        raise RuntimeError("BigCommerce did not retain the expected heading repair.")
    print(f"Published successfully. Backup: {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
