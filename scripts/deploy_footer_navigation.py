"""Deploy curated footer navigation columns to BigCommerce storefront.

Columns configured:
1. Contact Us (NAP: Quality Sweets - Indian Sweets Shop, 1384 Oak Tree Rd, phone, email, socials)
2. Shop:
   - All Indian Sweets (/indian-sweets/)
   - Barfi & Kaju Katli (/barfi/)
   - Bengali Sweets (/bengali-sweets/)
   - Indian Snacks & Namkeen (/indian-snacks/)
   - Mithai Boxes & Gift Baskets (/mithai-box/)
3. Visit & Order:
   - Takeout Menu (/menu/)
   - Catering & Bulk Orders (/catering/)
   - Quality Sweets Iselin NJ Store (/locations/iselin-nj/)
   - Contact Us (/contact-us/)
4. About & Help:
   - About Us (/about-us/)
   - Shipping & Refunds (/shipping-refunds/)
   - Packaging Information (/packaging-information/)
   - Security & Privacy (/security-and-privacy/)
   - Blog (/blog/)
   - Sitemap (/sitemap/)

Deployment channels:
- Analytics Provider 6 (Site Verification Tags) for 100% storefront-wide Blueprint coverage
- Banner 5 (HEADINGS on home_page)
- Script Manager (v3/content/scripts)
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
SCRIPT_NAME = "Quality Sweets Footer Navigation"

FOOTER_NAV_SCRIPT_HTML = r"""<script id="qs-footer-nap">
(function () {
  function applyFooterStructure() {
    var footerUpper = document.getElementById('FooterUpper');
    if (!footerUpper) return;

    // 1. Ensure NAP in Column 0 (Contact)
    var contact = footerUpper.querySelector('.Column.contact .custom_content') || 
                  document.querySelector('#block_2 .custom_content');
    if (contact && !contact.querySelector('.qs-footer-nap-name')) {
      if (!contact.getAttribute('itemscope')) {
        contact.setAttribute('itemscope', '');
        contact.setAttribute('itemtype', 'https://schema.org/SweetShop');
      }
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
      if (icon2 && !icon2.getAttribute('itemprop')) icon2.setAttribute('itemprop', 'telephone');
      var icon3Link = contact.querySelector('.icon3 a');
      if (icon3Link && !icon3Link.getAttribute('itemprop')) icon3Link.setAttribute('itemprop', 'email');
    }

    // 2. Transform Link Columns (Shop, Visit & Order, About & Help)
    if (!footerUpper.querySelector('#qs-footer-shop')) {
      var columns = footerUpper.querySelectorAll(':scope > .Column');
      if (columns.length >= 3) {
        // Column 1: Shop
        var colShop = columns[1];
        if (colShop) {
          colShop.className = 'Column qs-col-shop';
          colShop.innerHTML = [
            '<div class="footer-area Block" id="qs-footer-shop">',
            '  <h2>Shop</h2>',
            '  <div class="custom_content BlockContent">',
            '    <ul>',
            '      <li><a href="/indian-sweets/">All Indian Sweets</a></li>',
            '      <li><a href="/barfi/">Barfi &amp; Kaju Katli</a></li>',
            '      <li><a href="/bengali-sweets/">Bengali Sweets</a></li>',
            '      <li><a href="/indian-snacks/">Indian Snacks &amp; Namkeen</a></li>',
            '      <li><a href="/mithai-box/">Mithai Boxes &amp; Gift Baskets</a></li>',
            '    </ul>',
            '  </div>',
            '</div>'
          ].join('\n');
        }

        // Column 2: Visit & Order
        var colVisit = columns[2];
        if (colVisit) {
          colVisit.className = 'Column qs-col-visit';
          colVisit.innerHTML = [
            '<div class="footer-area Block" id="qs-footer-visit">',
            '  <h2>Visit &amp; Order</h2>',
            '  <div class="custom_content BlockContent">',
            '    <ul>',
            '      <li><a href="/menu/">Takeout Menu</a></li>',
            '      <li><a href="/catering/">Catering &amp; Bulk Orders</a></li>',
            '      <li><a href="/locations/iselin-nj/">Quality Sweets Iselin NJ Store</a></li>',
            '      <li><a href="/contact-us/">Contact Us</a></li>',
            '    </ul>',
            '  </div>',
            '</div>'
          ].join('\n');
        }

        // Column 3: About & Help (Column last)
        var colAbout = columns.length >= 4 ? columns[3] : document.createElement('div');
        colAbout.className = 'Column last qs-col-about';
        colAbout.style.display = 'block';
        colAbout.innerHTML = [
          '<div class="footer-area Block" id="qs-footer-about">',
          '  <h2>About &amp; Help</h2>',
          '  <div class="custom_content BlockContent">',
          '    <ul>',
          '      <li><a href="/about-us/">About Us</a></li>',
          '      <li><a href="/shipping-refunds/">Shipping &amp; Refunds</a></li>',
          '      <li><a href="/packaging-information/">Packaging Information</a></li>',
          '      <li><a href="/security-and-privacy/">Security &amp; Privacy</a></li>',
          '      <li><a href="/blog/">Blog</a></li>',
          '      <li><a href="/sitemap/">Sitemap</a></li>',
          '    </ul>',
          '  </div>',
          '</div>'
        ].join('\n');
        if (columns.length < 4) footerUpper.appendChild(colAbout);
      }
    }

    // 3. Apply layout styling
    if (!document.getElementById('qs-footer-layout-style')) {
      var style = document.createElement('style');
      style.id = 'qs-footer-layout-style';
      style.textContent = [
        '#FooterUpper { display: flex !important; flex-wrap: wrap !important; justify-content: space-between !important; gap: 20px !important; }',
        '#FooterUpper > .Column { float: none !important; margin: 0 !important; display: block !important; }',
        '#FooterUpper > .Column.contact { flex: 1 1 270px !important; max-width: 310px !important; }',
        '#FooterUpper > .Column:not(.contact) { flex: 1 1 180px !important; max-width: 230px !important; }',
        '#FooterUpper .BlockContent ul { list-style: none !important; padding: 0 !important; margin: 0 !important; }',
        '#FooterUpper .BlockContent li { font-size: 13.5px !important; line-height: 27px !important; padding: 0 0 0 14px !important; margin: 0 !important; }',
        '#FooterUpper .BlockContent li a { color: #fce8cc !important; text-decoration: none !important; transition: color 0.18s ease !important; font-family: "Plus Jakarta Sans", sans-serif !important; }',
        '#FooterUpper .BlockContent li a:hover { color: #ffd700 !important; text-decoration: underline !important; }',
        '#FooterUpper h2 { font-family: "Marcellus", Georgia, serif !important; font-size: 19px !important; color: #d4af37 !important; margin: 0 0 12px 0 !important; }',
        '@media (max-width: 800px) { #FooterUpper > .Column { flex: 1 1 45% !important; max-width: 48% !important; } }',
        '@media (max-width: 520px) { #FooterUpper > .Column { flex: 1 1 100% !important; max-width: 100% !important; } }'
      ].join('\n');
      document.head.appendChild(style);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyFooterStructure, { once: true });
  } else {
    applyFooterStructure();
  }
  window.addEventListener('load', applyFooterStructure, { once: true });
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
    parser = argparse.ArgumentParser(description="Deploy Footer Navigation to BigCommerce")
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

    # 1. Check Script Manager for existing scripts
    scripts_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/scripts"
    scripts_data = api_request(scripts_url, headers)
    existing_scripts = scripts_data.get("data", [])
    
    footer_script = next((s for s in existing_scripts if "Footer" in s.get("name", "")), None)

    script_payload = {
        "name": SCRIPT_NAME,
        "description": "Configures 4-column footer navigation layout across all storefront pages.",
        "html": FOOTER_NAV_SCRIPT_HTML,
        "auto_uninstall": True,
        "load_method": "default",
        "location": "footer",
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

    print(f"[Script Manager] Target script: {footer_script['name'] if footer_script else SCRIPT_NAME}")
    print(f"[Analytics Provider 6] Code length: {len(p6_code)}")
    print(f"[Banner 5] Content length: {len(banner5_content)}")

    if not args.apply:
        print("\n--- DRY RUN SUMMARY ---")
        print(f"- Would update Script Manager script '{SCRIPT_NAME}'")
        print("- Would update Analytics Provider 6 with full Footer Navigation & NAP script")
        print("- Would update Banner 5 on Homepage with full Footer Navigation & NAP script")
        print("Run with --apply to publish to BigCommerce.")
        return 0

    # Save backup before applying
    backup_file = BACKUP_DIR / f"footer-nav-backup-{timestamp}.json"
    backup_data = {
        "existing_scripts": existing_scripts,
        "provider6": provider6_data,
        "banner5": banner5
    }
    backup_file.write_text(json.dumps(backup_data, indent=2), encoding="utf-8")
    print(f"Backup saved to: {backup_file}")

    # Update Script Manager
    if footer_script:
        update_url = f"{scripts_url}/{footer_script['uuid']}"
        res = api_request(update_url, headers, method="PUT", payload=script_payload)
        print(f"[OK] Updated Script Manager script: {res['data']['uuid']}")
    else:
        res = api_request(scripts_url, headers, method="POST", payload=script_payload)
        print(f"[OK] Created Script Manager script: {res['data']['uuid']}")

    # Update Analytics Provider 6 (Global storefront coverage)
    clean_p6_code = re.sub(r'<script\s+id=["\']qs-footer-nap["\']>.*?</script>\s*', '', p6_code, flags=re.DOTALL)
    updated_p6_code = clean_p6_code.strip() + "\n" + FOOTER_NAV_SCRIPT_HTML
    p6_payload = {
        "code": updated_p6_code,
        "enabled": True,
        "data_tag_enabled": False
    }
    api_request(provider6_url, headers, method="PUT", payload=p6_payload)
    print(f"[OK] Updated Analytics Provider 6 (New length: {len(updated_p6_code)})")

    # Update Banner 5
    clean_b5_content = re.sub(r'<script\s+id=["\']qs-footer-nap["\']>.*?</script>\s*', '', banner5_content, flags=re.DOTALL)
    updated_b5_content = clean_b5_content.strip() + "\n" + FOOTER_NAV_SCRIPT_HTML
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

    print("\n[SUCCESS] Footer navigation successfully deployed to BigCommerce storefront!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
