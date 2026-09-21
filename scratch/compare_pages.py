import urllib.request
from bs4 import BeautifulSoup

def get_all_page_titles(base_url, max_pages=5):
    all_titles = []
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            titles = [a.get_text(strip=True) for a in soup.select('.ProductList .ProductDetails a') if a.get_text(strip=True)]
            if not titles:
                break
            for t in titles:
                all_titles.append((t, page))
        except Exception as e:
            break
    return all_titles

indian_sweets = get_all_page_titles('https://qualitysweetsnj.com/indian-sweets/')
bengali_sweets = get_all_page_titles('https://qualitysweetsnj.com/bengali-sweets/')

indian_dict = {t[0]: t[1] for t in indian_sweets}
bengali_dict = {t[0]: t[1] for t in bengali_sweets}

print(f"Total on Indian Sweets (across all pages): {len(indian_sweets)} (unique: {len(indian_dict)})")
print(f"Total on Bengali Sweets (across all pages): {len(bengali_sweets)} (unique: {len(bengali_dict)})")

print("\nWhere do Bengali Sweets appear in Indian Sweets?")
for name, b_page in sorted(bengali_dict.items()):
    in_page = indian_dict.get(name)
    if in_page:
        print(f"  [OK] {name:<35} -> Bengali pg {b_page} | Indian pg {in_page}")
    else:
        print(f"  [MISSING!] {name:<35} -> Bengali pg {b_page} | NOT in Indian Sweets!")
