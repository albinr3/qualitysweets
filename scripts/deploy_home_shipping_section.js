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

async function updateHomeBanner() {
  // 1. Fetch current banner 5
  const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/banners/5`, {
    headers: { 'X-Auth-Token': token, 'Accept': 'application/json' }
  });
  const banner = await res.json();
  const currentContent = banner.content;

  // 2. Backup current content
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  if (!fs.existsSync('scripts/backups')) fs.mkdirSync('scripts/backups', { recursive: true });
  fs.writeFileSync(`scripts/backups/banner-5-before-shipping-map-${timestamp}.json`, JSON.stringify(banner, null, 2));
  console.log(`Backup saved to scripts/backups/banner-5-before-shipping-map-${timestamp}.json`);

  // 3. Define the Shipping Section HTML to sit right above Featured Products
  const shippingSectionHtml = `
  <!-- BLOQUE 3: SECCIÓN DE ENVÍOS NACIONALES & MAPA DE TRÁNSITO FEDEX (ENCIMA DE FEATURED PRODUCTS) -->
  <div id="qs-home-shipping-section" style="background: #ffffff; border: 2px solid #ebdcc5; border-radius: 12px; margin-top: 24px; padding: 26px 22px; box-shadow: 0 4px 18px rgba(0,0,0,0.06); font-family: 'Plus Jakarta Sans', sans-serif;">
    
    <div style="text-align: center; margin-bottom: 22px;">
      <div style="display: inline-flex; align-items: center; justify-content: center; gap: 6px; background: rgba(136, 22, 40, 0.08); border: 1px solid rgba(136, 22, 40, 0.2); color: #881628; font-size: 11.5px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; padding: 5px 14px; border-radius: 50px; margin-bottom: 10px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#881628" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>
        <span>Nationwide Fresh Delivery &bull; Insulated Cold-Packs</span>
      </div>
      <h2 style="font-family: 'Marcellus', Georgia, serif; color: #7a1526; font-size: 26px; font-weight: 400; margin: 0 0 8px 0; letter-spacing: 0.3px;">
        When Will Your Fresh Sweets Arrive?
      </h2>
      <p style="color: #666; font-size: 14.5px; max-width: 720px; margin: 0 auto; line-height: 1.5;">
        Handcrafted daily in Iselin, NJ with <strong>zero preservatives</strong>. We dispatch orders <strong>Monday through Wednesday</strong> via FedEx Ground to ensure fast, weekend-free transit straight to your doorstep.
      </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; align-items: center;">
      
      <!-- MAP IMAGE CONTAINER -->
      <div style="background: #faf8f5; border: 1.5px solid #ebdcc5; border-radius: 10px; padding: 14px; text-align: center;">
        <a href="/shipping-refunds/" title="Click to view full shipping details and schedule" style="display: block; text-decoration: none;">
          <img src="${mapUrl}" alt="Quality Sweets FedEx Ground Transit Schedule Map from Iselin NJ" width="800" height="710" loading="lazy" decoding="async" style="width: 100%; height: auto; max-width: 480px; display: block; margin: 0 auto; border-radius: 6px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);" />
        </a>
        <div style="margin-top: 10px; font-size: 12px; color: #777;">
          <span><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: -2px; display: inline-block; margin-right: 2px;"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg> Origin: Iselin, NJ (08830) &bull; <a href="/shipping-refunds/" style="color: #7a1526; font-weight: 700; text-decoration: underline;">Click to open full shipping policy</a></span>
        </div>
      </div>

      <!-- TRANSIT SUMMARY & CTA -->
      <div style="display: flex; flex-direction: column; justify-content: center; gap: 14px;">
        
        <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px 16px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <span style="display: inline-block; width: 14px; height: 14px; background: #e6007e; border-radius: 3px; flex-shrink: 0;"></span>
            <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #4a0e17;">1-Day Transit (Tri-State Core)</strong>
          </div>
          <p style="font-size: 13px; color: #555; margin: 0; line-height: 1.5;">
            New Jersey, NYC Metro, Connecticut, Eastern Pennsylvania, Delaware &amp; Maryland arrive the very next business day!
          </p>
        </div>

        <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px 16px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <span style="display: inline-block; width: 14px; height: 14px; background: #00d2e6; border-radius: 3px; flex-shrink: 0;"></span>
            <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #4a0e17;">2-Day Transit (Midwest, South &amp; East)</strong>
          </div>
          <p style="font-size: 13px; color: #555; margin: 0; line-height: 1.5;">
            Ohio, Indiana, Illinois, Michigan, Virginia, North &amp; South Carolina, Georgia, Florida, and Massachusetts.
          </p>
        </div>

        <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px 16px;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
            <span style="display: inline-block; width: 14px; height: 14px; background: #ff8c00; border-radius: 3px; flex-shrink: 0;"></span>
            <strong style="font-family: 'Marcellus', Georgia, serif; font-size: 16px; color: #4a0e17;">3 to 5 Days (Texas &amp; West Coast)</strong>
          </div>
          <p style="font-size: 13px; color: #555; margin: 0; line-height: 1.5;">
            Texas, Midwest Plains (3 days), California &amp; West Coast (4-5 days) with protective temperature-controlled silver barrier wrap.
          </p>
        </div>

        <!-- ACTION BUTTONS -->
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 6px;">
          <a href="/shipping-refunds/" style="flex: 1 1 180px; text-align: center; background: #7a1526; color: #ffffff; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13.5px; font-weight: 700; padding: 11px 18px; border-radius: 6px; text-decoration: none; box-shadow: 0 3px 10px rgba(122, 21, 38, 0.25); transition: background 0.2s;">
            View Delivery Schedule &rarr;
          </a>
          <a href="/indian-sweets/" style="flex: 1 1 180px; text-align: center; background: #d4af37; color: #2e060c; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13.5px; font-weight: 800; padding: 11px 18px; border-radius: 6px; text-decoration: none; box-shadow: 0 3px 10px rgba(212, 175, 55, 0.25); transition: background 0.2s;">
            Order Sweets Online &rarr;
          </a>
        </div>

      </div>

    </div>

  </div>
`;

  // 4. Check if section already exists
  let newContent = currentContent;
  if (newContent.includes('qs-home-shipping-section')) {
    console.log('Replacing existing qs-home-shipping-section in banner 5');
    newContent = newContent.replace(/<!-- BLOQUE 3: SECCIÓN DE ENVÍOS NACIONALES[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/, shippingSectionHtml);
  } else {
    // Insert right before the closing </div> of #qs-hero-wrapper
    // Notice in scratch/banner_5_content.html:
    // ... <!-- TARJETA 3 ... </div> </div> </div> <script id="qs-footer-nap">
    const targetPattern = '<!-- TARJETA 3: MITHAI BOXES & GIFT BASKETS -->';
    const targetIdx = newContent.indexOf(targetPattern);
    if (targetIdx !== -1) {
      // Find the closing </div> of the cards grid, then insert before the closing of #qs-hero-wrapper
      // Or search for '<script id="qs-footer-nap">'
      const scriptIdx = newContent.indexOf('<script id="qs-footer-nap">');
      if (scriptIdx !== -1) {
        // Find the </div> just before the script
        const beforeScript = newContent.slice(0, scriptIdx);
        const lastDivIdx = beforeScript.lastIndexOf('</div>');
        if (lastDivIdx !== -1) {
          // Insert inside #qs-hero-wrapper right before its closing tag
          newContent = beforeScript.slice(0, lastDivIdx) + shippingSectionHtml + '\n' + beforeScript.slice(lastDivIdx) + newContent.slice(scriptIdx);
          console.log('Inserted shippingSectionHtml inside #qs-hero-wrapper before its closing tag');
        } else {
          newContent = beforeScript + shippingSectionHtml + newContent.slice(scriptIdx);
        }
      } else {
        newContent = newContent + shippingSectionHtml;
      }
    } else {
      console.error('Target pattern not found in banner 5 content');
      return;
    }
  }

  // 5. Update banner 5
  const updatePayload = {
    name: banner.name,
    content: newContent,
    page: banner.page,
    location: banner.location,
    date_type: banner.date_type,
    visible: banner.visible
  };

  const updateRes = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/banners/5`, {
    method: 'PUT',
    headers: {
      'X-Auth-Token': token,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(updatePayload)
  });

  const updateJson = await updateRes.json();
  console.log('Banner 5 update status:', updateRes.status);
  console.log('Updated banner name:', updateJson.name, '| visible:', updateJson.visible);
}

updateHomeBanner().catch(console.error);
