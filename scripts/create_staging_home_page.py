import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

store_hash = os.environ.get("BIGCOMMERCE_STORE_HASH")
access_token = os.environ.get("BIGCOMMERCE_ACCESS_TOKEN")

headers = {
    "X-Auth-Token": access_token,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

body_html = """
<!-- METATAG NOINDEX PARA BLINDAR PRIVACIDAD DE STAGING -->
<meta name="robots" content="noindex, nofollow">

<!-- GLOBAL STYLES & TYPOGRAPHY (MARCELLUS + PLUS JAKARTA SANS) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
  /* Hide default page title and breadcrumbs */
  .TitleHeading, #PageBreadcrumb {
    display: none !important;
  }

  /* Base Reset & Styling for Staging */
  .qs-staging-container {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #2e060c;
    max-width: 1180px;
    margin: 0 auto;
    padding: 0 15px;
    box-sizing: border-box;
  }

  .qs-staging-title, .qs-staging-container h1, .qs-staging-container h2, .qs-staging-container h3 {
    font-family: 'Marcellus', Georgia, 'Times New Roman', serif !important;
    letter-spacing: 0.3px;
    font-weight: 400;
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

  /* Grid de Productos Destacados */
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
    padding: 28px 20px 24px 20px;
    margin: 40px 0 50px 0;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    box-sizing: border-box;
  }
  .qs-ts-nav-btn {
    position: absolute;
    top: 54%;
    transform: translateY(-50%);
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: #ffffff;
    border: 1.5px solid #d4af37;
    color: #7a1526;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 20;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: all 0.2s ease;
  }
  .qs-ts-nav-btn:hover {
    background: #7a1526 !important;
    color: #ffffff !important;
    border-color: #7a1526 !important;
    transform: translateY(-50%) scale(1.08) !important;
  }
  .qs-ts-prev {
    left: -18px;
  }
  .qs-ts-next {
    right: -18px;
  }
  @media (max-width: 768px) {
    .qs-ts-prev { left: -8px; width: 36px; height: 36px; }
    .qs-ts-next { right: -8px; width: 36px; height: 36px; }
  }
  #owl-top-sellers .item {
    padding: 8px 10px;
  }
  #owl-top-sellers .qs-product-card {
    height: 100%;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
  }

  /* Section Modules */
  .qs-section-box {
    background: #ffffff;
    border: 1px solid #ebdcc5;
    border-radius: 12px;
    padding: 32px 28px;
    margin-bottom: 30px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  }

  /* FAQ Accordion Styling */
  .qs-faq-item {
    border-bottom: 1px solid #ebdcc5;
    padding: 16px 0;
  }
  .qs-faq-item:last-child {
    border-bottom: none;
  }
  .qs-faq-item summary {
    font-family: 'Marcellus', Georgia, serif;
    font-size: 18px;
    font-weight: 600;
    color: #4a0e17;
    cursor: pointer;
    list-style: none;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .qs-faq-item summary::-webkit-details-marker {
    display: none;
  }
  .qs-faq-item summary::after {
    content: '+';
    font-size: 22px;
    color: #d4af37;
    font-weight: 700;
  }
  .qs-faq-item[open] summary::after {
    content: '\\2212';
    color: #7a1526;
  }
  .qs-faq-content {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14.5px;
    line-height: 1.65;
    color: #444444;
    padding: 12px 0 4px 0;
  }
</style>

<div class="qs-staging-container">

  <!-- STAGING NOTICE BANNER -->
  <div style="background: #fff8e6; border: 2px dashed #d4af37; border-radius: 10px; padding: 16px 20px; margin: 20px 0 30px 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
    <div style="display: flex; align-items: center; gap: 12px;">
      <div style="width: 42px; height: 42px; background: rgba(212, 175, 55, 0.2); border: 1px solid #d4af37; border-radius: 8px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
      </div>
      <div>
        <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 17px; color: #7a1526; display: block;">PRIVATE STAGING PREVIEW ENVIRONMENT</strong>
        <span style="font-size: 13px; color: #665214;">This page is private, has <code>noindex, nofollow</code> active, and does not appear in navigation menus. The official production homepage remains 100% untouched.</span>
      </div>
    </div>
    <div style="background: #7a1526; color: #ffffff; padding: 6px 14px; border-radius: 50px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">
      STAGING PREVIEW ACTIVE
    </div>
  </div>

  <!-- ========================================================
       HERO CAROUSEL: 3 BANNERS (30% REDUCED HEIGHT)
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
    <button type="button" id="qs-prev-btn" aria-label="Previous Slide" style="position: absolute; top: 50%; left: 14px; transform: translateY(-50%); background: rgba(74, 14, 23, 0.8); color: #ffffff; border: 1.5px solid #d4af37; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10; transition: all 0.2s ease; box-shadow: 0 3px 10px rgba(0,0,0,0.3);">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </button>
    
    <button type="button" id="qs-next-btn" aria-label="Next Slide" style="position: absolute; top: 50%; right: 14px; transform: translateY(-50%); background: rgba(74, 14, 23, 0.8); color: #ffffff; border: 1.5px solid #d4af37; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10; transition: all 0.2s ease; box-shadow: 0 3px 10px rgba(0,0,0,0.3);">
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
       SECTION 1: HERO STOREFRONT & TRIAGE BAR
       ======================================================== -->
  <div style="background: radial-gradient(circle at 50% 15%, #881628 0%, #540c17 60%, #35050d 100%); color: #ffffff; border-radius: 14px; padding: 36px 24px 28px 24px; text-align: center; box-shadow: 0 10px 30px rgba(53, 5, 13, 0.35); border: 2px solid #d4af37; margin-bottom: 25px;">
    
    <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; background: rgba(212, 175, 55, 0.15); border: 1px solid #d4af37; color: #ffd700; font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; padding: 6px 18px; border-radius: 50px; margin-bottom: 18px;">
      <span>100% Pure Vegetarian &bull; Zero Chemical Preservatives &bull; Made Fresh Daily</span>
    </div>

    <h1 style="color: #ffffff; font-size: 34px; font-weight: 400; line-height: 1.3; margin: 0 0 14px 0; letter-spacing: 0.5px; text-shadow: 0 2px 10px rgba(0,0,0,0.6);">
      Authentic Indian Sweet Shop &mdash; Handcrafted Mithai &amp; Hot Snacks Daily
    </h1>

    <p style="color: #fce8cc; font-size: 15.5px; font-weight: 500; max-width: 820px; margin: 0 auto 26px auto; line-height: 1.6;">
      Serving the Tri-State from Oak Tree Road in Iselin, NJ since 2003. Pick up hot samosas and chaats to-go, or enjoy fresh artisan sweets shipped nationwide in insulated cold packs.
    </p>

    <!-- TRIAJE DE LOS 3 PILARES -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; max-width: 980px; margin: 0 auto 24px auto;">
      
      <a href="/indian-sweets/" style="display: flex; align-items: center; justify-content: flex-start; gap: 14px; background: #ffffff; padding: 12px 16px; border-radius: 10px; text-decoration: none; border: 2px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.25); min-height: 76px; box-sizing: border-box;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/394/btn_sweets_bg__81005.1789094378.350.350.jpg?c=2" alt="Order Sweets Online" style="width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37;" />
        <div style="text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25;">Order Sweets Online</div>
          <div style="color: #555; font-size: 12px; font-weight: 600; margin-top: 3px;">(USA Shipping)</div>
        </div>
      </a>

      <a href="/menu/" style="display: flex; align-items: center; justify-content: flex-start; gap: 14px; background: #ffffff; padding: 12px 16px; border-radius: 10px; text-decoration: none; border: 2px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.25); min-height: 76px; box-sizing: border-box;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/395/btn_takeout_bg__18527.1789094396.350.350.jpg?c=2" alt="Takeout & Pickup Menu" style="width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37;" />
        <div style="text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25;">Takeout &amp; Pickup Menu</div>
          <div style="color: #555; font-size: 12px; font-weight: 600; margin-top: 3px;">(Iselin Store)</div>
        </div>
      </a>

      <a href="/catering/" style="display: flex; align-items: center; justify-content: flex-start; gap: 14px; background: #ffffff; padding: 12px 16px; border-radius: 10px; text-decoration: none; border: 2px solid #ebdcc5; box-shadow: 0 4px 14px rgba(0,0,0,0.25); min-height: 76px; box-sizing: border-box;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/396/btn_catering_bg__82126.1789094396.350.350.jpg?c=2" alt="Wedding & Catering" style="width: 52px; height: 52px; border-radius: 8px; object-fit: cover; border: 1.5px solid #d4af37;" />
        <div style="text-align: left;">
          <div style="font-family: 'Marcellus', Georgia, serif; color: #6e101e; font-size: 15.5px; font-weight: 700; line-height: 1.25;">Wedding &amp; Catering</div>
          <div style="color: #555; font-size: 12px; font-weight: 600; margin-top: 3px;">(Tri-State)</div>
        </div>
      </a>

    </div>

    <!-- BADGES CONTACTO -->
    <div style="display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 12px; border-top: 1px solid rgba(212, 175, 55, 0.3); padding-top: 18px;">
      <div style="background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 6px; padding: 6px 14px; font-size: 13px; font-weight: 600; color: #ffd700; display: inline-flex; align-items: center; gap: 6px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        <span>1384 Oak Tree Rd, Iselin NJ &bull; Open Daily 10am&ndash;8pm</span>
      </div>
      <div style="background: rgba(0, 0, 0, 0.28); border: 1px solid rgba(212, 175, 55, 0.45); border-radius: 6px; padding: 6px 14px; font-size: 13px; font-weight: 600; color: #ffffff; display: inline-flex; align-items: center; gap: 6px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        <span>Store: <a href="tel:7322833799" style="color: #ffd700; text-decoration: underline; font-weight: 700;">(732) 283-3799</a></span>
      </div>
    </div>

  </div>

  <!-- ========================================================
       PARTE 2: FEATURED PRODUCTS (JUSTO DEBAJO DEL HERO)
       ======================================================== -->
  <div style="margin: 40px 0 50px 0;">
    <div style="text-align: center; margin-bottom: 25px;">
      <h2 style="font-size: 28px; color: #4a0e17; margin: 0 0 8px 0;">Featured Products</h2>
      <p style="color: #666; font-size: 14.5px; margin: 0;">Handcrafted daily in our Iselin kitchen &bull; Authentic recipes since 2003</p>
    </div>

    <!-- GRID DE FEATURED PRODUCTS -->
    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px;">
      
      <!-- 1. Gujia -->
      <div class="qs-product-card">
        <a href="/gujia/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/166/images/372/gujia__29512.1456187335.215.215.png?c=2" alt="Gujia" class="qs-product-img" /></a>
        <h3 class="qs-product-title"><a href="/gujia/" style="color: inherit; text-decoration: none;">Authentic Gujia</a></h3>
        <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
        <div class="qs-product-price">$8.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
        <a href="/gujia/" class="qs-btn-primary" style="padding: 8px 14px; font-size: 13px;">Choose Options</a>
      </div>

      <!-- 2. Jalebi -->
      <div class="qs-product-card">
        <a href="/jalebi/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/90/images/284/Jalebi__80913.1433725846.215.215.jpg?c=2" alt="Jalebi" class="qs-product-img" /></a>
        <h3 class="qs-product-title"><a href="/jalebi/" style="color: inherit; text-decoration: none;">Crispy Jalebi</a></h3>
        <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px;">&#9733;&#9733;&#9733;&#9733;&#9733; (5.0)</div>
        <div class="qs-product-price">$12.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
        <a href="/jalebi/" class="qs-btn-primary" style="padding: 8px 14px; font-size: 13px;">Add to Cart</a>
      </div>

      <!-- 3. Carrot Halwa -->
      <div class="qs-product-card">
        <a href="/carrot-halwa/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/93/images/288/Carrot_halwa__62877.1433729162.215.215.jpg?c=2" alt="Carrot Halwa" class="qs-product-img" /></a>
        <h3 class="qs-product-title"><a href="/carrot-halwa/" style="color: inherit; text-decoration: none;">Carrot Halwa (Gajar)</a></h3>
        <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.7)</div>
        <div class="qs-product-price">$7.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
        <a href="/carrot-halwa/" class="qs-btn-primary" style="padding: 8px 14px; font-size: 13px;">Choose Options</a>
      </div>

      <!-- 4. Red Chili Kaju -->
      <div class="qs-product-card">
        <a href="/red-chili-kaju/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/91/images/286/Red_Chilli_Cashews__50206.1433727938.215.215.jpg?c=2" alt="Red Chili Kaju" class="qs-product-img" /></a>
        <h3 class="qs-product-title"><a href="/red-chili-kaju/" style="color: inherit; text-decoration: none;">Spiced Red Chili Kaju</a></h3>
        <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px;">&#9733;&#9733;&#9733;&#9733;&#9733; (5.0)</div>
        <div class="qs-product-price">$16.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
        <a href="/red-chili-kaju/" class="qs-btn-primary" style="padding: 8px 14px; font-size: 13px;">Add to Cart</a>
      </div>

    </div>
  </div>

  <!-- ========================================================
       SECTION 3: HOT TAKEOUT COUNTER & STREET FOOD (ISELIN STORE)
       ======================================================== -->
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
      Prepared hot to order at our Oak Tree Road kitchen in Iselin, NJ. Our samosas are crafted daily with fresh hand-spiced potatoes, whole green peas, and crisp ajwain-infused dough&mdash;<strong>never frozen, fried strictly in clean 100% pure vegetable oil</strong>. Pair with our famous house-made tamarind and spicy mint chutneys or enjoy fresh street food specialties to-go:
    </p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; margin-bottom: 24px;">
      
      <!-- Card 1: Samosa & Papri Chaat -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/398/samosa_chaat_photo_1789098060133__20739.1789098260.350.350.jpg?c=2" alt="Samosa &amp; Papri Chaat" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Samosa &amp; Papri Chaat</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Crisp crushed samosas or papris layered with chilled spiced yogurt, fine crunchy sev, and house tamarind-mint chutneys.</span>
      </div>

      <!-- Card 2: Pani Puri Kits -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/399/pani_puri_photo_1789098074946__46127.1789098262.350.350.jpg?c=2" alt="Pani Puri Kits To-Go" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Pani Puri Kits To-Go</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Crispy hollow puris individually packed with seasoned potato-chickpea masala and freshly blended chilled mint-spiced water.</span>
      </div>

      <!-- Card 3: Hot Chole Bhatura -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/400/chole_bhatura_photo_1789098088650__70835.1789098264.350.350.jpg?c=2" alt="Hot Chole Bhatura" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Hot Chole Bhatura</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Two golden, fluffy puffed bhaturas served hot with rich slow-simmered Punjabi chickpea curry and pickled onions.</span>
      </div>

      <!-- Card 4: Aloo & Gobi Parathas -->
      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/401/stuffed_paratha_photo_1789098102913__76988.1789098265.350.350.jpg?c=2" alt="Aloo &amp; Gobi Parathas" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; display: block; margin-bottom: 6px;">Aloo &amp; Gobi Parathas</strong>
        <span style="font-size: 13px; color: #666; line-height: 1.5; display: block;">Griddled to perfection on traditional tawa with pure creamery butter and seasoned cauliflower or potato fillings.</span>
      </div>

    </div>

    <div style="display: flex; flex-wrap: wrap; gap: 12px;">
      <a href="/menu/" class="qs-btn-primary">View Full Iselin Takeout Menu &rarr;</a>
    </div>
  </div>

  <!-- ========================================================
       SECTION 4: ARTISAN SWEETS & COLD SHIPPING SYSTEM
       ======================================================== -->
  <div class="qs-section-box" style="border-left: 6px solid #d4af37;">
    <span style="color: #b38b1e; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">Express Delivery Across all 50 States</span>
    <h2 style="font-size: 26px; color: #4a0e17; margin: 4px 0 16px 0;">Artisan Indian Sweets Handcrafted Daily &amp; Shipped Nationwide</h2>
    
    <p style="font-size: 15px; line-height: 1.65; color: #444; margin-bottom: 22px;">
      Every morning in Iselin, New Jersey, our master confectioners boil pure whole farm milk for hours to create dense, aromatic khoya, grind premium whole cashews for silver-leaf Kaju Katli, and knead soft cottage cheese for tender Bengali Chum Chums. <strong>We never use chemical preservatives, artificial shelf-life extenders, or canned syrups.</strong>
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
        <span style="font-size: 13px; color: #666; line-height: 1.45;">Traditional Alwar-style caramelized grainy khoya fudge with subtle green cardamom.</span>
      </div>

      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; text-align: center;">
        <a href="/mango-sandesh/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/82/images/275/Mango_Sandesh__78298.1433712997.350.350.jpg?c=2" alt="Fresh Mango Sandesh" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" /></a>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; margin-bottom: 4px;"><a href="/mango-sandesh/" style="color: inherit; text-decoration: none;">Fresh Mango Sandesh</a></strong>
        <span style="font-size: 13px; color: #666; line-height: 1.45;">Melt-in-mouth Bengali chhena sweet blended with pure Alphonso mango pulp.</span>
      </div>

      <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; text-align: center;">
        <a href="/besan-ladoo/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/98/images/294/Besan_Ladoo__03878.1433732821.350.350.jpg?c=2" alt="Pure Besan Ladoo" style="width: 100%; height: 160px; object-fit: cover; border-radius: 6px; margin-bottom: 10px;" /></a>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16px; margin-bottom: 4px;"><a href="/besan-ladoo/" style="color: inherit; text-decoration: none;">Pure Besan Ladoo</a></strong>
        <span style="font-size: 13px; color: #666; line-height: 1.45;">Slow-roasted gram flour in 100% pure desi ghee with slivered California almonds.</span>
      </div>

    </div>

    <!-- 3 THERMAL PACKAGING STEPS -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin-bottom: 24px;">
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 18px;">
        <div style="width: 44px; height: 44px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #d4af37; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #4a0e17; font-size: 16px; display: block; margin-bottom: 6px;">1. Hermetic Freshness Seal</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Sweets are sealed immediately after morning preparation to lock in delicate moisture, natural aromas, and artisanal softness.</p>
      </div>
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 18px;">
        <div style="width: 44px; height: 44px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #d4af37; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2"><line x1="12" y1="2" x2="12" y2="22"></line><line x1="2" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line><line x1="19.07" y1="4.93" x2="4.93" y2="19.07"></line></svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #4a0e17; font-size: 16px; display: block; margin-bottom: 6px;">2. Food-Grade Cold Gel Packs</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Heavy-duty non-toxic refrigerant packs maintain a constant cool temperature throughout the nationwide shipping journey.</p>
      </div>
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 18px;">
        <div style="width: 44px; height: 44px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.15); border: 1.5px solid #d4af37; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #4a0e17; font-size: 16px; display: block; margin-bottom: 6px;">3. Multi-Layer Insulated Box</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Thermal barrier shield delivered via express carrier directly to your doorstep anywhere in the United States.</p>
      </div>
    </div>

    <a href="/indian-sweets/" class="qs-btn-gold">Shop All Sweets with Cold Shipping &rarr;</a>
  </div>

  <!-- SECTION 5: CURRENT TOP SELLERS (CAROUSEL MATCHING FEATURED PRODUCTS) -->
  <div id="qs-top-sellers-block">
    <div style="text-align: center; margin-bottom: 22px;">
      <h2 style="font-family: 'Marcellus', Georgia, serif; font-size: 28px; color: #4a0e17; margin: 0 0 8px 0; display: inline-flex; align-items: center; justify-content: center; gap: 14px;">
        <span style="display: inline-block; width: 45px; height: 1.5px; background: #d4af37;"></span>
        Current Top Sellers
        <span style="display: inline-block; width: 45px; height: 1.5px; background: #d4af37;"></span>
      </h2>
      <p style="color: #666; font-size: 14.5px; margin: 0;">Our most-ordered traditional sweets &bull; Shipped fresh nationwide in insulated cold packs</p>
    </div>

    <!-- PREV / NEXT NAVIGATION BUTTONS -->
    <button type="button" class="qs-ts-nav-btn qs-ts-prev" id="qs-ts-prev" aria-label="Previous Top Sellers">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </button>
    <button type="button" class="qs-ts-nav-btn qs-ts-next" id="qs-ts-next" aria-label="Next Top Sellers">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </button>

    <!-- OWL CAROUSEL TOP SELLERS (10 POPULAR PRODUCTS) -->
    <div class="ProductList owl-carousel" id="owl-top-sellers">
      
      <!-- 1. Kaju Katli -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/kaju-katli/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/77/images/308/Plain_Burfi__57958.1433826518.350.350.jpg?c=2" alt="Pure Kaju Katli" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/kaju-katli/" style="color: inherit; text-decoration: none;">Pure Kaju Katli</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
          <div class="qs-product-price">$9.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/kaju-katli/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 2. Motichur Ladoo -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/motichur-ladoo/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/104/images/299/Motichur_Ladoo__31599.1433801521.350.350.jpg?c=2" alt="Motichur Ladoo" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/motichur-ladoo/" style="color: inherit; text-decoration: none;">Motichur Ladoo</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
          <div class="qs-product-price">$6.50 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/motichur-ladoo/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 3. Khoya Pista Burfi -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/khoya-pista-burfi/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/113/images/309/Khoya_Pista_Burfi__02324.1433826917.350.350.jpg?c=2" alt="Khoya Pista Burfi" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/khoya-pista-burfi/" style="color: inherit; text-decoration: none;">Khoya Pista Burfi</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
          <div class="qs-product-price">$7.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/khoya-pista-burfi/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 4. Crispy Jalebi -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/jalebi/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/90/images/284/Jalebi__80913.1433725846.350.350.jpg?c=2" alt="Crispy Jalebi" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/jalebi/" style="color: inherit; text-decoration: none;">Crispy Jalebi</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (5.0)</div>
          <div class="qs-product-price">$12.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/jalebi/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Add to Cart</a>
        </div>
      </div>

      <!-- 5. Besan Ladoo -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/besan-ladoo/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/98/images/294/Besan_Ladoo__03878.1433732821.350.350.jpg?c=2" alt="Besan Ladoo" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/besan-ladoo/" style="color: inherit; text-decoration: none;">Besan Ladoo</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
          <div class="qs-product-price">$8.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/besan-ladoo/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 6. Milk Cake -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/milk-cake/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/105/images/301/Milk_Cake__92535.1433802617.350.350.jpg?c=2" alt="Rich Milk Cake" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/milk-cake/" style="color: inherit; text-decoration: none;">Rich Milk Cake</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
          <div class="qs-product-price">$7.50 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/milk-cake/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 7. Kala Jamun -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/kala-jamun/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/101/images/296/Kala_Jamoon__05636.1433734969.350.350.jpg?c=2" alt="Kala Jamun" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/kala-jamun/" style="color: inherit; text-decoration: none;">Kala Jamun</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
          <div class="qs-product-price">$7.50 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/kala-jamun/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 8. Malai Peda -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/malai-peda/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/86/images/331/Kadam_Keer__46637.1433875816.350.350.jpg?c=2" alt="Malai Peda" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/malai-peda/" style="color: inherit; text-decoration: none;">Malai Peda</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.7)</div>
          <div class="qs-product-price">$8.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/malai-peda/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 9. Pista Kaju Roll -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/kaju-roll/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/79/images/271/Kaju_Roll1__01965.1433603427.350.350.jpg?c=2" alt="Pista Kaju Roll" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/kaju-roll/" style="color: inherit; text-decoration: none;">Pista Kaju Roll</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.9)</div>
          <div class="qs-product-price">$8.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/kaju-roll/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
        </div>
      </div>

      <!-- 10. Malai Chum Chum -->
      <div class="item">
        <div class="qs-product-card">
          <a href="/malai-chum-chum/"><img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/84/images/351/MALAICHUM_CHUM__26837.1437440527.350.350.jpg?c=2" alt="Malai Chum Chum" class="qs-product-img" /></a>
          <h3 class="qs-product-title"><a href="/malai-chum-chum/" style="color: inherit; text-decoration: none;">Malai Chum Chum</a></h3>
          <div style="color: #d4af37; font-size: 13px; margin-bottom: 6px; letter-spacing: 1px;">&#9733;&#9733;&#9733;&#9733;&#9733; (4.8)</div>
          <div class="qs-product-price">$8.00 <span style="font-size: 12px; color: #888; font-weight: 400;">/ lb</span></div>
          <a href="/malai-chum-chum/" class="qs-btn-primary" style="margin-top: auto; padding: 9px 14px; font-size: 13px;">Choose Options</a>
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
      if (window.jQuery && typeof window.jQuery.fn.owlCarousel === 'function') {
        var $ = window.jQuery;
        var $owl = $("#owl-top-sellers");
        if ($owl.length && !$owl.data('owlCarousel')) {
          $owl.owlCarousel({
            items: 4,
            itemsDesktop: [1050, 4],
            itemsDesktopSmall: [970, 3],
            itemsTablet: [700, 2],
            itemsMobile: [480, 1],
            pagination: false,
            paginationNumbers: false,
            navigation: false,
            slideSpeed: 300
          });
          $("#qs-ts-next").off('click').on('click', function(e) {
            e.preventDefault();
            $owl.trigger('owl.next');
          });
          $("#qs-ts-prev").off('click').on('click', function(e) {
            e.preventDefault();
            $owl.trigger('owl.prev');
          });
        }
      } else {
        setTimeout(initTopSellersCarousel, 150);
      }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initTopSellersCarousel);
    } else {
      initTopSellersCarousel();
    }
  })();
  </script>

  <!-- SECTION 6: REGIONAL CATERING, WEDDINGS & MANDIRS TRI-STATE -->
  <div class="qs-section-box" style="border-left: 6px solid #4a0e17;">
    <span style="color: #7a1526; font-size: 12px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">B2B Services &bull; NJ, NY &amp; CT Tri-State Coverage</span>
    <h2 style="font-size: 26px; color: #4a0e17; margin: 4px 0 16px 0;">Authentic Mithai &amp; Samosa Catering for Weddings, Mandirs &amp; Events</h2>
    
    <p style="font-size: 15px; line-height: 1.65; color: #444; margin-bottom: 22px;">
      Whether you are celebrating a lavish Indian wedding reception in Manhattan, organizing a corporate Diwali gala in Jersey City, or requiring weekly pure prasad for your temple in Connecticut, Quality Sweets delivers uncompromised scale with authentic boutique flavor:
    </p>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px;">
      
      <!-- Catering Card 1: Wedding Gift Boxes -->
      <div style="padding: 16px; background: #fffdfa; border: 1px solid #ebdcc5; border-radius: 8px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/402/wedding_gift_box_1789098119353__27913.1789098267.350.350.jpg?c=2" alt="Wedding Sweet Boxes &amp; Return Gifts" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16.5px; display: block; margin-bottom: 6px;">Wedding Sweet Boxes &amp; Return Gifts</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Custom embossed gold luxury gift boxes with your choice of premium Kaju Katli, specialty burfis, and traditional ladoos.</p>
      </div>

      <!-- Catering Card 2: Temple Bulk Prasad -->
      <div style="padding: 16px; background: #fffdfa; border: 1px solid #ebdcc5; border-radius: 8px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/403/temple_bulk_prasad_1789098135260__33231.1789098269.350.350.jpg?c=2" alt="Temple &amp; Mandir Bulk Prasad" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16.5px; display: block; margin-bottom: 6px;">Temple &amp; Mandir Bulk Prasad</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Wholesale supply of Motichur Ladoo, Besan Ladoo, and Peda with direct bulk-per-pound rates for Hindu temples and religious gatherings.</p>
      </div>

      <!-- Catering Card 3: Bulk Samosa Trays -->
      <div style="padding: 16px; background: #fffdfa; border: 1px solid #ebdcc5; border-radius: 8px; display: flex; flex-direction: column;">
        <img src="https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/404/bulk_samosas_platter_1789098151834__74896.1789098270.350.350.jpg?c=2" alt="Bulk Fresh Samosa Trays" style="width: 100%; height: 175px; object-fit: cover; border-radius: 6px; margin-bottom: 12px;" />
        <strong style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 16.5px; display: block; margin-bottom: 6px;">Bulk Fresh Samosa Trays (50 - 1,000+ pcs)</strong>
        <p style="font-size: 13.5px; color: #555; line-height: 1.5; margin: 0;">Never-frozen hot samosa party platters delivered crisp for family gatherings, office catering, and community events.</p>
      </div>

    </div>

    <a href="/catering/" class="qs-btn-primary">Request Catering &amp; Bulk Quote &rarr;</a>
  </div>

  <!-- SECTION 7: QUALITY PROMISE & FRESHNESS GUARANTEE -->
  <div style="background: radial-gradient(circle at 50% 50%, #4a0e17 0%, #2e060c 100%); color: #ffffff; border-radius: 12px; padding: 36px 28px; margin-bottom: 30px; border: 1.5px solid #d4af37;">
    <div style="text-align: center; max-width: 800px; margin: 0 auto 28px auto;">
      <span style="color: #ffd700; font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase;">Tradition &bull; Purity &bull; Zero Shortcuts</span>
      <h2 style="font-size: 28px; color: #ffffff; margin: 6px 0 12px 0;">The Quality Sweets Standard: Pure Milk Khoya, Zero Compromises</h2>
      <p style="color: #fce8cc; font-size: 14.5px; line-height: 1.6;">We back every pound of sweets crafted in our kitchen with an unwavering purity commitment that has defined us on Oak Tree Road for over 20 years.</p>
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
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">No reconstituted milk powder, fillers, or artificial vegetable fats.</span>
      </div>

      <!-- Card 2: Zero Chemical Preservatives -->
      <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 10px; padding: 20px 16px; text-align: center; display: flex; flex-direction: column; align-items: center;">
        <div style="width: 52px; height: 52px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.18); border: 1.5px solid #ffd700; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            <path d="m9 12 2 2 4-4"></path>
          </svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #ffd700; display: block; margin-bottom: 6px;">Zero Chemical Preservatives</strong>
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">Honest shelf-life because we believe authentic mithai should always be real food.</span>
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
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">Dedicated pure vegetarian kitchen and preparation facility on Oak Tree Road.</span>
      </div>

      <!-- Card 4: 100% Freshness Guarantee -->
      <div style="background: rgba(255,255,255,0.08); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 10px; padding: 20px 16px; text-align: center; display: flex; flex-direction: column; align-items: center;">
        <div style="width: 52px; height: 52px; margin-bottom: 12px; background: rgba(212, 175, 55, 0.18); border: 1.5px solid #ffd700; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ffd700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="8" r="6"></circle>
            <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"></path>
          </svg>
        </div>
        <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #ffd700; display: block; margin-bottom: 6px;">100% Freshness Guarantee</strong>
        <span style="font-size: 13px; color: #f0e6d2; line-height: 1.45;">If your sweets do not arrive in pristine condition, we replace them immediately. Zero hassle.</span>
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
          No. Quality Sweets operates exclusively as a <strong>walk-in takeout counter and pickup shop</strong> with no dine-in seating. We prepare fresh hot samosas, chaats, street food, and pack fresh sweets by the pound to-go. We welcome customers to call ahead at <a href="tel:7322833799" style="color: #7a1526; font-weight: 700;">(732) 283-3799</a> to skip the waiting line.
        </div>
      </details>

      <details class="qs-faq-item">
        <summary>How do you ship delicate sweets like Chum Chum or Kaju Katli nationwide without spoiling?</summary>
        <div class="qs-faq-content">
          We pack our sweets using specialized insulated thermal containers combined with food-grade cold gel packs. Every order is prepared and dispatched via expedited carrier service to ensure your sweets arrive chilled, fresh, and in pristine condition across all 50 states.
        </div>
      </details>

      <details class="qs-faq-item">
        <summary>Do Quality Sweets products contain any chemical preservatives?</summary>
        <div class="qs-faq-content">
          Never. Since 2003, our founding principle has been uncompromised authenticity. We prepare our sweets daily using pure milk khoya, natural ghee, saffron, cardamom, and premium nuts with <strong>zero chemical preservatives or artificial shelf-life extenders</strong>.
        </div>
      </details>

      <details class="qs-faq-item">
        <summary>How much advance notice is required for wedding or temple bulk orders?</summary>
        <div class="qs-faq-content">
          For large custom wedding gift boxes or bulk samosa orders of 100+ pieces, we recommend placing your order 1 to 2 weeks in advance. For rush catering orders in the New Jersey, New York, and Connecticut tri-state area, please contact our catering desk directly by phone.
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

  <!-- FINAL STAGING ACTION CALLOUT -->
  <div style="text-align: center; background: #fff8e6; border: 1px solid #ebdcc5; border-radius: 8px; padding: 20px; margin: 30px 0;">
    <h3 style="color: #7a1526; margin: 0 0 6px 0; font-size: 19px;">What do you think of this homepage layout?</h3>
    <p style="color: #555; font-size: 14px; margin: 0 0 14px 0;">This private staging preview seamlessly unites the top hero banner, the active product catalog, and the 5 new SEO &amp; conversion sections.</p>
    <a href="https://qualitysweetsnj.com/" target="_blank" style="color: #7a1526; font-weight: 700; font-size: 13.5px; text-decoration: underline;">&larr; View current live homepage in production to compare</a>
  </div>

</div>
"""

payload = {
    "name": "Preview Home Staging",
    "type": "page",
    "url": "/preview-home-staging/",
    "body": body_html,
    "is_visible": False,  # Oculta de los menús
    "meta_title": "Preview Home Staging | Quality Sweets",
    "meta_description": "Private staging preview of the new Quality Sweets homepage."
}

# Comprobar si ya existe la página
req_list = urllib.request.Request(f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages", headers=headers)
with urllib.request.urlopen(req_list) as res:
    pages = json.loads(res.read().decode())

existing_page_id = None
for p in pages:
    if p.get("url") == "/preview-home-staging/":
        existing_page_id = p.get("id")
        break

if existing_page_id:
    print(f"Página existente encontrada (ID: {existing_page_id}). Actualizando...")
    req = urllib.request.Request(
        f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages/{existing_page_id}",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="PUT"
    )
else:
    print("Creando nueva página privada /preview-home-staging/...")
    req = urllib.request.Request(
        f"https://api.bigcommerce.com/stores/{store_hash}/v2/pages",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )

try:
    with urllib.request.urlopen(req) as res:
        result = json.loads(res.read().decode())
        print(f"SUCCESS: Page ID {result.get('id')}")
        print(f"URL: https://qualitysweetsnj.com{result.get('url')}")
except Exception as e:
    print(f"ERROR: {e}")
