import os
import urllib.request
import json
from dotenv import load_dotenv

load_dotenv()

store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

hero_html = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style id="qs-global-2-fonts-system">
  /* ===================================================
     QUALITY SWEETS - REGLA MAESTRA DE 2 FUENTES
     1. Display & Encabezados: 'Marcellus', Georgia, serif
     2. Lectura, Menús & UI:   'Plus Jakarta Sans', sans-serif
     =================================================== */

  /* 1. Textos Generales, Párrafos, Navegación y Menús */
  body, p, li, td, th, input, select, textarea, .breadcrumb,
  #SideCategoryList, .footer, .BlockContent, .ProductDescription,
  #menu, #menu ul, #menu li a, .navPages, .category-list a, .CategoryList, .TopMenu {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  }

  /* 2. Menú de Navegación: Mayor nitidez y peso visual */
  #menu li a {
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
  }

  /* 3. Encabezados de Toda la Página & Nombres de Productos */
  h1, h2, h3, h4, h5, h6,
  .Title, .ProductDetails strong, .ProductDetails strong a,
  .Block h2, .Block h3, .ProductList strong, .ProductList strong a,
  .product-title, .page-heading, .section-title, .qs-title,
  #ProductDetails .ProductDetails h1 {
    font-family: 'Marcellus', Georgia, 'Times New Roman', serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.3px !important;
  }

  /* 4. Títulos de Productos en Catálogo */
  .ProductList .ProductDetails strong a {
    font-size: 16px !important;
    color: #4a0e17 !important;
    line-height: 1.35 !important;
  }
  .ProductList .ProductDetails strong a:hover {
    color: #881628 !important;
  }

  /* 5. Precios y Botones de Compra */
  .ProductPrice, .PriceRating, .price, em.ProductPrice, .RetailPrice,
  .btn, .Button, .btn-primary, input[type="submit"], input[type="button"], a.btn,
  .btn-secondary, .ChooseOptions {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
  }
</style>

