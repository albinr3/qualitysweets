import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

# Check all places with SideCategoryList or mobile menu
matches = [m.start() for m in re.finditer(r'SideCategoryListFlyout', html)]
print("SideCategoryListFlyout count:", len(matches))
for i, pos in enumerate(matches):
    print(f"Match {i} at {pos}:")
    print(html[max(0, pos-200):min(len(html), pos+500)])
