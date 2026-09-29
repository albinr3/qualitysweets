import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

# Find all occurrences of qs-footer-nap
matches = [m.start() for m in re.finditer(r'qs-footer-nap', html)]
print("qs-footer-nap occurrences:", len(matches))
for i, pos in enumerate(matches):
    start = max(0, pos - 200)
    end = min(len(html), pos + 200)
    print(f"\n--- Occurrence {i} at {pos} ---")
    print(html[start:end])
