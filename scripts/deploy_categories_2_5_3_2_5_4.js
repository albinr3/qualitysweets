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

function categoryDescription({ prefix, h1, intro, body, faq }) {
  return `<style>
#CategoryHeading > .TitleHeading { display: none !important; }
#CategoryHeading .SubCategoryList, #CategoryHeading .SubCategoryListGrid { display: none !important; }
.${prefix}-intro, .${prefix}-seo { box-sizing: border-box; font-family: Arial, Helvetica, sans-serif; }
.${prefix}-intro { margin: 0 0 24px; text-align: center; }
.${prefix}-intro h1 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: clamp(2rem, 4vw, 3.05rem); line-height: 1.15; margin: 0 0 10px; }
.${prefix}-intro p { color: #544142; font-size: 1.03rem; line-height: 1.6; margin: 0 auto; max-width: 760px; }
.${prefix}-links { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 18px auto 0; }
.${prefix}-links a { background: #fffaf1; border: 1px solid #d9b778; border-radius: 999px; color: #6d1427 !important; display: inline-block; font-size: .93rem; font-weight: 700; padding: 10px 16px; text-decoration: none !important; }
.${prefix}-links a:hover, .${prefix}-card-cta:hover { background: #45101b; color: #fff !important; }
.${prefix}-seo { border-top: 1px solid #eadcc4; color: #4f4142; margin: 42px 0 24px; padding: 36px 0 8px; }
.${prefix}-seo h2 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: clamp(1.55rem, 3vw, 2.15rem); line-height: 1.2; margin: 0 0 12px; }
.${prefix}-seo h3 { color: #6d1427; font-family: Georgia, 'Times New Roman', serif; font-size: 1.2rem; margin: 0 0 7px; }
.${prefix}-seo p { font-size: 1rem; line-height: 1.7; margin: 0 0 17px; }
.${prefix}-grid { display: grid; gap: 16px; grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 21px 0 28px; }
.${prefix}-card { background: #fffaf1; border: 1px solid #eadcc4; border-radius: 10px; padding: 19px; }
.${prefix}-card p { font-size: .94rem; margin: 0; }
.${prefix}-card a { color: #6d1427; font-weight: 700; }
.${prefix}-faq { border-top: 1px solid #eadcc4; margin-top: 26px; }
.${prefix}-faq details { border-bottom: 1px solid #eadcc4; padding: 14px 0; }
.${prefix}-faq summary { color: #6d1427; cursor: pointer; font-family: Georgia, 'Times New Roman', serif; font-size: 1.08rem; font-weight: 700; }
.${prefix}-faq p { font-size: .95rem; margin: 10px 0 0; }
.qs-navigation-heading { border-bottom: 1px dashed #D9D6C8; color: #840B17; display: block; font-size: 24px; font-weight: 700; margin: 0; padding: 0 0 10px; }
@media (max-width: 640px) { .${prefix}-grid { grid-template-columns: 1fr; } .${prefix}-links a { width: 100%; } }
</style>

<section class="${prefix}-intro" aria-labelledby="${prefix}-title">
  <h1 id="${prefix}-title">${h1}</h1>
  <p>${intro}</p>
  <nav class="${prefix}-links" aria-label="Explore related Indian sweet collections">
    <a href="/indian-sweets/">All Indian Sweets</a>
    <a href="/bengali-sweets/">Bengali Sweets</a>
    <a href="/traditional-mithai/">Traditional Mithai</a>
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
    var seoContent = document.querySelector('.${prefix}-seo');
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
}

const barfi = categoryDescription({
  prefix: "qs-barfi",
  h1: "Premium Indian Barfi &amp; Pure Kaju Katli",
  intro: "Shop rich Indian barfi, pure Kaju Katli, milk cake, and classic khoya sweets made fresh in Iselin, New Jersey. Eligible items ship nationwide in insulated packaging.",
  body: `  <h2>Pure Kaju Katli &amp; Indian Barfi Made for Sharing</h2>
  <p>Barfi, also spelled burfi, is one of the most recognizable Indian sweets: rich, smooth, and made to be shared at celebrations, family gatherings, and everyday chai. At Quality Sweets, our Barfi and Kaju Katli collection brings together classic milk-based mithai and cashew-forward favorites made in-house in Iselin, New Jersey. From the first bite, these are the sweets people reach for when they want a creamy texture, a fragrant note of cardamom or saffron, or the unmistakable taste of pure cashew.</p>
  <p>Kaju Katli is prized for its delicate, melt-in-the-mouth texture and clean cashew flavor. Indian barfi has a wider family of styles, including milk-forward khoya sweets, pista and almond varieties, and richer chocolate or layered treats. Our catalog lets you browse the current selection and choose the flavors that fit your occasion. Every product page shows the available size, current price, and fulfillment information, helping you build an assortment with confidence.</p>

  <h2>Find Your Favorite Barfi &amp; Kaju Sweet</h2>
  <div class="qs-barfi-grid">
    <article class="qs-barfi-card"><h3>Pure Kaju Katli</h3><p>A timeless cashew mithai for gifts, puja, family tables, and celebrations. Look for the current Kaju Katli options in the catalog above.</p></article>
    <article class="qs-barfi-card"><h3>Khoya &amp; Milk Sweets</h3><p>Explore milk cake, kalakand, and other khoya-based sweets when you prefer a rich, creamy, milk-forward barfi experience.</p></article>
    <article class="qs-barfi-card"><h3>Nut &amp; Specialty Barfi</h3><p>Choose pista, almond, chocolate, or specialty varieties to add contrast to a mixed mithai order or a thoughtful gift box.</p></article>
  </div>

  <h2>Fresh Mithai from Our Iselin Sweet Shop</h2>
  <p>Quality Sweets has served the Iselin community since 2003 with vegetarian Indian sweets made fresh daily and with no preservatives. Our barfi is a natural choice when you want a box of sweets for guests, a holiday gathering, or a gift that feels both traditional and generous. Combine Kaju Katli with <a href="/bengali-sweets/">Bengali sweets</a> for a variety of soft and nutty textures, or add <a href="/traditional-mithai/">traditional mithai</a> for ladoos, pedas, and other familiar classics.</p>
  <p>Many eligible sweets can be ordered online for delivery across the USA. Shippable orders are packed in insulated packaging with cold gel packs to help protect freshness on the way. Because each sweet has its own handling requirements, review the individual product page before checkout to confirm current availability and fulfillment. Some delicate sweets may be offered for Iselin store pickup only so they can be enjoyed as our kitchen intended.</p>
  <p>For local pickup, Quality Sweets is located at 1384 Oak Tree Road, Iselin, NJ 08830, and is open daily from 10 AM to 8 PM. Browse the products above for current favorites, or return to <a href="/indian-sweets/">All Indian Sweets</a> to make a complete mithai assortment for your next celebration.</p>`,
  faq: {
    title: "Barfi &amp; Kaju Katli FAQ",
    items: [
      { q: "What is the difference between barfi and Kaju Katli?", a: "Kaju Katli is a cashew-based Indian sweet. Barfi is a broader family of mithai that can be made with milk, khoya, nuts, or other ingredients." },
      { q: "Are your barfi sweets made fresh?", a: "Yes. Quality Sweets makes mithai fresh daily in Iselin, New Jersey, with no preservatives." },
      { q: "Can I order Kaju Katli online?", a: "Many eligible sweets can ship nationwide. Please check the individual product page for current availability and fulfillment details." },
      { q: "Do you offer barfi for pickup in Iselin?", a: "Pickup availability is shown on each product page. Quality Sweets is at 1384 Oak Tree Road in Iselin and is open daily from 10 AM to 8 PM." }
    ]
  }
});

const traditional = categoryDescription({
  prefix: "qs-traditional",
  h1: "Traditional Indian Mithai &amp; Fresh Ladoos",
  intro: "Discover traditional Indian mithai made fresh in Iselin, New Jersey: ladoos, pedas, jalebi, gulab jamun, and more classic sweets for sharing and celebrations.",
  body: `  <h2>Traditional Indian Mithai for Every Celebration</h2>
  <p>Traditional Indian mithai turns an ordinary visit, festival, prayer, or family gathering into something worth sharing. At Quality Sweets, our collection includes the classics people look for first: ladoos, pedas, jalebi, gulab jamun, gujia, and other familiar Indian desserts. Made in-house in Iselin, New Jersey, these sweets bring together the rich textures, warm spices, and celebratory character that make mithai part of so many meaningful moments.</p>
  <p>Whether you are choosing a box for guests, preparing for a puja, or looking for a favorite from childhood, the collection makes it easy to browse the current options. Ladoos offer a round, celebratory bite; pedas are soft and milk-forward; jalebi brings its crisp, syrupy character; and gulab jamun is known for its tender texture and aromatic sweetness. Product pages show the live selection, sizes, price, and fulfillment details, so you can choose what suits your table.</p>

  <h2>Classic Indian Sweets to Know &amp; Share</h2>
  <div class="qs-traditional-grid">
    <article class="qs-traditional-card"><h3>Ladoos</h3><p>Explore Motichur, Besan, and other ladoo favorites for celebrations, prayers, gifts, and sweet everyday moments.</p></article>
    <article class="qs-traditional-card"><h3>Pedas, Jalebi &amp; Milk Sweets</h3><p>Choose creamy pedas or look for fresh jalebi and other milk-based classics when you want a familiar traditional dessert.</p></article>
    <article class="qs-traditional-card"><h3>Gulab Jamun, Gujia &amp; More</h3><p>Round out an assorted order with syrup-soaked sweets, festival favorites, and other traditional mithai from the current catalog.</p></article>
  </div>

  <h2>Fresh Mithai Made in Iselin Since 2003</h2>
  <p>Quality Sweets has served the Iselin community since 2003 with vegetarian Indian sweets made fresh daily and with no preservatives. Traditional mithai is at the heart of that work: it is what families bring home for guests, send with relatives, and place on a table during celebrations. The collection is designed to help you find the flavors you know while also making space to try something new.</p>
  <p>Many eligible Indian sweets are available to order online for delivery across the USA. Shippable items are packed in insulated packaging with cold gel packs to help protect freshness in transit. Availability varies by product, so open the individual product page before checkout to see its current fulfillment options. Some especially delicate or freshly prepared sweets may be available for Iselin store pickup only.</p>
  <p>For a more varied mithai box, pair these classics with <a href="/bengali-sweets/">Bengali Sweets</a> or <a href="/barfi/">Barfi &amp; Kaju Katli</a>. You can also return to <a href="/indian-sweets/">All Indian Sweets</a> to explore the complete collection. Local customers can visit Quality Sweets at 1384 Oak Tree Road, Iselin, NJ 08830, open daily from 10 AM to 8 PM.</p>`,
  faq: {
    title: "Traditional Mithai FAQ",
    items: [
      { q: "What is traditional Indian mithai?", a: "Mithai is the broad name for Indian sweets. This collection includes classics such as ladoos, pedas, jalebi, gulab jamun, gujia, and other familiar desserts." },
      { q: "Are your traditional sweets made fresh?", a: "Yes. Quality Sweets prepares mithai fresh daily in Iselin, New Jersey, with no preservatives." },
      { q: "Can I order ladoos and other mithai online?", a: "Many eligible products can ship nationwide. Review each product page for the current availability and fulfillment option." },
      { q: "Are all sweets available for nationwide shipping?", a: "No. Some delicate products may be offered only for pickup at our Iselin store to preserve their intended freshness." }
    ]
  }
});

const updates = [
  {
    id: 22,
    label: "Barfi & Kaju Katli",
    description: barfi,
    page_title: "Pure Kaju Katli & Indian Barfi Online | Handcrafted Burfi Delivery USA",
    meta_description: "Buy 100% pure cashew Kaju Katli & authentic Indian barfi. Made with pure khoya & real silver vark. No cheap flour fillers. Shipped fresh across the USA.",
    search_keywords: "kaju katli, barfi, burfi, indian barfi, indian burfi, kaju katli online",
  },
  {
    id: 2,
    label: "Traditional Mithai",
    description: traditional,
    page_title: "Traditional Indian Mithai | Fresh Ladoo, Jalebi & Pedas Online",
    meta_description: "Handcrafted traditional mithai since 2003. Golden Motichur Ladoo, Besan Ladoo, fresh crispy Jalebi, Kesar Peda & Gujia. Order online with USA fresh delivery.",
    search_keywords: "mithai, ladoo, jalebi, indian desserts, motichur ladoo, kesar peda, gulab jamun",
  },
];

const apply = process.argv.includes("--apply");
for (const update of updates) {
  const category = (await bcFetch(`/catalog/categories/${update.id}`)).data;
  const products = (await bcFetch(`/catalog/products?categories:in=${update.id}&limit=250&include_fields=id,name,custom_url`)).data;
  const wordCount = update.description.replace(/<[^>]+>/g, " ").match(/[A-Za-z]+(?:[-'][A-Za-z]+)*/g).length;
  console.log(`Category ${update.id}: ${category.name} (${category.custom_url.url})`);
  console.log("Current description length:", category.description.length);
  console.log("Products currently assigned:", products.map((product) => `${product.id}: ${product.name}`).join(" | "));
  console.log("Prepared content word count:", wordCount);

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
  if (result.description !== update.description || result.page_title !== update.page_title || result.meta_description !== update.meta_description) {
    throw new Error(`BigCommerce response did not match the requested update for Category ID ${update.id}.`);
  }
  console.log(`Updated Category ${result.id} successfully.`);
}

if (!apply) console.log("Dry run complete. Use --apply to update Category IDs 22 and 2.");
