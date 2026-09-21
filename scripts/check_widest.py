import urllib.request
from bs4 import BeautifulSoup

url = 'https://qualitysweetsnj.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
content_widest = soup.find('div', class_='main').find('div', class_='inner').find('div', class_='Widest')
for i, c in enumerate(content_widest.find_all(recursive=False)):
    print(f"{i}: {c.name} id={c.get('id')} class={c.get('class')}")
