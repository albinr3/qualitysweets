import urllib.request
import re

url = "https://qualitysweetsnj.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

try:
    with urllib.request.urlopen(req, timeout=15) as res:
        html = res.read().decode("utf-8", errors="ignore")
        title_m = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        kw_m = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        
        print("HTTP Status:", res.status)
        print("Live Title Tag:", title_m.group(1).strip() if title_m else "NOT FOUND")
        print("Live Meta Description:", desc_m.group(1).strip() if desc_m else "NOT FOUND")
        print("Live Meta Keywords:", kw_m.group(1).strip() if kw_m else "NOT FOUND")
except Exception as e:
    print("Error connecting to live store:", e)
