import os
import json
import re
import urllib.request
from dotenv import load_dotenv

load_dotenv()
store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

headers = {
    "X-Auth-Token": token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# ========================================================
# TOP BANNER (ID 5) - HERO CAROUSEL, TRIAGE & CATEGORIES
# ========================================================
banner_top_html = """
<!-- GLOBAL STYLES & TYPOGRAPHY (MARCELLUS + PLUS JAKARTA SANS) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style id="qs-global-2-fonts-system">
  /* Ocultar el carrusel nativo antiguo de baja resolución */
  #HomeSlideShow {
    display: none !important;
  }

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

  /* Tarjetas y Botones */
  .qs-btn-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: #7a1526;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 700;
    padding: 11px 22px;
    border-radius: 6px;
    text-decoration: none !important;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
  }
  .qs-btn-primary:hover {
    background: #540c17;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(122, 21, 38, 0.35);
  }

  .qs-btn-gold {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: #d4af37;
    color: #2e060c !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 800;
    padding: 11px 22px;
    border-radius: 6px;
    text-decoration: none !important;
    transition: all 0.2s ease;
    border: none;
    cursor: pointer;
  }
  .qs-btn-gold:hover {
    background: #c59f2a;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
  }

  .qs-btn-whatsapp {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: #25d366;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 700;
    padding: 11px 22px;
    border-radius: 6px;
    text-decoration: none !important;
    transition: all 0.2s ease;
  }
  .qs-btn-whatsapp:hover {
    background: #1ebc59;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);
  }

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

  #qs-hero-slider-container {
    aspect-ratio: 16 / 6.3 !important;
    max-height: 395px !important;
  }
  #qs-slides-wrapper {
    width: 100% !important;
    height: 100% !important;
  }
  .qs-carousel-slide {
    width: 100% !important;
    height: 100% !important;
    animation: qsFadeIn 0.35s ease-in-out;
  }
  .qs-carousel-slide a {
    display: block !important;
    width: 100% !important;
    height: 100% !important;
  }
  .qs-carousel-slide img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    object-position: center center !important;
    display: block !important;
  }
  @keyframes qsFadeIn {
    from { opacity: 0.4; }
    to { opacity: 1; }
  }
</style>

<div id="qs-home-top-container" style="margin: 0 0 25px 0;">

  <!-- ========================================================
       HERO CAROUSEL: 3 NEW CUSTOM HIGH-RES BANNERS (30% REDUCED HEIGHT)
       ======================================================== -->
  <div id="qs-hero-slider-container" style="position: relative; width: 100%; margin: 0 auto 28px auto; border-radius: 12px; overflow: hidden; box-shadow: 0 6px 20px rgba(0,0,0,0.15); border: 1.5px solid #ebdcc5; background: #fffdfa; aspect-ratio: 16 / 6.3; max-height: 395px;">
    
    <div id="qs-slides-wrapper" style="position: relative; width: 100%; height: 100%; overflow: hidden;">
      
      <!-- Slide 1: Welcome to Quality Sweets -->
      <div class="qs-carousel-slide" style="display: block; width: 100%; height: 100%;">
        <a href="/indian-sweets/" style="display: block; width: 100%; height: 100%; text-decoration: none;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/408/hero_banner_welcome_highres__39311.1789176649.1280.1280.webp?c=2" alt="Welcome to Quality Sweets - Traditional Indian Sweets Handcrafted Daily" style="width: 100%; height: 100%; object-fit: cover; object-position: center; display: block;" width="1024" height="576" />
        </a>
      </div>

      <!-- Slide 2: Assorted Sweets Gift Baskets -->
      <div class="qs-carousel-slide" style="display: none; width: 100%; height: 100%;">
        <a href="/gift-boxes/" style="display: block; width: 100%; height: 100%; text-decoration: none;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/406/hero_gift_baskets_banner__42648.1789173249.1280.1280.jpg?c=2" alt="Assorted Sweets Gift Baskets - Perfect for Every Celebration" style="width: 100%; height: 100%; object-fit: cover; object-position: center; display: block;" width="1024" height="576" />
        </a>
      </div>

      <!-- Slide 3: Special Bulk Pricing -->
      <div class="qs-carousel-slide" style="display: none; width: 100%; height: 100%;">
        <a href="/catering/" style="display: block; width: 100%; height: 100%; text-decoration: none;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/407/hero_bulk_pricing_banner__69363.1789173250.1280.1280.jpg?c=2" alt="Special Bulk Pricing on Indian Sweets - Shipping and In-Store Pickup Available" style="width: 100%; height: 100%; object-fit: cover; object-position: center; display: block;" width="1024" height="576" />
        </a>
      </div>

    </div>

    <!-- PREV / NEXT ARROW BUTTONS -->
    <button type="button" id="qs-prev-btn" aria-label="Previous Slide" style="position: absolute; top: 50%; left: 14px; transform: translateY(-50%); background: rgba(74, 14, 23, 0.85); color: #ffffff; border: 1.5px solid #d4af37; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10; transition: all 0.2s ease; box-shadow: 0 3px 10px rgba(0,0,0,0.3);">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </button>
    
    <button type="button" id="qs-next-btn" aria-label="Next Slide" style="position: absolute; top: 50%; right: 14px; transform: translateY(-50%); background: rgba(74, 14, 23, 0.85); color: #ffffff; border: 1.5px solid #d4af37; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10; transition: all 0.2s ease; box-shadow: 0 3px 10px rgba(0,0,0,0.3);">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>

    <!-- DOT INDICATORS -->
    <div id="qs-dots-wrapper" style="position: absolute; bottom: 14px; left: 0; right: 0; display: flex; justify-content: center; gap: 8px; z-index: 10;">
      <span class="qs-dot" data-index="0" style="width: 12px; height: 12px; border-radius: 50%; background: #d4af37; border: 1.5px solid #ffffff; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.4);"></span>
      <span class="qs-dot" data-index="1" style="width: 12px; height: 12px; border-radius: 50%; background: rgba(255,255,255,0.6); border: 1.5px solid #7a1526; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.4);"></span>
      <span class="qs-dot" data-index="2" style="width: 12px; height: 12px; border-radius: 50%; background: rgba(255,255,255,0.6); border: 1.5px solid #7a1526; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.4);"></span>
    </div>

  </div>

  <script type="text/javascript">
  (function() {
    var currentIndex = 0;
    var slides = document.querySelectorAll('.qs-carousel-slide');
    var dots = document.querySelectorAll('.qs-dot');
    var total = slides.length;
    var timer = null;

    if (!slides.length) return;

    function showSlide(idx) {
      if (idx < 0) idx = total - 1;
      if (idx >= total) idx = 0;
      currentIndex = idx;

      for (var i = 0; i < total; i++) {
        if (i === currentIndex) {
          slides[i].style.display = 'block';
          if (dots[i]) {
            dots[i].style.background = '#d4af37';
            dots[i].style.borderColor = '#ffffff';
          }
        } else {
          slides[i].style.display = 'none';
          if (dots[i]) {
            dots[i].style.background = 'rgba(255,255,255,0.6)';
            dots[i].style.borderColor = '#7a1526';
          }
        }
      }
    }

    function nextSlide() {
      showSlide(currentIndex + 1);
    }

    function prevSlide() {
      showSlide(currentIndex - 1);
    }

    function startTimer() {
      stopTimer();
      timer = setInterval(nextSlide, 5000);
    }

    function stopTimer() {
      if (timer) clearInterval(timer);
    }

    var nextBtn = document.getElementById('qs-next-btn');
    var prevBtn = document.getElementById('qs-prev-btn');
    var container = document.getElementById('qs-hero-slider-container');

    if (nextBtn) {
      nextBtn.addEventListener('click', function(e) {
        e.preventDefault();
        nextSlide();
        startTimer();
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function(e) {
        e.preventDefault();
        prevSlide();
        startTimer();
      });
    }

    for (var d = 0; d < dots.length; d++) {
      (function(index) {
        dots[index].addEventListener('click', function() {
          showSlide(index);
          startTimer();
        });
      })(d);
    }

    if (container) {
      container.addEventListener('mouseenter', stopTimer);
      container.addEventListener('mouseleave', startTimer);
    }

    startTimer();
  })();
  </script>

  <!-- ========================================================
       SECTION 1: HERO SERVICES & TRIAGE BAR
       ======================================================== -->
  <div style="background: radial-gradient(circle at 50% 15%, #881628 0%, #540c17 60%, #35050d 100%); color: #ffffff; border-radius: 14px; padding: 36px 24px 28px 24px; text-align: center; box-shadow: 0 10px 30px rgba(53, 5, 13, 0.35); border: 2px solid #d4af37; margin-bottom: 25px;">
    
    <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; background: rgba(212, 175, 55, 0.15); border: 1px solid #d4af37; color: #ffd700; font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; padding: 6px 18px; border-radius: 50px; margin-bottom: 18px;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
      <span>100% Pure Vegetarian &bull; Zero Chemical Preservatives &bull; Made Fresh Daily</span>
    </div>

    <h1 style="color: #ffffff; font-size: 34px; font-weight: 400; line-height: 1.3; margin: 0 0 14px 0; letter-spacing: 0.5px; text-shadow: 0 2px 10px rgba(0,0,0,0.6);">
      Authentic Indian Sweet Shop &bull; Fresh Mithai &amp; Hot Snacks Daily
    </h1>

    <p style="color: #fce8cc; font-size: 15.5px; font-weight: 500; max-width: 820px; margin: 0 auto 26px auto; line-height: 1.6;">
      Quality Sweets is an authentic Indian sweet shop in Iselin, NJ, serving handcrafted mithai, hot samosas, chaats, and nationwide sweet delivery since 2003.
    </p>

    <!-- TRIAJE DE LOS 3 PILARES -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; max-width: 980px; margin: 0 auto 24px auto;">
      
      <!-- BOTON 1: ENVIOS ECOMMERCE -->
      <a href="/indian-sweets/" class="qs-btn-white-card">
        <div style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; flex-shrink: 0; align-self: center;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/394/btn_sweets_bg__81005.1789094378.350.350.jpg?c=2" alt="Order Sweets Online" style="display: block; width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37;" />
        </div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; align-self: center; text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25;">Order Sweets Online</div>
          <div style="color: #555555; font-size: 12px; font-weight: 600; margin-top: 3px;">(USA Shipping)</div>
        </div>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; align-self: center;"><polyline points="9 18 15 12 9 6"/></svg>
      </a>

      <!-- BOTON 2: TAKEOUT LOCAL ISELIN -->
      <a href="/menu/" class="qs-btn-white-card">
        <div style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; flex-shrink: 0; align-self: center;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/395/btn_takeout_bg__18527.1789094396.350.350.jpg?c=2" alt="Takeout & Pickup Menu" style="display: block; width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37;" />
        </div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; align-self: center; text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25;">Takeout &amp; Pickup Menu</div>
          <div style="color: #555555; font-size: 12px; font-weight: 600; margin-top: 3px;">(Iselin Store)</div>
        </div>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; align-self: center;"><polyline points="9 18 15 12 9 6"/></svg>
      </a>

      <!-- BOTON 3: CATERING B2B -->
      <a href="/catering/" class="qs-btn-white-card">
        <div style="display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; flex-shrink: 0; align-self: center;">
          <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/396/btn_catering_bg__82126.1789094396.350.350.jpg?c=2" alt="Wedding & Catering" style="display: block; width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37;" />
        </div>
        <div style="flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; align-self: center; text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25;">Wedding &amp; Catering</div>
          <div style="color: #555555; font-size: 12px; font-weight: 600; margin-top: 3px;">(Tri-State)</div>
        </div>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; align-self: center;"><polyline points="9 18 15 12 9 6"/></svg>
      </a>

    </div>

    <!-- CONTACTO DIRECTO & HORARIOS -->
    <div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 12px; border-top: 1px solid rgba(212, 175, 55, 0.3); padding-top: 18px;">
      <div style="background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 6px; padding: 7px 14px; font-size: 13px; font-weight: 600; color: #ffd700; display: inline-flex; align-items: center; gap: 7px;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
        <span>1384 Oak Tree Rd, Iselin NJ &bull; Open Daily 10am&ndash;8pm</span>
      </div>

      <div style="background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 6px; padding: 7px 14px; font-size: 13px; font-weight: 600; color: #ffffff; display: inline-flex; align-items: center; gap: 7px;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        <span>Store: <a href="tel:7322833799" style="color: #ffd700; text-decoration: underline; font-weight: 700; margin-left: 2px;">(732) 283-3799</a></span>
      </div>

    </div>
  </div>

  <!-- TRUST BAR / E-E-A-T CON ICONOS SVGS -->
  <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px 20px; margin-top: 16px; display: flex; flex-wrap: wrap; justify-content: space-around; align-items: center; text-align: center; gap: 14px;">
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

  <!-- BLOQUE 2: LAS 3 TARJETAS VISUALES DE CATEGORÍAS -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 20px;">
    
    <!-- TARJETA 1: ALL INDIAN SWEETS -->
    <div style="background: #ffffff; border-radius: 10px; overflow: hidden; border: 1px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.08); display: flex; flex-direction: column; text-align: center;">
      <a href="/indian-sweets/" style="display: block; overflow: hidden;" title="All Indian Sweets">
        <img src="https://cdn6.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/sweets-banner.png?t=1433913168" alt="All Indian Sweets" style="width: 100%; height: auto; display: block; border-bottom: 2px solid #ebdcc5;" />
      </a>
      <div style="padding: 14px 16px 18px 16px; display: flex; flex-direction: column; flex-grow: 1;">
        <h3 style="color: #7a1526; font-size: 18px; font-weight: 700; margin: 0 0 6px 0; letter-spacing: 0.2px;">All Indian Sweets (52 Varieties)</h3>
        <p style="color: #555; font-size: 13px; line-height: 1.5; margin: 0 0 14px 0; flex-grow: 1;">
          Nut based, Bengali mithai, pure Kaju Katli, Chum Chum, and traditional ladoos. Shipped nationwide in cold packs.
        </p>
        <a href="/indian-sweets/" style="display: flex; align-items: center; justify-content: center; gap: 6px; background: #7a1526; color: #ffffff; font-size: 13.5px; font-weight: 700; padding: 10px 16px; border-radius: 6px; text-decoration: none; transition: background 0.2s;">
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
        <h3 style="color: #7a1526; font-size: 18px; font-weight: 700; margin: 0 0 6px 0; letter-spacing: 0.2px;">Indian Snacks &amp; Namkeen</h3>
        <p style="color: #555; font-size: 13px; line-height: 1.5; margin: 0 0 14px 0; flex-grow: 1;">
          Traditional Mathi, Namak Para, Gud Para, Sev &amp; Spiced Cashews. Crispy, savory snacks made fresh for your daily chai.
        </p>
        <a href="/indian-snacks/" style="display: flex; align-items: center; justify-content: center; gap: 6px; background: #d4af37; color: #2e060c; font-size: 13.5px; font-weight: 800; padding: 10px 16px; border-radius: 6px; text-decoration: none; transition: background 0.2s;">
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
        <h3 style="color: #7a1526; font-size: 18px; font-weight: 700; margin: 0 0 6px 0; letter-spacing: 0.2px;">Mithai Boxes &amp; Gift Baskets</h3>
        <p style="color: #555; font-size: 13px; line-height: 1.5; margin: 0 0 14px 0; flex-grow: 1;">
          Custom and ready-made gift boxes, Golden Ganesh boxes, Peacock boxes, and 5-10 lb holiday gift baskets.
        </p>
        <a href="/mithai-box/" style="display: flex; align-items: center; justify-content: center; gap: 6px; background: #4a0e17; color: #ffffff; font-size: 13.5px; font-weight: 700; padding: 10px 16px; border-radius: 6px; text-decoration: none; transition: background 0.2s;">
          <span>View Gift Boxes &rarr;</span>
        </a>
      </div>
    </div>

  </div>

</div>
"""

# ========================================================
# BOTTOM BANNER (ID 7) - TAKEOUT, ARTISAN, TOP SELLERS,
# CATERING, QUALITY PROMISE, FAQS & TRUST BANNERS
# ========================================================
banner_bottom_html = """
<style>
  /* Reset Megnor theme legacy floats and 320px width constraints */
  #SideTopSellers {
    display: none !important;
  }
  .banner_home_page_bottom {
    float: none !important;
    width: 100% !important;
    box-sizing: border-box !important;
  }
  #qs-home-bottom-container {
    width: 100% !important;
    max-width: 1180px !important;
    margin: 35px auto 20px auto !important;
    box-sizing: border-box !important;
    clear: both !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  #qs-home-bottom-container h2, #qs-home-bottom-container h3 {
    font-family: 'Marcellus', Georgia, 'Times New Roman', serif !important;
    letter-spacing: 0.3px;
    font-weight: 400;
  }
  .qs-section-box {
    background: #ffffff;
    border: 1px solid #ebdcc5;
    border-radius: 10px;
    padding: 28px 24px;
    margin-bottom: 35px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    box-sizing: border-box !important;
    width: 100% !important;
  }
  .qs-product-card {
    background: #ffffff;
    border: 1px solid #ebdcc5;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    display: flex;
    flex-direction: column;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  .qs-product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    border-color: #d4af37;
  }
  .qs-product-img {
    width: 100%;
    height: 190px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 12px;
  }
  .qs-product-title {
    font-family: 'Marcellus', Georgia, serif;
    font-size: 17px;
    color: #4a0e17;
    margin: 0 0 6px 0;
    line-height: 1.3;
    font-weight: 700;
  }
  .qs-product-price {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: #881628;
    margin-bottom: 12px;
  }
  #qs-top-sellers-block {
    position: relative;
    background: #faf7f2;
    border: 1px solid #ebdcc5;
    border-radius: 12px;
    padding: 28px 24px;
    margin: 40px 0 50px 0;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    box-sizing: border-box;
    width: 100% !important;
  }
  .qs-ts-header {
    text-align: center;
    margin-bottom: 24px;
    position: relative;
  }
  .qs-ts-title {
    font-family: 'Marcellus', Georgia, serif;
    font-size: 26px;
    color: #4a0e17;
    margin: 0 0 6px 0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
  }
  .qs-ts-title::before, .qs-ts-title::after {
    content: '';
    display: inline-block;
    width: 40px;
    height: 1.5px;
    background: #d4af37;
  }
  .qs-ts-subtitle {
    color: #666;
    font-size: 14px;
    margin: 0;
  }
  .qs-ts-carousel-wrapper {
    position: relative;
    padding: 0 10px;
  }
  .qs-product-slide {
    padding: 8px 10px;
    box-sizing: border-box;
  }
  .qs-product-card-inner {
    background: #ffffff;
    border: 1px solid #ebdcc5;
    border-radius: 10px;
    padding: 16px 14px;
    text-align: center;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    display: flex;
    flex-direction: column;
    height: 100%;
    box-sizing: border-box;
  }
  .qs-product-card-inner:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(74, 14, 23, 0.12);
    border-color: #d4af37;
  }
  .qs-product-img-wrap {
    width: 100%;
    height: 180px;
    overflow: hidden;
    border-radius: 8px;
    background: #fdfbf7;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
  }
  .qs-product-img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: transform 0.25s ease;
  }
  .qs-product-card-inner:hover .qs-product-img-wrap img {
    transform: scale(1.05);
  }
  .qs-product-name {
    font-family: 'Marcellus', Georgia, serif;
    font-size: 16px;
    font-weight: 600;
    color: #4a0e17;
    margin: 0 0 6px 0;
    line-height: 1.3;
    min-height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .qs-product-name a {
    color: #4a0e17;
    text-decoration: none;
  }
  .qs-product-name a:hover {
    color: #7a1526;
  }
  .qs-product-stars {
    color: #d4af37;
    font-size: 13px;
    margin-bottom: 6px;
    letter-spacing: 1px;
  }
  .qs-product-price {
    font-size: 16px;
    font-weight: 700;
    color: #7a1526;
    margin-bottom: 12px;
  }
  .qs-product-price span {
    font-size: 12.5px;
    color: #777;
    font-weight: 400;
  }
  .qs-btn-card {
    display: inline-block;
    background: #7a1526;
    color: #ffffff !important;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    padding: 9px 16px;
    border-radius: 6px;
    transition: all 0.2s ease;
    border: 1px solid #7a1526;
    margin-top: auto;
  }
  .qs-btn-card:hover {
    background: #941e32;
    border-color: #d4af37;
    box-shadow: 0 3px 10px rgba(122, 21, 38, 0.3);
  }
  .qs-ts-nav-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: #ffffff;
    border: 1.5px solid #d4af37;
    color: #7a1526;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 20;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    transition: all 0.2s ease;
  }
  .qs-ts-nav-btn:hover {
    background: #7a1526 !important;
    color: #ffffff !important;
    border-color: #7a1526 !important;
    transform: translateY(-50%) scale(1.08) !important;
  }
  .qs-ts-prev {
    left: -16px;
  }
  .qs-ts-next {
    right: -16px;
  }
  @media (max-width: 768px) {
    .qs-ts-prev { left: -8px; width: 36px; height: 36px; }
    .qs-ts-next { right: -8px; width: 36px; height: 36px; }
  }
  /* Fallback if JS hasn't initialized owlCarousel yet: clean horizontal scroll instead of vertical stack */
  #owl-top-sellers:not(.owl-theme) {
    display: flex !important;
    overflow-x: auto !important;
    scroll-snap-type: x mandatory;
    gap: 10px;
    padding-bottom: 10px;
  }
  #owl-top-sellers:not(.owl-theme) .qs-product-slide {
    flex: 0 0 calc(25% - 8px);
    min-width: 220px;
    scroll-snap-align: start;
  }
  .qs-faq-item {
    border-bottom: 1px solid #ebdcc5;
    padding: 14px 0;
  }
  .qs-faq-item summary {
    font-family: 'Marcellus', Georgia, serif;
    font-size: 17px;
    color: #7a1526;
    cursor: pointer;
    font-weight: 600;
  }
  .qs-faq-content {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14.5px;
    line-height: 1.65;
    color: #444444;
    padding: 12px 0 4px 0;
  }
</style>

<div id="qs-home-bottom-container" style="margin: 35px 0 20px 0;">

  <!-- SECTION 3: HOT TAKEOUT COUNTER & STREET FOOD (ISELIN STORE) -->
  <div class="qs-section-box" style="border-left: 6px solid #7a1526; background: #fffdfa;">
    <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 18px;">
      <div>
        <span style="color: #881628; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">Hot Food Counter &bull; Iselin Takeout</span>
        <h2 style="font-size: 26px; color: #4a0e17; margin: 4px 0 0 0;">Fresh Hot Samosas, Chaats &amp; Street Food To-Go</h2>
      </div>
      <div style="background: #fff8e6; border: 1px solid #d4af37; border-radius: 6px; padding: 8px 14px; font-size: 12.5px; font-weight: 700; color: #7a1526; display: inline-flex; align-items: center; gap: 6px;">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
        <span>Counter Pickup Only &bull; No Dine-In Seating</span>
      </div>
    </div>

    <p style="font-size: 15px; line-height: 1.65; color: #444; margin-bottom: 22px;">
      We fry our samosas fresh throughout the day on Oak Tree Road. Made with spiced potatoes, green peas, and ajwain dough (never frozen, and always fried in clean 100% vegetable oil). Enjoy them with our house-made mint and sweet tamarind chutneys, or pick up hot chaats to go:
    </p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; margin-bottom: 24px;">
      
      <!-- Card 1: Samosa & Papri Chaat -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/398/samosa_chaat_photo_1789098060133__20739.1789098260.350.350.jpg?c=2" alt="Samosa &amp; Papri Chaat" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Samosa &amp; Papri Chaat</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Crushed samosas or crispy papris with chilled yogurt, sev, and fresh tamarind-mint chutneys.</span>
      </div>

      <!-- Card 2: Pani Puri Kits -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/399/pani_puri_photo_1789098074946__46127.1789098262.350.350.jpg?c=2" alt="Pani Puri Kits To-Go" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Pani Puri Kits To-Go</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Crispy puris packed with spiced potato-chickpea filling and chilled spicy mint water.</span>
      </div>

      <!-- Card 3: Hot Chole Bhatura -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/400/chole_bhatura_photo_1789098088650__70835.1789098264.350.350.jpg?c=2" alt="Hot Chole Bhatura" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Hot Chole Bhatura</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Two puffy bhaturas served hot with slow-simmered Punjabi chickpea curry and pickled onions.</span>
      </div>

      <!-- Card 4: Aloo & Gobi Parathas -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/401/stuffed_paratha_photo_1789098102913__76988.1789098265.350.350.jpg?c=2" alt="Aloo &amp; Gobi Parathas" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Aloo &amp; Gobi Parathas</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Cooked hot on the tawa with real butter, stuffed with spiced potato or seasoned cauliflower.</span>
      </div>

    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 12px;">
      <a href="/menu/" class="qs-btn-primary">View Full Iselin Takeout Menu &rarr;</a>
    </div>
  </div>

  <!-- SECTION 4: ARTISAN SWEETS & COLD SHIPPING SYSTEM -->
  <div class="qs-section-box" style="border-left: 6px solid #d4af37;">
    <span style="color: #b38b1e; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">Express Delivery Across all 50 States</span>
    <h2 style="font-size: 26px; color: #4a0e17; margin: 4px 0 16px 0;">Artisan Indian Sweets Handcrafted Daily &amp; Shipped Nationwide</h2>
    
    <p style="font-size: 15px; line-height: 1.65; color: #444; margin-bottom: 22px;">
      Every morning on Oak Tree Road, our halwais boil fresh whole milk down into rich khoya, grind whole cashews for silver-leaf Kaju Katli, and make fresh chhena for soft Bengali Chum Chums. <strong>No milk powder, no chemical preservatives, and no canned syrups.</strong>
    </p>

    <!-- 4 PRODUCT SHOWCASE CARDS FOR ARTISAN SWEETS -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; margin-bottom: 24px;">
      
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; text-align: center;">
        <a href="/malai-chum-chum/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/84/images/351/MALAICHUM_CHUM__26837.1437440527.350.350.jpg?c=2" alt="Malai Chum Chum" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" /></a>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; margin-bottom: 4px;"><a href="/malai-chum-chum/" style="color: inherit; text-decoration: none;">Malai Chum Chum</a></strong>
        <span style="font-size: 13px; color: #666; line-height: 1.45;">Tender cottage cheese rolls soaked in light syrup, topped with rich clotted cream.</span>
      </div>

      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; text-align: center;">
        <a href="/milk-cake/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/105/images/301/Milk_Cake__92535.1433802617.350.350.jpg?c=2" alt="Slow-Cooked Milk Cake" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" /></a>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; margin-bottom: 4px;"><a href="/milk-cake/" style="color: inherit; text-decoration: none;">Slow-Cooked Milk Cake</a></strong>
        <span style="font-size: 13px; color: #666; line-height: 1.45;">Traditional Alwar-style caramelized khoya fudge with green cardamom.</span>
      </div>

      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; text-align: center;">
        <a href="/mango-sandesh/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/82/images/275/Mango_Sandesh__78298.1433712997.350.350.jpg?c=2" alt="Fresh Mango Sandesh" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" /></a>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; margin-bottom: 4px;"><a href="/mango-sandesh/" style="color: inherit; text-decoration: none;">Fresh Mango Sandesh</a></strong>
        <span style="font-size: 13px; color: #666; line-height: 1.45;">Soft Bengali chhena sweet blended with Alphonso mango pulp.</span>
      </div>

      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; text-align: center;">
        <a href="/besan-ladoo/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/98/images/294/Besan_Ladoo__03878.1433732821.350.350.jpg?c=2" alt="Pure Besan Ladoo" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" /></a>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; margin-bottom: 4px;"><a href="/besan-ladoo/" style="color: inherit; text-decoration: none;">Pure Besan Ladoo</a></strong>
        <span style="font-size: 13px; color: #666; line-height: 1.45;">Roasted gram flour in pure desi ghee with slivered almonds.</span>
      </div>

    </div>

    <!-- 3 THERMAL PACKAGING STEPS -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin-bottom: 24px;">
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 18px;">
        <div style="width: 44px; height: 44px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #d4af37; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #4a0e17; font-size: 16px; display: block; margin-bottom: 6px;">1. Sealed at Peak Freshness</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Sweets are sealed right after morning batches are made to preserve moisture, texture, and natural flavor.</p>
      </div>
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 18px;">
        <div style="width: 44px; height: 44px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #d4af37; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line><line x1="19.07" y1="4.93" x2="4.93" y2="19.07"></line></svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #4a0e17; font-size: 16px; display: block; margin-bottom: 6px;">2. Food-Grade Cold Packs</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Frozen gel packs keep the package cool in transit throughout delivery across the US.</p>
      </div>
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 18px;">
        <div style="width: 44px; height: 44px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #d4af37; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #4a0e17; font-size: 16px; display: block; margin-bottom: 6px;">3. Insulated Shipping Box</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Foil-lined thermal barrier delivered by express courier straight to your door.</p>
      </div>
    </div>

    <a href="/indian-sweets/" class="qs-btn-gold">Shop All Sweets with Cold Shipping &rarr;</a>
  </div>

  <!-- SECTION 5: CURRENT TOP SELLERS (CAROUSEL MATCHING FEATURED PRODUCTS) -->
  <div id="qs-top-sellers-block" class="qs-top-sellers-section">
    <div class="qs-ts-header">
      <h2 class="qs-ts-title">Current Top Sellers</h2>
      <p class="qs-ts-subtitle">Our most-ordered traditional sweets &bull; Shipped fresh nationwide in insulated cold packs</p>
    </div>

    <div class="qs-ts-carousel-wrapper">
      <button type="button" class="qs-ts-nav-btn qs-ts-prev" id="qs-ts-prev" aria-label="Previous Top Sellers">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
      </button>
      <button type="button" class="qs-ts-nav-btn qs-ts-next" id="qs-ts-next" aria-label="Next Top Sellers">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </button>

      <div class="owl-carousel" id="owl-top-sellers">
        
        <!-- 1. Kaju Katli -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/kaju-katli/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/77/images/308/Plain_Burfi__57958.1433826518.350.350.jpg?c=2" alt="Pure Kaju Katli" /></a>
            <h3 class="qs-product-name"><a href="/kaju-katli/">Pure Kaju Katli</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
            <div class="qs-product-price">$9.00 <span>/ lb</span></div>
            <a href="/kaju-katli/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 2. Motichur Ladoo -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/motichur-ladoo/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/104/images/299/Motichur_Ladoo__31599.1433801521.350.350.jpg?c=2" alt="Motichur Ladoo" /></a>
            <h3 class="qs-product-name"><a href="/motichur-ladoo/">Motichur Ladoo</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
            <div class="qs-product-price">$6.50 <span>/ lb</span></div>
            <a href="/motichur-ladoo/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 3. Khoya Pista Burfi -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/khoya-pista-burfi/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/113/images/309/Khoya_Pista_Burfi__02324.1433826917.350.350.jpg?c=2" alt="Khoya Pista Burfi" /></a>
            <h3 class="qs-product-name"><a href="/khoya-pista-burfi/">Khoya Pista Burfi</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
            <div class="qs-product-price">$7.00 <span>/ lb</span></div>
            <a href="/khoya-pista-burfi/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 4. Crispy Jalebi -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/jalebi/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/90/images/284/Jalebi__80913.1433725846.350.350.jpg?c=2" alt="Crispy Jalebi" /></a>
            <h3 class="qs-product-name"><a href="/jalebi/">Crispy Jalebi</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (5.0)</div>
            <div class="qs-product-price">$12.00 <span>/ lb</span></div>
            <a href="/jalebi/" class="qs-btn-card">Add to Cart</a>
          </div>
        </div>

        <!-- 5. Besan Ladoo -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/besan-ladoo/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/98/images/294/Besan_Ladoo__03878.1433732821.350.350.jpg?c=2" alt="Besan Ladoo" /></a>
            <h3 class="qs-product-name"><a href="/besan-ladoo/">Besan Ladoo</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
            <div class="qs-product-price">$8.00 <span>/ lb</span></div>
            <a href="/besan-ladoo/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 6. Milk Cake -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/milk-cake/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/105/images/301/Milk_Cake__92535.1433802617.350.350.jpg?c=2" alt="Rich Milk Cake" /></a>
            <h3 class="qs-product-name"><a href="/milk-cake/">Rich Milk Cake</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
            <div class="qs-product-price">$7.50 <span>/ lb</span></div>
            <a href="/milk-cake/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 7. Kala Jamun -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/kala-jamun/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/101/images/296/Kala_Jamoon__05636.1433734969.350.350.jpg?c=2" alt="Kala Jamun" /></a>
            <h3 class="qs-product-name"><a href="/kala-jamun/">Kala Jamun</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
            <div class="qs-product-price">$7.50 <span>/ lb</span></div>
            <a href="/kala-jamun/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 8. Malai Peda -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/malai-peda/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/86/images/331/Kadam_Keer__46637.1433875816.350.350.jpg?c=2" alt="Malai Peda" /></a>
            <h3 class="qs-product-name"><a href="/malai-peda/">Malai Peda</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.7)</div>
            <div class="qs-product-price">$8.00 <span>/ lb</span></div>
            <a href="/malai-peda/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 9. Pista Kaju Roll -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/kaju-roll/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/79/images/271/Kaju_Roll1__01965.1433603427.350.350.jpg?c=2" alt="Pista Kaju Roll" /></a>
            <h3 class="qs-product-name"><a href="/kaju-roll/">Pista Kaju Roll</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
            <div class="qs-product-price">$8.00 <span>/ lb</span></div>
            <a href="/kaju-roll/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

        <!-- 10. Malai Chum Chum -->
        <div class="qs-product-slide">
          <div class="qs-product-card-inner">
            <a href="/malai-chum-chum/" class="qs-product-img-wrap"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/84/images/351/MALAICHUM_CHUM__26837.1437440527.350.350.jpg?c=2" alt="Malai Chum Chum" /></a>
            <h3 class="qs-product-name"><a href="/malai-chum-chum/">Malai Chum Chum</a></h3>
            <div class="qs-product-stars">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
            <div class="qs-product-price">$8.00 <span>/ lb</span></div>
            <a href="/malai-chum-chum/" class="qs-btn-card">Choose Options</a>
          </div>
        </div>

      </div>
    </div>

    <div style="text-align: center; margin-top: 25px;">
      <a href="/indian-sweets/" class="qs-btn-primary" style="font-size: 15px; padding: 13px 28px;">
        Explore All 52 Indian Sweets &rarr;
      </a>
    </div>
  </div>

  <script type="text/javascript">
  (function() {
    function initTopSellersCarousel() {
      var $ = window.jQuery || window.$;
      if ($ && typeof $.fn.owlCarousel === 'function') {
        var $owl = $("#owl-top-sellers");
        if ($owl.length && !$owl.hasClass('owl-carousel-init')) {
          $owl.addClass('owl-carousel-init');
          $owl.owlCarousel({
            items: 4,
            itemsDesktop: [1000, 4],
            itemsDesktopSmall: [970, 3],
            itemsTablet: [700, 2],
            itemsMobile: [480, 1],
            pagination: false,
            navigation: false,
            slideSpeed: 300
          });
          $(document).off('click', '#qs-ts-next').on('click', '#qs-ts-next', function(e) {
            e.preventDefault();
            $owl.trigger('owl.next');
          });
          $(document).off('click', '#qs-ts-prev').on('click', '#qs-ts-prev', function(e) {
            e.preventDefault();
            $owl.trigger('owl.prev');
          });
        }
      } else {
        setTimeout(initTopSellersCarousel, 80);
      }
    }

    if (typeof jQuery !== 'undefined') {
      jQuery(document).ready(initTopSellersCarousel);
    } else if (typeof $ !== 'undefined') {
      $(document).ready(initTopSellersCarousel);
    }
    window.addEventListener('load', initTopSellersCarousel);
    initTopSellersCarousel();
  })();
  </script>

  <!-- SECTION 6: REGIONAL CATERING, WEDDINGS & MANDIRS TRI-STATE -->
  <div class="qs-section-box" style="border-left: 6px solid #4a0e17;">
    <span style="color: #7a1526; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">B2B Services &bull; NJ, NY &amp; CT Tri-State Coverage</span>
    <h2 style="font-size: 26px; color: #4a0e17; margin: 4px 0 16px 0;">Authentic Mithai &amp; Samosa Catering for Weddings, Mandirs &amp; Events</h2>
    
    <p style="font-size: 15px; line-height: 1.65; color: #444; margin-bottom: 22px;">
      From wedding receptions in Manhattan and Diwali events in Jersey City to weekly prasad for temples across Connecticut, we prepare large orders fresh in our Iselin kitchen:
    </p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px;">
      
      <!-- Catering Card 1: Wedding Gift Boxes -->
      <div style="padding: 16px; background: #fffdfa; border: 1px solid #ebdcc5; border-radius: 8px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/402/wedding_gift_box_1789098119353__27913.1789098267.350.350.jpg?c=2" alt="Wedding Sweet Boxes &amp; Return Gifts" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16.5px; display: block; margin-bottom: 6px;">Wedding Sweet Boxes &amp; Return Gifts</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Gift boxes packed with your choice of Kaju Katli, burfi, and ladoos.</p>
      </div>

      <!-- Catering Card 2: Temple Bulk Prasad -->
      <div style="padding: 16px; background: #fffdfa; border: 1px solid #ebdcc5; border-radius: 8px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/403/temple_bulk_prasad_1789098135260__33231.1789098269.350.350.jpg?c=2" alt="Temple &amp; Mandir Bulk Prasad" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16.5px; display: block; margin-bottom: 6px;">Temple &amp; Mandir Bulk Prasad</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Bulk orders of Motichur Ladoo, Besan Ladoo, and Peda packed by the pound for temples and community gatherings.</p>
      </div>

      <!-- Catering Card 3: Bulk Samosa Trays -->
      <div style="padding: 16px; background: #fffdfa; border: 1px solid #ebdcc5; border-radius: 8px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/404/bulk_samosas_platter_1789098151834__74896.1789098270.350.350.jpg?c=2" alt="Bulk Fresh Samosa Trays" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16.5px; display: block; margin-bottom: 6px;">Bulk Fresh Samosa Trays (50 - 1,000+ pcs)</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Hot samosa party platters fried fresh to order for family gatherings, office lunches, and community events.</p>
      </div>

    </div>

    <a href="/catering/" class="qs-btn-primary">Request Catering &amp; Bulk Quote &rarr;</a>
  </div>

  <!-- SECTION 7: QUALITY PROMISE & FRESHNESS GUARANTEE -->
  <div style="background: radial-gradient(circle at 50% 50%, #4a0e17 0%, #2e060c 100%); color: #ffffff; border-radius: 12px; padding: 36px 28px; margin-bottom: 30px; border: 1.5px solid #d4af37;">
    <div style="text-align: center; max-width: 800px; margin: 0 auto 28px auto;">
      <span style="color: #ffd700; font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase;">Tradition &bull; Purity &bull; Zero Shortcuts</span>
      <h2 style="font-size: 28px; color: #ffffff; margin: 6px 0 12px 0;">The Quality Sweets Standard: Real Milk Khoya, Zero Shortcuts</h2>
      <p style="color: #fce8cc; font-size: 14.5px; line-height: 1.6;">Since 2003, we have made our sweets the traditional way on Oak Tree Road: pure ingredients, time-tested recipes, and no fillers.</p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; margin-bottom: 24px;">
      
      <!-- Card 1: 100% Real Milk Khoya -->
      <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 10px; padding: 20px 16px; text-align: center; display: flex; flex-direction: column; align-items: center;">
        <div style="width: 52px; height: 52px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.18); border: 1.5px solid #ffd700; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M8 2h8v2H8z"></path>
            <path d="M9 4v3l-2 3v10a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V10l-2-3V4"></path>
            <line x1="7" y1="14" x2="17" y2="14"></line>
          </svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #ffd700; display: block; margin-bottom: 6px;">100% Real Milk Khoya</strong>
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">Made with fresh reduced milk. No milk powder, starches, or vegetable oil fillers.</span>
      </div>

      <!-- Card 2: Zero Preservatives -->
      <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 10px; padding: 20px 16px; text-align: center; display: flex; flex-direction: column; align-items: center;">
        <div style="width: 52px; height: 52px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.18); border: 1.5px solid #ffd700; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            <path d="m9 12 2 2 4-4"></path>
          </svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #ffd700; display: block; margin-bottom: 6px;">Zero Preservatives</strong>
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">We don't add chemicals to artificially extend shelf life. Mithai is meant to be eaten fresh.</span>
      </div>

      <!-- Card 3: Strict 100% Pure Veg -->
      <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 10px; padding: 20px 16px; text-align: center; display: flex; flex-direction: column; align-items: center;">
        <div style="width: 52px; height: 52px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.18); border: 1.5px solid #ffd700; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 20A7 7 0 0 1 4 13a7 7 0 0 1 7-7c4 0 7 2 9 6-2 4-5 6-9 6z"></path>
            <path d="M11 6c0 4 2 7 6 7"></path>
          </svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #ffd700; display: block; margin-bottom: 6px;">Strict 100% Pure Veg</strong>
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">Strictly vegetarian kitchen and equipment on Oak Tree Road. No eggs, no gelatin.</span>
      </div>

      <!-- Card 4: Freshness Guarantee -->
      <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 10px; padding: 20px 16px; text-align: center; display: flex; flex-direction: column; align-items: center;">
        <div style="width: 52px; height: 52px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.18); border: 1.5px solid #ffd700; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="8" r="6"></circle>
            <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"></path>
          </svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #ffd700; display: block; margin-bottom: 6px;">Freshness Guarantee</strong>
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">If your package arrives damaged or not fresh, contact us within 24 hours and we'll make it right.</span>
      </div>

    </div>
  </div>

  <!-- SECTION 8: FREQUENTLY ASKED QUESTIONS (FAQS) -->
  <div class="qs-section-box">
    <div style="text-align: center; margin-bottom: 24px;">
      <span style="color: #7a1526; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">Helpful Information &bull; Quick Answers</span>
      <h2 style="font-size: 26px; color: #4a0e17; margin: 4px 0 0 0;">Frequently Asked Questions About Quality Sweets</h2>
    </div>

    <div style="max-width: 900px; margin: 0 auto;">
      
      <details class="qs-faq-item" open>
        <summary>Can I sit and eat inside your Oak Tree Road store in Iselin, NJ?</summary>
        <div class="qs-faq-content">
          No. We are strictly a <strong>takeout counter and pickup shop</strong> with no dine-in tables. We fry hot samosas and chaats fresh all day and pack sweets by the pound to go. Call ahead at <a href="tel:7322833799" style="color: #7a1526; font-weight: 700;">(732) 283-3799</a> to have your order ready when you walk in.
        </div>
      </details>

      <details class="qs-faq-item">
        <summary>How do you ship delicate sweets like Chum Chum or Kaju Katli nationwide without spoiling?</summary>
        <div class="qs-faq-content">
          We pack each box with insulated thermal liners and frozen cold gel packs, then ship via expedited carrier. Sweets stay cool in transit and arrive fresh anywhere in the continental US.
        </div>
      </details>

      <details class="qs-faq-item">
        <summary>Do Quality Sweets products contain any chemical preservatives?</summary>
        <div class="qs-faq-content">
          Never. We make our sweets daily using pure milk khoya, real ghee, cardamom, and nuts, with <strong>zero artificial preservatives or additives</strong>.
        </div>
      </details>

      <details class="qs-faq-item">
        <summary>How much advance notice is required for wedding or temple bulk orders?</summary>
        <div class="qs-faq-content">
          For custom wedding boxes or orders of 100+ samosas, please order 1 to 2 weeks ahead. If you need catering on short notice in NJ, NY, or CT, call the shop.
        </div>
      </details>

    </div>
  </div>

  <!-- ORIGINAL PRESERVATIVES & SATISFACTION BANNER + BENGALI SWEETS DISCLAIMER -->
  <div style="margin: 40px auto 30px auto; text-align: center; max-width: 100%;">
    <p style="margin: 0 0 16px 0; text-align: center;">
      <img src="https://cdn10.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/bottom-banner-long-01.png" alt="100% Satisfaction Guaranteed, No Added Preservatives, Hand Made" style="max-width: 100%; height: auto; display: block; margin: 0 auto; vertical-align: middle;" width="951" height="130" />
    </p>
    <p style="margin: 0; text-align: center;">
      <img src="https://cdn10.bigcommerce.com/s-2ygwtj/product_images/uploaded_images/disclaimer1-01.png" alt="Bengali Sweets Two-Day Delivery Recommendation &amp; Price Notice" style="max-width: 100%; height: auto; display: block; margin: 0 auto; vertical-align: middle;" width="600" height="65" />
    </p>
  </div>

</div>
"""

# Keep the deployed homepage free of the duplicate editorial carousel. The
# storefront's native Current Top Sellers section remains the single source of
# this heading; this script must not reintroduce the retired banner section.
_editorial_top_sellers_pattern = (
    r"<!-- SECTION 5: CURRENT TOP SELLERS \(CAROUSEL MATCHING FEATURED PRODUCTS\) -->"
    r".*?"
    r"(?=<!-- SECTION 6: REGIONAL CATERING, WEDDINGS & MANDIRS TRI-STATE -->)"
)
banner_bottom_html, _removed_editorial_top_sellers = re.subn(
    _editorial_top_sellers_pattern, "", banner_bottom_html, count=1, flags=re.DOTALL
)
if _removed_editorial_top_sellers != 1:
    raise RuntimeError("Expected exactly one editorial Top Sellers section in the deployment source.")

# ========================================================
# EXECUTE PUT REQUESTS TO BIGCOMMERCE BANNERS API
# ========================================================
print("Updating Banner ID 5 (Top Banner: Carousel + Triage + Categories)...")
payload_top = {
    "name": "HEADINGS",
    "content": banner_top_html,
    "page": "home_page",
    "location": "top",
    "date_type": "always",
    "visible": "1"
}

req_top = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/5",
    data=json.dumps(payload_top).encode("utf-8"),
    headers=headers,
    method="PUT"
)

try:
    with urllib.request.urlopen(req_top) as res:
        data_top = json.loads(res.read().decode())
        print(f"[OK] Banner 5 updated successfully! ID: {data_top.get('id')}")
except Exception as e:
    print(f"[ERROR] Failed to update Banner 5: {e}")

print("\nUpdating Banner ID 7 (Bottom Banner: Takeout + Artisan + Top Sellers + Catering + Purity + FAQs + Trust Banners)...")
payload_bottom = {
    "name": "Preservatives Banner",
    "content": banner_bottom_html,
    "page": "home_page",
    "location": "bottom",
    "date_type": "always",
    "visible": "1"
}

req_bottom = urllib.request.Request(
    f"https://api.bigcommerce.com/stores/{store_hash}/v2/banners/7",
    data=json.dumps(payload_bottom).encode("utf-8"),
    headers=headers,
    method="PUT"
)

try:
    with urllib.request.urlopen(req_bottom) as res:
        data_bottom = json.loads(res.read().decode())
        print(f"[OK] Banner 7 updated successfully! ID: {data_bottom.get('id')}")
except Exception as e:
    print(f"[ERROR] Failed to update Banner 7: {e}")

print("\n=== PRODUCTION DEPLOYMENT COMPLETE ===")
