"""Repair the legacy-theme layout isolation for the home-page bottom banner.

The script preserves the current BigCommerce banner content and prepends a
small, idempotent CSS override.  Run with --apply to publish the repair.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request

from dotenv import load_dotenv


FIX_STYLE_ID = "qs-bottom-layout-fix"
FIX_CSS = """
/* The Coffee theme assigns every descendant of a bottom banner a 320px float.
   Neutralize that rule only for this custom home module. */
.Block.banner_home_page_bottom #qs-home-bottom-container {
  clear: both !important;
  float: none !important;
  margin: 35px auto 20px !important;
  max-width: 1180px !important;
  min-width: 0 !important;
  width: 100% !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container > div {
  clear: both !important;
  float: none !important;
  margin-left: 0 !important;
  width: 100% !important;
}

/* These are the header, grid and CTA wrappers directly inside each custom
   section.  They must not inherit the theme's float or 320px width. */
.Block.banner_home_page_bottom #qs-home-bottom-container > div > div,
.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box > div {
  clear: both !important;
  float: none !important;
  margin-left: 0 !important;
  width: auto !important;
}

/* Restore the authored grids and their cards after the legacy override. */
.Block.banner_home_page_bottom #qs-home-bottom-container div[style*="grid-template-columns"] {
  display: grid !important;
  float: none !important;
  margin-left: 0 !important;
  width: 100% !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container div[style*="grid-template-columns"] > div {
  float: none !important;
  margin-left: 0 !important;
  min-width: 0 !important;
  width: auto !important;
}

/* Keep the product carousel's own layout engine in control. */
.Block.banner_home_page_bottom #qs-home-bottom-container #owl-top-sellers,
.Block.banner_home_page_bottom #qs-home-bottom-container .qs-ts-carousel-wrapper,
.Block.banner_home_page_bottom #qs-home-bottom-container .owl-wrapper-outer {
  clear: both !important;
  float: none !important;
  margin-left: 0 !important;
  width: 100% !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container #owl-top-sellers .qs-product-slide {
  float: none !important;
  margin-left: 0 !important;
  width: auto !important;
}

/* A floating legacy rule escaped the first expanded FAQ answer, allowing the
   following questions to wrap beside it.  Keep every accordion item in the
   normal document flow. */
.Block.banner_home_page_bottom #qs-home-bottom-container .qs-faq-item {
  box-sizing: border-box !important;
  clear: both !important;
  display: block !important;
  float: none !important;
  width: 100% !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-faq-item summary {
  clear: both !important;
  display: block !important;
  width: 100% !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-faq-content {
  box-sizing: border-box !important;
  clear: both !important;
  float: none !important;
  margin-left: 0 !important;
  width: 100% !important;
}

/* Give the nationwide artisan-sweets feature a deliberate product-showcase
   hierarchy.  The selectors identify its unique gold left border, so the
   treatment does not change the other home-page panels. */
.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] {
  background: linear-gradient(135deg, #fffdf8 0%, #fffaf0 100%) !important;
  border: 1px solid #ecd99c !important;
  border-left: 5px solid #d4af37 !important;
  box-shadow: 0 10px 30px rgba(92, 52, 9, 0.07) !important;
  padding: 34px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > span {
  background: #f6e9bd !important;
  border-radius: 999px !important;
  color: #8a6512 !important;
  display: inline-block !important;
  font-size: 11px !important;
  letter-spacing: 1.1px !important;
  padding: 6px 10px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > h2 {
  color: #4a0e17 !important;
  font-size: clamp(25px, 2.2vw, 33px) !important;
  line-height: 1.18 !important;
  margin: 12px 0 10px !important;
  max-width: 760px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > p {
  color: #5f5651 !important;
  font-size: 15px !important;
  margin: 0 0 25px !important;
  max-width: 840px !important;
}

/* Four products fill the row on desktop.  At narrower widths they become a
   balanced 2x2 grid instead of leaving a single card stranded below. */
.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] {
  gap: 14px !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  margin-bottom: 27px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] > div {
  background: #ffffff !important;
  border: 1px solid #eadfca !important;
  border-radius: 10px !important;
  box-shadow: 0 4px 13px rgba(74, 14, 23, 0.05) !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
  padding: 10px !important;
  transition: border-color 180ms ease, box-shadow 180ms ease, transform 180ms ease !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] > div:hover {
  border-color: #d4af37 !important;
  box-shadow: 0 10px 20px rgba(74, 14, 23, 0.11) !important;
  transform: translateY(-3px) !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] > div > a:first-child {
  border-radius: 7px !important;
  display: block !important;
  overflow: hidden !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] img {
  height: 142px !important;
  margin-bottom: 9px !important;
  transition: transform 220ms ease !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] > div:hover img {
  transform: scale(1.035) !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] strong {
  font-size: 16px !important;
  line-height: 1.25 !important;
  margin: 2px 0 6px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] span {
  color: #6d6560 !important;
  font-size: 12.5px !important;
  line-height: 1.48 !important;
}

/* The delivery proof points read as one concise shipping promise, rather
   than a second, competing set of product cards. */
.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] {
  background: #f9f1d8 !important;
  border: 1px solid #ead59b !important;
  border-radius: 10px !important;
  gap: 0 !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  margin: 0 0 23px !important;
  padding: 6px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] > div {
  align-items: start !important;
  background: transparent !important;
  border: 0 !important;
  border-left: 1px solid #e6d19a !important;
  border-radius: 0 !important;
  display: grid !important;
  gap: 2px 10px !important;
  grid-template-columns: 38px minmax(0, 1fr) !important;
  grid-template-rows: auto auto !important;
  padding: 12px 14px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] > div:first-child {
  border-left: 0 !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] > div > div {
  grid-row: 1 / span 2 !important;
  height: 36px !important;
  margin: 0 !important;
  width: 36px !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] strong {
  font-size: 14px !important;
  line-height: 1.25 !important;
  margin: 0 !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] p {
  font-size: 12px !important;
  line-height: 1.4 !important;
  margin: 0 !important;
}

.Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > .qs-btn-gold {
  box-shadow: 0 5px 13px rgba(179, 139, 30, 0.2) !important;
  display: flex !important;
  margin: 0 auto !important;
  padding: 13px 24px !important;
  width: fit-content !important;
}

@media (max-width: 1100px) {
  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }

  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] img {
    height: 175px !important;
  }
}

