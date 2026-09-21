"""Remove the online-delivery section from the live home bottom banner."""

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
SECTION_ID = "qs-online-indian-sweets-delivery"
BACKUP_DIRECTORY = Path(__file__).with_name("backups")


def request_json(url, headers, method="GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def remove_section(content):
    pattern = (
        r"\s*<!-- ONLINE INDIAN SWEETS DELIVERY IN USA -->"
        r"\s*<div\s+id=[\"']" + re.escape(SECTION_ID) + r"[\"'][^>]*>.*?</div>\s*"
    )
    updated, replacements = re.subn(pattern, "\n\n", content, count=1, flags=re.DOTALL | re.IGNORECASE)
    if replacements > 1:
        raise RuntimeError("More than one delivery section matched; refusing to publish.")
    return updated, replacements


def save_backup(banner):
    BACKUP_DIRECTORY.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIRECTORY / f"banner-{BANNER_ID}-before-delivery-section-removal-{timestamp}.json"
    backup_path.write_text(json.dumps(banner, ensure_ascii=False, indent=2), encoding="utf-8")
    return backup_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="publish the removal")
    args = parser.parse_args()

    load_dotenv()
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    if not store_hash or not token:
        print("Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN.", file=sys.stderr)
        return 1

    url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/{BANNER_ID}"
    headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Auth-Token": token}
    banner = request_json(url, headers)
    content, replacements = remove_section(banner.get("content", ""))
    print(f"Banner {BANNER_ID} current hash: {hashlib.sha256(banner.get('content', '').encode()).hexdigest()[:12]}")
    print(f"Delivery sections removed: {replacements}")
    if replacements == 0:
        print("Section is already absent. No change needed.")
        return 0
    if SECTION_ID in content:
        raise RuntimeError("The section identifier remains after replacement; refusing to publish.")
    if not args.apply:
        print("Dry run only. Use --apply to publish the removal.")
        return 0

    backup_path = save_backup(banner)
    payload = {
        "name": banner["name"], "content": content, "page": banner["page"],
        "location": banner["location"], "date_type": banner["date_type"], "visible": str(banner["visible"]),
    }
    saved = request_json(url, headers, method="PUT", payload=payload)
    if SECTION_ID in saved.get("content", ""):
        raise RuntimeError("BigCommerce did not retain the removal.")
    print(f"Published successfully. Backup: {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
