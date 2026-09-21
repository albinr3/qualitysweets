import urllib.request
import re

for url in ['https://qualitysweetsnj.com/menu/', 'https://qualitysweetsnj.com/menu/chaats/']:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as res:
        html = res.read().decode('utf-8', errors='ignore')
        print(f"=== Verifying {url} ===")
        chaat_cards = re.findall(r'<h3>(.*?)</h3>\s*<p class="price">(.*?)</p>', html)
        for name, price in chaat_cards:
            print(f"  {name:<25}: {price}")
