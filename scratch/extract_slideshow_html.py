import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

idx = html.find('slide-show')
if idx != -1:
    print(html[idx-100:idx+1500])
