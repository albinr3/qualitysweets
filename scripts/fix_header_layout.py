"""Apply an idempotent desktop layout repair for the legacy Coffee header.

The theme positions the logo absolutely without constraining its dimensions and
limits the category navigation to 740px.  This creates an overlap with the
utility/search bar and wraps the last category on a second line.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

from dotenv import load_dotenv


SCRIPT_NAME = "Quality Sweets Header Layout"
STYLE_ID = "qs-header-layout"
HEADER_CSS = """
/* Legacy Coffee theme: desktop header alignment. */
@media screen and (min-width: 1101px) {
  #Header {
    /* The secondary utility bar already sits outside the header flow. */
    margin-bottom: 8px !important;
    min-height: 190px !important;
  }

  #Header > .inner {
    max-width: 1180px !important;
    min-height: 190px !important;
  }

  #Header .header-logo {
    left: 0 !important;
    margin: 0 !important;
    position: absolute !important;
    top: 10px !important;
    width: 195px !important;
    z-index: 10 !important;
  }

  #Header .header-logo a,
  #Header #LogoImage {
    display: block !important;
  }

  #Header #LogoImage {
    height: 174px !important;
    object-fit: contain !important;
    object-position: left top !important;
    width: 195px !important;
  }

  #Header .TopMenu {
    width: auto !important;
  }

  #Header .PageMenu {
    clear: none !important;
    float: none !important;
    left: 220px !important;
    margin: 0 !important;
    max-width: none !important;
    position: absolute !important;
    right: 0 !important;
    top: 78px !important;
  }

  #Header .PageMenu > .inner,
  #Header .PageMenu .CategoryList,
  #Header .PageMenu ul.sf-horizontal {
    width: 100% !important;
  }

  #Header .PageMenu ul.sf-horizontal {
    display: flex !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
  }

  #Header .PageMenu ul.sf-horizontal > li {
    flex: 0 1 auto !important;
    white-space: nowrap !important;
  }

  #Header .PageMenu #SideCategoryList > .BlockContent > .SideCategoryListFlyout > ul > li > a {
    font-size: 15px !important;
    padding: 12px 9px !important;
  }

  #Header .header-secondary {
    bottom: -80px !important;
    left: auto !important;
    right: 0 !important;
    width: 650px !important;
  }
}

/* Keep the same hierarchy on smaller desktop/tablet widths without affecting
   the theme's existing mobile menu. */
@media screen and (min-width: 801px) and (max-width: 1100px) {
  #Header {
    margin-bottom: 8px !important;
    min-height: 182px !important;
  }

  #Header > .inner {
    min-height: 182px !important;
  }

  #Header .header-logo {
    left: 0 !important;
    margin: 0 !important;
    position: absolute !important;
    top: 12px !important;
    width: 160px !important;
    z-index: 10 !important;
  }

  #Header #LogoImage {
    height: 150px !important;
    object-fit: contain !important;
    object-position: left top !important;
    width: 160px !important;
  }

  #Header .TopMenu {
    width: auto !important;
  }

  #Header .PageMenu {
    clear: none !important;
    float: none !important;
    left: 175px !important;
    margin: 0 !important;
    max-width: none !important;
    position: absolute !important;
    right: 0 !important;
    top: 76px !important;
  }

  #Header .PageMenu > .inner,
  #Header .PageMenu .CategoryList,
  #Header .PageMenu ul.sf-horizontal {
    width: 100% !important;
  }

  #Header .PageMenu ul.sf-horizontal {
    display: flex !important;
    flex-wrap: nowrap !important;
    justify-content: space-between !important;
  }

  #Header .PageMenu ul.sf-horizontal > li {
    flex: 0 1 auto !important;
    white-space: nowrap !important;
  }

  #Header .PageMenu #SideCategoryList > .BlockContent > .SideCategoryListFlyout > ul > li > a {
    font-size: 12px !important;
    padding: 11px 4px !important;
  }

  #Header .header-secondary {
    bottom: -78px !important;
    left: auto !important;
    right: 0 !important;
    width: 600px !important;
  }
}
""".strip()


def request_json(url: str, headers: dict[str, str], method: str = "GET", payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def script_html() -> str:
    css_json = json.dumps(HEADER_CSS)
    return f"""<script>
(function () {{
  var prior = document.getElementById('{STYLE_ID}');
  if (prior) prior.remove();
  var style = document.createElement('style');
  style.id = '{STYLE_ID}';
  style.textContent = {css_json};
  document.head.appendChild(style);
}})();
</script>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="publish the header repair")
    args = parser.parse_args()

    load_dotenv()
    store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
    access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")
    if not store_hash or not access_token:
        print("Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN.", file=sys.stderr)
        return 1

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Auth-Token": access_token,
    }
    scripts_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/scripts"
    response = request_json(scripts_url, headers)
    existing = next((item for item in response.get("data", []) if item.get("name") == SCRIPT_NAME), None)
    action = "update" if existing else "create"
    print(f"Header layout script: {action}.")

    if not args.apply:
        print("Dry run only. Use --apply to publish the header repair.")
        return 0

    payload = {
        "name": SCRIPT_NAME,
        "description": "Contains the Coffee theme logo and navigation in a responsive desktop header.",
        "html": script_html(),
        "auto_uninstall": True,
        "load_method": "default",
        "location": "head",
        "visibility": "all_pages",
        "kind": "script_tag",
        "consent_category": "essential",
    }
    endpoint = f"{scripts_url}/{existing['uuid']}" if existing else scripts_url
    saved = request_json(endpoint, headers, method="PUT" if existing else "POST", payload=payload)
    saved_html = saved.get("data", {}).get("html", "")
    if STYLE_ID not in saved_html:
        print("BigCommerce did not retain the header layout script.", file=sys.stderr)
        return 1

    print("Header layout repair published and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
