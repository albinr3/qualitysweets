import urllib.request
import re

for url in ['https://qualitysweetsnj.com/menu/', 'https://qualitysweetsnj.com/menu/street-food-snacks/']:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8', errors='ignore')
        print(f"=== Verifying {url} ===")
        cards = re.findall(r'<h3>(.*?)</h3>\s*<p class="price">(.*?)</p>\s*<p>(.*?)</p>', html)
        for name, price, desc in cards:
            print(f"  {name:<30} | {price:<12} | {desc[:60]}...")
        if "Dhokla" in html:
            print("  [WARNING] Dhokla still found in page!")
        else:
            print("  [OK] Dhokla successfully removed!")
