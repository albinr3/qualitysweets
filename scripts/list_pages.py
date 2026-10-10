from pathlib import Path
import json, urllib.request

env = {}
for line in Path('.env').read_text(encoding='utf-8').splitlines():
    if '=' in line and not line.startswith('#'):
        k, v = line.strip().split('=', 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

req = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{env['BIGCOMMERCE_STORE_HASH']}/v2/pages",
    headers={"X-Auth-Token": env["BIGCOMMERCE_ACCESS_TOKEN"], "Accept": "application/json"}
)
with urllib.request.urlopen(req) as resp:
    pages = json.loads(resp.read().decode())
    for p in pages:
        print(f"ID {p.get('id')}: {p.get('url')} -> '{p.get('name')}' (visible={p.get('is_visible')})")
