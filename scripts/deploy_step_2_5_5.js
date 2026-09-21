import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, "../.env");
if (!fs.existsSync(envPath)) throw new Error("Missing .env with BigCommerce credentials.");

for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
  const [key, ...value] = trimmed.split("=");
  process.env[key.trim()] ??= value.join("=").trim().replace(/^['\"]|['\"]$/g, "");
}

const storeHash = process.env.BIGCOMMERCE_STORE_HASH;
const accessToken = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const clientId = process.env.BIGCOMMERCE_CLIENT_ID;
if (!storeHash || !accessToken) throw new Error("BIGCOMMERCE_STORE_HASH and BIGCOMMERCE_ACCESS_TOKEN are required.");

const baseUrl = `https://api.bigcommerce.com/stores/${storeHash}/v3`;
const headers = {
  "X-Auth-Token": accessToken,
  Accept: "application/json",
  "Content-Type": "application/json",
  ...(clientId ? { "X-Auth-Client": clientId } : {}),
};

async function bcFetch(endpoint, options = {}) {
  const response = await fetch(`${baseUrl}${endpoint}`, { ...options, headers });
  const text = await response.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = { raw: text };
  }
  if (!response.ok) throw new Error(`BigCommerce HTTP ${response.status}: ${JSON.stringify(body)}`);
  return body;
}

function contentH1Count(html) {
  return (html.match(/<h1\b/gi) || []).length;
}

function categoriesH2Count(html) {
  return (html.match(/<h2\b[^>]*>\s*Categories\s*<\/h2>/gi) || []).length;
}

