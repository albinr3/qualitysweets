import urllib.request
import json
from pathlib import Path
from test_bc_page_llms import HEADERS, STORE_HASH

ROOT = Path(__file__).resolve().parent.parent
full_text = (ROOT / "llms-full.txt").read_text(encoding="utf-8")
html_body = f'<pre style="word-wrap: break-word; white-space: pre-wrap; font-family: ui-monospace, Menlo, Monaco, Consolas, monospace; font-size: 14px; line-height: 1.6; color: #1a1a1a; background: #ffffff; padding: 24px; margin: 0; box-sizing: border-box;">{full_text}</pre>'

# 1. Create raw page /llms-full
payload = {
    "name": "llms-full.txt",
    "type": "raw",
    "body": html_body,
    "url": "/llms-full",
    "is_visible": False,
    "parent_id": 0
}

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/pages",
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        print(f"Page llms-full created: HTTP {resp.status}")
        data = json.loads(resp.read().decode("utf-8"))
        page_id = data.get("id")
        print(f"Page ID: {page_id}")
except urllib.error.HTTPError as e:
    print(f"Error creating page: HTTP {e.code}")
    print(e.read().decode("utf-8"))

# 2. Create redirect /llms-full.txt -> /llms-full
redirect_payload = {
    "path": "/llms-full.txt",
    "forward": {
        "type": "manual",
        "ref": "https://qualitysweetsnj.com/llms-full"
    }
}
req2 = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/redirects",
    data=json.dumps(redirect_payload).encode("utf-8"),
    headers=HEADERS,
    method="POST"
)
try:
    with urllib.request.urlopen(req2) as resp:
        print(f"Redirect /llms-full.txt created: HTTP {resp.status}")
except urllib.error.HTTPError as e:
    print(f"Redirect error: HTTP {e.code}")
    print(e.read().decode("utf-8"))
