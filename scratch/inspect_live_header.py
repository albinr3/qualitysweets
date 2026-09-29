import urllib.request

req = urllib.request.Request('https://qualitysweetsnj.com/', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

idx = html.find('id="SideCategoryList"')
if idx != -1:
    print("SideCategoryList:")
    print(html[idx:idx+3500])
else:
    print("SideCategoryList not found")

menu_idx = html.find('id="menu"')
if menu_idx != -1:
    print("\n--- id='menu' ---")
    print(html[menu_idx:menu_idx+1500])
