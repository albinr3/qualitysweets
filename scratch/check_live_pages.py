import urllib.request
import re

def check_url(url):
    print(f"=== Checking {url} ===")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as res:
            html = res.read().decode('utf-8', errors='ignore')
            # Look for product titles / cards
            titles = re.findall(r'<div class="ProductDetails">.*?<a href="[^"]*">([^<]+)</a>', html, re.DOTALL)
            if not titles:
                titles = re.findall(r'class="p-name"[^>]*><a[^>]*>([^<]+)</a>', html)
            if not titles:
                # Classic BigCommerce Blueprint or Stencil pattern
                titles = re.findall(r'<a href="https://qualitysweetsnj\.com/[^"/]+/"[^>]*class="[^"]*(?:p-name|card-title|TrackLink)[^"]*"[^>]*>([^<]+)</a>', html)
            if not titles:
                titles = re.findall(r'<div class="ProductImage[^"]*">\s*<a href="([^"]+)"', html)
            
            print(f"Found {len(titles)} product items:")
            for t in titles[:10]:
                print(f"  - {t.strip()}")
            if len(titles) > 10:
                print(f"  ... and {len(titles) - 10} more")
            
            # Check pagination
            pages = re.findall(r'page=\d+', html)
            print(f"Pagination links found: {set(pages)}")
            
            # Check specifically for Khoya Kalakand
            if "Khoya Kalakand" in html:
                print(">>> Khoya Kalakand IS found on page HTML!")
            else:
                print(">>> Khoya Kalakand NOT found on page HTML!")
                
            # Check specifically for Sweets Basket Assortment
            if "Sweets Basket Assortment" in html:
                print(">>> Sweets Basket Assortment IS found on page HTML!")
            else:
                print(">>> Sweets Basket Assortment NOT found on page HTML!")

    except Exception as e:
        print("Error:", e)

check_url('https://qualitysweetsnj.com/indian-sweets/')
check_url('https://qualitysweetsnj.com/bengali-sweets/')
