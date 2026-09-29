import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
print(f"Total script tags: {len(scripts)}")
for i, s in enumerate(scripts):
    snippet = s.strip()[:100].replace('\n', ' ')
    if any(k in s for k in ['qs-', 'Header', 'Footer', 'SideCategoryList', 'catering', 'menu']):
        print(f"Script {i}: {snippet}...")
