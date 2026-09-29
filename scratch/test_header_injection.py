import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

# Check instances of SideCategoryListFlyout
matches = list(re.finditer(r'<div class="SideCategoryListFlyout">\s*<ul class="sf-menu sf-horizontal">', html))
print(f"Found {len(matches)} category flyout menus in HTML:")

for i, m in enumerate(matches):
    start = m.start()
    end = html.find('</ul>', start) + 5
    menu_html = html[start:end]
    print(f"\n--- Menu {i} ---")
    items = re.findall(r'<li><a href="[^"]*">(.*?)</a>', menu_html)
    print("Items:", items)
