import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://qualitysweetsnj.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as res:
    html = res.read().decode("utf-8", errors="ignore")

soup = BeautifulSoup(html, "html.parser")

print(f"Total HTML length: {len(html)}")

# Find all banners
banner_divs = soup.find_all("div", class_=re.compile(r"Banner", re.I))
print(f"Found {len(banner_divs)} banner elements:")
for b in banner_divs:
    print("  Class:", b.get("class"), "ID:", b.get("id"))

# Check for slide show
slideshow = soup.find(id="slide_show") or soup.find(class_=re.compile(r"slide", re.I))
if slideshow:
    print("Slideshow found: id =", slideshow.get("id"), "class =", slideshow.get("class"))
    # Check images inside slideshow
    for img in slideshow.find_all("img"):
        print("   Slide img:", img.get("src"))

# Print children of div.inner
slideshow = soup.find(id="HomeSlideShow")
if slideshow and slideshow.parent:
    print("\nChildren of div.inner:")
    for i, child in enumerate(slideshow.parent.find_all(recursive=False)):
        print(f"  {i}: <{child.name} id='{child.get('id')}' class='{child.get('class')}'>")


