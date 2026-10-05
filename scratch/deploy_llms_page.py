import urllib.request
import json
from pathlib import Path
from test_bc_page_llms import load_env, HEADERS, STORE_HASH

ROOT = Path(__file__).resolve().parent.parent
llms_text = (ROOT / "llms.txt").read_text(encoding="utf-8")

# Prepare HTML for raw page. Using <pre> ensures both human browsers and LLM scrapers see pristine text.
html_body = f'<pre style="word-wrap: break-word; white-space: pre-wrap; font-family: ui-monospace, Menlo, Monaco, Consolas, monospace; font-size: 14px; line-height: 1.6; color: #1a1a1a; background: #ffffff; padding: 24px; margin: 0; box-sizing: border-box;">{llms_text}</pre>'

payload = {
    "name": "llms.txt",
    "type": "raw",
    "body": html_body,
    "url": "/llms",
    "is_visible": False,
    "parent_id": 0
}

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{STORE_HASH}/v2/pages/20",
    data=json.dumps(payload).encode("utf-8"),
    headers=HEADERS,
    method="PUT"
)

try:
    with urllib.request.urlopen(req) as resp:
        print(f"Page 20 updated successfully! HTTP {resp.status}")
        data = json.loads(resp.read().decode("utf-8"))
        print(f"Page Name: {data.get('name')}, URL: {data.get('url')}, Visible: {data.get('is_visible')}")
except urllib.error.HTTPError as e:
    print(f"Error updating page 20: HTTP {e.code}")
    print(e.read().decode("utf-8"))
except Exception as e:
    print(f"Unexpected error: {e}")
