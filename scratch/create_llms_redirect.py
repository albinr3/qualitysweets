import urllib.request
import json
from test_bc_page_llms import load_env, HEADERS, STORE_HASH

payload = {
    "path": "/llms.txt",
    "forward": {
        "type": "manual",
        "ref": "https://qualitysweetsnj.com/llms"
    }
}

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/redirects",
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print("Redirect create response:", resp.status)
        data = json.loads(resp.read().decode("utf-8"))
        print("Created redirect:", data)
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
