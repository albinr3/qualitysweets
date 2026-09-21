import os
import json
import urllib.request
import re
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

# New street food grid HTML
new_street_food_cards = """<article class="card"><h3>Fresh Samosas — Never Frozen</h3><p class="price">$1.75</p><p>Freshly made golden pastry cones stuffed with seasoned potatoes and green peas. Prepared fresh daily from 6:00 AM.</p></article><article class="card"><h3>Chole Bhatura</h3><p class="price">$9.00</p><p>Two giant, freshly puffed bhature served with rich Punjabi chole masala, onions, and spicy Indian pickle.</p></article><article class="card"><h3>Chole Puri</h3><p class="price">$9.00</p><p>Four warm, fluffy whole wheat puris served with authentic spiced chickpea curry and pickle.</p></article><article class="card"><h3>Paneer Pakoda</h3><p class="price">$15.00 / lb</p><p>Fresh paneer slices dipped in a spiced gram flour batter and fried until golden and crisp. Sold by the pound.</p></article><article class="card"><h3>Cut Mirchy Pakoda</h3><p class="price">$6.00 / lb</p><p>Spiced green pepper pakodas, sliced and double-fried for maximum crunch and heat. Sold by the pound.</p></article><article class="card"><h3>Aloo Paratha</h3><p class="price">$8.00</p><p>Freshly griddled whole wheat flatbread stuffed with seasoned mashed potatoes, fresh cilantro, and spices.</p></article><article class="card"><h3>Gobi Paratha</h3><p class="price">$8.00</p><p>Fresh griddled flatbread generously stuffed with spiced grated cauliflower and traditional herbs.</p></article><article class="card"><h3>Paneer Paratha</h3><p class="price">$8.00</p><p>Handcrafted flatbread filled with seasoned grated paneer, fresh herbs, and warm Indian spices.</p></article>"""

# 1. Update content/menu/index.html
index_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'menu', 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Replace the grid inside section id="street-food"
pattern_index = r'(<section id="street-food">.*?<div class="grid">).*?(</div><p class="secondary">)'
updated_index = re.sub(pattern_index, r'\g<1>' + new_street_food_cards + r'\g<2>', index_content, flags=re.DOTALL)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(updated_index)
print("Updated local content/menu/index.html")

# 2. Update content/menu/street-food-snacks.html
street_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'menu', 'street-food-snacks.html')
with open(street_path, 'r', encoding='utf-8') as f:
    street_content = f.read()

pattern_street = r'(<h2>Street Food &amp; Snack Menu</h2><div class="grid">).*?(</div><p>For chaat)'
updated_street = re.sub(pattern_street, r'\g<1>' + new_street_food_cards + r'\g<2>', street_content, flags=re.DOTALL)
# Update FAQ to remove Khaman Dhokla reference
updated_street = updated_street.replace('Paneer Pakoda, Cut Mirchy Pakoda and Khaman Dhokla are listed by the pound.', 'Paneer Pakoda and Cut Mirchy Pakoda are listed by the pound.')

with open(street_path, 'w', encoding='utf-8') as f:
    f.write(updated_street)
print("Updated local content/menu/street-food-snacks.html")

# 3. Deploy to BigCommerce API for Page 10 (/menu/)
url_p10 = f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/10'
payload_p10 = json.dumps({"body": updated_index}).encode('utf-8')
req_p10 = urllib.request.Request(url_p10, data=payload_p10, headers={
    'X-Auth-Token': token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}, method='PUT')

with urllib.request.urlopen(req_p10) as res:
    resp_p10 = json.loads(res.read().decode('utf-8'))
    print(f"API Success for Page 10 ({resp_p10.get('name')})! Status: {res.status}")

# 4. Deploy to BigCommerce API for Page 12 (/menu/street-food-snacks/)
url_p12 = f'https://api.bigcommerce.com/stores/{store_hash}/v2/pages/12'
payload_p12 = json.dumps({"body": updated_street}).encode('utf-8')
req_p12 = urllib.request.Request(url_p12, data=payload_p12, headers={
    'X-Auth-Token': token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}, method='PUT')

with urllib.request.urlopen(req_p12) as res:
    resp_p12 = json.loads(res.read().decode('utf-8'))
    print(f"API Success for Page 12 ({resp_p12.get('name')})! Status: {res.status}")
