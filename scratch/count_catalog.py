import urllib.request
from bs4 import BeautifulSoup

def count_products(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check products in catalog list
    # BigCommerce Blueprint uses .ProductList li or .ListItem
    items = soup.select('.ProductList li')
    if not items:
        items = soup.select('.productGrid .product')
    if not items:
        items = soup.select('.product')
    print(f"URL: {url}")
    print(f"Total .ProductList li found: {len(soup.select('.ProductList li'))}")
    
    titles = [a.get_text(strip=True) for a in soup.select('.ProductList .ProductDetails a') if a.get_text(strip=True)]
    print(f"Titles found ({len(titles)}): {titles[:5]}...")
    
    # Check pagination
    p_links = [a.get('href') for a in soup.select('.CategoryPagination a')]
    print(f"Pagination: {p_links}")

count_products('https://qualitysweetsnj.com/indian-sweets/')
count_products('https://qualitysweetsnj.com/bengali-sweets/')
