import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

# Check where .SideCategoryListFlyout exists
menus = re.findall(r'<div class="SideCategoryListFlyout">\s*<ul class="sf-menu sf-horizontal">([\s\S]*?)</ul>\s*</div>', html)
print(f"Total menus matched: {len(menus)}")

for i, m in enumerate(menus):
    print(f"\n--- Menu {i} ---")
    items = re.findall(r'<li><a href="([^"]*)">(.*?)</a>', m)
    for href, text in items:
        print(f"  - [{text}] -> {href}")
