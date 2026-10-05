import urllib.request
import json
from test_bc_page_llms import load_env, HEADERS, STORE_HASH

update_payload = {'url': '/llms', 'is_visible': True}
req = urllib.request.Request(
    f'https://api.bigcommerce.com/stores/{STORE_HASH}/v2/pages/20',
    data=json.dumps(update_payload).encode('utf-8'),
    headers=HEADERS,
    method='PUT'
)
try:
    with urllib.request.urlopen(req) as resp:
        print('Updated page 20:', resp.status)
        print(resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('Update error:', e.code, e.read().decode('utf-8'))

for test_url in ['https://qualitysweetsnj.com/llms', 'https://qualitysweetsnj.com/llms/']:
    try:
        r = urllib.request.urlopen(urllib.request.Request(test_url, headers={'User-Agent': 'Mozilla/5.0'}))
        print(f'{test_url} -> {r.status}, Content-Type: {r.headers.get("Content-Type")}')
        print(r.read(200).decode('utf-8', errors='ignore'))
    except urllib.error.HTTPError as e:
        print(f'{test_url} -> HTTPError {e.code}')
