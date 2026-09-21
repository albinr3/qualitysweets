import urllib.request
from bs4 import BeautifulSoup

url = "https://qualitysweetsnj.com/indian-sweets/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    
    footer_upper = soup.find(id="FooterUpper")
    if footer_upper:
        contact_col = footer_upper.find(class_="contact")
        if contact_col:
            print("=== CONTACT COL ON /indian-sweets/ ===")
            print(contact_col.prettify())
