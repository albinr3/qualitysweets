import urllib.request
from bs4 import BeautifulSoup

url = 'https://qualitysweetsnj.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
b_bottom = soup.find(class_='banner_home_page_bottom')
curr = b_bottom
while curr:
    print(f"{curr.name} id={curr.get('id')} class={curr.get('class')}")
    curr = curr.parent
