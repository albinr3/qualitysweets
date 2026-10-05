import urllib.request
import json
from test_bc_page_llms import load_env, HEADERS, STORE_HASH

req = urllib.request.Request(f'https://api.bigcommerce.com/stores/{STORE_HASH}/v2/pages/20', headers=HEADERS)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print('Page 20 data:', data)

urls = [
    'https://qualitysweetsnj.com/llms.txt',
    'https://qualitysweetsnj.com/llms.txt/',
    'https://qualitysweetsnj.com/llms-txt/',
    'https://qualitysweetsnj.com/pages.php?pageid=20'
]

for test_url in urls:
    try:
        r = urllib.request.urlopen(urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'}))
        print(f'{test_url} -> {r.status}, Content-Type: {r.headers.get("Content-Type")}')
        print('Sample:', r.read(100).decode('utf-8', errors='ignore'))
    except urllib.error.HTTPError as e:
        print(f'{test_url} -> HTTPError {e.code}')
