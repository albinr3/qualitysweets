"""Deploy Takeout Menu header navigation link to BigCommerce storefront.

This script updates:
1. Script Manager (v3/content/scripts)
2. Analytics Provider 6 (Site Verification Tags) for 100% storefront-wide Blueprint coverage
3. Banner 5 (Homepage top banner)

The script injects "Takeout Menu" (/menu/) into both desktop (.PageMenu)
and mobile (.Responsive_Menu) navigation bars before "Indian Catering & Bulk Orders".

Sub-items configured:
- Chaat Counter (/menu/chaats/)
- Hot Street Food & Snacks (/menu/street-food-snacks/)
- Mithai Counter (In-Store) (/menu/mithai-counter/)
- Drinks & Lassi (/menu/drinks/)
"""

import argparse
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
SCRIPT_NAME = "Quality Sweets Header Navigation"
SCRIPT_ID = "qs-header-takeout-nav"

HEADER_NAV_SCRIPT_HTML = r"""<script id="qs-header-takeout-nav">
(function () {
  function injectTakeoutMenu() {
    var menus = document.querySelectorAll('.SideCategoryListFlyout > ul.sf-menu');
    if (!menus || menus.length === 0) return;

    menus.forEach(function (menu) {
      if (menu.querySelector('.qs-nav-takeout')) return;

      var li = document.createElement('li');
      li.className = 'qs-nav-takeout';
      li.innerHTML = '<a href="/menu/">Takeout Menu</a>' +
        '<ul>' +
          '<li><a href="/menu/chaats/">Chaat Counter</a></li>' +
          '<li><a href="/menu/street-food-snacks/">Hot Street Food &amp; Snacks</a></li>' +
          '<li><a href="/menu/mithai-counter/">Mithai Counter (In-Store)</a></li>' +
          '<li><a href="/menu/drinks/">Drinks &amp; Lassi</a></li>' +
        '</ul>';

      // Insert before Catering if present, otherwise append
      var cateringLi = Array.from(menu.children).find(function (el) {
        var a = el.querySelector(':scope > a');
        return a && a.getAttribute('href') && a.getAttribute('href').indexOf('/catering/') !== -1;
      });

      if (cateringLi) {
        menu.insertBefore(li, cateringLi);
      } else {
        menu.appendChild(li);
      }
    });

    if (window.jQuery && typeof window.jQuery.fn.superfish === 'function') {
      try { window.jQuery('ul.sf-menu').superfish(); } catch (e) {}
    }
  }

  if (!document.getElementById('qs-header-takeout-style')) {
    var style = document.createElement('style');
    style.id = 'qs-header-takeout-style';
    style.textContent = [
      '#Header .PageMenu ul.sf-horizontal > li.qs-nav-takeout { flex: 0 1 auto !important; white-space: nowrap !important; }',
      '#Header .PageMenu ul.sf-horizontal > li.qs-nav-takeout > a { font-weight: 700 !important; }',
      '#Header .PageMenu ul.sf-horizontal > li.qs-nav-takeout:hover > ul { display: block !important; }',
      '#Header .PageMenu ul.sf-horizontal > li.qs-nav-takeout ul { min-width: 220px !important; }',
      '@media screen and (min-width: 1101px) {',
      '  #Header .PageMenu #SideCategoryList > .BlockContent > .SideCategoryListFlyout > ul > li > a { font-size: 14.5px !important; padding: 12px 7px !important; }',
      '}'
    ].join('\n');
    document.head.appendChild(style);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectTakeoutMenu, { once: true });
  } else {
    injectTakeoutMenu();
  }
  window.addEventListener('load', injectTakeoutMenu, { once: true });
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
    parser = argparse.ArgumentParser(description="Deploy Takeout Menu link to Header Navigation")
    parser.add_argument("--apply", action="store_true", help="Apply changes to live store")
    args = parser.parse_args()

    load_dotenv(ROOT / ".env")
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

    if not store_hash or not token:
        print("Note: BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN not found in .env.", file=sys.stderr)
        print("To deploy via API, set them in .env and run: python scripts/deploy_header_navigation.py --apply", file=sys.stderr)
        print("\n--- STANDALONE HTML/JS CODE READY TO COPY & PASTE ---")
        print(HEADER_NAV_SCRIPT_HTML)
        return 1

    headers = get_headers(token)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # 1. Check Script Manager
    scripts_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/scripts"
    scripts_data = api_request(scripts_url, headers)
    existing_scripts = scripts_data.get("data", [])
    header_script = next((s for s in existing_scripts if SCRIPT_NAME in s.get("name", "")), None)

    script_payload = {
        "name": SCRIPT_NAME,
        "description": "Injects Takeout Menu link and dropdown into desktop and mobile header navigation.",
        "html": HEADER_NAV_SCRIPT_HTML,
        "auto_uninstall": True,
        "load_method": "default",
        "location": "head",
        "visibility": "storefront",
        "kind": "script_tag",
        "consent_category": "essential",
        "enabled": True
    }

    # 2. Check Analytics Provider 6
    provider6_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/settings/analytics/6"
    provider6_data = api_request(provider6_url, headers)
    p6_code = provider6_data.get("data", {}).get("code", "")

    # 3. Check Banner 5
    banner5_url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5"
    banner5 = api_request(banner5_url, headers)
    banner5_content = banner5.get("content", "")

    print(f"[Script Manager] Target script: {header_script['name'] if header_script else SCRIPT_NAME}")
    print(f"[Analytics Provider 6] Code length: {len(p6_code)}")
    print(f"[Banner 5] Content length: {len(banner5_content)}")

    if not args.apply:
        print("\n--- DRY RUN SUMMARY ---")
        print(f"- Would register Script Manager script '{SCRIPT_NAME}'")
        print("- Would inject Takeout Menu script into Analytics Provider 6 (100% storefront coverage)")
        print("- Would inject Takeout Menu script into Banner 5 (Homepage)")
        print("Run with --apply to publish to BigCommerce.")
        return 0

    # Save backup before applying
    backup_file = BACKUP_DIR / f"header-nav-backup-{timestamp}.json"
    backup_data = {
        "existing_scripts": existing_scripts,
        "provider6": provider6_data,
        "banner5": banner5
    }
    backup_file.write_text(json.dumps(backup_data, indent=2), encoding="utf-8")
    print(f"Backup saved to: {backup_file}")

    # Update Script Manager
    if header_script:
        update_url = f"{scripts_url}/{header_script['uuid']}"
        res = api_request(update_url, headers, method="PUT", payload=script_payload)
        print(f"[OK] Updated Script Manager script: {res['data']['uuid']}")
    else:
        res = api_request(scripts_url, headers, method="POST", payload=script_payload)
        print(f"[OK] Created Script Manager script: {res['data']['uuid']}")

    # Update Analytics Provider 6 (Global storefront coverage)
    clean_p6_code = re.sub(rf'<script\s+id=["\']{SCRIPT_ID}["\']>.*?</script>\s*', '', p6_code, flags=re.DOTALL)
    updated_p6_code = clean_p6_code.strip() + "\n" + HEADER_NAV_SCRIPT_HTML
    p6_payload = {
        "code": updated_p6_code,
        "enabled": True,
        "data_tag_enabled": False
    }
    api_request(provider6_url, headers, method="PUT", payload=p6_payload)
    print(f"[OK] Updated Analytics Provider 6 (New length: {len(updated_p6_code)})")

    # Update Banner 5
    clean_b5_content = re.sub(rf'<script\s+id=["\']{SCRIPT_ID}["\']>.*?</script>\s*', '', banner5_content, flags=re.DOTALL)
    updated_b5_content = clean_b5_content.strip() + "\n" + HEADER_NAV_SCRIPT_HTML
    b5_payload = {
        "name": banner5["name"],
        "content": updated_b5_content,
        "page": banner5["page"],
        "location": banner5["location"],
        "date_type": banner5["date_type"],
        "visible": str(banner5["visible"]),
    }
    b5_res = api_request(banner5_url, headers, method="PUT", payload=b5_payload)
    print(f"[OK] Updated Banner 5 (New length: {len(b5_res.get('content', ''))})")

    print("\n[SUCCESS] Takeout Menu link successfully deployed to Header Navigation!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
