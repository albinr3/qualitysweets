import urllib.request
import re

url = "https://qualitysweetsnj.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")
    # Find all stylesheet links
    css_links = re.findall(r'<link[^>]+rel=[\"\']stylesheet[\"\'][^>]+href=[\"\']([^\"\']+)[\"\']', html, re.I)
    for cl in css_links:
        print("CSS Link:", cl)
        if "theme" in cl or "styles" in cl or "coffee" in cl or "default" in cl:
            try:
                css_req = urllib.request.Request(cl, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(css_req) as cr:
                    css = cr.read().decode("utf-8", errors="ignore")
                    matches = re.findall(r'([^{}]*(?:FooterUpper|block_2|icon1|icon2|icon3)[^{]*\{[^}]*\})', css, re.I)
                    for m in matches[:10]:
                        print("Match:", m.strip())
            except Exception as e:
                print("Error loading css:", e)
