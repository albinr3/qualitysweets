import urllib.request
from bs4 import BeautifulSoup

url = "https://qualitysweetsnj.com/catering/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    desc = soup.find(class_="CategoryDescription")
    if desc:
        parents = [p.name + ("#" + p.get("id") if p.get("id") else "") + ("." + ".".join(p.get("class", [])) if p.get("class") else "") for p in desc.parents]
        print("Parent hierarchy for CategoryDescription:")
        for p in parents[:8]:
            print(" ->", p)
