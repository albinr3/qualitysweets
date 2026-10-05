import urllib.request
import json
from test_bc_page_llms import load_env, HEADERS, STORE_HASH

# Test v3 storefront redirects POST
payload = [
    {
        "from_path": "/llms.txt",
        "site_id": 1000,
        "to": {
            "type": "url",
            "url": "https://qualitysweetsnj.com/about-us"
        }
    }
]

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v3/storefront/redirects",
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print("v3 Redirect POST Status:", resp.status)
        data = json.loads(resp.read().decode("utf-8"))
        print("Data:", json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
