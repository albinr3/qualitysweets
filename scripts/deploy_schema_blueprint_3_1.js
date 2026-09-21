/**
 * Publishes server-rendered JSON-LD through content fields supported by the
 * legacy BigCommerce Blueprint / Coffee theme. Run without --apply to inspect
 * every proposed change. With --apply, a timestamped API-content backup is
 * written to scripts/backups before production updates begin.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DOMAIN = "https://qualitysweetsnj.com";
const WEBSITE_ID = `${DOMAIN}/#website`;
const BUSINESS_ID = `${DOMAIN}/#business`;
const BANNER_ID = 5;
const CATERING_CATEGORY_ID = 21;
const TAKEOUT_CATEGORY_ID = 15;
const CONTACT_PATH = "/contact-us/";
const LOCATION_PATH = "/locations/iselin-nj/";
const APPLY = process.argv.includes("--apply");
const productLimitArgument = process.argv.find((argument) => argument.startsWith("--product-limit="));
const productOffsetArgument = process.argv.find((argument) => argument.startsWith("--product-offset="));
const PRODUCT_LIMIT = productLimitArgument ? Number(productLimitArgument.split("=")[1]) : Infinity;
const PRODUCT_OFFSET = productOffsetArgument ? Number(productOffsetArgument.split("=")[1]) : 0;

function loadEnv() {
  const envPath = path.join(ROOT, ".env");
  if (!fs.existsSync(envPath)) return;
  for (const raw of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const index = line.indexOf("=");
    process.env[line.slice(0, index).trim()] = line.slice(index + 1).trim().replace(/^['"]|['"]$/g, "");
  }
}

loadEnv();
const STORE_HASH = process.env.BIGCOMMERCE_STORE_HASH;
const ACCESS_TOKEN = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const CLIENT_ID = process.env.BIGCOMMERCE_CLIENT_ID;
if (!STORE_HASH || !ACCESS_TOKEN) throw new Error("Missing BigCommerce credentials in .env.");

const API_ROOT = `https://api.bigcommerce.com/stores/${STORE_HASH}`;
const headers = { "X-Auth-Token": ACCESS_TOKEN, Accept: "application/json", "Content-Type": "application/json" };
if (CLIENT_ID) headers["X-Auth-Client"] = CLIENT_ID;

function delay(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function api(pathname, options = {}, attempt = 0) {
  const response = await fetch(`${API_ROOT}${pathname}`, { headers, ...options });
  const text = await response.text();
  if (response.status === 429 && attempt < 5) {
    const retryAfter = Number(response.headers.get("retry-after"));
    await delay(Number.isFinite(retryAfter) && retryAfter > 0 ? retryAfter * 1000 : 2000 * (attempt + 1));
    return api(pathname, options, attempt + 1);
  }
  const body = text ? JSON.parse(text) : {};
  if (!response.ok) throw new Error(`${options.method || "GET"} ${pathname} failed (${response.status}): ${text}`);
  return body.data ?? body;
}

function absoluteUrl(url) {
  if (!url) return DOMAIN;
  return url.startsWith("http") ? url : `${DOMAIN}${url.startsWith("/") ? "" : "/"}${url}`;
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function managedScript(id, value) {
  const json = JSON.stringify(value).replace(/<\/script/gi, "<\\/script");
  return `<script id="${id}" type="application/ld+json">${json}</script>`;
}

function withSchema(html, id, value) {
  const pattern = new RegExp(`\\s*<script\\s+id=["']${escapeRegExp(id)}["'][^>]*>.*?<\\/script>`, "gis");
  return `${String(html || "").replace(pattern, "").trim()}\n${managedScript(id, value)}`;
}

function sameHtml(left, right) {
  const normalize = (value) => String(value || "")
    .replace(/\r\n/g, "\n")
    .replace(/%%GLOBAL_ShopPathSSL%%/g, DOMAIN)
    .trim();
  return normalize(left) === normalize(right);
}

function textFromHtml(html) {
  return String(html || "")
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/g, "'")
    .replace(/\s+/g, " ")
    .trim();
}

function businessNode() {
  return {
    "@type": ["FoodEstablishment", "OnlineStore"],
    "@id": BUSINESS_ID,
    name: "Quality Sweets - Indian Sweets Shop",
    alternateName: ["Quality Sweets", "Quality Sweets NJ"],
    url: `${DOMAIN}/`,
    image: "https://cdn10.bigcommerce.com/s-2ygwtj/products/176/images/410/quality-sweets-iselin-storefront-oak-tree-road__61587.1789245785.1280.1280.jpg?c=2",
    telephone: "+17322833799",
    priceRange: "$$",
    acceptsReservations: false,
    hasMenu: `${DOMAIN}/menu/`,
    servesCuisine: ["Indian", "Bengali"],
    address: {
      "@type": "PostalAddress",
      streetAddress: "1384 Oak Tree Road",
      addressLocality: "Iselin",
      addressRegion: "NJ",
      postalCode: "08830",
      addressCountry: "US",
    },
    geo: { "@type": "GeoCoordinates", latitude: 40.5739404, longitude: -74.3261661 },
    openingHoursSpecification: [{
      "@type": "OpeningHoursSpecification",
      dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      opens: "10:00",
      closes: "20:00",
    }],
    sameAs: ["https://www.facebook.com/qualitysweetsnj", "https://www.instagram.com/qualitysweetsofoaktree/"],
    areaServed: { "@type": "Country", name: "United States" },
  };
}

function homepageSchema() {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        url: `${DOMAIN}/`,
        name: "Quality Sweets - Indian Sweets Shop",
        alternateName: ["Quality Sweets", "Quality Sweets NJ"],
        publisher: { "@id": BUSINESS_ID },
      },
      businessNode(),
    ],
  };
}

function breadcrumb(items, pageUrl) {
  return {
    "@type": "BreadcrumbList",
    "@id": `${pageUrl}#breadcrumb`,
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

function categorySchema(category, categories) {
  const ancestors = [];
  let current = category;
  while (current) {
    ancestors.unshift(current);
    current = current.parent_id ? categories.get(current.parent_id) : null;
  }
  const url = absoluteUrl(category.custom_url?.url);
  const crumbs = [{ name: "Home", url: `${DOMAIN}/` }, ...ancestors.map((item) => ({ name: item.name, url: absoluteUrl(item.custom_url?.url) }))];
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "CollectionPage",
        "@id": `${url}#collectionpage`,
        url,
        name: category.name,
        isPartOf: { "@id": WEBSITE_ID },
        breadcrumb: { "@id": `${url}#breadcrumb` },
      },
      breadcrumb(crumbs, url),
    ],
  };
}

function offerFor(item, productUrl, price, availability) {
  if (availability !== "available" || !Number.isFinite(Number(price)) || Number(price) <= 0) return null;
  return {
    "@type": "Offer",
    url: productUrl,
    priceCurrency: "USD",
    price: Number(price),
    availability: "https://schema.org/InStock",
    itemCondition: "https://schema.org/NewCondition",
  };
}

function productFields(product, productUrl, image, categoryName) {
  const fields = {
    "@type": "Product",
    name: product.name,
    url: productUrl,
    description: textFromHtml(product.description) || product.name,
  };
  if (image) fields.image = image;
  if (product.sku) fields.sku = product.sku;
  if (categoryName) fields.category = categoryName;
  return fields;
}

function productSchema(product, categories) {
  const url = absoluteUrl(product.custom_url?.url);
  const image = product.images?.find((item) => item.is_thumbnail)?.url_standard || product.images?.[0]?.url_standard || product.images?.[0]?.url_thumbnail;
  const categoryName = product.categories?.map((id) => categories.get(id)?.name).find(Boolean);
  const variants = (product.variants || []).filter((variant) => variant.sku || variant.id);

  if (variants.length <= 1) {
    const item = productFields(product, url, image, categoryName);
    const offer = offerFor(product, url, product.calculated_price ?? product.price, product.availability);
    if (offer) item.offers = offer;
    return { "@context": "https://schema.org", ...item };
  }

  const groupId = `${url}#productgroup`;
  const variantNodes = variants.map((variant) => {
    const labels = (variant.option_values || []).map((option) => option.label).filter(Boolean);
    const node = productFields({ ...product, name: labels.length ? `${product.name} — ${labels.join(", ")}` : product.name, sku: variant.sku || product.sku }, url, image, categoryName);
    node["@id"] = `${url}#variant-${variant.id}`;
    node.isVariantOf = { "@id": groupId };
    const offer = offerFor(variant, url, variant.calculated_price || variant.price || product.price, product.availability);
    if (offer) node.offers = offer;
    return node;
  });
  const variesBy = [...new Set(variants.flatMap((variant) => (variant.option_values || []).map((option) => option.option_display_name || option.display_name)).map((name) => String(name).toLowerCase()).filter((name) => name === "size" || name === "color").map((name) => `https://schema.org/${name}`))];
  const group = {
    "@type": "ProductGroup",
    "@id": groupId,
    name: product.name,
    url,
    productGroupID: product.sku || String(product.id),
    hasVariant: variantNodes.map((node) => ({ "@id": node["@id"] })),
  };
  if (variesBy.length) group.variesBy = variesBy;
  return { "@context": "https://schema.org", "@graph": [group, ...variantNodes] };
}

function contactSchema() {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "ContactPage",
        "@id": `${DOMAIN}${CONTACT_PATH}#contactpage`,
        url: `${DOMAIN}${CONTACT_PATH}`,
        name: "Contact Quality Sweets - Indian Sweets Shop",
        mainEntity: { "@id": BUSINESS_ID },
      },
      businessNode(),
    ],
  };
}

function locationSchema() {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebPage",
        "@id": `${DOMAIN}${LOCATION_PATH}#webpage`,
        url: `${DOMAIN}${LOCATION_PATH}`,
        name: "Quality Sweets - Indian Sweets Shop Iselin NJ Store",
        mainEntity: { "@id": BUSINESS_ID },
      },
      businessNode(),
    ],
  };
}

function pagePayload(page, body) {
  return {
    name: page.name,
    type: page.type,
    url: page.url,
    body,
    is_visible: page.is_visible,
    meta_title: page.meta_title || "",
    meta_description: page.meta_description || "",
  };
}

function bannerPayload(banner, content) {
  return {
    name: banner.name,
    content,
    page: banner.page,
    location: banner.location,
    date_type: banner.date_type,
    visible: String(banner.visible),
  };
}

function backup(changes) {
  const dir = path.join(__dirname, "backups");
  fs.mkdirSync(dir, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const target = path.join(dir, `schema-blueprint-before-${stamp}.json`);
  fs.writeFileSync(target, JSON.stringify(changes, null, 2), "utf8");
  return target;
}

async function main() {
  const [banner, pages, categoryResponse, products] = await Promise.all([
    api(`/v2/banners/${BANNER_ID}`),
    api("/v2/pages?limit=250"),
    api("/v3/catalog/categories?limit=250"),
    api("/v3/catalog/products?limit=250"),
  ]);
  const categories = new Map(categoryResponse.map((category) => [category.id, category]));
  const changes = [];
  const homeContent = withSchema(banner.content, "qs-schema-home-v1", homepageSchema());
  if (!sameHtml(homeContent, banner.content)) changes.push({ kind: "banner", id: BANNER_ID, before: banner.content, after: homeContent, payload: bannerPayload(banner, homeContent) });

  const cateringPath = path.join(ROOT, "content", "catering", "index.html");
  const cateringContent = fs.readFileSync(cateringPath, "utf8");
  const catering = categories.get(CATERING_CATEGORY_ID);
  if (!catering) throw new Error("Catering category 21 was not found.");
  if (!sameHtml(catering.description, cateringContent)) changes.push({ kind: "category", id: catering.id, before: catering.description, after: cateringContent, payload: { description: cateringContent } });

  for (const category of categoryResponse.filter((item) => item.is_visible && ![CATERING_CATEGORY_ID, TAKEOUT_CATEGORY_ID].includes(item.id))) {
    const content = withSchema(category.description, `qs-schema-category-${category.id}-v1`, categorySchema(category, categories));
    if (!sameHtml(content, category.description)) changes.push({ kind: "category", id: category.id, before: category.description, after: content, payload: { description: content } });
  }

  const pagesByPath = new Map(pages.filter((page) => page.url).map((page) => [page.url, page]));
  for (const [pagePath, id, generator] of [[CONTACT_PATH, "qs-schema-contact-v1", contactSchema], [LOCATION_PATH, "qs-schema-location-v1", locationSchema]]) {
    const summary = pagesByPath.get(pagePath);
    if (!summary) throw new Error(`Required CMS page was not found: ${pagePath}`);
    const page = await api(`/v2/pages/${summary.id}`);
    const content = withSchema(page.body, id, generator());
    if (!sameHtml(content, page.body)) changes.push({ kind: "page", id: page.id, before: page.body, after: content, payload: pagePayload(page, content) });
  }

  const visibleProducts = products
    .filter((product) => product.is_visible)
    .sort((left, right) => left.id - right.id)
    .slice(PRODUCT_OFFSET, PRODUCT_OFFSET + PRODUCT_LIMIT);
  for (const listed of visibleProducts) {
    const product = await api(`/v3/catalog/products/${listed.id}?include=images,variants`);
    const content = withSchema(product.description, `qs-schema-product-${product.id}-v1`, productSchema(product, categories));
    if (!sameHtml(content, product.description)) changes.push({ kind: "product", id: product.id, before: product.description, after: content, payload: { description: content } });
  }

  const summary = changes.reduce((result, change) => ({ ...result, [change.kind]: (result[change.kind] || 0) + 1 }), {});
  console.log(`${APPLY ? "APPLY" : "DRY RUN"}: ${JSON.stringify(summary)}; ${changes.length} changes prepared.`);
  if (!APPLY) return;
  const backupPath = backup(changes.map(({ kind, id, before }) => ({ kind, id, before })));
  console.log(`Backup written: ${backupPath}`);
  for (const change of changes) {
    const endpoint = change.kind === "banner" ? `/v2/banners/${change.id}` : change.kind === "page" ? `/v2/pages/${change.id}` : change.kind === "category" ? `/v3/catalog/categories/${change.id}` : `/v3/catalog/products/${change.id}`;
    await api(endpoint, { method: "PUT", body: JSON.stringify(change.payload) });
    console.log(`[OK] ${change.kind} ${change.id}`);
  }
}

main().catch((error) => {
  console.error(`[ERROR] ${error.message}`);
  process.exit(1);
});
