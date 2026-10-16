const fs = require('fs');

const env = {};
if (fs.existsSync('.env')) {
  fs.readFileSync('.env', 'utf8').split('\n').forEach(line => {
    const parts = line.trim().split('=');
    if (parts.length >= 2 && !parts[0].startsWith('#')) {
      env[parts[0].trim()] = parts.slice(1).join('=').trim().replace(/^['"]|['"]$/g, '');
    }
  });
}

const storeHash = env.BIGCOMMERCE_STORE_HASH || process.env.BIGCOMMERCE_STORE_HASH;
const token = env.BIGCOMMERCE_ACCESS_TOKEN || process.env.BIGCOMMERCE_ACCESS_TOKEN;

const mapUrl = "https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/419/fedex_ground_transit_map_nj__73504.1792114202.1280.1280.png?c=2";

const shippingPageHtml = `
<div id="qs-shipping-page-wrapper" style="max-width: 1040px; margin: 0 auto; padding: 10px 0 40px 0; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #2e060c; line-height: 1.65;">
  
  <!-- HERO BANNER -->
  <div style="background: radial-gradient(circle at 50% 20%, #881628 0%, #540c17 65%, #35050d 100%); color: #ffffff; border-radius: 14px; padding: 36px 24px; text-align: center; border: 2px solid #d4af37; box-shadow: 0 10px 30px rgba(53, 5, 13, 0.25); margin-bottom: 30px;">
    <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; background: rgba(212, 175, 55, 0.15); border: 1px solid #d4af37; color: #ffd700; font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; padding: 6px 18px; border-radius: 50px; margin-bottom: 16px;">
      <span>Fast Nationwide Shipping &bull; Insulated Cold Packs &bull; Made Fresh Daily</span>
    </div>
    <h1 style="font-family: 'Marcellus', Georgia, serif; font-size: 32px; font-weight: 400; color: #ffffff; margin: 0 0 12px 0; letter-spacing: 0.3px; text-shadow: 0 2px 8px rgba(0,0,0,0.5);">
      Shipping Policy &amp; Delivery Schedule
    </h1>
    <p style="color: #fce8cc; font-size: 15.5px; max-width: 780px; margin: 0 auto; line-height: 1.6;">
      At Quality Sweets, all our traditional Indian mithai and Bengali sweets are handcrafted daily in Iselin, NJ with <strong>zero chemical preservatives</strong>. To ensure peak freshness, we ship orders across the continental United States in insulated cold-pack packaging via FedEx.
    </p>
  </div>

  <!-- 4 TRUST PILLARS (CLEAN SVGS - NO EMOJIS) -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 35px;">
    
    <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 10px; padding: 20px 16px; text-align: center;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#e6007e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto 10px auto; display: block;"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>
      <div style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #7a1526; font-weight: 700; margin-bottom: 6px;">1-Day Tri-State Delivery</div>
      <div style="font-size: 13px; color: #666;">Next-day arrival for most of NJ, NYC Metro, CT, Eastern PA, DE &amp; MD.</div>
    </div>

    <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 10px; padding: 20px 16px; text-align: center;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#008fa0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto 10px auto; display: block;"><path d="m10 20-1.25-2.5-2.5 1.25"/><path d="M14 20l1.25-2.5 2.5 1.25"/><path d="M17.5 15l2.5 1.25-1.25 2.5"/><path d="m2 12 20 0"/><path d="m20 10 1.25-2.5-2.5-1.25"/><path d="m16 4-1.25 2.5-2.5-1.25"/><path d="m12 2 0 20"/><path d="m8 4 1.25 2.5 2.5-1.25"/><path d="m4 10-1.25-2.5 2.5-1.25"/><path d="m4 14-1.25 2.5 2.5 1.25"/></svg>
      <div style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #7a1526; font-weight: 700; margin-bottom: 6px;">Insulated Cold-Packs</div>
      <div style="font-size: 13px; color: #666;">Silver thermal barrier liners and food-safe frozen gel packs preserve freshness.</div>
    </div>

    <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 10px; padding: 20px 16px; text-align: center;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto 10px auto; display: block;"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"></rect><line x1="16" x2="16" y1="2" y2="6"></line><line x1="8" x2="8" y1="2" y2="6"></line><line x1="3" x2="21" y1="10" y2="10"></line></svg>
      <div style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #7a1526; font-weight: 700; margin-bottom: 6px;">Mon&ndash;Wed Dispatch</div>
      <div style="font-size: 13px; color: #666;">We ship early in the week so sweets never sit in transit depots over the weekend.</div>
    </div>

    <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 10px; padding: 20px 16px; text-align: center;">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#2e7d32" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin: 0 auto 10px auto; display: block;"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
      <div style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #7a1526; font-weight: 700; margin-bottom: 6px;">Zero Preservatives</div>
      <div style="font-size: 13px; color: #666;">100% pure vegetarian, artisanal Indian sweets made fresh every single morning.</div>
    </div>

  </div>

  <!-- MAIN TRANSIT MAP & SCHEDULE SECTION -->
  <div style="background: #ffffff; border: 2px solid #ebdcc5; border-radius: 14px; padding: 28px 24px; box-shadow: 0 4px 18px rgba(0,0,0,0.06); margin-bottom: 35px;">
    
    <div style="text-align: center; margin-bottom: 24px;">
      <h2 style="font-family: 'Marcellus', Georgia, serif; font-size: 25px; color: #7a1526; margin: 0 0 10px 0;">
        FedEx Ground &amp; Home Delivery Schedule
      </h2>
      <p style="font-size: 14.5px; color: #555; max-width: 740px; margin: 0 auto;">
        Locate your state on the official FedEx transit map below to see your estimated delivery timeframe from our Iselin, NJ facility.
      </p>
    </div>

    <!-- MAP CONTAINER -->
    <div style="text-align: center; margin: 0 auto 28px auto; max-width: 820px; background: #faf8f5; border: 1px solid #ebdcc5; border-radius: 10px; padding: 16px;">
      <img src="${mapUrl}" alt="FedEx Ground Transit Schedule Map - Quality Sweets Iselin NJ" style="width: 100%; height: auto; max-width: 780px; display: block; margin: 0 auto; border-radius: 6px;" />
    </div>

    <!-- SCHEDULE BREAKDOWN TABLE & EXPLANATION -->
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 20px; align-items: start;">
      
      <!-- ZONE BREAKDOWN -->
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 10px; padding: 20px;">
        <h3 style="font-family: 'Marcellus', Georgia, serif; font-size: 18px; color: #7a1526; margin: 0 0 14px 0;">
          Transit Time by Region
        </h3>
        <ul style="list-style: none; padding: 0; margin: 0; font-size: 13.5px; line-height: 1.8;">
          <li style="margin-bottom: 10px; padding-left: 24px; position: relative;">
            <span style="position: absolute; left: 0; top: 3px; width: 14px; height: 14px; background: #e6007e; border-radius: 3px; display: inline-block;"></span>
            <strong>1 Day (Pink):</strong> New Jersey, NYC Metro, Connecticut, Eastern Pennsylvania, Delaware, Maryland.
          </li>
          <li style="margin-bottom: 10px; padding-left: 24px; position: relative;">
            <span style="position: absolute; left: 0; top: 3px; width: 14px; height: 14px; background: #00d2e6; border-radius: 3px; display: inline-block;"></span>
            <strong>2 Days (Cyan):</strong> Western PA, Ohio, Indiana, Illinois, Michigan, Virginia, North Carolina, South Carolina, Georgia, Florida, Upstate NY, Massachusetts, Rhode Island.
          </li>
          <li style="margin-bottom: 10px; padding-left: 24px; position: relative;">
            <span style="position: absolute; left: 0; top: 3px; width: 14px; height: 14px; background: #ff8c00; border-radius: 3px; display: inline-block;"></span>
            <strong>3 Days (Orange):</strong> Texas, Missouri, Iowa, Wisconsin, Minnesota, Kansas, Oklahoma, Nebraska, North &amp; South Dakota.
          </li>
          <li style="padding-left: 24px; position: relative;">
            <span style="position: absolute; left: 0; top: 3px; width: 14px; height: 14px; background: #00cc00; border-radius: 3px; display: inline-block;"></span>
            <strong>4&ndash;5 Days (Green/Purple):</strong> Western States (Colorado, Arizona, California, Washington, Oregon, Nevada, Utah). <em>*Express shipping recommended for heat-sensitive items.</em>
          </li>
        </ul>
      </div>

      <!-- DISPATCH RULES -->
      <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 10px; padding: 20px;">
        <h3 style="font-family: 'Marcellus', Georgia, serif; font-size: 18px; color: #7a1526; margin: 0 0 14px 0;">
          Weekly Dispatch Schedule
        </h3>
        <p style="font-size: 13.5px; color: #555; margin-bottom: 12px;">
          Because our sweets are made without artificial preservatives, we avoid weekend warehouse holds:
        </p>
        <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 6px; overflow: hidden; font-size: 13px;">
          <div style="display: flex; background: #7a1526; color: #ffffff; font-weight: 700; padding: 8px 12px;">
            <span style="flex: 1;">Order Dispatched</span>
            <span style="flex: 1; text-align: right;">Delivery Days (1-3 Days)</span>
          </div>
          <div style="display: flex; padding: 8px 12px; border-bottom: 1px solid #ebdcc5;">
            <span style="flex: 1;"><strong>Monday</strong></span>
            <span style="flex: 1; text-align: right; color: #7a1526; font-weight: 600;">Tuesday &ndash; Thursday</span>
          </div>
          <div style="display: flex; padding: 8px 12px; border-bottom: 1px solid #ebdcc5; background: #faf8f5;">
            <span style="flex: 1;"><strong>Tuesday</strong></span>
            <span style="flex: 1; text-align: right; color: #7a1526; font-weight: 600;">Wednesday &ndash; Friday</span>
          </div>
          <div style="display: flex; padding: 8px 12px;">
            <span style="flex: 1;"><strong>Wednesday</strong></span>
            <span style="flex: 1; text-align: right; color: #7a1526; font-weight: 600;">Thursday &ndash; Friday</span>
          </div>
        </div>
        <p style="font-size: 12px; color: #777; margin-top: 10px; font-style: italic;">
          *Orders placed Wednesday afternoon through Sunday are freshly packed and dispatched first thing on Monday.
        </p>
      </div>

    </div>

  </div>

  <!-- FRESHNESS & STORAGE GUIDELINES (SVGS - NO EMOJIS) -->
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 20px; margin-bottom: 35px;">
    
    <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 12px; padding: 22px; box-shadow: 0 2px 10px rgba(0,0,0,0.04);">
      <h3 style="font-family: 'Marcellus', Georgia, serif; font-size: 18px; color: #7a1526; margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#008fa0" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m10 20-1.25-2.5-2.5 1.25"/><path d="M14 20l1.25-2.5 2.5 1.25"/><path d="M17.5 15l2.5 1.25-1.25 2.5"/><path d="m2 12 20 0"/><path d="m20 10 1.25-2.5-2.5-1.25"/><path d="m16 4-1.25 2.5-2.5-1.25"/><path d="m12 2 0 20"/><path d="m8 4 1.25 2.5 2.5-1.25"/><path d="m4 10-1.25-2.5 2.5-1.25"/><path d="m4 14-1.25 2.5 2.5 1.25"/></svg>
        <span>How We Package Your Sweets</span>
      </h3>
      <p style="font-size: 13.5px; color: #555; line-height: 1.6; margin: 0 0 10px 0;">
        Every box is prepared by our master confectioners on the day of dispatch. We pack your sweets inside food-grade airtight containers, wrap them in specialized reflective thermal insulation, and surround them with non-toxic frozen ice gel packs.
      </p>
      <p style="font-size: 13.5px; color: #555; line-height: 1.6; margin: 0;">
        This proprietary packaging maintains an optimal cool environment for up to 48&ndash;72 hours in transit.
      </p>
    </div>

    <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 12px; padding: 22px; box-shadow: 0 2px 10px rgba(0,0,0,0.04);">
      <h3 style="font-family: 'Marcellus', Georgia, serif; font-size: 18px; color: #7a1526; margin: 0 0 10px 0; display: flex; align-items: center; gap: 8px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/><path d="M6 2v20"/><path d="M3 2v6a3 3 0 0 0 6 0V2"/></svg>
        <span>Care &amp; Storage Upon Delivery</span>
      </h3>
      <p style="font-size: 13.5px; color: #555; line-height: 1.6; margin: 0 0 10px 0;">
        Please open your package as soon as it arrives. Transfer all fresh milk and cottage-cheese based sweets (such as Rasgulla, Chum Chum, Sandesh, Kalakand and Peda) directly into the refrigerator.
      </p>
      <p style="font-size: 13.5px; color: #555; line-height: 1.6; margin: 0;">
        For the best authentic taste and texture, bring sweets to room temperature 15 minutes before serving. Enjoy within 5&ndash;7 days of delivery.
      </p>
    </div>

  </div>

  <!-- REFUND & REPLACEMENT POLICY -->
  <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 12px; padding: 24px; margin-bottom: 35px;">
    <h3 style="font-family: 'Marcellus', Georgia, serif; font-size: 20px; color: #7a1526; margin: 0 0 10px 0;">
      Our 100% Freshness Guarantee &amp; Refund Policy
    </h3>
    <p style="font-size: 14px; color: #555; line-height: 1.65; margin: 0 0 12px 0;">
      We take immense pride in every box of mithai that leaves our store. Because our products are perishable food items made fresh daily without preservatives, <strong>we cannot accept physical returns</strong> once food items have shipped.
    </p>
    <p style="font-size: 14px; color: #555; line-height: 1.65; margin: 0 0 12px 0;">
      However, if your order arrives damaged, spoiled due to carrier delay, or incorrect, please notify us within <strong>24 hours of delivery</strong> with photos of the package and items. We will gladly issue an immediate replacement or full refund.
    </p>
    <p style="font-size: 14px; color: #7a1526; font-weight: 600; margin: 0;">
      Customer Support: <a href="mailto:orders@qualitysweetsnj.com" style="color: #7a1526; text-decoration: underline;">orders@qualitysweetsnj.com</a> &bull; Phone: <a href="tel:7322833799" style="color: #7a1526; text-decoration: underline;">(732) 283-3799</a>
    </p>
  </div>

  <!-- BOTTOM CALL TO ACTION -->
  <div style="text-align: center; padding: 10px 0;">
    <a href="/indian-sweets/" style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; background: #7a1526; color: #ffffff; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 15px; font-weight: 700; padding: 14px 32px; border-radius: 8px; text-decoration: none; box-shadow: 0 4px 15px rgba(122, 21, 38, 0.35); transition: background 0.2s;">
      <span>Explore All Fresh Indian Sweets Online &rarr;</span>
    </a>
  </div>

</div>
`;

async function updateShippingPage() {
  const payload = {
    name: "Shipping & Refunds",
    meta_title: "Shipping & Delivery Policy | Fresh Mithai Shipped Nationwide | Quality Sweets",
    meta_description: "Quality Sweets shipping policy, FedEx Ground transit schedule map from Iselin NJ, insulated cold-pack packaging, and nationwide delivery details.",
    search_keywords: "quality sweets shipping, mithai shipping fedex, indian sweets nationwide delivery, fresh sweets delivery schedule",
    is_visible: true,
    body: shippingPageHtml
  };

  const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/content/pages/2`, {
    method: 'PUT',
    headers: {
      'X-Auth-Token': token,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const json = await res.json();
  console.log('Update page 2 status:', res.status);
}

updateShippingPage().catch(console.error);
