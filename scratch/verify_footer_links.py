import urllib.request

links = {
    "All Indian Sweets": "/indian-sweets/",
    "Barfi & Kaju Katli": "/barfi/",
    "Bengali Sweets": "/bengali-sweets/",
    "Indian Snacks & Namkeen": "/indian-snacks/",
    "Mithai Boxes & Gift Baskets": "/mithai-box/",
    "Takeout Menu": "/menu/",
    "Catering & Bulk Orders": "/catering/",
    "Quality Sweets Iselin NJ Store": "/locations/iselin-nj/",
    "Contact Us": "/contact-us/",
    "About Us": "/about-us/",
    "Shipping & Refunds": "/shipping-refunds/",
    "Packaging Information": "/packaging-information/",
    "Security & Privacy": "/security-and-privacy/",
    "Blog": "/blog/",
    "Sitemap": "/sitemap/",
}

base = "https://qualitysweetsnj.com"
for name, path in links.items():
    url = base + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            print(f"[OK {resp.status}] {name:30} -> {url} (Final: {resp.geturl()})")
    except urllib.error.HTTPError as e:
        print(f"[ERR {e.code}] {name:30} -> {url}")
    except Exception as e:
        print(f"[EXC] {name:30} -> {url}: {e}")
