import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

print('Length of HTML:', len(html))
for level in ['h1', 'h2', 'h3', 'h4']:
    hs = re.findall(rf'<{level}[^>]*>(.*?)</{level}>', html, re.IGNORECASE | re.DOTALL)
    print(f'{level.upper()} count: {len(hs)}')
    for h in hs[:6]:
        cleaned = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h)).strip()
        print(f'   {cleaned[:70]}')

# Look for header elements and scripts
header = re.search(r'<div[^>]*id=["\']Header["\'][^>]*>(.*?)</div>', html, re.IGNORECASE | re.DOTALL)
if header:
    print('Header snippet found')

# Look for Banners or HomeContent
banners = re.findall(r'<div[^>]*class=["\'][^"\']*Banner[^"\']*["\'][^>]*>', html, re.IGNORECASE)
print('Banner divs found:', len(banners))
