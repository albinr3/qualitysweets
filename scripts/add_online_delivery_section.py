"""Add the nationwide-delivery SEO section to the live home bottom banner."""

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
INSERT_BEFORE = "<!-- SECTION 8: FREQUENTLY ASKED QUESTIONS (FAQS) -->"
BACKUP_DIRECTORY = Path(__file__).with_name("backups")

SECTION = '''
  <!-- ONLINE INDIAN SWEETS DELIVERY IN USA -->
  <div id="qs-online-indian-sweets-delivery" class="qs-section-box" style="background: #fffdf8; border-left: 5px solid #d4af37;">
    <span style="color: #7a1526; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">Fresh Mithai • Nationwide Shipping</span>
    <h2 style="font-size: 26px; color: #4a0e17; margin: 8px 0 12px 0;">Online Indian Sweets Delivery in USA</h2>
    <p style="font-size: 15px; color: #555; line-height: 1.65; margin: 0 0 18px 0; max-width: 850px;">Order fresh Indian sweets online for delivery anywhere in the USA. Every box of mithai is prepared with care in Iselin, New Jersey, then packed in insulated cold packs to help it arrive fresh for gifting, celebrations, and everyday cravings.</p>
    <a href="/indian-sweets/" class="qs-btn-primary">Shop Indian Sweets Online &rarr;</a>
  </div>

'''


def request_json(url, headers, method="GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def add_section(content):
    if SECTION_ID in content:
        return content, False
    if INSERT_BEFORE not in content:
        raise RuntimeError("FAQ marker was not found; refusing to insert the section in an unknown location.")
    return content.replace(INSERT_BEFORE, SECTION + INSERT_BEFORE, 1), True


def save_backup(banner):
    BACKUP_DIRECTORY.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIRECTORY / f"banner-{BANNER_ID}-before-online-delivery-section-{timestamp}.json"
    backup_path.write_text(json.dumps(banner, ensure_ascii=False, indent=2), encoding="utf-8")
    return backup_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="publish the section")
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
    content, changed = add_section(banner.get("content", ""))
    print(f"Banner {BANNER_ID} current hash: {hashlib.sha256(banner.get('content', '').encode()).hexdigest()[:12]}")
    print(f"Section added: {changed}")
    if not changed:
        print("Section already exists. No change needed.")
        return 0
    print(f"Banner {BANNER_ID} updated hash: {hashlib.sha256(content.encode()).hexdigest()[:12]}")
    if not args.apply:
        print("Dry run only. Use --apply to publish the section.")
        return 0

    backup_path = save_backup(banner)
    payload = {
        "name": banner["name"], "content": content, "page": banner["page"],
        "location": banner["location"], "date_type": banner["date_type"], "visible": str(banner["visible"]),
    }
    saved = request_json(url, headers, method="PUT", payload=payload)
    if SECTION_ID not in saved.get("content", ""):
        raise RuntimeError("BigCommerce did not retain the delivery section.")
    print(f"Published successfully. Backup: {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
