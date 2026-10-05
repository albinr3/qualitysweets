import urllib.request
import json
from test_bc_page_llms import load_env, HEADERS, STORE_HASH

# Try to create a redirect for /llms.txt via v2 redirects API
redirect_payload = {
    "path": "/llms.txt",
    "forward": {
        "type": "manual",
        "ref": 0
    },
    "url": "https://qualitysweetsnj.com/pages.php?pageid=20"
}

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/redirects",
    data=json.dumps(redirect_payload).encode("utf-8"),
    headers=HEADERS,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print("Redirect create response:", resp.status)
        data = json.loads(resp.read().decode("utf-8"))
        print("Redirect created:", data)
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
