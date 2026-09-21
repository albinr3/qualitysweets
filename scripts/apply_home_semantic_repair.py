"""Publish an idempotent semantic repair for legacy theme headings on the home.

The legacy BigCommerce theme is not exposed by the available Theme API.  This
script stores a small DOM-only repair in the existing home top banner so the
rendered storefront has the required heading hierarchy without hiding any UI.
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


BANNER_ID = 5
SCRIPT_ID = "qs-home-semantic-heading-repair"
BACKUP_DIRECTORY = Path(__file__).with_name("backups")
HERO_COPY_OLD = (
    "Serving Oak Tree Road in Iselin, NJ since 2003. Pick up hot samosas and chaats to go, "
    "or order fresh sweets shipped nationwide in insulated cold packs."
)
HERO_COPY_NEW = (
    "Quality Sweets is an authentic Indian sweet shop in Iselin, NJ, serving handcrafted mithai, "
    "hot samosas, chaats, and nationwide sweet delivery since 2003."
)

SCRIPT = r'''<script id="qs-home-semantic-heading-repair">
(function () {
  function retag(node, tagName, text) {
    if (!node || node.tagName.toLowerCase() === tagName) {
      if (node && text) node.textContent = text;
      return node;
    }
    var replacement = document.createElement(tagName);
    Array.prototype.forEach.call(node.attributes, function (attribute) {
      replacement.setAttribute(attribute.name, attribute.value);
    });
    replacement.innerHTML = node.innerHTML;
    if (text) replacement.textContent = text;
    node.parentNode.replaceChild(replacement, node);
    return replacement;
  }

  function repairHeadings() {
    document.querySelectorAll('h2.slide-heading').forEach(function (heading) {
      if (!heading.textContent.trim()) retag(heading, 'span');
    });

    document.querySelectorAll('#SideCategoryList h2').forEach(function (heading) {
      if (heading.closest('#FooterUpper')) {
        retag(heading, 'h3', 'Shop by Category');
      } else {
        retag(heading, 'span');
      }
    });

    var contact = document.querySelector('#block_2 > h2');
    if (contact) contact.textContent = 'Contact Quality Sweets';

    var social = document.querySelector('#socnet > h4');
    if (social) retag(social, 'h3', 'Connect with Us');

    var information = document.querySelector('#block_3 > h2');
    if (information) retag(information, 'h3', 'Customer Information');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', repairHeadings, { once: true });
  } else {
    repairHeadings();
  }
  window.addEventListener('load', repairHeadings, { once: true });
}());
</script>'''


def request_json(url, headers, method="GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def with_repair(content):
    if HERO_COPY_OLD in content:
        content = content.replace(HERO_COPY_OLD, HERO_COPY_NEW, 1)
    elif HERO_COPY_NEW not in content:
        raise RuntimeError("Expected hero copy was not found; refusing to publish an unknown replacement.")
    pattern = rf'<script\s+id=["\']{re.escape(SCRIPT_ID)}["\']>.*?</script>\s*'
    clean_content = re.sub(pattern, "", content, flags=re.IGNORECASE | re.DOTALL)
    return SCRIPT + "\n" + clean_content


def save_backup(banner):
    BACKUP_DIRECTORY.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIRECTORY / f"banner-{BANNER_ID}-before-semantic-repair-{timestamp}.json"
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
    headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Auth-Token": token}
    banner = request_json(url, headers)
    current_content = banner.get("content", "")
    updated_content = with_repair(current_content)
    print(f"Banner {BANNER_ID} current hash: {hashlib.sha256(current_content.encode()).hexdigest()[:12]}")
    print(f"Banner {BANNER_ID} repaired hash: {hashlib.sha256(updated_content.encode()).hexdigest()[:12]}")

    if not args.apply:
        print("Dry run only. Use --apply to publish the semantic repair.")
        return 0

    backup_path = save_backup(banner)
    payload = {
        "name": banner["name"], "content": updated_content, "page": banner["page"],
        "location": banner["location"], "date_type": banner["date_type"], "visible": str(banner["visible"]),
    }
    saved_banner = request_json(url, headers, method="PUT", payload=payload)
    if SCRIPT_ID not in saved_banner.get("content", ""):
        raise RuntimeError("BigCommerce did not retain the semantic repair.")
    print(f"Published successfully. Backup: {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
