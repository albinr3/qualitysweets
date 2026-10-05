import os
import json
import re
import time
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get('BIGCOMMERCE_STORE_HASH')
token = os.environ.get('BIGCOMMERCE_ACCESS_TOKEN')

headers = {
    "X-Auth-Token": token,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def api_request(url, data=None, method="GET"):
    req_data = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8')
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        print(f"HTTPError {e.code} for {method} {url}: {err_msg}")
        return {"error": e.code, "message": err_msg}
    except Exception as e:
        print(f"Error for {method} {url}: {e}")
        return {"error": str(e)}

# PRODUCT IMAGES MAPPING: (product_id, image_id) -> alt_text
ALT_MAPPING = {
    # Product 76: Matka Kaju
    (76, 270): "Handcrafted Matka Kaju cashew fudge sweet in decorative mini pot - Quality Sweets Iselin NJ",
    # Product 77: Kaju Katli
    (77, 308): "Authentic diamond cut Kaju Katli cashew fudge with edible silver foil - Quality Sweets",
    # Product 78: Manpasand
    (78, 267): "Manpasand layered cashew and pistachio mithai diamond sweet - Quality Sweets",
    # Product 79: Kaju Roll
    (79, 271): "Handcrafted Kaju Roll cashew sweet filled with crushed pistachios - Quality Sweets",
    # Product 80: Anarkali
    (80, 272): "Artisan Anarkali cashew sweet crafted with saffron and nuts - Quality Sweets",
    # Product 81: Kahmiri Peeta
    (81, 273): "Kashmiri Peeta traditional soft sweet flavored with cardamon - Quality Sweets",
    # Product 82: Mango Sandesh
    (82, 275): "Fresh Bengali Mango Sandesh made from fresh chenna and real mango pulp - Quality Sweets",
    # Product 83: Palki
    (83, 276): "Palki handcrafted royal decorative mithai for celebrations - Quality Sweets",
    # Product 84: Malai Chum Chum
    (84, 351): "Tender Bengali Malai Chum Chum soaked in aromatic saffron syrup - Quality Sweets",
    # Product 85: Pista Sandesh
    (85, 277): "Fresh Bengali Pista Sandesh garnished with crushed pistachios - Quality Sweets",
    # Product 86: Malai Peda
    (86, 331): "Traditional Malai Peda soft milk sweet garnished with pistachios - Quality Sweets",
    # Product 87: Pineapple Chum Chum
    (87, 280): "Pineapple Chum Chum infused with natural pineapple flavor - Quality Sweets",
    # Product 88: Rose Chum Chum
    (88, 281): "Rose Chum Chum delicately flavored with fragrant rose water - Quality Sweets",
    # Product 89: Pista Pan
    (89, 283): "Pista Pan handcrafted betel leaf shaped pistachio and cashew sweet - Quality Sweets",
    # Product 90: Jalebi
    (90, 284): "Crisp spiral Jalebi fried fresh daily and soaked in saffron syrup - Quality Sweets",
    # Product 91: Red Chili Kaju
    (91, 286): "Roasted crunchy cashews tossed in savory red chili spice blend - Quality Sweets",
    # Product 92: Moong Dal Halwa
    (92, 287): "Rich Moong Dal Halwa slow cooked with pure desi ghee and nuts - Quality Sweets",
    # Product 93: Carrot Halwa
    (93, 288): "Traditional Gajar Ka Halwa carrot pudding slow cooked with milk and ghee - Quality Sweets",
    # Product 94: Imarti
    (94, 289): "Golden flower shaped Imarti sweet made from urad dal and saffron syrup - Quality Sweets",
    # Product 95: Maysore Pak
    (95, 290): "Authentic Mysore Pak melt in mouth gram flour and ghee confection - Quality Sweets",
    # Product 96: Patisa
    (96, 291): "Flaky layered Patisa soan papdi flavored with cardamom and almonds - Quality Sweets",
    # Product 97: Balushahi
    (97, 293): "Flaky traditional Balushahi glazed in sugar syrup - Quality Sweets",
    # Product 98: Besan Ladoo
    (98, 294): "Pure Besan Ladoo roasted gram flour rounds with ghee and cardamom - Quality Sweets",
    # Product 99: Chocolate Burfee
    (99, 295): "Double layer Chocolate Burfi rich cocoa and condensed milk fudge - Quality Sweets",
    # Product 100: Gajar Burfi
    (100, 297): "Fresh Gajar Burfi spiced carrot and milk fudge with dry fruits - Quality Sweets",
    # Product 101: Kala Jamun
    (101, 296): "Deep caramel Kala Jamun soft dark cottage cheese dumplings in syrup - Quality Sweets",
    # Product 102: White Peda
    (102, 298): "Traditional White Peda cardamom infused condensed milk confection - Quality Sweets",
    # Product 103: Black Pepper Cashew
    (103, 300): "Whole roasted crunchy cashews coated with cracked black pepper - Quality Sweets",
    # Product 104: Motichur Ladoo
    (104, 299): "Traditional Motichur Ladoo soft golden chickpea pearls with cardamom - Quality Sweets",
    # Product 105: Milk Cake
    (105, 301): "Traditional slow cooked caramelized Milk Cake fudge with roasted grains - Quality Sweets",
    # Product 106: Small Mathi
    (106, 302): "Crispy savory Small Mathi traditional Punjabi flaky crackers - Quality Sweets",
    # Product 107: Seerni
    (107, 393): "Traditional crisp Seerni sugar coated celebratory sweet snack - Quality Sweets",
    # Product 108: Coconut Jamun
    (108, 303): "Soft Gulab Jamun rolled in toasted shredded coconut flakes - Quality Sweets",
    # Product 109: Tranga Burfi
    (109, 304): "Tri color Tiranga Burfi saffron white and pistachio layered sweet - Quality Sweets",
    # Product 110: Besan Burfi
    (110, 305): "Golden Besan Burfi roasted chickpea flour fudge topped with sliced nuts - Quality Sweets",
    # Product 111: Matri (Namak Para)
    (111, 306): "Crisp diamond cut Matri Namak Para savory carom seed snack - Quality Sweets",
    # Product 112: Plain Burfi
    (112, 307): "Classic Plain Khoya Burfi velvety condensed milk fudge squares - Quality Sweets",
    # Product 113: Khoya Pista Burfi
    (113, 309): "Rich Khoya Pista Burfi milk fudge topped with green pistachios - Quality Sweets",
    # Product 114: Malai Jamun
    (114, 310): "Tender Malai Jamun stuffed with sweet rich clotted cream - Quality Sweets",
    # Product 115: Sakar Para
    (115, 311): "Crispy diamond cut Sakar Para traditional sweet wheat crackers - Quality Sweets",
    # Product 116: Gud Para
    (116, 312): "Crisp Punjabi Gud Para sweet crackers glazed with pure natural jaggery - Quality Sweets",
    # Product 117: Malai Sandwich
    (117, 313): "Bengali Malai Sandwich soft chenna sweet filled with sweetened cream - Quality Sweets",
    # Product 118: Cream Roll
    (118, 314): "Crispy baked puff pastry Cream Roll filled with sweet vanilla frosting - Quality Sweets",
    # Product 119: Modak
    (119, 315): "Traditional sweet Modak dumpling for festive offerings and prasad - Quality Sweets",
    # Product 120: Channa Mango Malai
    (120, 316): "Fresh Chenna Mango Malai soft cottage cheese in rich mango sauce - Quality Sweets",
    # Product 121: Chenna Murgi
    (121, 349): "Chenna Murki bite sized candied cottage cheese cubes - Quality Sweets",
    # Product 122: Sweet Mathi
    (122, 320): "Traditional round Sweet Mathi crispy festive sweet crackers - Quality Sweets",
    # Product 123: Big Salted Mathi
    (123, 318): "Traditional large Salted Mathi crispy savory spiced snack - Quality Sweets",
    # Product 124: Unsalted Mathi
    (124, 319): "Traditional flaky Unsalted Mathi Punjabi crispy tea time cracker - Quality Sweets",
    # Product 125: Kesar Chum Chum
    (125, 321): "Saffron infused Kesar Chum Chum soft Bengali sweet in light syrup - Quality Sweets",
    # Product 126: Rasgulla (Large)
    (126, 322): "Fresh spongy Bengali Rasgulla dumplings soaked in light sugar syrup - Quality Sweets",
    # Product 127: Gulab Jamoon (Large)
    (127, 323): "Warm golden brown Gulab Jamun dumplings soaked in rose cardamom syrup - Quality Sweets",
    # Product 128: Angoori Gulab Jamun
    (128, 324): "Bite sized Angoori Gulab Jamun mini cottage cheese dumplings in syrup - Quality Sweets",
    # Product 129: Rose Angoori Rasgulla
    (129, 325): "Miniature Rose Angoori Rasgulla soft spongy pearls in rose syrup - Quality Sweets",
    # Product 130: Angoori Rasgulla
    (130, 326): "Delicate Angoori Rasgulla bite sized cottage cheese pearls in syrup - Quality Sweets",
    # Product 131: Bengali Kalakand
    (131, 327): "Fresh Bengali Kalakand soft granular milk fudge with cardamom - Quality Sweets",
    # Product 132: Khoya Kalakand
    (132, 328): "Rich Khoya Kalakand artisan slow cooked caramelized milk sweet - Quality Sweets",
    # Product 133: Cherry Chum Chum
    (133, 350): "Bright Cherry Chum Chum traditional Bengali chenna sweet with cherries - Quality Sweets",
    # Product 134: Badana
    (134, 329): "Golden sweet Badana crisp fried chickpea droplets soaked in syrup - Quality Sweets",
    # Product 135: Kadam Keer
    (135, 332): "Traditional Bengali Kadam Keer rasgulla coated in granular khoya - Quality Sweets",
    # Product 137: Petha
    (137, 330): "Authentic Agra style Petha translucent candied ash gourd sweet - Quality Sweets",
    # Product 138: Assorted Sweets Basket
    (138, 333): "Festive Assorted Sweets Basket featuring premium handcrafted mithai - Quality Sweets",
    # Product 139: Bengali Sweet Box
    (139, 334): "Assorted Bengali Sweet Box with fresh rasgulla, chum chum, and sandesh - Quality Sweets",
    # Product 140: Assorted Sweets Box
    (140, 335): "One pound Assorted Sweets Box with assorted burfi, ladoos, and peda - Quality Sweets",
    # Product 141: Gold Ganesh Box (Small)
    (141, 340): "Decorative Small Gold Ganesh Gift Box filled with artisan Indian sweets - Quality Sweets",
    # Product 142: Golden Ganesh Box (Large)
    (142, 339): "Luxury Large Golden Ganesh Gift Box for weddings and Diwali gifts - Quality Sweets",
    # Product 143: Assorted Dry Snack Box
    (143, 338): "Assorted Savory Snack Box with crispy mathi, namak para, and sev - Quality Sweets",
    # Product 144: Restaurant Chaat Menu
    (144, 341): "Quality Sweets Iselin store takeout menu featuring chaat and hot snacks",
    # Product 145: Thick Sev
    (145, 343): "Crunchy spiced Thick Sev crispy chickpea flour snack noodles - Quality Sweets",
    # Product 146: Snack Mix
    (146, 344): "Signature savory Indian Snack Mix with spiced lentils, sev, and nuts - Quality Sweets",
    # Product 147: Fine Sev
    (147, 345): "Crispy golden Fine Sev thin chickpea flour noodles for chaat and snacks - Quality Sweets",
    # Product 148: Bengali Red and Gold Gift Box
    (148, 346): "Ornate Red and Gold Gift Box filled with fresh Bengali sweets - Quality Sweets",
    # Product 149: Small Red and Gold Gift Box
    (149, 347): "Festive Small Red and Gold Sweet Box perfect for return gifts and favors - Quality Sweets",
    # Product 150: Kesar Peda
    (150, 348): "Aromatic Kesar Peda saffron infused condensed milk sweet with pistachios - Quality Sweets",
    # Product 151: Purple Gift Box
    (151, 352): "Elegant Purple Holiday Gift Box for assorted mithai and festive gifts - Quality Sweets",
    # Product 152: Orange Gift Box
    (152, 353): "Vibrant Orange Celebration Gift Box filled with fresh Indian sweets - Quality Sweets",
    # Product 153: Gift Wrapped Sweets Basket
    (153, 354): "Custom Gift Wrapped Sweets Basket decorated with festive ribbon - Quality Sweets",
    # Product 154: Mix Burfee Golden Gift Box (Img 355 & 359)
    (154, 355): "Mix Burfi Golden Gift Box featuring assorted cashew, pistachio and plain burfi",
    (154, 359): "Deluxe golden gift box filled with handcrafted assorted burfi varieties",
    # Product 155: Sweets Basket Assortment
    (155, 356): "Deluxe holiday Sweets Basket Assortment for family celebrations and gifts - Quality Sweets",
    # Product 156: Sweets Basket
    (156, 357): "Round Sweets Basket decorated with handcrafted artisan Indian mithai - Quality Sweets",
    # Product 157: Dry Snack Assortment
    (157, 358): "Party Tray Dry Snack Assortment with roasted nuts and savory namkeen - Quality Sweets",
    # Product 158: Special Assorted Sweets Box
    (158, 361): "Special Red Assorted Sweets Box for Diwali, weddings, and celebrations - Quality Sweets",
    # Product 159: Red Snack Gift Box
    (159, 363): "Festive Red Snack Gift Box with savory Indian mathi and spiced namkeen - Quality Sweets",
    # Product 160: Red Pepper Cashew Gift Box
    (160, 364): "Premium Gift Box of spiced Red Pepper Cashews roasted fresh - Quality Sweets",
    # Product 161: Karva Chauth Box
    (161, 365): "Special Karva Chauth Sweets Box with traditional feni, mathi, and sweets - Quality Sweets",
    # Product 162: Mixed Sweets Box
    (162, 366): "Fresh 1 Lb Mixed Sweets Box with assorted traditional Indian mithai - Quality Sweets",
    # Product 163: Til bhuga
    (163, 367): "Traditional Til Bhuga winter sweet made with sesame seeds and khoya - Quality Sweets",
    # Product 164: Till Chikki
    (164, 368): "Crispy Til Chikki crunchy sesame seed and jaggery brittle - Quality Sweets",
    # Product 165: Rewdi
    (165, 369): "Traditional crunchy Rewri crisp sesame and jaggery candy bites - Quality Sweets",
    # Product 166: Gujia
    (166, 372): "Golden fried festive Gujia pastry stuffed with sweet khoya and dry fruits - Quality Sweets",
    # Product 167: Holiday Season Peacock Gift Box (1.5 lbs) (Img 373, 374, 375)
    (167, 373): "Peacock Holiday Season Gift Box 1.5 lbs filled with assorted fresh mithai",
    (167, 374): "Top view of ornate Peacock festive sweet box packaging - Quality Sweets",
    (167, 375): "Side angle of Peacock gift box showcasing luxury Indian sweet assortment",
    # Product 168: 5 LB Assorted Gift Basket
    (168, 382): "Grand 5 Lb Assorted Sweets Gift Basket for weddings, corporate gifts, and Diwali",
    # Product 169: 10 Lb Assorted Sweets Gift Basket
    (169, 383): "Luxury 10 Lb Assorted Sweets Gift Basket loaded with handcrafted mithai - Quality Sweets",
    # Product 170: Bengali Ladoo Basket - Diwali Special
    (170, 380): "Diwali Special Bengali and Ladoo Gift Basket decorated for festive gifting",
    # Product 171: Blue & Gold Holiday Gift Box (Img 386 & 387)
    (171, 386): "Blue and Gold Holiday Gift Box featuring assorted handcrafted Indian sweets",
    (171, 387): "Interior view of Blue and Gold celebration box filled with fresh burfi and peda",
    # Product 172: Holiday Gift Box
    (172, 388): "Luxury Holiday Gift Box designed for corporate gifting and festive gatherings",
    # Product 173: Holiday Collection Box
    (173, 389): "Festive Holiday Collection Box containing assorted artisan Indian mithai varieties",
    # Product 174: Makki Ki Roti and Saag Special
    (174, 390): "Traditional Punjabi Sarson Ka Saag and Makki Ki Roti winter meal special",
    # Product 175: The flaxseed pinni (Img 391 & 392)
    (175, 391): "Wholesome Flaxseed Pinni Alsi Ladoo nutritious winter sweet made with pure ghee",
    (175, 392): "Traditional Punjabi Alsi Pinni flaxseed laddu with nuts and jaggery",
    # Product 176: __Store Assets__ (Used across storefront)
    (176, 394): "Order Sweets Online nationwide shipping from Quality Sweets",
    (176, 395): "Takeout and pickup menu order to-go at Quality Sweets Iselin NJ",
    (176, 396): "Indian wedding catering and bulk mithai orders across NJ NY and CT",
    (176, 397): "Fresh Samosa Chaat with chickpeas yogurt mint and tamarind chutneys",
    (176, 398): "Crisp Samosa Chaat plated with spiced chole yogurt and fresh sev",
    (176, 399): "Crispy Pani Puri shells with spiced potato filling and tangy mint water",
    (176, 400): "Hot fluffy Chole Bhatura served with spicy chickpea curry and pickle",
    (176, 401): "Freshly griddled Stuffed Aloo and Gobi Parathas served with butter",
    (176, 402): "Decorative Indian wedding sweet box and return gift favor packaging",
    (176, 403): "Bulk fresh Indian mithai boxes prepared for temple prasad and puja",
    (176, 404): "Commercial party platter of freshly fried crisp vegetarian samosas",
    (176, 405): "Quality Sweets storefront welcome banner - Handcrafted Indian sweets daily",
    (176, 406): "Assorted sweets gift baskets banner for weddings, festivals, and celebrations",
    (176, 407): "Special bulk pricing on Indian sweets and catering orders banner",
    (176, 408): "Quality Sweets high resolution storefront welcome hero banner",
    (176, 409): "Samosa Chaat takeout menu hero image - Fresh street food in Iselin NJ",
    (176, 410): "Quality Sweets storefront exterior at 1384 Oak Tree Road Iselin New Jersey",
    (176, 411): "Fresh Indian sweets display glass counter inside Quality Sweets store",
    (176, 412): "Bengali sweets selection card with Rasgulla, Chum Chum, and Sandesh",
    (176, 413): "Barfi and Kaju Katli assortment category showcase card",
    (176, 414): "Traditional Indian mithai category card with Ladoos, Jalebi, and Pedas",
    (176, 415): "Commercial catering trays of freshly fried samosas ready for event delivery",
    (176, 416): "Crisp golden jalebi catering trays prepared for wedding dessert tables",
    (176, 417): "Bulk fresh Gud Para coated in pure jaggery for catering orders",
    (176, 418): "Handcrafted Kaju Rolls prepared fresh in Quality Sweets kitchen"
}

print(f"Total mapped image alts: {len(ALT_MAPPING)}")

def optimize_all_product_images():
    print("\n--- OPTIMIZING CATALOG PRODUCT IMAGES ---")
    success_count = 0
    fail_count = 0
    results = []

    for (p_id, img_id), alt_text in ALT_MAPPING.items():
        url = f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products/{p_id}/images/{img_id}"
        payload = {"description": alt_text}
        res = api_request(url, data=payload, method="PUT")
        if res.get("data") and res["data"].get("description") == alt_text:
            success_count += 1
            print(f"[OK] Product {p_id} Image {img_id} -> '{alt_text}'")
            results.append({"product_id": p_id, "image_id": img_id, "alt": alt_text, "status": "SUCCESS"})
        else:
            fail_count += 1
            print(f"[FAIL] Product {p_id} Image {img_id} -> {res}")
            results.append({"product_id": p_id, "image_id": img_id, "alt": alt_text, "status": "FAILED", "error": res})
        time.sleep(0.1) # Be gentle with API rate limits

    print(f"\nProduct images optimization summary: {success_count} succeeded, {fail_count} failed out of {len(ALT_MAPPING)}")
    return results

def optimize_storefront_pages():
    print("\n--- OPTIMIZING STOREFRONT PAGES ---")
    # Page 2: Shipping & Refunds
    p2 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/2")
    if p2 and "body" in p2:
        body2 = p2["body"]
        # Replace ups-map alt
        body2 = body2.replace('alt="ups-map.gif"', 'alt="UPS Ground delivery transit times map across the United States from Iselin New Jersey"')
        body2 = body2.replace('title="ups-map.gif"', 'title="UPS Ground Delivery Map - Quality Sweets"')
        # Replace shipping-banner alt
        body2 = body2.replace('alt="shipping-banner.png"', 'alt="Quality Sweets nationwide fresh shipping and insulated cold packaging policy"')
        body2 = body2.replace('title="shipping-banner.png"', 'title="Fresh Nationwide Shipping Guarantee - Quality Sweets"')
        res2 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/2", data={"body": body2}, method="PUT")
        print("Page 2 (Shipping & Refunds) updated:", "id" in res2)

    # Page 5: Security And Privacy
    p5 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/5")
    if p5 and "body" in p5:
        body5 = p5["body"]
        body5 = body5.replace('alt="secure payment"', 'alt="Secure encrypted online payment processing with PayPal and credit cards"')
        body5 = body5.replace('alt="" width="300"', 'alt="PayPal verified secure payment gateway guarantee" width="300"')
        body5 = body5.replace('alt="contact-us3.png"', 'alt="Quality Sweets customer support and order assistance contact desk"')
        body5 = body5.replace('title="contact-us3.png"', 'title="Quality Sweets Customer Support"')
        res5 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/5", data={"body": body5}, method="PUT")
        print("Page 5 (Security And Privacy) updated:", "id" in res5)

    # Page 7: Packaging Information
    p7 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/7")
    if p7 and "body" in p7:
        body7 = p7["body"]
        body7 = body7.replace('alt="screen-shot-2015-09-22-at-12.00.02-pm.png"', 'alt="Custom insulated corrugated shipping box with thermal protection for fresh Indian sweets delivery"')
        body7 = body7.replace('title="screen-shot-2015-09-22-at-12.00.02-pm.png"', 'title="Insulated Shipping Box Packaging - Quality Sweets"')
        body7 = body7.replace('alt="dry-ice-1.jpg"', 'alt="Food grade dry ice and cold gel insulation packs preserving mithai freshness during transit"')
        body7 = body7.replace('title="dry-ice-1.jpg"', 'title="Dry Ice and Cold Gel Packs - Quality Sweets"')
        res7 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/7", data={"body": body7}, method="PUT")
        print("Page 7 (Packaging Information) updated:", "id" in res7)

def optimize_banners():
    print("\n--- OPTIMIZING BANNERS ---")
    b8 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/8")
    if b8 and "content" in b8:
        content8 = b8["content"]
        content8 = content8.replace('alt="mid-website-banners.png"', 'alt="Quality Sweets handcrafted Indian sweets, snacks, and celebratory gift boxes in Iselin NJ"')
        content8 = content8.replace('title="mid-website-banners.png"', 'title="Quality Sweets Handcrafted Indian Sweets and Snacks"')
        res8 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/8", data={"content": content8}, method="PUT")
        print("Banner 8 updated:", "id" in res8)

def optimize_categories():
    print("\n--- OPTIMIZING CATEGORIES ---")
    # Category 15: Takeout Menu (/chaats-archived/)
    c15 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/15")
    if c15 and c15.get("data"):
        desc15 = c15["data"].get("description", "")
        desc15 = desc15.replace('alt="quality-sweets-menu.jpg"', 'alt="Quality Sweets Iselin store takeout menu featuring chaat, samosas, and Indian snacks"')
        desc15 = desc15.replace('title="quality-sweets-menu.jpg"', 'title="Quality Sweets Takeout Menu"')
        res15 = api_request(f"https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/categories/15", data={"description": desc15}, method="PUT")
        print("Category 15 updated:", "data" in res15)

if __name__ == "__main__":
    results = optimize_all_product_images()
    optimize_storefront_pages()
    optimize_banners()
    optimize_categories()

    with open("scratch/optimization_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\n[FINISHED] All optimizations executed and recorded in scratch/optimization_results.json")
