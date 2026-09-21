import urllib.request
from bs4 import BeautifulSoup

url = "https://qualitysweetsnj.com/catering/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    col1 = soup.find(id="LayoutColumn1")
    if col1:
        print("Children of #LayoutColumn1:")
        for child in col1.children:
            if child.name:
                print(" -", child.name, "id:", child.get("id"), "class:", child.get("class"))
