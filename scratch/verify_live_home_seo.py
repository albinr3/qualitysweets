import urllib.request
import re

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

print("Script qs-home-images-seo present in live HTML:", 'id="qs-home-images-seo"' in html)

# Let's inspect the images in live HTML
imgs = re.findall(r'<img[^>]*>', html)
print(f"Total img tags found in raw HTML: {len(imgs)}")

# Let's check Banner 5 images
print("\nBanner 5 category cards in live HTML:")
for img in imgs:
    if 'sweets-banner' in img or 'snacks-banner' in img or 'gift-boxes-banner' in img:
        print(img)

# Let's check featured product card images in live HTML
print("\nSample featured product images in live HTML:")
found = 0
for img in imgs:
    if '/products/' in img and found < 5:
        alt = re.search(r'alt=["\']([^"\']*)["\']', img)
        print(f"Product Img: alt='{alt.group(1) if alt else 'EMPTY'}'")
        found += 1
