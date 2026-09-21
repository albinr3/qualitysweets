/**
 * Publishes GA4 and interaction events in the verified global-code provider
 * used by this Legacy Blueprint store. BigCommerce's native GA4 provider is
 * unavailable on Blueprint, so it is intentionally not enabled here.
 * Run without --apply for a dry-run. The Script Manager experiment is removed
 * to prevent future duplicate events.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const APPLY = process.argv.includes("--apply");
const MEASUREMENT_ID = "G-34WFEPDKY8";
const GLOBAL_CODE_PROVIDER_ID = 6;
const AFFILIATE_CONVERSION_PROVIDER_ID = 7;
const SCRIPT_MANAGER_NAME = "Quality Sweets GA4 Interaction Events";

function loadEnv() {
  const envPath = path.join(ROOT, ".env");
  if (!fs.existsSync(envPath)) return;
  for (const sourceLine of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const line = sourceLine.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const separator = line.indexOf("=");
    process.env[line.slice(0, separator).trim()] = line.slice(separator + 1).trim().replace(/^['"]|['"]$/g, "");
  }
}

loadEnv();
const storeHash = process.env.BIGCOMMERCE_STORE_HASH;
const accessToken = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const clientId = process.env.BIGCOMMERCE_CLIENT_ID;
if (!storeHash || !accessToken) throw new Error("Missing BigCommerce credentials in .env.");

const headers = { "X-Auth-Token": accessToken, Accept: "application/json", "Content-Type": "application/json" };
if (clientId) headers["X-Auth-Client"] = clientId;

async function api(pathname, options = {}) {
  const response = await fetch(`https://api.bigcommerce.com/stores/${storeHash}${pathname}`, { headers, ...options });
  const body = await response.text();
  if (!response.ok) throw new Error(`${options.method || "GET"} ${pathname} failed (${response.status}): ${body}`);
  return body ? JSON.parse(body).data : null;
}

const interactionCode = String.raw`<!-- Google tag (gtag.js) - Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}"></script>
<script id="qs-ga4-interaction-events-v2">
(function () {
  "use strict";
  var startedCateringQuote = false;
  window.dataLayer = window.dataLayer || [];
  function gtag(){window.dataLayer.push(arguments);}
  window.gtag = window.gtag || gtag;
  window.gtag("js", new Date());
  window.gtag("config", "${MEASUREMENT_ID}");

  function pageType() {
    var currentPath = window.location.pathname.toLowerCase();
    if (currentPath.indexOf("/catering/") === 0) return "catering";
    if (currentPath.indexOf("/menu/") === 0) return "takeout_menu";
    if (currentPath.indexOf("/locations/") === 0) return "location";
    if (currentPath === "/contact-us/") return "contact";
    if (document.querySelector('meta[property="og:type"][content="product"]')) return "product";
    return "storefront";
  }

  function send(name, params) {
    var eventParams = params || {};
    eventParams.page_type = eventParams.page_type || pageType();
    if (typeof window.gtag === "function") {
      window.gtag("event", name, eventParams);
      return;
    }
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(["event", name, eventParams]);
  }

  function ctaLocation(link) {
    if (link.closest("header")) return "header";
    if (link.closest("footer")) return "footer";
    if (link.closest(".qs-catering")) return "catering_content";
    if (link.closest(".qs-menu")) return "takeout_menu_content";
    return "page_content";
  }

  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("a[href]");
    if (!link) return;
    var href = link.getAttribute("href") || "";
    var lowerHref = href.toLowerCase();
    var params = { cta_location: ctaLocation(link) };
    if (lowerHref.indexOf("tel:") === 0) send("click_call_store", params);
    else if (lowerHref.indexOf("mailto:orders@qualitysweetsnj.com") === 0) send("click_email_orders", params);
    else if (lowerHref.indexOf("maps.app.goo.gl") !== -1 || lowerHref.indexOf("google.com/maps") !== -1) send("click_directions", params);
    else if (lowerHref.indexOf("cart.php?action=add") !== -1) {
      var directProductMatch = lowerHref.match(/[?&]product_id=(\d+)/);
      send("add_to_cart", { cta_location: ctaLocation(link), items: directProductMatch ? [{ item_id: directProductMatch[1] }] : [] });
    }
    else if (lowerHref.indexOf("checkout.php") !== -1) send("begin_checkout", params);
  });

  function productItem(form) {
    if (!form) return null;
    var input = form.querySelector('input[name="product_id"]');
    if (!input || !input.value) return null;
    var heading = document.querySelector('#ProductDetails h1, .PrimaryProductDetails h1, h1');
    var item = { item_id: input.value };
    if (heading && heading.textContent.trim()) item.item_name = heading.textContent.trim();
    return item;
  }

  function setupEcommerceEvents() {
    var productForm = document.getElementById("productDetailsAddToCartForm");
    var item = productItem(productForm);
    if (item) {
      send("view_item", { items: [item] });
      productForm.addEventListener("submit", function () { send("add_to_cart", { items: [item] }); });
    }
    if (window.location.pathname.toLowerCase().indexOf("/cart.php") === 0 && window.location.search.toLowerCase().indexOf("action=add") === -1) send("view_cart", { items: [] });
  }

  function setupCateringForm() {
    var cateringForm = document.getElementById("b2b-catering-form");
    if (!cateringForm) return;
    cateringForm.addEventListener("focusin", function () {
      if (startedCateringQuote) return;
      startedCateringQuote = true;
      send("catering_quote_start", { cta_location: "catering_form" });
    });
    cateringForm.addEventListener("change", function (event) {
      var target = event.target;
      if (!target || (target.name !== "event_type" && target.name !== "service")) return;
      send("select_catering_service", { cta_location: "catering_form", service_type: target.value || "unspecified" });
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { setupCateringForm(); setupEcommerceEvents(); });
  else { setupCateringForm(); setupEcommerceEvents(); }
  if (window.location.pathname.toLowerCase().indexOf("/menu/") === 0) send("view_takeout_menu", { cta_location: "page_load" });
}());
</script>`;

const purchaseCode = String.raw`<script id="qs-ga4-purchase-v2">
(function () {
  "use strict";
  var orderId1 = String("%%ORDER_ID%%").trim();
  var orderId2 = String("%%GLOBAL_OrderId%%").trim();
  var transactionId = (orderId1 && orderId1.indexOf("%%") === -1) ? orderId1 : ((orderId2 && orderId2.indexOf("%%") === -1) ? orderId2 : "");
  if (!transactionId) {
    try {
      var match = window.location.pathname.match(/\/order-confirmation\/(\d+)/i) || (window.location.search && window.location.search.match(/[?&]order_?id=(\d+)/i));
      if (match) transactionId = match[1];
    } catch (e) {}
  }

  var amount1 = String("%%ORDER_AMOUNT%%").trim();
  var amount2 = String("%%GLOBAL_OrderAmount%%").trim();
  var rawAmount = (amount1 && amount1.indexOf("%%") === -1) ? amount1 : ((amount2 && amount2.indexOf("%%") === -1) ? amount2 : "");
  var value = Number(rawAmount.replace(/[^0-9.-]/g, ""));

  if (!transactionId || transactionId.indexOf("%%") !== -1 || !Number.isFinite(value) || value < 0) return;
  var storageKey = "qs_ga4_purchase_" + transactionId;
  try { if (window.sessionStorage && sessionStorage.getItem(storageKey)) return; } catch (error) {}
  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== "function") {
    window.gtag = function () { window.dataLayer.push(arguments); };
    var tag = document.createElement("script");
    tag.async = true;
    tag.src = "https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}";
    document.head.appendChild(tag);
    window.gtag("js", new Date());
    window.gtag("config", "${MEASUREMENT_ID}", { send_page_view: false });
  }
  window.gtag("event", "purchase", { transaction_id: transactionId, value: value, currency: "USD" });
  try { if (window.sessionStorage) sessionStorage.setItem(storageKey, "1"); } catch (error) {}
}());
</script>`;

const desiredGlobalCode = { code: interactionCode, enabled: true, data_tag_enabled: false };
const desiredAffiliateCode = { code: purchaseCode, enabled: true, data_tag_enabled: false };

const providers = await api("/v3/settings/analytics");
const globalCode = providers.find((provider) => provider.id === GLOBAL_CODE_PROVIDER_ID);
const affiliateCode = providers.find((provider) => provider.id === AFFILIATE_CONVERSION_PROVIDER_ID);
if (!globalCode || !affiliateCode) throw new Error("Expected BigCommerce analytics providers were not found.");
const scripts = await api("/v3/content/scripts");
const legacyScript = scripts.find((script) => script.name === SCRIPT_MANAGER_NAME);

const actions = [];
if (["code", "enabled", "data_tag_enabled"].some((field) => globalCode[field] !== desiredGlobalCode[field])) actions.push("update global interaction code");
if (["code", "enabled", "data_tag_enabled"].some((field) => affiliateCode[field] !== desiredAffiliateCode[field])) actions.push("enable order-confirmation purchase code");
if (legacyScript) actions.push("remove inactive Script Manager duplicate");
console.log(`DRY RUN: ${JSON.stringify({ analytics: actions.length, actions })}.`);
if (!APPLY || actions.length === 0) process.exitCode = 0;
else {
  const backupDirectory = path.join(__dirname, "backups");
  fs.mkdirSync(backupDirectory, { recursive: true });
  const backupPath = path.join(backupDirectory, `ga4-native-before-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
  fs.writeFileSync(backupPath, JSON.stringify({ captured_at: new Date().toISOString(), providers: { globalCode, affiliateCode }, scriptManager: legacyScript || null }, null, 2));
  if (actions.includes("update global interaction code")) await api(`/v3/settings/analytics/${GLOBAL_CODE_PROVIDER_ID}`, { method: "PUT", body: JSON.stringify(desiredGlobalCode) });
  if (actions.includes("enable order-confirmation purchase code")) await api(`/v3/settings/analytics/${AFFILIATE_CONVERSION_PROVIDER_ID}`, { method: "PUT", body: JSON.stringify(desiredAffiliateCode) });
  if (legacyScript) await api(`/v3/content/scripts/${legacyScript.uuid}`, { method: "DELETE" });
  console.log(`APPLY: ${actions.join("; ")}. Backup: ${path.relative(ROOT, backupPath)}`);
}
