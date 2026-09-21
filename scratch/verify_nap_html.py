import urllib.request

for url in ["https://qualitysweetsnj.com/", "https://qualitysweetsnj.com/indian-sweets/"]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        print(f"URL: {url}")
        print("Contains 'qs-footer-nap'?", "qs-footer-nap" in html)
        print("Contains 'Quality Sweets - Indian Sweets Shop'?", "Quality Sweets - Indian Sweets Shop" in html)
        print("-" * 50)
