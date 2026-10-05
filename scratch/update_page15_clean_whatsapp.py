import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ['BIGCOMMERCE_STORE_HASH']
token = os.environ['BIGCOMMERCE_ACCESS_TOKEN']
headers = {
    'X-Auth-Token': token,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# 1. Fetch current body from v2
res = requests.get(f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15', headers=headers)
if res.status_code != 200:
    print(f"Error fetching page: {res.status_code} - {res.text}")
    exit(1)

body = res.json()['body']

# 2. Make substitutions
replacements = [
    # Notice banner
    (
        'Call or WhatsApp ahead and we will have your order packed to go.',
        'Call ahead and we will have your order packed to go.'
    ),
    # Takeout button color (change from plain white .qs-btn to .qs-btn .qs-btn--gold)
    (
        '<div class="qs-actions"><a class="qs-btn" href="/menu/">View the Takeout Menu</a></div>',
        '<div class="qs-actions"><a class="qs-btn qs-btn--gold" href="/menu/">View the Takeout Menu</a></div>'
    ),
    # Street food section
    (
        '<p><a href="/menu/">See the official Iselin takeout menu</a> and order ahead by phone or WhatsApp to skip the wait.</p>',
        '<p><a href="/menu/">See the official Iselin takeout menu</a> and order ahead by phone to skip the wait.</p>'
    ),
    # Phone / WhatsApp section
    (
        '<p><strong>Phone:</strong> <a href="tel:+17322833799">(732) 283-3799</a><br><strong>WhatsApp:</strong> <a href="https://wa.me/17328037617" target="_blank" rel="noopener">(732) 803-7617</a></p>',
        '<p><strong>Phone:</strong> <a href="tel:+17322833799">(732) 283-3799</a></p>'
    ),
    # FAQ details
    (
        '<details><summary>Can I call ahead for a pickup order?</summary><p>Yes. Call <a href="tel:+17322833799">(732) 283-3799</a> or message <a href="https://wa.me/17328037617" target="_blank" rel="noopener">WhatsApp</a> to arrange a counter pickup.</p></details>',
        '<details><summary>Can I call ahead for a pickup order?</summary><p>Yes. Call <a href="tel:+17322833799">(732) 283-3799</a> to arrange a counter pickup.</p></details>'
    )
]

for old, new in replacements:
    if old not in body:
        print(f"FAILED TO FIND TARGET: {old[:50]}...")
        exit(1)
    body = body.replace(old, new)
    print(f"Replaced: {old[:40]}... -> {new[:40]}...")

# 3. Check for any remaining whatsapp references
remaining_wa = [line for line in body.split('\n') if 'whatsapp' in line.lower() or 'wa.me' in line.lower() or '803' in line]
print(f"Remaining WhatsApp lines: {len(remaining_wa)}")
if remaining_wa:
    for line in remaining_wa:
        print("Remaining line:", line.strip())
    exit(1)

# 4. PUT updated body to BigCommerce
put_res = requests.put(
    f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/15',
    headers=headers,
    json={'body': body}
)

if put_res.status_code == 200:
    print("SUCCESS: Page 15 updated on BigCommerce!")
else:
    print(f"ERROR: Update failed with status {put_res.status_code}: {put_res.text}")
    exit(1)
