"""Deploy Roadmap Step 2.3: the public Iselin, NJ local landing page."""

import json
import os
import urllib.request
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()
STORE_HASH = os.environ["BIGCOMMERCE_STORE_HASH"]
TOKEN = os.environ["BIGCOMMERCE_ACCESS_TOKEN"]
API_ROOT = f"https://api.bigcommerce.com/stores/{STORE_HASH}"
HEADERS = {
    "X-Auth-Token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def upload_image(filename: str, description: str) -> str:
    """Upload optimized location photography to the existing storefront media product."""
    path = Path("content/locations") / filename
    with path.open("rb") as image_file:
        response = requests.post(
            f"{API_ROOT}/v3/catalog/products/176/images",
            headers={"X-Auth-Token": TOKEN},
            files={"image_file": (filename, image_file, "image/jpeg")},
            data={"description": description, "is_thumbnail": False},
            timeout=30,
        )
    response.raise_for_status()
    return response.json()["data"]["url_zoom"]


# The media files were uploaded in the initial Step 2.3 deployment. Reuse them
# on future page edits so a copy of the same photo is never created in the CDN.
storefront_url = "https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/410/quality-sweets-iselin-storefront-oak-tree-road__61587.1789245785.1280.1280.jpg?c=2"
counter_url = "https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/411/quality-sweets-iselin-mithai-counter__70430.1789245787.1280.1280.jpg?c=2"

body = r"""
<style>
  .TitleHeading{display:none!important}.qs-location{font-family:Arial,sans-serif;color:#361018;max-width:1180px;margin:0 auto;padding:18px 14px 42px;line-height:1.65;box-sizing:border-box}.qs-location *{box-sizing:border-box}.qs-location h1,.qs-location h2,.qs-location h3{font-family:Georgia,serif;color:#701326;line-height:1.24}.qs-location h1{font-size:clamp(29px,4vw,45px);margin:8px 0 14px}.qs-location h2{font-size:clamp(24px,3vw,32px);margin:0 0 14px}.qs-location h3{font-size:21px;margin:0 0 8px}.qs-location p{font-size:16px}.qs-hero{background:linear-gradient(135deg,#4b0714,#87182d);border:2px solid #d7b35a;border-radius:14px;color:#fff;padding:clamp(28px,5vw,58px);text-align:center}.qs-hero h1{color:#fff}.qs-hero p{color:#ffefd5;max-width:850px;margin:0 auto 23px}.qs-kicker{color:#ffd878;font-size:12px;font-weight:700;letter-spacing:1.1px;text-transform:uppercase}.qs-notice{background:#fff5dc;border:2px solid #d7b35a;border-radius:10px;color:#48101a;max-width:900px;margin:24px auto;padding:15px 18px;font-weight:700}.qs-actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}.qs-btn{background:#fff;color:#701326!important;border-radius:6px;display:inline-block;font-weight:700;padding:12px 19px;text-decoration:none}.qs-btn--gold{background:#d7b35a;color:#3b0b14!important}.qs-section{margin-top:30px;padding:28px;background:#fffdf9;border:1px solid #eadfcb;border-radius:12px;box-shadow:0 3px 14px rgba(58,17,24,.06)}.qs-photo-grid,.qs-detail-grid{display:grid;gap:20px;grid-template-columns:repeat(2,minmax(0,1fr))}.qs-photo{margin:0}.qs-photo img{display:block;width:100%;height:340px;object-fit:cover;border-radius:9px}.qs-photo figcaption{color:#6a5556;font-size:13px;margin-top:8px}.qs-list{padding-left:20px}.qs-list li{margin:8px 0}.qs-details{background:#fff6e7;border-left:5px solid #d7b35a;border-radius:7px;padding:20px}.qs-map{border:0;border-radius:9px;min-height:350px;width:100%}.qs-faq details{border-top:1px solid #eadfcb;padding:14px 0}.qs-faq summary{color:#701326;cursor:pointer;font-family:Georgia,serif;font-size:18px;font-weight:700}@media(max-width:700px){.qs-photo-grid,.qs-detail-grid{grid-template-columns:1fr}.qs-photo img{height:290px}.qs-section{padding:22px 18px}}
</style>

<main class="qs-location">
  <section class="qs-hero">
    <div class="qs-kicker">Oak Tree Road &bull; Iselin, New Jersey &bull; Since 2003</div>
    <h1>Quality Sweets &mdash; Authentic Indian Sweet Shop &amp; Takeout in Iselin, NJ</h1>
    <p>Visit our Oak Tree Road counter for fresh handcrafted mithai, hot samosas, and authentic Indian chaat. We proudly serve Iselin, Edison, Woodbridge, and Central New Jersey.</p>
    <div class="qs-notice">TAKEOUT &amp; COUNTER PICKUP ONLY &mdash; NO DINE-IN SEATING. Call or WhatsApp ahead and we will have your order packed to go.</div>
    <div class="qs-actions"><a class="qs-btn qs-btn--gold" href="tel:+17322833799">Call for Counter Pickup</a><a class="qs-btn" href="/menu/">View the Takeout Menu</a></div>
  </section>

  <section class="qs-section">
    <div class="qs-photo-grid">
      <figure class="qs-photo"><img src="__STOREFRONT_URL__" alt="Quality Sweets storefront at 1384 Oak Tree Road in Iselin, NJ" width="900" height="1020" fetchpriority="high"><figcaption>Quality Sweets on Oak Tree Road in Iselin, NJ.</figcaption></figure>
      <figure class="qs-photo"><img src="__COUNTER_URL__" alt="Fresh Indian mithai display counter at Quality Sweets in Iselin, NJ" width="900" height="1018" loading="lazy" decoding="async"><figcaption>Choose from fresh mithai at our in-store counter.</figcaption></figure>
    </div>
  </section>

  <section class="qs-section">
    <h2>Fresh Mithai Counter by the Pound on Oak Tree Road</h2>
    <p>Our Indian sweet shop near Edison prepares a wide selection of fresh mithai for counter pickup. Build a custom 1 lb, 2 lb, or 5 lb assortment of Bengali sweets, Kaju Katli, Motichur Ladoo, milk cake, pedas, and more. Quality Sweets is 100% vegetarian, made fresh daily, and uses no chemical preservatives.</p>
    <p>Looking to send a gift outside New Jersey? Browse our <a href="/indian-sweets/">Indian sweets available for nationwide delivery</a>.</p>
  </section>

  <section class="qs-section">
    <h2>Hot Samosas, Chaats &amp; Street Food To-Go</h2>
    <p>Pick up hot food prepared for takeout at our Iselin counter: freshly fried samosas, pani puri, samosa chaat, chole bhatura, parathas, pakodas, and more. Hot menu items are made for local pickup and are not available for postal shipping.</p>
    <p><a href="/menu/">See the official Iselin takeout menu</a> and order ahead by phone or WhatsApp to skip the wait.</p>
  </section>

  <section class="qs-section">
    <h2>Visit Our Store: Location, Hours &amp; Easy Pickup in Iselin / Edison NJ</h2>
    <div class="qs-detail-grid">
      <div class="qs-details">
        <h3>Quality Sweets</h3>
        <p><strong>Address:</strong><br>1384 Oak Tree Road<br>Iselin, NJ 08830<br><em>Conveniently bordering Edison, NJ</em></p>
        <p><strong>Phone:</strong> <a href="tel:+17322833799">(732) 283-3799</a></p>
        <p><strong>Hours:</strong><br>Monday&ndash;Sunday: 10:00 AM&ndash;8:00 PM<br>Open 7 days a week</p>
        <p><strong>Parking:</strong> Customer parking is available behind the store; please use the rear parking area when visiting Oak Tree Road.</p>
        <p>For current store photos, customer reviews, and updates, visit our <a href="https://share.google/bx8zwSjwrbn4FwjKH" target="_blank" rel="noopener">Google Business Profile</a>.</p>
        <p><a class="qs-btn qs-btn--gold" href="https://maps.app.goo.gl/CxdRcdqp4ikhE7wd7" target="_blank" rel="noopener">Get Directions</a></p>
      </div>
      <iframe class="qs-map" title="Map to Quality Sweets at 1384 Oak Tree Road, Iselin, NJ" loading="lazy" src="https://www.google.com/maps?q=40.5739404,-74.3261661&amp;z=16&amp;output=embed"></iframe>
    </div>
  </section>

  <section class="qs-section">
    <h2>Easy Pickup from NYC, Long Island &amp; Connecticut</h2>
    <p>Quality Sweets is a convenient stop for shoppers visiting the Little India corridor on Oak Tree Road. From New York City or Long Island, take the New Jersey Turnpike toward Central New Jersey and continue to Oak Tree Road. Metropark station is also about five minutes away by car. Call ahead and we will box your mithai and hot snacks for a quick pickup.</p>
  </section>

  <section class="qs-section qs-faq">
    <h2>Local Store FAQs</h2>
    <details><summary>Do you have tables or dine-in seating?</summary><p>No. We are a takeout and counter-pickup shop only. All food and sweets are packed to go.</p></details>
    <details><summary>Can I call ahead for a pickup order?</summary><p>Yes. Call <a href="tel:+17322833799">(732) 283-3799</a> to arrange a counter pickup.</p></details>
    <details><summary>Where should I park?</summary><p>Customer parking is available behind the store. Please use the rear parking area during busy Oak Tree Road hours.</p></details>
  </section>
</main>
<script>
  (function () {
    function replaceWithDiv(node) {
      var replacement = document.createElement('div');
      for (var i = 0; i < node.attributes.length; i += 1) {
        replacement.setAttribute(node.attributes[i].name, node.attributes[i].value);
      }
      replacement.className += ' qs-nonheading-label';
      replacement.innerHTML = node.innerHTML;
      node.parentNode.replaceChild(replacement, node);
    }

    Array.prototype.slice.call(document.querySelectorAll('h2')).forEach(function (heading) {
      if (heading.textContent.trim().toLowerCase() === 'categories') replaceWithDiv(heading);
    });
    Array.prototype.slice.call(document.querySelectorAll('h1')).forEach(function (heading) {
      if (heading.textContent.trim() === 'Quality Sweets Iselin NJ Store') heading.remove();
    });
  }());
</script>
""".replace("__STOREFRONT_URL__", storefront_url).replace("__COUNTER_URL__", counter_url)

payload = {
    "name": "Quality Sweets Iselin NJ Store",
    "type": "page",
    "url": "/locations/iselin-nj/",
    "body": body,
    "is_visible": True,
    "meta_title": "Indian Sweets | Quality Sweets Iselin & Woodbridge NJ",
    "meta_description": "Visit Quality Sweets on Oak Tree Rd in Iselin, NJ. Fresh handcrafted mithai, hot samosas & chaat for takeout & pickup. Serving Woodbridge & Central NJ.",
}

request = urllib.request.Request(f"{API_ROOT}/v2/pages", headers=HEADERS)
with urllib.request.urlopen(request, timeout=30) as response:
    pages = json.loads(response.read().decode("utf-8"))

existing = next((page for page in pages if page.get("url") == payload["url"]), None)
if existing:
    method, endpoint = "PUT", f"{API_ROOT}/v2/pages/{existing['id']}"
else:
    method, endpoint = "POST", f"{API_ROOT}/v2/pages"

request = urllib.request.Request(
    endpoint,
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method=method,
)
with urllib.request.urlopen(request, timeout=30) as response:
    result = json.loads(response.read().decode("utf-8"))

print(json.dumps({"page_id": result["id"], "url": f"https://qualitysweetsnj.com{result['url']}", "storefront_image": storefront_url, "counter_image": counter_url}, indent=2))
