import requests

res = requests.get('https://qualitysweetsnj.com/locations/iselin-nj/', headers={'User-Agent': 'Mozilla/5.0'})
tag = '<div class="qs-actions">'
start = res.text.find(tag)
if start != -1:
    end = res.text.find('</div>', start) + 6
    print("LIVE ACTIONS HTML:")
    print(res.text[start:end])
else:
    print("Not found")
