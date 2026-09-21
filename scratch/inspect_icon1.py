import urllib.request
import re

url = "https://qualitysweetsnj.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8", errors="ignore")
    css_links = re.findall(r'<link[^>]+rel=[\"\']stylesheet[\"\'][^>]+href=[\"\']([^\"\']+)[\"\']', html, re.I)
    for cl in css_links:
        try:
            cr = urllib.request.urlopen(urllib.request.Request(cl, headers={"User-Agent": "Mozilla/5.0"}))
            css = cr.read().decode("utf-8", errors="ignore")
            matches = re.findall(r'([^{}]*icon1[^{]*\{[^}]*\})', css, re.I)
            if matches:
                print("In", cl)
                for m in matches:
                    print("  ", m.strip())
        except Exception as e:
            pass