<div id="qs-hero-wrapper" style="margin: 0 0 30px 0; padding: 0;">
  
  <!-- BLOQUE 1: HERO PRINCIPAL DE SERVICIOS & TRIAJE -->
  <div style="background: radial-gradient(circle at 50% 15%, #881628 0%, #540c17 60%, #35050d 100%); color: #ffffff; border-radius: 14px; padding: 36px 24px 28px 24px; text-align: center; box-shadow: 0 10px 30px rgba(53, 5, 13, 0.35); border: 2px solid #d4af37;">
    
    <!-- BADGE SUPERIOR CON SVG HOJA -->
    <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; background: rgba(212, 175, 55, 0.15); border: 1px solid #d4af37; color: #ffd700; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; padding: 6px 18px; border-radius: 50px; margin-bottom: 18px;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
      <span>100% Pure Vegetarian &bull; Zero Chemical Preservatives &bull; Made Fresh Daily</span>
    </div>

    <!-- H1 PRINCIPAL DE LA HOME (FUENTE MARCELLUS - ARTESANAL & ELEGANTE) -->
    <h1 style="font-family: 'Marcellus', 'Oswald', Georgia, serif; color: #ffffff; font-size: 34px; font-weight: 400; line-height: 1.3; margin: 0 0 14px 0; letter-spacing: 0.5px; text-shadow: 0 2px 10px rgba(0,0,0,0.6);">
      Authentic Indian Sweet Shop &mdash; Handcrafted Mithai &amp; Hot Snacks Daily
    </h1>

    <!-- SUBTITULO -->
    <p style="font-family: 'Plus Jakarta Sans', sans-serif; color: #fce8cc; font-size: 15.5px; font-weight: 500; max-width: 820px; margin: 0 auto 26px auto; line-height: 1.6; letter-spacing: 0.15px;">
      Serving the Tri-State from Oak Tree Road in Iselin, NJ since 2003. Pick up hot samosas and chaats to-go, or enjoy fresh artisan sweets shipped nationwide in insulated cold packs.
    </p>

    <!-- TRIAJE DE LOS 3 BOTONES DE SERVICIO CON FONDO BLANCO, FOTO CENTRADA & TIPOGRAFIA MARCELLUS -->
    <style>
      .qs-btn-white-card {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 14px !important;
        background: #ffffff !important;
        padding: 12px 16px !important;
        border-radius: 10px !important;
        text-decoration: none !important;
        border: 2px solid #ebdcc5 !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.25) !important;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
        box-sizing: border-box !important;
        min-height: 76px !important;
      }
      .qs-btn-white-card:hover {
        transform: translateY(-3px) scale(1.015) !important;
        border-color: #d4af37 !important;
        box-shadow: 0 8px 22px rgba(212, 175, 55, 0.35), 0 4px 12px rgba(0,0,0,0.25) !important;
      }
    </style>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; max-width: 980px; margin: 0 auto 24px auto;">
      
      <!-- BOTON 1: ENVIOS ECOMMERCE -->
      <a href="/indian-sweets/" class="qs-btn-white-card" style="display: flex; align-items: center; justify-content: flex-start; gap: 14px; background: #ffffff; padding: 12px 16px; border-radius: 10px; text-decoration: none; border: 2px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.25); box-sizing: border-box; min-height: 76px;">
        <div style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; flex-shrink: 0; align-self: center;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/394/btn_sweets_bg__81005.1789094378.350.350.jpg?c=2" alt="Order Sweets Online" style="display: block; width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37; box-shadow: 0 2px 6px rgba(0,0,0,0.15);" />
        </div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; align-self: center; text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25; letter-spacing: 0.2px;">Order Sweets Online</div>
          <div style="font-family: 'Plus Jakarta Sans', sans-serif; color: #555555; font-size: 12px; font-weight: 600; margin-top: 3px;">(USA Shipping)</div>
        </div>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; align-self: center;"><polyline points="9 18 15 12 9 6"/></svg>
      </a>

      <!-- BOTON 2: TAKEOUT LOCAL ISELIN -->
      <a href="/menu/" class="qs-btn-white-card" style="display: flex; align-items: center; justify-content: flex-start; gap: 14px; background: #ffffff; padding: 12px 16px; border-radius: 10px; text-decoration: none; border: 2px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.25); box-sizing: border-box; min-height: 76px;">
        <div style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; flex-shrink: 0; align-self: center;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/395/btn_takeout_bg__18527.1789094396.350.350.jpg?c=2" alt="Takeout & Pickup Menu" style="display: block; width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37; box-shadow: 0 2px 6px rgba(0,0,0,0.15);" />
        </div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; align-self: center; text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25; letter-spacing: 0.2px;">Takeout &amp; Pickup Menu</div>
          <div style="font-family: 'Plus Jakarta Sans', sans-serif; color: #555555; font-size: 12px; font-weight: 600; margin-top: 3px;">(Iselin Store)</div>
        </div>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; align-self: center;"><polyline points="9 18 15 12 9 6"/></svg>
      </a>

      <!-- BOTON 3: CATERING B2B -->
      <a href="/catering/" class="qs-btn-white-card" style="display: flex; align-items: center; justify-content: flex-start; gap: 14px; background: #ffffff; padding: 12px 16px; border-radius: 10px; text-decoration: none; border: 2px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.25); box-sizing: border-box; min-height: 76px;">
        <div style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; flex-shrink: 0; align-self: center;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/396/btn_catering_bg__82126.1789094396.350.350.jpg?c=2" alt="Wedding & Catering" style="display: block; width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37; box-shadow: 0 2px 6px rgba(0,0,0,0.15);" />
        </div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; align-self: center; text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25; letter-spacing: 0.2px;">Wedding &amp; Catering</div>
          <div style="font-family: 'Plus Jakarta Sans', sans-serif; color: #555555; font-size: 12px; font-weight: 600; margin-top: 3px;">(Tri-State)</div>
        </div>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; align-self: center;"><polyline points="9 18 15 12 9 6"/></svg>
      </a>

    </div>

    <!-- CONTACTO DIRECTO & HORARIOS CON BADGES ELEGANTE -->
    <div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 12px; border-top: 1px solid rgba(212, 175, 55, 0.3); padding-top: 18px; margin-top: 6px;">
      
      <div style="background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 6px; padding: 7px 14px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-weight: 600; color: #ffd700; display: inline-flex; align-items: center; gap: 7px;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>1384 Oak Tree Rd, Iselin NJ &bull; Open Daily 10am&ndash;8pm</span>
      </div>

      <div style="background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 6px; padding: 7px 14px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; font-weight: 600; color: #ffffff; display: inline-flex; align-items: center; gap: 7px;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        <span>Store: <a href="tel:7322833799" style="color: #ffd700; text-decoration: underline; font-weight: 700; margin-left: 2px;">(732) 283-3799</a></span>
      </div>

    </div>
  </div>

  <!-- TRUST BAR / E-E-A-T CON ICONOS SVGS -->
  <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px 20px; margin-top: 16px; display: flex; flex-wrap: wrap; justify-content: space-around; align-items: center; text-align: center; gap: 14px; font-family: 'Plus Jakarta Sans', sans-serif;">
    <div style="color: #4a0e17; font-size: 13.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 7px;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="#d4af37"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      <span>Featured on News 12 NJ &amp; Bon Appétit</span>
    </div>
    <div style="color: #4a0e17; font-size: 13.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 7px;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>
      <span>20+ Years Serving Oak Tree Road</span>
    </div>
    <div style="color: #4a0e17; font-size: 13.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 7px;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#2b6cb0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.28 1.28L3 12l5.8 1.9a2 2 0 0 1 1.28 1.28L12 21l1.9-5.8a2 2 0 0 1 1.28-1.28L21 12l-5.8-1.9a2 2 0 0 1-1.28-1.28Z"/></svg>
      <span>Insulated Cold Gel Shipping</span>
    </div>
    <div style="color: #4a0e17; font-size: 13.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 7px;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8Z"/><path d="m9 12 2 2 4-4"/></svg>
      <span>Samosas Fresh Daily (Never Frozen)</span>
    </div>
  </div>

  <!-- BLOQUE 2: LAS 3 TARJETAS VISUALES CON SUS IMÁGENES ORIGINALES Y TEXTOS/ENLACES EXACTOS DE CATÁLOGO -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 20px;">
    
    <!-- TARJETA 1: ALL INDIAN SWEETS -->
    <div style="background: #ffffff; border-radius: 10px; overflow: hidden; border: 1px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.08); display: flex; flex-direction: column; text-align: center;">
      <a href="/indian-sweets/" style="display: block; overflow: hidden;" title="All Indian Sweets">
        <img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/sweets-banner.png?t=1433913168" alt="All Indian Sweets" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />
      </a>
      <div style="padding: 14px 16px 18px 16px; display: flex; flex-direction: column; flex-grow: 1;">
        <h3 style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 18px; font-weight: 700; margin: 0 0 6px 0; letter-spacing: 0.2px;">All Indian Sweets (52 Varieties)</h3>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; color: #555; font-size: 13px; line-height: 1.5; margin: 0 0 14px 0; flex-grow: 1;">
          Nut Based, Bengali Mithai, Pure Kaju Katli, Chum Chum &amp; Traditional Ladoos. Shipped nationwide in cold packs.
        </p>
        <a href="/indian-sweets/" style="display: flex; align-items: center; justify-content: center; gap: 6px; background: #7a1526; color: #ffffff; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13.5px; font-weight: 700; padding: 10px 16px; border-radius: 6px; text-decoration: none; transition: background 0.2s;">
          <span>Shop All Sweets &rarr;</span>
        </a>
      </div>
    </div>

    <!-- TARJETA 2: INDIAN SNACKS & NAMKEEN -->
    <div style="background: #ffffff; border-radius: 10px; overflow: hidden; border: 1px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.08); display: flex; flex-direction: column; text-align: center;">
      <a href="/indian-snacks/" style="display: block; overflow: hidden;" title="Indian Snacks & Namkeen">
        <img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/snacks-banner.png?t=1433913279" alt="Indian Snacks & Namkeen" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />
      </a>
      <div style="padding: 14px 16px 18px 16px; display: flex; flex-direction: column; flex-grow: 1;">
        <h3 style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 18px; font-weight: 700; margin: 0 0 6px 0; letter-spacing: 0.2px;">Indian Snacks &amp; Namkeen</h3>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; color: #555; font-size: 13px; line-height: 1.5; margin: 0 0 14px 0; flex-grow: 1;">
          Traditional Mathi, Namak Para, Gud Para, Sev &amp; Spiced Cashews. The authentic accompaniment for chai time.
        </p>
        <a href="/indian-snacks/" style="display: flex; align-items: center; justify-content: center; gap: 6px; background: #d4af37; color: #2e060c; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13.5px; font-weight: 800; padding: 10px 16px; border-radius: 6px; text-decoration: none; transition: background 0.2s;">
          <span>Explore Snacks &rarr;</span>
        </a>
      </div>
    </div>

    <!-- TARJETA 3: MITHAI BOXES & GIFT BASKETS -->
    <div style="background: #ffffff; border-radius: 10px; overflow: hidden; border: 1px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.08); display: flex; flex-direction: column; text-align: center;">
      <a href="/mithai-box/" style="display: block; overflow: hidden;" title="Mithai Boxes & Gift Baskets">
        <img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/gift-boxes-banner.png" alt="Mithai Boxes & Gift Baskets" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />
      </a>
      <div style="padding: 14px 16px 18px 16px; display: flex; flex-direction: column; flex-grow: 1;">
        <h3 style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 18px; font-weight: 700; margin: 0 0 6px 0; letter-spacing: 0.2px;">Mithai Boxes &amp; Gift Baskets</h3>
        <p style="font-family: 'Plus Jakarta Sans', sans-serif; color: #555; font-size: 13px; line-height: 1.5; margin: 0 0 14px 0; flex-grow: 1;">
          Custom &amp; ready-made gift boxes, Golden Ganesh boxes, Peacock boxes &amp; 5-10 Lb luxury holiday baskets.
        </p>
        <a href="/mithai-box/" style="display: flex; align-items: center; justify-content: center; gap: 6px; background: #4a0e17; color: #ffffff; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13.5px; font-weight: 700; padding: 10px 16px; border-radius: 6px; text-decoration: none; transition: background 0.2s;">
          <span>View Gift Boxes &rarr;</span>
        </a>
      </div>
    </div>

  </div>

</div>
"""

headers = {
    "X-Auth-Token": access_token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "name": "HEADINGS",
    "page": "home_page",
    "location": "top",
    "date_type": "always",
    "visible": 1,
    "content": hero_html
}

url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5"
req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="PUT")

try:
    with urllib.request.urlopen(req) as res:
        print("Banner 5 update status:", res.status)
        data = json.loads(res.read().decode())
        print("Updated banner name:", data.get("name"))
except Exception as e:
    print("Error updating banner 5:", e)
