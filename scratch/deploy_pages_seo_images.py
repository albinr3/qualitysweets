import os
import json
import re
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {
    "X-Auth-Token": token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def api_request(url, data=None, method="GET"):
    req_data = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        print(f"HTTPError {e.code} for {method} {url}: {err_msg}")
        return {"error": e.code, "message": err_msg}
    except Exception as e:
        print(f"Error for {method} {url}: {e}")
        return {"error": str(e)}

print("=== 1. OPTIMIZING CATERING PAGE (/catering/ - Category 21) ===")
cat21 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21")
if cat21 and cat21.get('data'):
    desc21 = cat21['data'].get('description', '')
    
    # 1. Wedding gift box card
    desc21 = desc21.replace(
        '<img class="qs-card-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/402/wedding_gift_box_1789098119353__27913.1789098267.350.350.jpg?c=2" alt="Mithai gift box for a wedding" loading="lazy">',
        '<img class="qs-card-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/402/wedding_gift_box_1789098119353__27913.1789098267.350.350.jpg?c=2" alt="Decorative Indian mithai gift boxes for wedding return gifts and celebrations - Quality Sweets NJ" width="350" height="350" loading="lazy" decoding="async">'
    )
    
    # 2. Bulk samosas platter card
    desc21 = desc21.replace(
        '<img class="qs-card-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/404/bulk_samosas_platter_1789098151834__74896.1789098270.350.350.jpg?c=2" alt="Fresh samosas prepared for a large order" loading="lazy">',
        '<img class="qs-card-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/404/bulk_samosas_platter_1789098151834__74896.1789098270.350.350.jpg?c=2" alt="Freshly fried crispy samosa platters prepared for party catering in NJ NY CT" width="350" height="350" loading="lazy" decoding="async">'
    )
    
    # 3. Temple bulk prasad card
    desc21 = desc21.replace(
        '<img class="qs-card-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/403/temple_bulk_prasad_1789098135260__33231.1789098269.350.350.jpg?c=2" alt="Bulk mithai order for a temple celebration" loading="lazy">',
        '<img class="qs-card-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/403/temple_bulk_prasad_1789098135260__33231.1789098269.350.350.jpg?c=2" alt="Handcrafted bulk mithai boxes for temple celebrations and mandir prasad in New Jersey" width="350" height="350" loading="lazy" decoding="async">'
    )
    
    # 4. Samosa feature image
    desc21 = desc21.replace(
        '<img class="qs-feature-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/404/bulk_samosas_platter_1789098151834__74896.1789098270.350.350.jpg?c=2" alt="Samosa catering platter" loading="lazy">',
        '<img class="qs-feature-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/404/bulk_samosas_platter_1789098151834__74896.1789098270.350.350.jpg?c=2" alt="Crispy hot samosa party catering platter ready for pickup or Tri-State delivery" width="350" height="350" loading="lazy" decoding="async">'
    )
    
    # 5. Wedding favor box
    desc21 = desc21.replace(
        '<img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/402/wedding_gift_box_1789098119353__27913.1789098267.350.350.jpg?c=2" alt="Wedding mithai favor box" loading="lazy">',
        '<img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/402/wedding_gift_box_1789098119353__27913.1789098267.350.350.jpg?c=2" alt="Custom wedding mithai favor box with artisan Indian sweets - Quality Sweets Iselin" width="350" height="350" loading="lazy" decoding="async">'
    )
    
    # 6. Temple prasad feature image
    desc21 = desc21.replace(
        '<img class="qs-feature-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/403/temple_bulk_prasad_1789098135260__33231.1789098269.350.350.jpg?c=2" alt="Indian sweets for temple and mandir orders" loading="lazy">',
        '<img class="qs-feature-image" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/403/temple_bulk_prasad_1789098135260__33231.1789098269.350.350.jpg?c=2" alt="Authentic bulk Indian sweets assortments for temple events and community gatherings" width="350" height="350" loading="lazy" decoding="async">'
    )
    
    res21 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/21", data={"description": desc21}, method="PUT")
    print("Catering Category 21 updated:", "data" in res21)

print("\n=== 2. OPTIMIZING TAKEOUT MENU HERO (/menu/ - Page 10) ===")
p10 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/10")
if p10 and "body" in p10:
    b10 = p10["body"]
    b10 = b10.replace(
        '<img class="menu-hero" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/409/samosa-chaat-menu-hero__27274.1789244397.1280.1280.jpg?c=2" alt="Samosa chaat topped with chickpeas, yogurt, cilantro and chutneys">',
        '<img class="menu-hero" src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/409/samosa-chaat-menu-hero__27274.1789244397.1280.1280.jpg?c=2" alt="Fresh hot samosa chaat with chickpeas, yogurt, cilantro and tamarind chutney - Quality Sweets Iselin Takeout Menu" width="1200" height="600" fetchpriority="high">'
    )
    res10 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/10", data={"body": b10}, method="PUT")
    print("Page 10 (Takeout Menu) updated:", "id" in res10)

print("\n=== 3. OPTIMIZING BANNER 5 (Home Page Category Cards) ===")
b5 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5")
if b5 and "content" in b5:
    c5 = b5["content"]
    c5 = c5.replace(
        '<img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/sweets-banner.png?t=1433913168" alt="All Indian Sweets" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />',
        '<img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/sweets-banner.png?t=1433913168" alt="All Indian Sweets - Handcrafted traditional and Bengali mithai selection at Quality Sweets" width="600" height="270" loading="lazy" decoding="async" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />'
    )
    c5 = c5.replace(
        '<img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/snacks-banner.png?t=1433913279" alt="Indian Snacks & Namkeen" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />',
        '<img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/snacks-banner.png?t=1433913279" alt="Indian Snacks and Namkeen - Mathi, namak para, sev and spiced cashews at Quality Sweets" width="600" height="270" loading="lazy" decoding="async" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />'
    )
    c5 = c5.replace(
        '<img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/gift-boxes-banner.png" alt="Mithai Boxes & Gift Baskets" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />',
        '<img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/gift-boxes-banner.png" alt="Mithai Boxes and Gift Baskets - Luxury Indian sweets gift hampers for Diwali and weddings" width="600" height="270" loading="lazy" decoding="async" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />'
    )
    res5 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5", data={"content": c5}, method="PUT")
    print("Banner 5 updated:", "id" in res5)

print("\n=== 4. OPTIMIZING BANNER 7 (Home Page Product & Service Cards) ===")
b7 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/7")
if b7 and "content" in b7:
    c7 = b7["content"]
    # Add width="350" height="160" loading="lazy" decoding="async" to the product images if missing
    replacements = [
        ('alt="Samosa &amp; Papri Chaat" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />',
         'alt="Fresh Samosa and Papri Chaat to-go in Iselin NJ - Quality Sweets" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />'),
        
        ('alt="Pani Puri Kits To-Go" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />',
         'alt="Crispy Pani Puri kits to-go with flavored water - Quality Sweets Iselin" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />'),
        
        ('alt="Hot Chole Bhatura" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />',
         'alt="Fresh hot Chole Bhatura with spiced chickpeas - Quality Sweets Iselin Takeout" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />'),
        
        ('alt="Aloo &amp; Gobi Parathas" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />',
         'alt="Fresh griddled Aloo and Gobi Parathas with butter - Quality Sweets" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />'),
        
        ('alt="Malai Chum Chum" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />',
         'alt="Bengali Malai Chum Chum handcrafted fresh daily - Quality Sweets" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />'),
        
        ('alt="Slow-Cooked Milk Cake" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />',
         'alt="Traditional slow cooked caramelized Milk Cake fudge - Quality Sweets" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />'),
        
        ('alt="Fresh Mango Sandesh" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />',
         'alt="Fresh artisan Mango Sandesh Bengali cottage cheese sweet - Quality Sweets" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />'),
        
        ('alt="Pure Besan Ladoo" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />',
         'alt="Traditional roasted Besan Ladoo with pure desi ghee - Quality Sweets" width="350" height="160" loading="lazy" decoding="async" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" />'),
        
        ('alt="Wedding Sweet Boxes &amp; Return Gifts" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />',
         'alt="Luxury wedding sweet boxes and celebratory return gifts - Quality Sweets NJ" width="350" height="175" loading="lazy" decoding="async" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />'),
        
        ('alt="Temple &amp; Mandir Bulk Prasad" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />',
         'alt="Fresh temple and mandir bulk prasad mithai boxes in NJ and NY - Quality Sweets" width="350" height="175" loading="lazy" decoding="async" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />'),
        
        ('alt="Bulk Fresh Samosa Trays" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />',
         'alt="Commercial party trays of freshly fried samosas for event catering - Quality Sweets" width="350" height="175" loading="lazy" decoding="async" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />')
    ]
    for old_sub, new_sub in replacements:
        c7 = c7.replace(old_sub, new_sub)
    
    res7 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/7", data={"content": c7}, method="PUT")
    print("Banner 7 updated:", "id" in res7)

print("\n[SUCCESS] Completed all page and banner image SEO enhancements.")
