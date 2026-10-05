import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {
    "X-Auth-Token": token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Fetch Banner 5
req = urllib.request.Request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5", headers=headers)
with urllib.request.urlopen(req) as resp:
    b5 = json.loads(resp.read().decode())

content = b5['content']

seo_script = """
<script id="qs-home-images-seo">
(function () {
  function optimizeHomeImages() {
    // 1. Logo
    var logo = document.getElementById('LogoImage') || document.querySelector('img[src*="qs2021-01"]');
    if (logo) {
      logo.alt = 'Quality Sweets - Authentic Indian Sweets & Mithai in Iselin NJ';
      if (!logo.getAttribute('width')) logo.setAttribute('width', '240');
      if (!logo.getAttribute('height')) logo.setAttribute('height', '50');
      logo.setAttribute('fetchpriority', 'high');
    }

    // 2. Theme Slideshow Carousel Images
    var slides = document.querySelectorAll('.slide-show img, .slide-image, img[src*="theme_images"]');
    slides.forEach(function (img) {
      var src = img.getAttribute('src') || '';
      if (src.indexOf('gift_basket') !== -1) {
        img.alt = 'Assorted Indian Sweets Gift Baskets and Festive Hampers - Quality Sweets Iselin NJ';
        img.setAttribute('title', 'Festive Mithai Gift Baskets');
        img.setAttribute('loading', 'lazy');
        img.setAttribute('decoding', 'async');
      } else if (src.indexOf('QS_banner') !== -1) {
        img.alt = 'Quality Sweets Authentic Handcrafted Indian Mithai and Fresh Snacks Daily';
        img.setAttribute('title', 'Handcrafted Indian Sweets Daily');
        img.setAttribute('loading', 'lazy');
        img.setAttribute('decoding', 'async');
      } else if (src.indexOf('bulk_orders') !== -1) {
        img.alt = 'Special Bulk Pricing on Indian Sweets and Event Catering in NJ NY CT - Quality Sweets';
        img.setAttribute('title', 'Bulk Mithai and Catering Orders');
        img.setAttribute('loading', 'lazy');
        img.setAttribute('decoding', 'async');
      }
    });

    // 3. Decorative Blueprint rating star icons (WCAG / SEO Accessibility)
    var ratings = document.querySelectorAll('img[src*="IcoRating"]');
    ratings.forEach(function (img) {
      if (!img.getAttribute('alt')) {
        img.setAttribute('alt', 'Customer Rating');
        img.setAttribute('role', 'presentation');
      }
    });

    // 4. Loader gif/png (decorative)
    var loaders = document.querySelectorAll('img[src*="loader.png"]');
    loaders.forEach(function (img) {
      if (!img.getAttribute('alt')) {
        img.setAttribute('alt', '');
        img.setAttribute('role', 'presentation');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', optimizeHomeImages, { once: true });
  } else {
    optimizeHomeImages();
  }
  window.addEventListener('load', optimizeHomeImages, { once: true });
})();
</script>
"""

if 'id="qs-home-images-seo"' not in content:
    content += "\n" + seo_script
    req_update = urllib.request.Request(
        f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5",
        data=json.dumps({"content": content}).encode('utf-8'),
        headers=headers,
        method="PUT"
    )
    with urllib.request.urlopen(req_update) as resp:
        res = json.loads(resp.read().decode())
        print("Updated Banner 5 with Home SEO images script. ID:", res.get('id'))
else:
    print("Banner 5 already contains qs-home-images-seo script.")
