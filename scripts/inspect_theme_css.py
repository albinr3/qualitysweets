import urllib.request
import re

url = 'https://qualitysweetsnj.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

links = re.findall(r'href="([^"]+\.css[^"]*)"', html)
for l in links:
    print('CSS:', l)
