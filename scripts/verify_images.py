import urllib.request
import json

with open('scripts/uploaded_images.json') as f:
    images = json.load(f)

additional_urls = {
    "malai_chum_chum": "https://cdn10.bigcommerce.com/s-2ygwtj/products/84/images/351/MALAICHUM_CHUM__26837.1437440527.350.350.jpg?c=2",
    "milk_cake": "https://cdn10.bigcommerce.com/s-2ygwtj/products/105/images/301/Milk_Cake__92535.1433802617.350.350.jpg?c=2",
    "mango_sandesh": "https://cdn10.bigcommerce.com/s-2ygwtj/products/82/images/275/Mango_Sandesh__78298.1433712997.350.350.jpg?c=2",
    "besan_ladoo": "https://cdn10.bigcommerce.com/s-2ygwtj/products/98/images/294/Besan_Ladoo__03878.1433732821.350.350.jpg?c=2",
    "gujia": "https://cdn10.bigcommerce.com/s-2ygwtj/products/166/images/372/gujia__29512.1456187335.215.215.png?c=2",
    "jalebi": "https://cdn10.bigcommerce.com/s-2ygwtj/products/90/images/284/Jalebi__80913.1433725846.215.215.jpg?c=2",
    "carrot_halwa": "https://cdn10.bigcommerce.com/s-2ygwtj/products/93/images/288/Carrot_halwa__62877.1433729162.215.215.jpg?c=2",
    "red_chili_kaju": "https://cdn10.bigcommerce.com/s-2ygwtj/products/91/images/286/Red_Chilli_Cashews__50206.1433727938.215.215.jpg?c=2",
    "kaju_katli": "https://cdn10.bigcommerce.com/s-2ygwtj/products/77/images/308/Plain_Burfi__57958.1433826518.215.215.jpg?c=2",
    "motichur_ladoo": "https://cdn10.bigcommerce.com/s-2ygwtj/products/104/images/299/Motichur_Ladoo__31599.1433801521.215.215.jpg?c=2",
    "khoya_pista_burfi": "https://cdn10.bigcommerce.com/s-2ygwtj/products/113/images/309/Khoya_Pista_Burfi__02324.1433826917.215.215.jpg?c=2",
    "bottom_banner_long": "https://cdn10.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/bottom-banner-long-01.png",
    "disclaimer_ribbon": "https://cdn10.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/disclaimer1-01.png",
    "carousel_slide_1": "https://cdn10.bigcommerce.com/s-2ygwtj/product_images/theme_images/gift_basket2023-01.png?t=1774230828",
    "carousel_slide_2": "https://cdn10.bigcommerce.com/s-2ygwtj/product_images/theme_images/QS_banner_2025-01.png?t=1774230828",
    "carousel_slide_3": "https://cdn10.bigcommerce.com/s-2ygwtj/product_images/theme_images/bulk_orders-01.png?t=1774230828"
}
images.update(additional_urls)

print("Verifying all staging images:")
for name, url in images.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            print(f"OK [200]: {name} -> {resp.headers.get('content-type')}")
    except Exception as e:
        print(f"FAIL: {name} -> {e}")