@media (max-width: 680px) {
  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] {
    padding: 25px 18px !important;
  }

  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(230px"] {
    grid-template-columns: 1fr !important;
  }

  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] {
    grid-template-columns: 1fr !important;
  }

  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] > div,
  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] > div:first-child {
    border-left: 0 !important;
    border-top: 1px solid #e6d19a !important;
  }

  .Block.banner_home_page_bottom #qs-home-bottom-container .qs-section-box[style*="d4af37"] > div[style*="minmax(280px"] > div:first-child {
    border-top: 0 !important;
  }
}
""".strip()


def content_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def without_layout_fix(content: str) -> str:
    pattern = rf'<style\s+id=["\']{re.escape(FIX_STYLE_ID)}["\']>.*?</style>\s*'
    return re.sub(pattern, "", content, flags=re.IGNORECASE | re.DOTALL)


def with_layout_fix(content: str) -> str:
    return f'<style id="{FIX_STYLE_ID}">\n{FIX_CSS}\n</style>\n{without_layout_fix(content)}'


def request_json(url: str, headers: dict[str, str], method: str = "GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="publish the repaired banner")
    parser.add_argument("--remove", action="store_true", help="remove the layout repair")
    args = parser.parse_args()
    if args.apply and args.remove:
        parser.error("--apply and --remove cannot be used together")

    load_dotenv()
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    if not store_hash or not access_token:
        print("Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN.", file=sys.stderr)
        return 1

    url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/7"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": access_token,
    }
    banner = request_json(url, headers)
    current_content = banner.get("content", "")
    if not current_content:
        print("Banner 7 has no content; refusing to publish an empty replacement.", file=sys.stderr)
        return 1

    updated_content = without_layout_fix(current_content) if args.remove else with_layout_fix(current_content)
    print(f"Banner 7 content hash: {content_hash(current_content)}")
    print(f"Repaired content hash: {content_hash(updated_content)}")

    if not args.apply and not args.remove:
        print("Dry run only. Use --apply to publish the layout repair.")
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
    saved_content = saved_banner.get("content", "")
    if args.apply and FIX_STYLE_ID not in saved_content:
        print("BigCommerce accepted the request but the layout fix was not retained.", file=sys.stderr)
        return 1

    if args.remove and FIX_STYLE_ID in saved_content:
        print("BigCommerce accepted the request but the layout repair was not removed.", file=sys.stderr)
        return 1

    print("Banner 7 layout repair removed and verified." if args.remove else "Banner 7 layout repair published and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
