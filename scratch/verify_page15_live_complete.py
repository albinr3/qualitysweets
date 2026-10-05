import requests

url = 'https://qualitysweetsnj.com/locations/iselin-nj/'
res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
content = res.text

# Check WhatsApp references
wa_found = 'whatsapp' in content.lower()
wame_found = 'wa.me' in content.lower()
num_found = '803' in content or '803-7617' in content

print("Live checks:")
print("Status:", res.status_code)
print("WhatsApp text in live page:", wa_found)
print("wa.me in live page:", wame_found)
print("WhatsApp number in live page:", num_found)

# Check button in live page
start = content.find('<div class="qs-actions">')
if start != -1:
    end = content.find('</div>', start) + 6
    print("Live button HTML:", content[start:end])
else:
    print("qs-actions not found")
