import urllib.request
from bs4 import BeautifulSoup

url = "https://qualitysweetsnj.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
    contact = soup.select_one("#FooterUpper .Column.contact")
    if contact:
        print(contact.prettify())
