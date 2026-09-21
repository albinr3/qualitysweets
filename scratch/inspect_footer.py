import urllib.request
import re
from bs4 import BeautifulSoup

url = "https://qualitysweetsnj.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    
    footer_upper = soup.find(id="FooterUpper")
    if footer_upper:
        print("=== FOOTER UPPER ===")
        print(footer_upper.prettify())
    
    footer_lower = soup.find(id="Footer")
    if footer_lower:
        print("=== FOOTER ===")
        print(footer_lower.prettify())
