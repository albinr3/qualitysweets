import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, "../.env");

if (!fs.existsSync(envPath)) {
  throw new Error("Missing .env with BigCommerce credentials.");
}

for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
  const [key, ...value] = trimmed.split("=");
  process.env[key.trim()] ??= value.join("=").trim().replace(/^['\"]|['\"]$/g, "");
}

const storeHash = process.env.BIGCOMMERCE_STORE_HASH;
const accessToken = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const clientId = process.env.BIGCOMMERCE_CLIENT_ID;

if (!storeHash || !accessToken) {
  throw new Error("BIGCOMMERCE_STORE_HASH and BIGCOMMERCE_ACCESS_TOKEN are required.");
}

const baseUrl = `https://api.bigcommerce.com/stores/${storeHash}/v3`;
const headers = {
  "X-Auth-Token": accessToken,
  Accept: "application/json",
  "Content-Type": "application/json",
  ...(clientId ? { "X-Auth-Client": clientId } : {}),
};

async function bcFetch(endpoint, options = {}) {
  const response = await fetch(`${baseUrl}${endpoint}`, { ...options, headers });
  const body = await response.json();
  if (!response.ok) throw new Error(`BigCommerce HTTP ${response.status}: ${JSON.stringify(body)}`);
  return body;
}

const description = `<style>
#CategoryHeading > .TitleHeading { display: none !important; }
#CategoryHeading .SubCategoryList, #CategoryHeading .SubCategoryListGrid { display: none !important; }
.qs-navigation-heading { border-bottom: 1px dashed #D9D6C8; color: #840B17; display: block; font-size: 24px; font-weight: 700; margin: 0; padding: 0 0 10px; }
.qs-bengali-intro, .qs-bengali-seo { box-sizing: border-box; font-family: Arial, Helvetica, sans-serif; }
.qs-bengali-intro { margin: 0 0 24px; text-align: center; }
.qs-bengali-intro h1 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: clamp(2rem, 4vw, 3.05rem); line-height: 1.15; margin: 0 0 10px; }
.qs-bengali-intro p { color: #544142; font-size: 1.03rem; line-height: 1.6; margin: 0 auto; max-width: 760px; }
.qs-bengali-links { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 18px auto 0; }
.qs-bengali-links a { background: #fffaf1; border: 1px solid #d9b778; border-radius: 999px; color: #6d1427 !important; display: inline-block; font-size: .93rem; font-weight: 700; padding: 10px 16px; text-decoration: none !important; }
.qs-bengali-links a:hover, .qs-bengali-card-cta:hover { background: #45101b; color: #fff !important; }
.qs-bengali-seo { border-top: 1px solid #eadcc4; color: #4f4142; margin: 42px 0 24px; padding: 36px 0 8px; }
.qs-bengali-seo h2 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: clamp(1.55rem, 3vw, 2.15rem); line-height: 1.2; margin: 0 0 12px; }
.qs-bengali-seo h3 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: 1.2rem; margin: 0 0 7px; }
.qs-bengali-seo p { font-size: 1rem; line-height: 1.7; margin: 0 0 17px; }
.qs-bengali-grid { display: grid; gap: 16px; grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 21px 0 28px; }
.qs-bengali-card { background: #fffaf1; border: 1px solid #eadcc4; border-radius: 10px; padding: 19px; }
.qs-bengali-card p { font-size: .94rem; margin: 0; }
.qs-bengali-card a { color: #6d1427; font-weight: 700; }
.qs-bengali-card-cta { background: #6d1427; border-radius: 6px; color: #fff !important; display: inline-block; font-size: .9rem; margin-top: 18px; padding: 10px 14px; text-decoration: none !important; }
.qs-bengali-faq { border-top: 1px solid #eadcc4; margin-top: 26px; }
.qs-bengali-faq details { border-bottom: 1px solid #eadcc4; padding: 14px 0; }
.qs-bengali-faq summary { color: #6d1427; cursor: pointer; font-family: Georgia, 'Times New Roman', serif; font-size: 1.08rem; font-weight: 700; }
.qs-bengali-faq p { font-size: .95rem; margin: 10px 0 0; }
@media (max-width: 640px) { .qs-bengali-grid { grid-template-columns: 1fr; } .qs-bengali-links a { width: 100%; } }
</style>

<section class="qs-bengali-intro" aria-labelledby="qs-bengali-title">
  <h1 id="qs-bengali-title">Authentic Bengali Sweets (No Preservatives)</h1>
  <p>Discover soft, milk-based Bengali mithai made fresh in Iselin, New Jersey. Shop Chum Chum, Rasgulla, Sandesh, Kalakand, and other chhena sweets with nationwide shipping available on eligible items.</p>
  <nav class="qs-bengali-links" aria-label="Explore related Indian sweet collections">
    <a href="/indian-sweets/">All Indian Sweets</a>
    <a href="/barfi/">Barfi &amp; Kaju Katli</a>
    <a href="/traditional-mithai/">Traditional Mithai</a>
  </nav>
</section>

<section class="qs-bengali-seo" aria-labelledby="qs-bengali-story">
  <h2 id="qs-bengali-story">Why Bengali Mithai Starts with Fresh Chhena</h2>
  <p>Bengali sweets are loved for their delicate texture: light, milky, gently sweet, and often finished with syrup, saffron, cardamom, nuts, or fruit-inspired flavors. At Quality Sweets, we make Bengali mithai in-house in Iselin, New Jersey, with fresh chhena—the soft curdled-milk base that gives sweets such as Rasgulla, Sandesh, and Chum Chum their character. We use no preservatives, so the collection is prepared with the attention that these classic sweets deserve.</p>
  <p>For many families, Bengali sweets bring back the flavor of a favorite sweet shop: a tender Chum Chum, a syrupy Rasgulla, or a creamy bite of Sandesh shared after a meal or offered to guests. If you are trying Bengali mithai for the first time, this is a welcoming place to start. The flavors are often less heavy than dense nut sweets, with a soft texture and balanced sweetness that makes them easy to share. If you already have a favorite, browse the catalog above for current varieties, sizes, and availability.</p>

  <h2>Explore Bengali Sweets for Sharing, Gifting &amp; Everyday Treats</h2>
  <div class="qs-bengali-grid">
    <article class="qs-bengali-card">
      <h3>Chum Chum &amp; Cham Cham</h3>
      <p>Chum Chum, also spelled chomchom or cham cham, is a beloved Bengali sweet with a tender chhena center. Explore current varieties, including familiar Malai, Rose, Cherry, and other seasonal flavors when available.</p>
    </article>
    <article class="qs-bengali-card">
      <h3>Rasgulla &amp; Sandesh</h3>
      <p>Choose Rasgulla for a soft, syrup-soaked sweet, or Sandesh for a more delicate chhena confection. Both are timeless ways to enjoy the lighter side of Bengali mithai.</p>
    </article>
    <article class="qs-bengali-card">
      <h3>More Bengali Favorites</h3>
      <p>Look for Kalakand, Malai Sandwich, Kadam Keer, and other specialties in the live catalog. Selection can vary with fresh preparation, so product pages show the current options.</p>
    </article>
  </div>

  <h2>Fresh Bengali Sweets from Iselin, NJ</h2>
  <p>Quality Sweets has served the Iselin community since 2003 with vegetarian Indian sweets made fresh daily. Our Bengali sweet shop collection is for a box to bring home, a thoughtful gift, a celebration, or a sweet addition to a family table. Every product page is the best place to confirm its current flavor, quantity, price, and fulfillment details. Some delicate items may be available for Iselin store pickup only so they can be enjoyed in the condition intended by our kitchen.</p>
  <p>Many eligible Bengali sweets can be ordered online for delivery across the USA. We pack shippable orders in insulated packaging with cold gel packs to help protect freshness in transit. Because each sweet has its own texture and handling needs, please review the product page before checkout; it will show the availability and fulfillment options currently offered. For local pickup, visit Quality Sweets at 1384 Oak Tree Road, Iselin, NJ 08830, open daily from 10 AM to 8 PM.</p>
  <p>Build a varied Indian sweets assortment by pairing Bengali mithai with <a href="/barfi/">Barfi and Kaju Katli</a> or <a href="/traditional-mithai/">Traditional Mithai</a>. Or return to <a href="/indian-sweets/">All Indian Sweets</a> to browse the complete collection. Whether you call it Chum Chum, chomchom, or cham cham, our goal is simple: make it easy to find fresh Bengali sweets with the authentic, tender character people look for.</p>

  <section class="qs-bengali-faq" aria-labelledby="qs-bengali-faq-title">
    <h2 id="qs-bengali-faq-title">Bengali Sweets FAQ</h2>
    <details><summary>What are Bengali sweets made from?</summary><p>Many Bengali sweets are made with fresh chhena, a soft curdled-milk base. Ingredients vary by product, so please review each product page for current details.</p></details>
    <details><summary>Do your Bengali sweets contain preservatives?</summary><p>No. Quality Sweets makes its Bengali mithai with no preservatives and prepares sweets fresh daily.</p></details>
    <details><summary>What is the difference between Rasgulla and Chum Chum?</summary><p>Both are chhena-based Bengali sweets. Rasgulla is typically a soft, syrup-soaked round sweet, while Chum Chum has a firmer oblong shape and may be finished with flavors or fillings.</p></details>
    <details><summary>Can I order Bengali sweets online for delivery?</summary><p>Many eligible items can ship across the USA in insulated packaging. Check each product page for its current availability and fulfillment details.</p></details>
    <details><summary>Are any Bengali sweets pickup only?</summary><p>Some especially delicate items may be available only for pickup at our Iselin store to protect their freshness. Product pages identify the current fulfillment option.</p></details>
  </section>
</section>

<script>
(function () {
  function demoteNavigationCategoryHeadings() {
    Array.prototype.forEach.call(document.querySelectorAll('h2'), function (heading) {
      if (heading.textContent.trim().toLowerCase() !== 'categories') return;
      var label = document.createElement('div');
      label.className = (heading.className ? heading.className + ' ' : '') + 'qs-navigation-heading';
      label.innerHTML = heading.innerHTML;
      Array.prototype.forEach.call(heading.attributes, function (attribute) {
        if (attribute.name !== 'class') label.setAttribute(attribute.name, attribute.value);
      });
      heading.parentNode.replaceChild(label, heading);
    });
  }
  function moveSeoContentBelowCatalog() {
    var seoContent = document.querySelector('.qs-bengali-seo');
    var categoryContent = document.getElementById('CategoryContent');
    if (!seoContent || !categoryContent || seoContent.dataset.moved === 'true') return;
    categoryContent.insertAdjacentElement('afterend', seoContent);
    seoContent.dataset.moved = 'true';
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      demoteNavigationCategoryHeadings();
      moveSeoContentBelowCatalog();
    });
  } else {
    demoteNavigationCategoryHeadings();
    moveSeoContentBelowCatalog();
  }
}());
</script>`;

const payload = {
  description,
  page_title: "Bengali Sweets Online | Fresh Chum Chum, Rasgulla & Sandesh Delivery",
  meta_description: "Authentic Bengali sweets made from fresh artisan chhena with zero preservatives. Famous Chum Chum, Angoori Rasgulla & Sandesh shipped fresh across USA.",
  search_keywords: "bengali sweets, chum chum, chomchom, cham cham, rasgulla, sandesh, bengali mithai",
};

const apply = process.argv.includes("--apply");
const category = (await bcFetch("/catalog/categories/8")).data;
const products = (await bcFetch("/catalog/products?categories:in=8&limit=250&include_fields=id,name,custom_url,availability")).data;

console.log(`Category ${category.id}: ${category.name} (${category.custom_url.url})`);
console.log("Current description length:", category.description.length);
console.log("Products currently assigned:", products.map((product) => `${product.id}: ${product.name} (${product.custom_url?.url || "no custom URL"})`).join(" | "));
console.log("Prepared content word count:", description.replace(/<[^>]+>/g, " ").match(/[A-Za-z]+(?:[-'][A-Za-z]+)*/g).length);

if (!apply) {
  console.log("Dry run complete. Use --apply to update Category ID 8.");
  process.exit(0);
}

const result = (await bcFetch("/catalog/categories/8", {
  method: "PUT",
  body: JSON.stringify(payload),
})).data;

if (result.page_title !== payload.page_title || result.meta_description !== payload.meta_description || result.description !== description) {
  throw new Error("BigCommerce response did not match the requested Category ID 8 update.");
}

console.log(`Updated Category ${result.id} successfully.`);
console.log(`Title: ${result.page_title}`);
console.log(`Meta description: ${result.meta_description}`);
console.log(`Description length: ${result.description.length}`);
