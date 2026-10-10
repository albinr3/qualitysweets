import urllib.request
import re

def inspect_links(page_url):
    req = urllib.request.Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {page_url}: {e}")
        return
        
    print(f"\n=======================================================")
    print(f"PÁGINA: {page_url}")
    print(f"=======================================================")
    
    pattern = r'<a[^>]+href=["\']([^"\']*(?:samosas|pani-puri)[^"\']*)["\'][^>]*>(.*?)</a>'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
    
    seen = set()
    for href, raw_text in matches:
        clean_text = re.sub(r'<[^>]+>', '', raw_text).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        key = (href, clean_text)
        if key not in seen:
            seen.add(key)
            print(f"  • Enlace: {href}")
            print(f"    Texto Ancla: \"{clean_text}\"")

inspect_links("https://qualitysweetsnj.com/")
inspect_links("https://qualitysweetsnj.com/menu/")
inspect_links("https://qualitysweetsnj.com/menu/chaats/")
inspect_links("https://qualitysweetsnj.com/menu/street-food-snacks/")
inspect_links("https://qualitysweetsnj.com/menu/samosas/")
inspect_links("https://qualitysweetsnj.com/menu/pani-puri/")
