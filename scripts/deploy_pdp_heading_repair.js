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

const headingRepairScript = `
<!-- QUALITY SWEETS - PDP HEADING HIERARCHY REPAIR (SEO & ACCESSIBILITY) -->
<script id="qs-pdp-heading-hierarchy-repair">
(function() {
  function retag(el, newTagName, addClass) {
    if (!el || el.tagName.toLowerCase() === newTagName.toLowerCase()) return el;
    var newEl = document.createElement(newTagName);
    for (var i = 0; i < el.attributes.length; i++) {
      var attr = el.attributes[i];
      newEl.setAttribute(attr.name, attr.value);
    }
    while (el.firstChild) {
      newEl.appendChild(el.firstChild);
    }
    if (addClass) newEl.classList.add(addClass);
    if (el.parentNode) el.parentNode.replaceChild(newEl, el);
    return newEl;
  }

  function repairPdpHeadings() {
    var isPdp = document.body.classList.contains('productPage') || 
                document.getElementById('productDetailsAddToCartForm') ||
                document.querySelector('.ProductMain');
    if (!isPdp) return;

    // 1. Pre-H1 Drawer and Header categories: retag to span so H1 is the very first heading
    var preH2s = document.querySelectorAll('#DrawerMenu .CategoryList h2, #Header .CategoryList h2, .PageMenu #SideCategoryList h2');
    preH2s.forEach(function(h2) {
      retag(h2, 'span', 'qs-cat-nav-title');
    });

    // 2. Remove empty H4 BrandName under H1
    var brandH4 = document.querySelector('.ProductMain h4.BrandName');
    if (brandH4) {
      if (!brandH4.textContent.trim()) {
        var valParent = brandH4.closest('.Value');
        if (valParent && !valParent.textContent.trim()) {
          valParent.remove();
        } else {
          brandH4.remove();
        }
      }
    }

    // 3. Review form H5 -> H3 to prevent level skip under H2 Product Reviews
    var reviewH5 = document.querySelector('#rating_box h5, #ProductReviews h5');
    if (reviewH5) {
      retag(reviewH5, 'h3', 'qs-review-form-title');
    }

    // 4. Sidebar utility headings in .Left -> H3 to avoid competing with PDP H2 sections
    var sideH2s = document.querySelectorAll('.Left #SideCategoryList h2, .Left #SidePopularProducts h2, .Left #SideNewsletterBox h2, .Left .Block h2');
    sideH2s.forEach(function(h2) {
      retag(h2, 'h3', 'qs-side-h3');
    });

    // 5. Footer utility headings in #FooterUpper -> H3
    var footerHeadings = document.querySelectorAll('#FooterUpper h2, #FooterUpper h4, .footer-main h2, .footer-main h4');
    footerHeadings.forEach(function(h) {
      retag(h, 'h3', 'qs-footer-h3');
    });
  }

  // Inject companion CSS for seamless visual styling
  if (!document.getElementById('qs-pdp-heading-repair-style')) {
    var style = document.createElement('style');
    style.id = 'qs-pdp-heading-repair-style';
    style.textContent = [
      '.PageMenu #SideCategoryList .qs-cat-nav-title { display: none !important; }',
      '#DrawerMenu .qs-cat-nav-title { display: block; font-family: Oswald, sans-serif; font-size: 16px; font-weight: 600; color: #5b1e19; margin: 0 0 10px 0; padding: 10px 15px; }',
      '.Left h3.qs-side-h3 { border-bottom: 1px dashed #D9D6C8 !important; color: #840B17 !important; padding: 0 0 10px !important; font-family: Oswald, "Plus Jakarta Sans", sans-serif !important; font-size: 16px !important; font-weight: 700 !important; margin: 0 0 10px 0 !important; text-transform: uppercase !important; }',
      '#rating_box h3.qs-review-form-title { font-size: 15px !important; font-weight: 700 !important; color: #7a1526 !important; font-family: "Marcellus", Georgia, serif !important; margin: 15px 0 10px 0 !important; }',
      '#FooterUpper h3.qs-footer-h3, #FooterUpper .Block h3.qs-footer-h3 { font-family: "Marcellus", Georgia, serif !important; font-size: 19px !important; color: #d4af37 !important; margin: 0 0 12px 0 !important; font-weight: 700 !important; }'
    ].join('\\n');
    document.head.appendChild(style);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', repairPdpHeadings, { once: true });
  } else {
    repairPdpHeadings();
  }
  window.addEventListener('load', repairPdpHeadings, { once: true });
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
  const backupPath = path.join(backupDir, `provider6-before-heading-repair-${timestamp}.json`);
  fs.writeFileSync(backupPath, JSON.stringify(getJson, null, 2), "utf8");
  console.log(`Saved backup to ${backupPath}`);

  let updatedCode = currentCode;

  // 2. Also ensure qs-footer-nap generates <h3> instead of <h2> for footer columns
  if (updatedCode.includes("qs-footer-nap")) {
    console.log("Updating qs-footer-nap columns to use <h3> instead of <h2>...");
    updatedCode = updatedCode.replace("<h2>Shop</h2>", "<h3>Shop</h3>");
    updatedCode = updatedCode.replace("<h2>Visit &amp; Order</h2>", "<h3>Visit &amp; Order</h3>");
    updatedCode = updatedCode.replace("<h2>About &amp; Help</h2>", "<h3>About &amp; Help</h3>");
    updatedCode = updatedCode.replace("#FooterUpper h2 {", "#FooterUpper h2, #FooterUpper h3, #FooterUpper .Column h3 {");
  }

  // 3. Inject or update qs-pdp-heading-hierarchy-repair
  if (updatedCode.includes("qs-pdp-heading-hierarchy-repair")) {
    console.log("Replacing existing qs-pdp-heading-hierarchy-repair in Provider 6...");
    updatedCode = updatedCode.replace(
      /<!-- QUALITY SWEETS - PDP HEADING HIERARCHY REPAIR[\s\S]*?<\/script>\s*/,
      headingRepairScript.trim() + "\n"
    );
  } else {
    console.log("Appending qs-pdp-heading-hierarchy-repair to Provider 6...");
    updatedCode = updatedCode.trim() + "\n\n" + headingRepairScript.trim() + "\n";
  }

  // 4. PUT updated code to Provider 6
  console.log("Publishing updated Provider 6 code...");
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
