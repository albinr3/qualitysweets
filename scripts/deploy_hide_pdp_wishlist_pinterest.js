import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const envPath = path.join(ROOT, ".env");

const env = {};
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const idx = trimmed.indexOf("=");
    env[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim().replace(/^['"]|['"]$/g, "");
  }
}

const storeHash = env.BIGCOMMERCE_STORE_HASH || process.env.BIGCOMMERCE_STORE_HASH;
const token = env.BIGCOMMERCE_ACCESS_TOKEN || process.env.BIGCOMMERCE_ACCESS_TOKEN;

if (!storeHash || !token) {
  console.error("Missing BIGCOMMERCE_STORE_HASH or BIGCOMMERCE_ACCESS_TOKEN.");
  process.exit(1);
}

const hideWishlistPinterestScript = `
<!-- QUALITY SWEETS - PDP HIDE WISHLIST & PINTEREST BUTTONS -->
<script id="qs-pdp-hide-wishlist-pinterest">
(function() {
  function removeUnwantedButtons() {
    var isPdp = document.body.classList.contains('productPage') || 
                document.getElementById('productDetailsAddToCartForm') ||
                document.querySelector('.ProductMain');
    if (!isPdp) return;

    // 1. Remove Wishlist buttons and forms on PDP
    var wishlistEls = document.querySelectorAll(
      '#SideProductAddToWishList, .AddToWishlistLink, .wishTrigger, .wishlist-button, form#frmWishList'
    );
    wishlistEls.forEach(function(el) {
      if (el && el.parentNode) el.parentNode.removeChild(el);
    });

    // 2. Remove Pinterest containers, buttons, and iframes
    var pinterestEls = document.querySelectorAll(
      '.PinterestButtonContainer, a[href*="pinterest.com/pin/create/button"], [data-pin-do="buttonPin"], [data-pin-log="button_save"], span[data-pin-save="true"], iframe[src*="pinterest.com"]'
    );
    pinterestEls.forEach(function(el) {
      if (el && el.parentNode) el.parentNode.removeChild(el);
    });
  }

  // Inject immediate CSS rules into head to avoid any visual flicker (FOUC)
  if (!document.getElementById('qs-pdp-hide-buttons-style')) {
    var style = document.createElement('style');
    style.id = 'qs-pdp-hide-buttons-style';
    style.textContent = [
      '.productPage #SideProductAddToWishList,',
      '.productPage .AddToWishlistLink,',
      '.productPage .wishTrigger,',
      '.productPage .wishlist-button,',
      '.productPage form#frmWishList,',
      '.productPage .PinterestButtonContainer,',
      '.productPage a[href*="pinterest.com/pin/create/button"],',
      '.productPage [data-pin-do="buttonPin"],',
      '.productPage [data-pin-log="button_save"],',
      '.productPage span[data-pin-save="true"],',
      '.productPage iframe[src*="pinterest.com"],',
      '#SideProductAddToWishList,',
      '.AddToWishlistLink,',
      '.wishTrigger,',
      '.PinterestButtonContainer {',
      '  display: none !important;',
      '  visibility: hidden !important;',
      '  height: 0 !important;',
      '  width: 0 !important;',
      '  margin: 0 !important;',
      '  padding: 0 !important;',
      '  opacity: 0 !important;',
      '  pointer-events: none !important;',
      '  overflow: hidden !important;',
      '}',
      '.productPage .addto {',
      '  margin-top: 14px !important;',
      '  margin-bottom: 8px !important;',
      '  display: block !important;',
      '  clear: both !important;',
      '  width: 100% !important;',
      '}',
      '.productPage .addto .BulkDiscount {',
      '  display: block !important;',
      '  width: 100% !important;',
      '}',
      '.productPage .addto input.btn.add-to-cart,',
      '.productPage input.add-to-cart {',
      '  display: block !important;',
      '  width: 100% !important;',
      '  max-width: 480px !important;',
      '  height: auto !important;',
      '  min-height: 48px !important;',
      '  padding: 13px 28px !important;',
      '  font-size: 16px !important;',
      '  font-weight: 700 !important;',
      '  font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;',
      '  letter-spacing: 0.5px !important;',
      '  text-transform: uppercase !important;',
      '  background: #7a1526 !important;',
      '  color: #ffffff !important;',
      '  border: none !important;',
      '  border-radius: 8px !important;',
      '  box-shadow: 0 4px 12px rgba(122, 21, 38, 0.22) !important;',
      '  cursor: pointer !important;',
      '  transition: all 0.2s ease !important;',
      '  text-align: center !important;',
      '  box-sizing: border-box !important;',
      '  line-height: normal !important;',
      '}',
      '.productPage .addto input.btn.add-to-cart:hover,',
      '.productPage input.add-to-cart:hover {',
      '  background: #5e0d19 !important;',
      '  box-shadow: 0 6px 16px rgba(122, 21, 38, 0.32) !important;',
      '  transform: translateY(-1px) !important;',
      '}',
      '.productPage .addto input.btn.add-to-cart:active,',
      '.productPage input.add-to-cart:active {',
      '  transform: translateY(0) !important;',
      '  box-shadow: 0 2px 8px rgba(122, 21, 38, 0.2) !important;',
      '}'
    ].join('\\n');
    document.head.appendChild(style);
  }

  // Execute DOM cleanup at multiple lifecycle stages to ensure removal
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', removeUnwantedButtons, { once: true });
  } else {
    removeUnwantedButtons();
  }
  window.addEventListener('load', removeUnwantedButtons, { once: true });

  // Safety observer in case external scripts dynamically re-inject Pinterest widgets
  if (window.MutationObserver) {
    var observer = new MutationObserver(function() {
      var pin = document.querySelector('.PinterestButtonContainer, [data-pin-do="buttonPin"], span[data-pin-save="true"]');
      var wish = document.querySelector('#SideProductAddToWishList, .wishTrigger');
      if (pin || wish) {
        removeUnwantedButtons();
      }
    });
    observer.observe(document.body || document.documentElement, { childList: true, subtree: true });
    setTimeout(function() { observer.disconnect(); }, 10000);
  }
})();
</script>
`;

async function deploy() {
  console.log("Fetching current Provider 6 configuration...");
  const getRes = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/settings/analytics/6`, {
    headers: { "X-Auth-Token": token, "Accept": "application/json" }
  });
  if (!getRes.ok) {
    throw new Error(`Failed to fetch Provider 6: ${getRes.status} ${await getRes.text()}`);
  }
  const getJson = await getRes.json();
  const currentCode = (getJson.data && getJson.data.code) || "";

  // 1. Backup Provider 6
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const backupDir = path.join(ROOT, "scripts", "backups");
  if (!fs.existsSync(backupDir)) fs.mkdirSync(backupDir, { recursive: true });
  const backupPath = path.join(backupDir, `provider6-before-hide-buttons-${timestamp}.json`);
  fs.writeFileSync(backupPath, JSON.stringify(getJson, null, 2), "utf8");
  console.log(`Saved backup to ${backupPath}`);

  let updatedCode = currentCode;

  // 2. Inject or update qs-pdp-hide-wishlist-pinterest
  if (updatedCode.includes("qs-pdp-hide-wishlist-pinterest")) {
    console.log("Replacing existing qs-pdp-hide-wishlist-pinterest in Provider 6...");
    updatedCode = updatedCode.replace(
      /<!-- QUALITY SWEETS - PDP HIDE WISHLIST & PINTEREST BUTTONS[\s\S]*?<\/script>\s*/,
      hideWishlistPinterestScript.trim() + "\n"
    );
  } else {
    console.log("Appending qs-pdp-hide-wishlist-pinterest to Provider 6...");
    updatedCode = updatedCode.trim() + "\n\n" + hideWishlistPinterestScript.trim() + "\n";
  }

  // 3. PUT updated code to Provider 6
  console.log("Publishing updated Provider 6 code to BigCommerce...");
  const putRes = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/settings/analytics/6`, {
    method: "PUT",
    headers: {
      "X-Auth-Token": token,
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({
      channel_id: 1,
      id: 6,
      is_enabled: true,
      code: updatedCode
    })
  });

  if (!putRes.ok) {
    throw new Error(`Failed to update Provider 6: ${putRes.status} ${await putRes.text()}`);
  }
  const putJson = await putRes.json();
  console.log("Provider 6 updated successfully! Code length:", putJson.data?.code?.length);
}

deploy().catch(console.error);
