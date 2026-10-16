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

const scriptHtml = `<script id="qs-pdp-shipping-transit-script">
(function() {
  function injectShippingWidget() {
    // Only run on Product Detail Pages
    var form = document.getElementById('productDetailsAddToCartForm');
    if (!form) return;
    if (document.getElementById('qs-pdp-shipping-widget')) return;

    var container = document.createElement('div');
    container.id = 'qs-pdp-shipping-widget';
    container.style.cssText = 'margin: 18px 0 14px 0; background: #fdfbf7; border: 1.5px solid #ebdcc5; border-radius: 10px; padding: 14px 16px; font-family: "Plus Jakarta Sans", sans-serif; box-sizing: border-box;';

    container.innerHTML = [
      '<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid rgba(212, 175, 55, 0.3);">',
      '  <div style="display: flex; align-items: center; gap: 8px; color: #7a1526; font-family: \\'Marcellus\\', Georgia, serif; font-size: 15.5px; font-weight: 700;">',
      '    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7a1526" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>',
      '    <span>Nationwide Delivery &bull; FedEx Transit Schedule</span>',
      '  </div>',
      '  <span style="background: rgba(212, 175, 55, 0.2); border: 1px solid #d4af37; color: #6e101e; font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px;">Cold-Pack Insulated</span>',
      '</div>',
      '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin-bottom: 12px; font-size: 12px; color: #4a0e17;">',
      '  <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 6px; padding: 7px 9px;">',
      '    <strong style="color: #e6007e; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.3px;">Tri-State Core</strong>',
      '    <span>1 Day (NJ, NY, CT, PA)</span>',
      '  </div>',
      '  <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 6px; padding: 7px 9px;">',
      '    <strong style="color: #008fa0; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.3px;">Midwest &amp; South</strong>',
      '    <span>2 Days Delivery</span>',
      '  </div>',
      '  <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 6px; padding: 7px 9px;">',
      '    <strong style="color: #d97706; display: block; font-size: 11px; text-transform: uppercase; letter-spacing: 0.3px;">Texas &amp; West</strong>',
      '    <span>3 to 5 Days</span>',
      '  </div>',
      '</div>',
      '<button type="button" id="qs-btn-toggle-transit-map" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; background: #ffffff; border: 1.5px solid #d4af37; color: #7a1526; font-family: \\'Plus Jakarta Sans\\', sans-serif; font-size: 13px; font-weight: 700; padding: 9px 14px; border-radius: 6px; cursor: pointer; transition: all 0.2s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">',
      '  <span>📍 View FedEx Transit Map &amp; Delivery Days</span>',
      '  <span id="qs-map-arrow" style="font-size: 11px; transition: transform 0.2s ease;">▼</span>',
      '</button>',
      '<div id="qs-pdp-map-drawer" style="display: none; margin-top: 14px; padding-top: 14px; border-top: 1px dashed #ebdcc5; text-align: center;">',
      '  <div style="background: #ffffff; border: 1px solid #ebdcc5; border-radius: 8px; padding: 10px; margin-bottom: 10px;">',
      '    <img src="${mapUrl}" alt="FedEx Ground Transit Schedule Map Quality Sweets" style="width: 100%; height: auto; max-width: 480px; display: block; margin: 0 auto; border-radius: 4px;" loading="lazy" />',
      '  </div>',
      '  <p style="font-size: 12px; color: #555; line-height: 1.5; margin: 0 0 8px 0; text-align: left;">',
      '    📅 <strong>Dispatch Schedule:</strong> Orders ship <strong>Monday through Wednesday</strong> via FedEx Ground to ensure sweets arrive fresh without weekend transit holds. Made daily with 0 chemical preservatives.',
      '  </p>',
      '  <div style="text-align: right;">',
      '    <a href="/shipping-refunds/" target="_blank" style="color: #7a1526; font-size: 12.5px; font-weight: 700; text-decoration: underline;">Open Full Shipping Policy &rarr;</a>',
      '  </div>',
      '</div>'
    ].join('\\n');

    // Insert after form or inside .addto
    var addto = form.querySelector('.addto');
    if (addto && addto.parentNode) {
      addto.parentNode.insertBefore(container, addto.nextSibling);
    } else {
      form.appendChild(container);
    }

    // Add toggle behavior
    var toggleBtn = document.getElementById('qs-btn-toggle-transit-map');
    var drawer = document.getElementById('qs-pdp-map-drawer');
    var arrow = document.getElementById('qs-map-arrow');
    if (toggleBtn && drawer && arrow) {
      toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        var isOpen = drawer.style.display !== 'none';
        drawer.style.display = isOpen ? 'none' : 'block';
        arrow.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
        toggleBtn.style.background = isOpen ? '#ffffff' : '#f4eee4';
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectShippingWidget, { once: true });
  } else {
    injectShippingWidget();
  }
  window.addEventListener('load', injectShippingWidget, { once: true });
})();
</script>`;

async function deployPdpScript() {
  // Check if existing script exists
  const listRes = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/content/scripts`, {
    headers: { 'X-Auth-Token': token, 'Accept': 'application/json' }
  });
  const listJson = await listRes.json();
  const existing = (listJson.data || []).find(s => s.name === 'Quality Sweets Product Shipping Transit Map');

  const scriptPayload = {
    name: 'Quality Sweets Product Shipping Transit Map',
    description: 'Displays nationwide delivery transit widget and collapsible FedEx schedule map on all Product Detail Pages.',
    html: scriptHtml,
    location: 'footer',
    visibility: 'storefront',
    kind: 'script_tag',
    load_method: 'default',
    consent_category: 'essential',
    enabled: true,
    channel_id: 1
  };

  let res;
  if (existing) {
    console.log('Updating existing script UUID:', existing.uuid);
    res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/content/scripts/${existing.uuid}`, {
      method: 'PUT',
      headers: {
        'X-Auth-Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(scriptPayload)
    });
  } else {
    console.log('Creating new script...');
    res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/content/scripts`, {
      method: 'POST',
      headers: {
        'X-Auth-Token': token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(scriptPayload)
    });
  }

  const result = await res.json();
  console.log('Script deployment status:', res.status);
  console.log('Result UUID:', result.data ? result.data.uuid : result);
}

deployPdpScript().catch(console.error);
