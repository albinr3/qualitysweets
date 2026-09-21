import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

headers = {
    "X-Auth-Token": access_token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 1. Check existing scripts in Script Manager
list_url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/content/scripts"
req = urllib.request.Request(list_url, headers=headers)

try:
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        existing = data.get("data", [])
        print(f"Found {len(existing)} existing scripts.")
        for s in existing:
            if "Typography" in s.get("name", ""):
                print(f"Deleting older typography script {s['uuid']}...")
                del_req = urllib.request.Request(f"{list_url}/{s['uuid']}", headers=headers, method="DELETE")
                urllib.request.urlopen(del_req)
except Exception as e:
    print("Error listing scripts:", e)

# 2. Prepare Global 2-Font Typography inside compliant <script> tag
css_rules = """
  /* 1. Base Body & Reading Text */
  body, p, li, td, th, input, select, textarea, .breadcrumb, #SideCategoryList, .footer, .BlockContent, .ProductDescription {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  }

  /* 2. Brand Titles, Headings & Product Titles */
  h1, h2, h3, h4, h5, h6,
  .Title, .ProductDetails strong, .ProductDetails strong a,
  .Block h2, .Block h3, .ProductList strong, .ProductList strong a,
  .product-title, .page-heading, .section-title, .qs-title,
  #ProductDetails .ProductDetails h1 {
    font-family: 'Marcellus', Georgia, 'Times New Roman', serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.3px;
  }

  /* 3. Navigation Bar & Category Links */
  #menu, #menu ul, #menu li a, .navPages, .category-list a, .CategoryList, .header-logo, .TopMenu {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.4px;
  }

  /* 4. Product Prices, Add to Cart Buttons & Badges */
  .ProductPrice, .PriceRating, .price, em.ProductPrice, .RetailPrice,
  .btn, .Button, .btn-primary, input[type="submit"], input[type="button"], a.btn,
  .btn-secondary, .ChooseOptions {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px;
  }

  /* Refinamiento sutil en títulos de productos */
  .ProductList .ProductDetails strong a {
    font-size: 15.5px !important;
    color: #4a0e17 !important;
    line-height: 1.35 !important;
  }
  .ProductList .ProductDetails strong a:hover {
    color: #881628 !important;
  }
""".replace("\n", " ").replace('"', '\\"')

typography_html = f"""<script>
(function() {{
  if (!document.getElementById('qs-google-fonts')) {{
    var link = document.createElement('link');
    link.id = 'qs-google-fonts';
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Marcellus&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap';
    document.head.appendChild(link);
  }}
  if (!document.getElementById('qs-global-typography')) {{
    var style = document.createElement('style');
    style.id = 'qs-global-typography';
    style.innerHTML = "{css_rules}";
    document.head.appendChild(style);
  }}
}})();
</script>"""

payload = {
    "name": "Quality Sweets Global Typography",
    "description": "Harmonizes store typography to exactly 2 luxury artisan fonts: Marcellus for headings and Plus Jakarta Sans for body and UI",
    "html": typography_html,
    "auto_uninstall": True,
    "load_method": "default",
    "location": "head",
    "visibility": "all_pages",
    "kind": "script_tag",
    "consent_category": "essential"
}

create_req = urllib.request.Request(
    list_url,
    data=json.dumps(payload).encode("utf-8"),
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(create_req) as res:
        print("Global Typography script created successfully! Status:", res.status)
        created = json.loads(res.read().decode())
        print("Script UUID:", created["data"]["uuid"])
except urllib.error.HTTPError as e:
    print("HTTPError creating script:", e.code, e.read().decode())
except Exception as e:
    print("Error creating script:", e)
