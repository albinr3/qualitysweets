import urllib.request, re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

css_files = re.findall(r'href="([^"]+\.css[^"]*)"', html)
for c in css_files:
    print('CSS:', c)

# find font-family definitions in the first CSS or HTML
google_fonts = re.findall(r'fonts\.googleapis\.com[^\'"]+', html)
print('Google fonts:', google_fonts)
