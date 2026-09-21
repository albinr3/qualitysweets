import urllib.request
from PIL import Image
import io

urls = [
    'https://cdn10.bigcommerce.com/s-2ygwtj/product_images/theme_images/gift_basket2023-01.png?t=1774230828',
    'https://cdn10.bigcommerce.com/s-2ygwtj/product_images/theme_images/QS_banner_2025-01.png?t=1774230828',
    'https://cdn10.bigcommerce.com/s-2ygwtj/product_images/theme_images/bulk_orders-01.png?t=1774230828'
]
for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        im = Image.open(io.BytesIO(resp.read()))
        name = u.split('/')[-1].split('?')[0]
        print(f"{name}: {im.size}")
