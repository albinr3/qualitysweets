"""Deploy Quality Sweets - Indian Sweets Shop to the footer NAP across BigCommerce storefront.

This script updates:
1. BigCommerce Script Manager (v3/content/scripts):
   Injects a storefront-wide footer script ensuring the exact NAP:
   Name: Quality Sweets - Indian Sweets Shop
   Address: 1384 Oak Tree Road, Iselin, NJ 08830
   Phone: Mobile No.: 732-283-3799
   Email: orders@qualitysweetsnj.com
   with proper schema microdata and responsive gold/Plus Jakarta Sans branding.
2. Banner 5 (v2/banners/5) on home page:
   Synchronizes home-page semantic repair script to also include the footer NAP.

Usage:
  python scripts/deploy_footer_nap.py           # Dry run
  python scripts/deploy_footer_nap.py --apply   # Apply to production
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

ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = Path(__file__).resolve().parent / "backups"
SCRIPT_NAME = "Quality Sweets Footer NAP"

NAP_SCRIPT_HTML = r"""<script id="qs-footer-nap">
(function () {
  function applyFooterNAP() {
    var contact = document.querySelector('#block_2 .custom_content') || 
                  document.querySelector('#FooterUpper .Column.contact .custom_content');
    if (!contact) return;
    
    // Prevent duplicate insertion
    if (contact.querySelector('.qs-footer-nap-name')) return;
    
    // Add semantic schema microdata to container
    if (!contact.getAttribute('itemscope')) {
      contact.setAttribute('itemscope', '');
      contact.setAttribute('itemtype', 'https://schema.org/SweetShop');
    }
    
    // Create the Business Name element for NAP
    var nameEl = document.createElement('div');
    nameEl.className = 'qs-footer-nap-name';
    nameEl.setAttribute('itemprop', 'name');
    nameEl.textContent = 'Quality Sweets - Indian Sweets Shop';
    nameEl.style.cssText = 'color: #ffd700; font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-weight: 700; font-size: 14.5px; line-height: 1.35; margin-bottom: 5px; display: block; letter-spacing: 0.2px;';
    
    var icon1 = contact.querySelector('.icon1');
    if (icon1) {
      if (!icon1.getAttribute('itemprop')) {
        icon1.setAttribute('itemprop', 'address');
        icon1.setAttribute('itemscope', '');
        icon1.setAttribute('itemtype', 'https://schema.org/PostalAddress');
      }
      contact.insertBefore(nameEl, icon1);
    } else {
      contact.prepend(nameEl);
    }
    
    var icon2 = contact.querySelector('.icon2');
    if (icon2 && !icon2.getAttribute('itemprop')) {
      icon2.setAttribute('itemprop', 'telephone');
    }
    
    var icon3Link = contact.querySelector('.icon3 a');
    if (icon3Link && !icon3Link.getAttribute('itemprop')) {
      icon3Link.setAttribute('itemprop', 'email');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyFooterNAP, { once: true });
  } else {
    applyFooterNAP();
  }
  window.addEventListener('load', applyFooterNAP, { once: true });
})();
</script>"""


def get_headers(token):
    return {
        "X-Auth-Token": token,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


def api_request(url, headers, method="GET", payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Deploy Footer NAP to BigCommerce")
    parser.add_argument("--apply", action="store_true", help="Apply changes to live store")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    if not store_hash or not token:
        print("Error: Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN in .env", file=sys.stderr)
        return 1

    headers = get_headers(token)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # 1. Check Script Manager for existing Footer NAP script
    scripts_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/scripts"
    scripts_data = api_request(scripts_url, headers)
    existing_scripts = scripts_data.get("data", [])
    
    footer_script = next((s for s in existing_scripts if s.get("name") == SCRIPT_NAME), None)
    
    script_payload = {
        "name": SCRIPT_NAME,
        "description": "Establishes canonical NAP (Name, Address, Phone) with business name 'Quality Sweets - Indian Sweets Shop' in the footer contact block across all storefront pages.",
        "html": NAP_SCRIPT_HTML,
        "auto_uninstall": True,
        "load_method": "default",
        "location": "footer",
        "visibility": "storefront",
        "kind": "script_tag",
        "consent_category": "essential",
        "enabled": True
    }

    if footer_script:
        print(f"[Script Manager] Found existing script '{SCRIPT_NAME}' (UUID: {footer_script['uuid']})")
    else:
        print(f"[Script Manager] Script '{SCRIPT_NAME}' will be created.")

    # 2. Check Analytics Provider 6 (Site Verification Tags - Global Blueprint Head Script)
    provider6_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/settings/analytics/6"
    provider6_data = api_request(provider6_url, headers)
    p6_code = provider6_data.get("data", {}).get("code", "")
    has_footer_nap_in_p6 = "qs-footer-nap" in p6_code

    print(f"[Analytics Provider 6] Code length: {len(p6_code)}, has qs-footer-nap: {has_footer_nap_in_p6}")

    # 3. Check Banner 5 (top home banner)
    banner5_url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5"
    banner5 = api_request(banner5_url, headers)
    banner5_content = banner5.get("content", "")
    has_footer_nap_in_banner5 = "qs-footer-nap" in banner5_content

    print(f"[Banner 5] ID 5 ({banner5.get('name')}) length: {len(banner5_content)}, has qs-footer-nap: {has_footer_nap_in_banner5}")

    if not args.apply:
        print("\n--- DRY RUN SUMMARY ---")
        if footer_script:
            print(f"- Would UPDATE Script Manager script {footer_script['uuid']}")
        else:
            print("- Would CREATE new Script Manager script 'Quality Sweets Footer NAP'")
        if not has_footer_nap_in_p6:
            print("- Would APPEND qs-footer-nap to Analytics Provider 6 (for 100% site-wide Blueprint coverage)")
        if not has_footer_nap_in_banner5:
            print("- Would APPEND qs-footer-nap logic into Banner 5 for instant home-page coverage")
        print("Run with --apply to publish changes to BigCommerce.")
        return 0

    # Save backup before applying
    backup_file = BACKUP_DIR / f"footer-nap-backup-{timestamp}.json"
    backup_data = {
        "existing_scripts": existing_scripts,
        "provider6": provider6_data,
        "banner5": banner5
    }
    backup_file.write_text(json.dumps(backup_data, indent=2), encoding="utf-8")
    print(f"Backup saved to: {backup_file}")

    # Apply Script Manager changes
    if footer_script:
        update_url = f"{scripts_url}/{footer_script['uuid']}"
        res = api_request(update_url, headers, method="PUT", payload=script_payload)
        print(f"[OK] Updated Script Manager script: {res['data']['uuid']}")
    else:
        res = api_request(scripts_url, headers, method="POST", payload=script_payload)
        print(f"[OK] Created Script Manager script: {res['data']['uuid']}")

    # Apply Provider 6 changes (Site Verification Tags - Site-Wide)
    if not has_footer_nap_in_p6:
        clean_p6_code = re.sub(r'<script\s+id=["\']qs-footer-nap["\']>.*?</script>\s*', '', p6_code, flags=re.DOTALL)
        updated_p6_code = clean_p6_code.strip() + "\n" + NAP_SCRIPT_HTML
        p6_payload = {
            "code": updated_p6_code,
            "enabled": True,
            "data_tag_enabled": False
        }
        api_request(provider6_url, headers, method="PUT", payload=p6_payload)
        print(f"[OK] Updated Analytics Provider 6 with footer NAP script (New length: {len(updated_p6_code)})")
    else:
        print("[Analytics Provider 6] Already contains qs-footer-nap.")

    # Apply Banner 5 changes
    if not has_footer_nap_in_banner5:
        updated_banner5_content = banner5_content + "\n" + NAP_SCRIPT_HTML
        b5_payload = {
            "name": banner5["name"],
            "content": updated_banner5_content,
            "page": banner5["page"],
            "location": banner5["location"],
            "date_type": banner5["date_type"],
            "visible": str(banner5["visible"]),
        }
        b5_res = api_request(banner5_url, headers, method="PUT", payload=b5_payload)
        print(f"[OK] Updated Banner 5 with footer NAP script (New length: {len(b5_res.get('content', ''))})")
    else:
        print("[Banner 5] Already contains qs-footer-nap.")

    print("\n[SUCCESS] Footer NAP 'Quality Sweets - Indian Sweets Shop' successfully deployed to BigCommerce storefront!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
