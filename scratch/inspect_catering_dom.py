import urllib.request
from bs4 import BeautifulSoup

url = "https://qualitysweetsnj.com/catering/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
        print("HTML Length:", len(html))
        
        # Check if .qs-catering is in html
        if "qs-catering" in html:
            print("[FOUND] .qs-catering is in the raw HTML response!")
        else:
            print("[MISSING] .qs-catering is NOT in raw HTML!")
            
        soup = BeautifulSoup(html, "html.parser")
        desc = soup.find(class_="CategoryDescription") or soup.find(id="CategoryDescription")
        if desc:
            print("[FOUND] CategoryDescription block found!")
        else:
            print("[NOT FOUND] CategoryDescription tag not found by class/id")
            
        # Print layout container classes/ids around body
        body = soup.find("body")
        if body:
            print("Body class/id:", body.get("class"), body.get("id"))
            
except Exception as e:
    print("Error:", e)
