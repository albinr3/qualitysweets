import os
import sys
import urllib.request
import json
from dotenv import load_dotenv

sys.path.insert(0, '.')

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')
headers = {'X-Auth-Token': token, 'Accept': 'application/json', 'Content-Type': 'application/json'}

scripts_url = f'https://api.bigcommerce.com/stores/{store_hash}/v3/content/scripts'
req = urllib.request.Request(scripts_url, headers=headers)
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    footer_script = next((s for s in data['data'] if 'Footer' in s.get('name', '')), None)
    print("Found script:", footer_script)
    if footer_script:
        uuid = footer_script['uuid']
        put_url = f'{scripts_url}/{uuid}'
        from scripts.deploy_footer_navigation import FOOTER_NAV_SCRIPT_HTML
        payload = {
            'name': 'Quality Sweets Footer Navigation',
            'description': 'Configures clean 4-column footer layout',
            'html': FOOTER_NAV_SCRIPT_HTML,
            'auto_uninstall': True,
            'load_method': 'default',
            'location': 'footer',
            'visibility': 'storefront',
            'kind': 'script_tag',
            'consent_category': 'essential',
            'enabled': True
        }
        try:
            req_put = urllib.request.Request(put_url, headers=headers, method='PUT', data=json.dumps(payload).encode())
            with urllib.request.urlopen(req_put) as res_put:
                print('Success:', res_put.status)
        except urllib.error.HTTPError as e:
            print('HTTPError:', e.code, e.read().decode())