function wordCount(html) {
  return (html.replace(/<[^>]+>/g, " ").match(/[A-Za-z]+(?:[-'][A-Za-z]+)*/g) || []).length;
}

function addSavoriesNavigation(description) {
  let updated = description.replace(/#CategoryHeading \.SubCategoryList, #CategoryHeading \.SubCategoryListGrid \{ display: none !important; \}\n?/g, "");
  const oldLinks = `    <a href="/mithai-box/">Mithai Gift Boxes</a>\n  </nav>`;
  const newLinks = `    <a href="/mithai-box/">Mithai Gift Boxes</a>\n    <a href="/savories/">Savory Snacks &amp; Namkeen</a>\n  </nav>`;
  if (!updated.includes(oldLinks)) throw new Error("Could not find the expected Indian Snacks navigation block.");
  updated = updated.replace(oldLinks, newLinks);

  const oldCard = `<article class="qs-snacks-card"><h3>Build a Chai-Time Assortment</h3><p>Pair a favorite namkeen with <a href="/indian-sweets/">Indian sweets</a> or a few pieces of <a href="/barfi/">Barfi and Kaju Katli</a> for a more complete tea-time spread.</p></article>`;
  const newCard = `<article class="qs-snacks-card"><h3>Shop Savory Snacks &amp; Namkeen</h3><p>Looking for Mathi, Namak Para, Gud Para, Sev, and other savory favorites? Browse our dedicated <a href="/savories/">Indian Savory Snacks &amp; Namkeen</a> collection.</p></article>`;
  if (!updated.includes(oldCard)) throw new Error("Could not find the expected Indian Snacks category card.");
  updated = updated.replace(oldCard, newCard);
  return updated;
}

const savoriesDescription = `<style>
#CategoryHeading > .TitleHeading { color: #6d1427 !important; display: block !important; font-family: Georgia, 'Times New Roman', serif !important; font-size: clamp(2rem, 4vw, 3.05rem) !important; line-height: 1.15 !important; margin: 0 0 10px !important; text-align: center; }
.qs-savories-intro, .qs-savories-seo { box-sizing: border-box; font-family: Arial, Helvetica, sans-serif; }
.qs-savories-intro { color: #544142; margin: 0 0 24px; text-align: center; }
.qs-savories-intro p { font-size: 1.03rem; line-height: 1.6; margin: 0 auto; max-width: 760px; }
.qs-savories-links { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 18px auto 0; }
.qs-savories-links a { background: #fffaf1; border: 1px solid #d9b778; border-radius: 999px; color: #6d1427 !important; display: inline-block; font-size: .93rem; font-weight: 700; padding: 10px 16px; text-decoration: none !important; }
.qs-savories-links a:hover { background: #45101b; color: #fff !important; }
.qs-savories-seo { border-top: 1px solid #eadcc4; color: #4f4142; margin: 42px 0 24px; padding: 36px 0 8px; }
.qs-savories-seo h2 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: clamp(1.55rem, 3vw, 2.15rem); line-height: 1.2; margin: 0 0 12px; }
.qs-savories-seo h3 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: 1.2rem; margin: 0 0 7px; }
.qs-savories-seo p { font-size: 1rem; line-height: 1.7; margin: 0 0 17px; }
.qs-savories-grid { display: grid; gap: 16px; grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 21px 0 28px; }
.qs-savories-card { background: #fffaf1; border: 1px solid #eadcc4; border-radius: 10px; padding: 19px; }
.qs-savories-card p { font-size: .94rem; margin: 0; }
.qs-savories-faq { border-top: 1px solid #eadcc4; margin-top: 26px; }
.qs-savories-faq details { border-bottom: 1px solid #eadcc4; padding: 14px 0; }
.qs-savories-faq summary { color: #6d1427; cursor: pointer; font-family: Georgia, 'Times New Roman', serif; font-size: 1.08rem; font-weight: 700; }
.qs-savories-faq p { font-size: .95rem; margin: 10px 0 0; }
.qs-navigation-heading { border-bottom: 1px dashed #d9d6c8; color: #840b17; display: block; font-size: 24px; font-weight: 700; margin: 0; padding: 0 0 10px; }
@media (max-width: 640px) { .qs-savories-grid { grid-template-columns: 1fr; } .qs-savories-links a { width: 100%; } }
</style>

<section class="qs-savories-intro">
  <p>Shop Indian savory snacks and namkeen for chai time, sharing, and everyday cravings. Browse crisp Mathi, Namak Para, Gud Para, Sev, snack mix, and other familiar savory favorites from Quality Sweets in Iselin, New Jersey.</p>
  <nav class="qs-savories-links" aria-label="Explore related Quality Sweets collections">
    <a href="/indian-snacks/">All Indian Snacks &amp; Namkeen</a>
    <a href="/indian-sweets/">All Indian Sweets</a>
    <a href="/mithai-box/">Mithai Gift Boxes</a>
  </nav>
</section>

<section class="qs-savories-seo">
  <h2>Indian Savory Snacks for Chai Time and Sharing</h2>
  <p>Indian savory snacks, often called namkeen, bring crunch, warmth, and a balanced salty bite to a tea break, a family visit, or a table set out for guests. This collection brings together the dry snacks people reach for when they want something crisp beside masala chai: Mathi, Namak Para, Gud Para, Sev, snack mix, and related favorites. Browse the live catalog above for the current products, sizes, prices, and availability.</p>
  <p>Every savory snack has its own character. Mathi, also spelled matri, is a crisp, flaky-style snack that many families enjoy with tea. Namak Para offers a savory, bite-sized option, while Gud Para adds a sweeter contrast. Sev is a thin, crunchy noodle-like snack that works on its own or as part of a broader snack spread. The individual product page is the best place to confirm the current ingredients, flavor, package size, and fulfillment details for any item.</p>

  <h2>Find Your Favorite Namkeen Snack</h2>
  <div class="qs-savories-grid">
    <article class="qs-savories-card"><h3>Mathi &amp; Namak Para</h3><p>Choose classic crisp snacks for chai time, quick pantry treats, or an easy addition to a gathering with family and friends.</p></article>
    <article class="qs-savories-card"><h3>Gud Para &amp; Sweet-Savory Bites</h3><p>Explore the current sweet-and-salty options when you want a snack with a little contrast and familiar texture.</p></article>
    <article class="qs-savories-card"><h3>Fine Sev, Thick Sev &amp; Snack Mix</h3><p>Browse crunchy Sev and snack mix for a simple savory choice, a shareable bowl, or a chai-time assortment.</p></article>
  </div>

  <h2>Order Namkeen Online or Visit Quality Sweets in Iselin</h2>
  <p>Quality Sweets has served the Iselin community since 2003 with Indian sweets, snacks, and familiar flavors for celebrations and everyday enjoyment. Whether you are choosing a bag of Mathi for home or putting together a larger snack table, the products above show the current selection in one place. For a broader assortment, return to <a href="/indian-snacks/">Indian Snacks &amp; Namkeen</a>, where you can also find other chai-time options and spiced cashews.</p>
  <p>Many eligible savory snacks can be ordered online for delivery across the USA. Shipping availability can vary by item, so check the individual product page before checkout for the current fulfillment details. Local customers can shop or arrange pickup at Quality Sweets, 1384 Oak Tree Road, Iselin, NJ 08830. The store is open daily from 10 AM to 8 PM. Add a box of <a href="/indian-sweets/">Indian sweets</a> or a <a href="/mithai-box/">mithai gift box</a> when you want to pair something sweet with your savory snacks.</p>

  <section class="qs-savories-faq" aria-labelledby="qs-savories-faq-title">
    <h2 id="qs-savories-faq-title">Indian Savory Snacks FAQ</h2>
    <details><summary>What are Indian savory snacks?</summary><p>Indian savory snacks, also known as namkeen, are crisp snacks with savory, spiced, or sweet-and-salty flavors. This collection includes Mathi, Namak Para, Gud Para, Sev, and snack mix.</p></details>
    <details><summary>What is the difference between Mathi and Namak Para?</summary><p>Both are crisp Indian snacks, but they have different shapes and textures. Browse the product pages for the current options and item-specific details.</p></details>
    <details><summary>Can I order namkeen snacks online?</summary><p>Many eligible snacks can be ordered online for delivery across the USA. Check the individual product page for current availability and fulfillment details.</p></details>
    <details><summary>Can I buy savory snacks locally in Iselin?</summary><p>Yes. Quality Sweets is at 1384 Oak Tree Road, Iselin, NJ 08830, and is open daily from 10 AM to 8 PM.</p></details>
  </section>
</section>

<script>
(function () {
  function setNativeHeading() {
    var heading = document.querySelector('#CategoryHeading > .TitleHeading');
    if (!heading) return;
    heading.textContent = "Indian Savory Snacks & Namkeen";
    heading.setAttribute('data-qs-seo-heading', 'true');
  }
  function demoteCategoriesHeadings(root) {
    var scope = root && root.querySelectorAll ? root : document;
    var headings = [];
    if (scope.nodeType === 1 && scope.matches && scope.matches('h2')) headings.push(scope);
    Array.prototype.push.apply(headings, scope.querySelectorAll('h2'));
    headings.forEach(function (heading) {
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
    var seoContent = document.querySelector('.qs-savories-seo');
    var categoryContent = document.getElementById('CategoryContent');
    if (!seoContent || !categoryContent || seoContent.dataset.moved === 'true') return;
    categoryContent.insertAdjacentElement('afterend', seoContent);
    seoContent.dataset.moved = 'true';
  }
  function repair() {
    setNativeHeading();
    demoteCategoriesHeadings(document);
    moveSeoContentBelowCatalog();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', repair);
  else repair();
  new MutationObserver(function (records) {
    records.forEach(function (record) {
      Array.prototype.forEach.call(record.addedNodes, function (node) {
        if (node.nodeType === 1) demoteCategoriesHeadings(node);
      });
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
}());
</script>`;

async function verifyLiveNutsRedirect() {
  const response = await fetch("https://qualitysweetsnj.com/nuts/", { method: "GET", redirect: "manual" });
  const location = response.headers.get("location") || "";
  if (response.status !== 301 || !location.includes("/indian-snacks/")) {
    throw new Error(`Live /nuts/ redirect verification failed: HTTP ${response.status}, Location: ${location || "(none)"}`);
  }
  console.log(`Verified live redirect: /nuts/ -> ${location}`);
}

const apply = process.argv.includes("--apply");
const [parent, nuts, savories] = await Promise.all([
  bcFetch("/catalog/categories/1").then((body) => body.data),
  bcFetch("/catalog/categories/16").then((body) => body.data),
  bcFetch("/catalog/categories/18").then((body) => body.data),
]);

if (parent.custom_url?.url !== "/indian-snacks/" || nuts.custom_url?.url !== "/nuts/" || savories.custom_url?.url !== "/savories/") {
  throw new Error("Category URLs do not match the approved Step 2.5.5 targets. Refusing to update.");
}
if (nuts.parent_id !== 1 || savories.parent_id !== 1) {
  throw new Error("Nuts and Savories must remain children of Indian Snacks before this deployment.");
}

const nutsProducts = (await bcFetch("/catalog/products?categories:in=16&limit=250&include_fields=id,name,categories")).data;
const savoriesProducts = (await bcFetch("/catalog/products?categories:in=18&limit=250&include_fields=id,name,custom_url")).data;
if (nutsProducts.length !== 2) throw new Error(`Expected 2 Nuts products; found ${nutsProducts.length}. Refusing to change category assignments.`);
if (savoriesProducts.length < 3) throw new Error(`Savories needs at least 3 products to remain indexable; found ${savoriesProducts.length}.`);

const parentDescription = addSavoriesNavigation(parent.description);
for (const [label, description] of [["Indian Snacks", parentDescription], ["Savories", savoriesDescription]]) {
  if (contentH1Count(description) !== 0) throw new Error(`${label} description contains a content H1.`);
  if (categoriesH2Count(description) !== 0) throw new Error(`${label} description contains an H2 named Categories.`);
}
if (wordCount(savoriesDescription) < 400) throw new Error("Savories description must contain at least 400 words.");

console.log(`Indian Snacks: ${parent.name} — prepared H1 tags ${contentH1Count(parentDescription)}, Categories H2 tags ${categoriesH2Count(parentDescription)}`);
console.log(`Nuts: ${nutsProducts.length} products to merge — ${nutsProducts.map((product) => product.name).join(" | ")}`);
console.log(`Savories: ${savoriesProducts.length} products — prepared ${wordCount(savoriesDescription)} words, H1 tags ${contentH1Count(savoriesDescription)}, Categories H2 tags ${categoriesH2Count(savoriesDescription)}`);

if (!apply) {
  console.log("Dry run complete. Use --apply to execute all of Step 2.5.5.");
  process.exit(0);
}

for (const product of nutsProducts) {
  const existingCategories = product.categories || [];
  const categories = [...new Set([...existingCategories.filter((categoryId) => categoryId !== 16), 1])];
  const result = (await bcFetch(`/catalog/products/${product.id}`, {
    method: "PUT",
    body: JSON.stringify({ categories }),
  })).data;
  if (result.categories.includes(16) || !result.categories.includes(1)) {
    throw new Error(`Product ${product.id} category verification failed.`);
  }
  console.log(`Merged product ${product.id}: ${result.name}`);
}

const updatedParent = (await bcFetch("/catalog/categories/1", {
  method: "PUT",
  body: JSON.stringify({ description: parentDescription }),
})).data;
if (updatedParent.description !== parentDescription || contentH1Count(updatedParent.description) !== 0 || categoriesH2Count(updatedParent.description) !== 0) {
  throw new Error("Indian Snacks update did not pass heading validation.");
}

const updatedSavories = (await bcFetch("/catalog/categories/18", {
  method: "PUT",
  body: JSON.stringify({
    description: savoriesDescription,
    page_title: "Indian Savory Snacks & Namkeen | Mathi, Sev & Namak Para",
    meta_description: "Shop Indian savory snacks and namkeen: Mathi, Namak Para, Gud Para, Sev and snack mix. Order eligible items online or shop Quality Sweets in Iselin.",
    search_keywords: "indian savory snacks, namkeen snacks, indian savories, namak para online, mathi online, sev indian snack",
  }),
})).data;
if (updatedSavories.description !== savoriesDescription || contentH1Count(updatedSavories.description) !== 0 || categoriesH2Count(updatedSavories.description) !== 0) {
  throw new Error("Savories update did not pass heading validation.");
}

const hiddenNuts = (await bcFetch("/catalog/categories/16", {
  method: "PUT",
  body: JSON.stringify({
    is_visible: false,
    custom_url: { url: "/nuts-archived/", is_customized: true },
  }),
})).data;
if (hiddenNuts.is_visible || hiddenNuts.custom_url?.url !== "/nuts-archived/") {
  throw new Error("Nuts category was not hidden and archived as expected.");
}

const redirects = await bcFetch("/storefront/redirects", {
  method: "PUT",
  body: JSON.stringify([
    { from_path: "/nuts/", site_id: 1000, to: { type: "category", entity_id: 1 } },
    { from_path: "/Snacks/nuts/", site_id: 1000, to: { type: "category", entity_id: 1 } },
  ]),
});
console.log(`Configured ${Array.isArray(redirects.data) ? redirects.data.length : 2} redirect route(s) to Indian Snacks.`);

await verifyLiveNutsRedirect();
console.log("Step 2.5.5 completed successfully.");
