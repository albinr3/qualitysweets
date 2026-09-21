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
  const body = await response.json();
  if (!response.ok) throw new Error(`BigCommerce HTTP ${response.status}: ${JSON.stringify(body)}`);
  return body;
}

function categoryDescription({ prefix, heading, intro, links, body, faq }) {
  return `<style>
#CategoryHeading > .TitleHeading { color: #6d1427 !important; display: block !important; font-family: Georgia, 'Times New Roman', serif !important; font-size: clamp(2rem, 4vw, 3.05rem) !important; line-height: 1.15 !important; margin: 0 0 10px !important; text-align: center; }
#CategoryHeading .SubCategoryList, #CategoryHeading .SubCategoryListGrid { display: none !important; }
.${prefix}-intro, .${prefix}-seo { box-sizing: border-box; font-family: Arial, Helvetica, sans-serif; }
.${prefix}-intro { color: #544142; margin: 0 0 24px; text-align: center; }
.${prefix}-intro p { font-size: 1.03rem; line-height: 1.6; margin: 0 auto; max-width: 760px; }
.${prefix}-links { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 18px auto 0; }
.${prefix}-links a { background: #fffaf1; border: 1px solid #d9b778; border-radius: 999px; color: #6d1427 !important; display: inline-block; font-size: .93rem; font-weight: 700; padding: 10px 16px; text-decoration: none !important; }
.${prefix}-links a:hover { background: #45101b; color: #fff !important; }
.${prefix}-seo { border-top: 1px solid #eadcc4; color: #4f4142; margin: 42px 0 24px; padding: 36px 0 8px; }
.${prefix}-seo h2 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: clamp(1.55rem, 3vw, 2.15rem); line-height: 1.2; margin: 0 0 12px; }
.${prefix}-seo h3 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: 1.2rem; margin: 0 0 7px; }
.${prefix}-seo p { font-size: 1rem; line-height: 1.7; margin: 0 0 17px; }
.${prefix}-grid { display: grid; gap: 16px; grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 21px 0 28px; }
.${prefix}-card { background: #fffaf1; border: 1px solid #eadcc4; border-radius: 10px; padding: 19px; }
.${prefix}-card p { font-size: .94rem; margin: 0; }
.${prefix}-faq { border-top: 1px solid #eadcc4; margin-top: 26px; }
.${prefix}-faq details { border-bottom: 1px solid #eadcc4; padding: 14px 0; }
.${prefix}-faq summary { color: #6d1427; cursor: pointer; font-family: Georgia, 'Times New Roman', serif; font-size: 1.08rem; font-weight: 700; }
.${prefix}-faq p { font-size: .95rem; margin: 10px 0 0; }
.qs-navigation-heading { border-bottom: 1px dashed #d9d6c8; color: #840b17; display: block; font-size: 24px; font-weight: 700; margin: 0; padding: 0 0 10px; }
@media (max-width: 640px) { .${prefix}-grid { grid-template-columns: 1fr; } .${prefix}-links a { width: 100%; } }
</style>

<section class="${prefix}-intro">
  <p>${intro}</p>
  <nav class="${prefix}-links" aria-label="Explore related Quality Sweets collections">
    ${links.map(({ href, label }) => `<a href="${href}">${label}</a>`).join("\n    ")}
  </nav>
</section>

<section class="${prefix}-seo">
${body}
  <section class="${prefix}-faq" aria-labelledby="${prefix}-faq-title">
    <h2 id="${prefix}-faq-title">${faq.title}</h2>
    ${faq.items.map(({ q, a }) => `<details><summary>${q}</summary><p>${a}</p></details>`).join("\n    ")}
  </section>
</section>

<script>
(function () {
  function setNativeHeading() {
    var heading = document.querySelector('#CategoryHeading > .TitleHeading');
    if (!heading) return;
    heading.textContent = ${JSON.stringify(heading)};
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
    var seoContent = document.querySelector('.${prefix}-seo');
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
}

const snacks = categoryDescription({
  prefix: "qs-snacks",
  heading: "Traditional Indian Snacks & Namkeen",
  intro: "Browse traditional Indian snacks and namkeen for chai time, sharing, and everyday cravings. Find crisp savory favorites, sweet-and-salty treats, and pantry-ready selections prepared with the familiar flavors of an Indian snack shop.",
  links: [
    { href: "/indian-sweets/", label: "All Indian Sweets" },
    { href: "/barfi/", label: "Barfi &amp; Kaju Katli" },
    { href: "/mithai-box/", label: "Mithai Gift Boxes" },
  ],
  body: `  <h2>Indian Snacks &amp; Namkeen for Chai Time and Sharing</h2>
  <p>Indian snacks and namkeen bring a satisfying contrast of crunch, spice, sweetness, and savory flavor to any tea break or gathering. At Quality Sweets, this collection makes it easy to browse familiar favorites for a quick treat at home, a snack tray for guests, or a thoughtful addition to a mithai order. Look through the live catalog above for the current selection, package sizes, prices, and availability.</p>
  <p>Namkeen is a broad name for savory Indian snacks. Depending on the item, you may find a crisp, lightly spiced bite; a sweet-and-salty combination; or a snack with a warmer masala finish. These are the kinds of pantry staples that pair naturally with masala chai, make an easy offering when friends stop by, and add variety to a festive table beside Indian sweets. Each product has its own ingredients and flavor profile, so the individual product page is the best place to review the current details before ordering.</p>

  <h2>Find a Favorite Indian Snack</h2>
  <div class="qs-snacks-grid">
    <article class="qs-snacks-card"><h3>Crisp Savory Namkeen</h3><p>Explore crunchy savory snacks when you want a classic companion for chai, a light bite between meals, or something simple to share.</p></article>
    <article class="qs-snacks-card"><h3>Sweet &amp; Salty Treats</h3><p>Choose a balanced sweet-and-salty snack for a change of pace, a family movie night, or an easy item to keep on hand for guests.</p></article>
    <article class="qs-snacks-card"><h3>Build a Chai-Time Assortment</h3><p>Pair a favorite namkeen with <a href="/indian-sweets/">Indian sweets</a> or a few pieces of <a href="/barfi/">Barfi and Kaju Katli</a> for a more complete tea-time spread.</p></article>
  </div>

  <h2>Order Indian Snacks Online or Visit Our Iselin Shop</h2>
  <p>Quality Sweets has served the Iselin community since 2003 with Indian sweets, snacks, and familiar flavors for celebrations and everyday enjoyment. Our snack collection is designed for customers who know exactly what they are looking for as well as those who want to discover something new. Browse the products above to see what is currently available; product pages show the size, price, and fulfillment information for each item.</p>
  <p>Many eligible snacks can be ordered online for delivery across the USA. Availability and shipping options vary by product, so review the product page before checkout for the current information. For local shopping and pickup, Quality Sweets is at 1384 Oak Tree Road, Iselin, NJ 08830, open daily from 10 AM to 8 PM. If you are planning a gift or gathering, browse our <a href="/mithai-box/">mithai boxes and sweet gift baskets</a> for a ready-to-share option.</p>`,
  faq: {
    title: "Indian Snacks &amp; Namkeen FAQ",
    items: [
      { q: "What is namkeen?", a: "Namkeen is a broad term for savory Indian snacks. Flavors and ingredients vary by item, so review the individual product page for the current details." },
      { q: "Can I order Indian snacks online?", a: "Many eligible snacks can be ordered online for delivery across the USA. Check each product page for current availability and fulfillment options." },
      { q: "What Indian snacks pair well with chai?", a: "Crisp savory namkeen and sweet-and-salty treats are popular chai-time choices. Browse the live catalog for the flavors currently available." },
      { q: "Can I buy snacks locally in Iselin?", a: "Yes. Quality Sweets is at 1384 Oak Tree Road, Iselin, NJ 08830, and is open daily from 10 AM to 8 PM." },
    ],
  },
});

const giftBoxes = categoryDescription({
  prefix: "qs-gift-boxes",
  heading: "Luxury Mithai Boxes & Sweet Gift Baskets",
  intro: "Share a memorable Indian sweets gift with luxury mithai boxes and sweet gift baskets for Diwali, weddings, corporate gifting, thank-yous, and family celebrations. Browse the current assortment to find a box that fits your occasion.",
  links: [
    { href: "/indian-sweets/", label: "All Indian Sweets" },
    { href: "/bengali-sweets/", label: "Bengali Sweets" },
    { href: "/catering/", label: "Wedding &amp; Event Orders" },
  ],
  body: `  <h2>Indian Mithai Gift Boxes for Every Meaningful Occasion</h2>
  <p>A mithai box is a generous way to mark a holiday, thank a host, welcome a new neighbor, or bring something special to a family celebration. Quality Sweets offers Indian sweet gift boxes and baskets built around the flavors people love to share: classic mithai, nut-based favorites, Bengali sweets, and assorted treats. Browse the live products above to see the current gift-box styles, sizes, prices, and availability.</p>
  <p>Gift giving is often about making the recipient feel remembered. A well-chosen assortment gives them several flavors to enjoy and makes the moment feel festive without needing an elaborate occasion. Choose an option that suits the people and moment you have in mind, whether it is a Diwali gathering, a wedding celebration, a client thank-you, a housewarming, or a simple visit with family and friends. Product pages provide the current assortment details so you can order with confidence.</p>

  <h2>Choose a Sweet Gift That Fits the Moment</h2>
  <div class="qs-gift-boxes-grid">
    <article class="qs-gift-boxes-card"><h3>Diwali Sweets &amp; Festival Gifting</h3><p>Share an Indian sweets gift box for Diwali, puja, or a seasonal gathering. The live catalog shows the current festive options and sizes.</p></article>
    <article class="qs-gift-boxes-card"><h3>Wedding &amp; Return Gifts</h3><p>For wedding favors and larger gift needs, explore the current boxes or visit our <a href="/catering/">catering and event orders page</a> to request a quote.</p></article>
    <article class="qs-gift-boxes-card"><h3>Corporate &amp; Thank-You Gifts</h3><p>Choose a polished mithai assortment for clients, colleagues, hosts, and loved ones when a standard gift does not feel personal enough.</p></article>
  </div>

  <h2>Fresh Indian Sweets from Iselin, NJ</h2>
  <p>Quality Sweets has served the Iselin community since 2003 with vegetarian Indian sweets made fresh daily and with no preservatives. We know a gift box has to arrive with the care and quality the occasion deserves. That is why the individual product page is the best source for each box's current selection, size, price, and fulfillment details. You can also create a more personal assortment by browsing <a href="/indian-sweets/">All Indian Sweets</a>, <a href="/bengali-sweets/">Bengali Sweets</a>, and <a href="/barfi/">Barfi &amp; Kaju Katli</a>.</p>
  <p>Many eligible gift boxes can be ordered online for delivery across the USA. Shippable orders are packed in insulated packaging with cold gel packs to help protect freshness in transit. Because availability and handling needs vary by product, check the product page before checkout for the current fulfillment options. For local pickup, visit Quality Sweets at 1384 Oak Tree Road, Iselin, NJ 08830, open daily from 10 AM to 8 PM.</p>`,
  faq: {
    title: "Mithai Gift Boxes FAQ",
    items: [
      { q: "What occasions are mithai boxes good for?", a: "Mithai boxes are popular for Diwali, weddings, thank-yous, corporate gifts, housewarmings, puja, and family celebrations." },
      { q: "Can I ship mithai gift boxes across the USA?", a: "Many eligible gift boxes can ship nationwide in insulated packaging with cold gel packs. Review each product page for current shipping availability." },
      { q: "Do you offer wedding favors or larger gift orders?", a: "Yes. Visit our catering and event orders page to request a quote for wedding favors, return gifts, or a larger celebration." },
      { q: "Are the sweets in your gift boxes made fresh?", a: "Quality Sweets makes vegetarian Indian sweets fresh daily in Iselin, New Jersey, with no preservatives. The individual product page lists the current box details." },
    ],
  },
});

const updates = [
  {
    id: 1,
    expectedUrl: "/indian-snacks/",
    label: "Indian Snacks & Namkeen",
    description: snacks,
    page_title: "Traditional Indian Snacks & Namkeen Online | Quality Sweets",
    meta_description: "Shop traditional Indian snacks and namkeen online. Discover crisp savory favorites and chai-time treats from Quality Sweets, with nationwide delivery on eligible items.",
    search_keywords: "indian snacks, namkeen, indian namkeen, chai snacks, savory indian snacks, indian snacks online",
  },
  {
    id: 14,
    expectedUrl: "/mithai-box/",
    label: "Mithai Boxes & Gift Baskets",
    description: giftBoxes,
    page_title: "Luxury Mithai Gift Boxes & Indian Sweet Baskets | Quality Sweets",
    meta_description: "Shop luxury mithai gift boxes and Indian sweet baskets for Diwali, weddings, corporate gifts, and celebrations. Nationwide delivery on eligible boxes.",
    search_keywords: "mithai box, mithai gift box, indian sweet gift box, diwali sweets, indian gift baskets, mithai gifts",
  },
];

function contentH1Count(html) {
  return (html.match(/<h1\b/gi) || []).length;
}

function categoriesH2Count(html) {
  return (html.match(/<h2\b[^>]*>\s*Categories\s*<\/h2>/gi) || []).length;
}

const apply = process.argv.includes("--apply");
for (const update of updates) {
  const category = (await bcFetch(`/catalog/categories/${update.id}`)).data;
  if (category.custom_url?.url !== update.expectedUrl) {
    throw new Error(`Category ${update.id} URL is ${category.custom_url?.url || "missing"}; expected ${update.expectedUrl}. Refusing to update.`);
  }

  const products = (await bcFetch(`/catalog/products?categories:in=${update.id}&limit=250&include_fields=id,name,custom_url`)).data;
  const wordCount = update.description.replace(/<[^>]+>/g, " ").match(/[A-Za-z]+(?:[-'][A-Za-z]+)*/g).length;
  if (contentH1Count(update.description) !== 0) throw new Error(`${update.label} content must not include an H1.`);
  if (categoriesH2Count(update.description) !== 0) throw new Error(`${update.label} content must not include an H2 named Categories.`);

  console.log(`Category ${category.id}: ${category.name} (${category.custom_url.url})`);
  console.log("Current description length:", category.description.length);
  console.log("Products currently assigned:", products.map((product) => `${product.id}: ${product.name}`).join(" | "));
  console.log("Prepared content word count:", wordCount);
  console.log("Prepared content H1 tags:", contentH1Count(update.description));
  console.log("Prepared H2 'Categories' tags:", categoriesH2Count(update.description));

  if (!apply) continue;
  const result = (await bcFetch(`/catalog/categories/${update.id}`, {
    method: "PUT",
    body: JSON.stringify({
      description: update.description,
      page_title: update.page_title,
      meta_description: update.meta_description,
      search_keywords: update.search_keywords,
    }),
  })).data;

  if (
    result.description !== update.description ||
    result.page_title !== update.page_title ||
    result.meta_description !== update.meta_description ||
    contentH1Count(result.description) !== 0 ||
    categoriesH2Count(result.description) !== 0
  ) {
    throw new Error(`BigCommerce response did not pass the SEO validation for Category ID ${update.id}.`);
  }
  console.log(`Updated Category ${result.id} successfully.`);
}

if (!apply) console.log("Dry run complete. Use --apply to update Category IDs 1 and 14.");
