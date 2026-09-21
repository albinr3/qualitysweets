/**
 * Deploys the sitewide GA4 interaction instrumentation through BigCommerce
 * Script Manager. Run without --apply to inspect changes. The script does not
 * create a second Google tag: it sends events through the existing gtag()
 * configuration (G-34WFEPDKY8).
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const APPLY = process.argv.includes("--apply");
const INSPECT = process.argv.includes("--inspect");
const SCRIPT_NAME = "Quality Sweets GA4 Interaction Events";

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

const headers = {
  "X-Auth-Token": accessToken,
  Accept: "application/json",
  "Content-Type": "application/json",
};
if (clientId) headers["X-Auth-Client"] = clientId;

async function api(pathname, options = {}) {
  const response = await fetch(`https://api.bigcommerce.com/stores/${storeHash}${pathname}`, { headers, ...options });
  const body = await response.text();
  if (!response.ok) throw new Error(`${options.method || "GET"} ${pathname} failed (${response.status}): ${body}`);
  return body ? JSON.parse(body).data : null;
}

const html = String.raw`<script id="qs-ga4-interaction-events-v1">
(function () {
  "use strict";
  var startedCateringQuote = false;

  function pageType() {
    var path = window.location.pathname.toLowerCase();
    if (path.indexOf("/catering/") === 0) return "catering";
    if (path.indexOf("/menu/") === 0) return "takeout_menu";
    if (path.indexOf("/locations/") === 0) return "location";
    if (path === "/contact-us/") return "contact";
    if (document.querySelector('meta[property="og:type"][content="product"]')) return "product";
    return "storefront";
  }

  function send(name, params) {
    var eventParams = params || {};
    eventParams.page_type = eventParams.page_type || pageType();
    if (typeof window.gtag === "function") {
      window.gtag("event", name, eventParams);
    }
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

    if (lowerHref.indexOf("tel:") === 0) {
      send("click_call_store", params);
    } else if (lowerHref.indexOf("mailto:orders@qualitysweetsnj.com") === 0) {
      send("click_email_orders", params);
    } else if (lowerHref.indexOf("maps.app.goo.gl") !== -1 || lowerHref.indexOf("google.com/maps") !== -1) {
      send("click_directions", params);
    } else if (lowerHref.indexOf("checkout.php") !== -1) {
      send("begin_checkout", params);
    }
  });

  var cateringForm = document.getElementById("b2b-catering-form");
  if (cateringForm) {
    cateringForm.addEventListener("focusin", function () {
      if (startedCateringQuote) return;
      startedCateringQuote = true;
      send("catering_quote_start", { cta_location: "catering_form" });
    });
    cateringForm.addEventListener("change", function (event) {
      var target = event.target;
      if (!target || (target.name !== "event_type" && target.name !== "service")) return;
      var value = target.value || "unspecified";
      send("select_catering_service", { cta_location: "catering_form", service_type: value });
    });
  }

  if (window.location.pathname.toLowerCase().indexOf("/menu/") === 0) {
    send("view_takeout_menu", { cta_location: "page_load" });
  }
}());
</script>`;

const payload = {
  name: SCRIPT_NAME,
  description: "GA4 intent and funnel events. Uses the existing Google tag; no customer data is sent.",
  html,
  location: "footer",
  visibility: "storefront",
  kind: "script_tag",
  load_method: "default",
  consent_category: "analytics",
};

const currentScripts = await api("/v3/content/scripts");
const current = currentScripts.find((script) => script.name === SCRIPT_NAME);
if (INSPECT) {
  const analyticsProviders = await api("/v3/settings/analytics");
  console.log(JSON.stringify(current ? {
    uuid: current.uuid,
    name: current.name,
    location: current.location,
    visibility: current.visibility,
    kind: current.kind,
    load_method: current.load_method,
    consent_category: current.consent_category,
    html_length: current.html.length,
  } : null, null, 2));
  console.log(JSON.stringify({ analytics_providers: analyticsProviders }, null, 2));
}
const same = current && ["description", "html", "location", "visibility", "kind", "load_method", "consent_category"].every((field) => current[field] === payload[field]);

if (same) {
  console.log("DRY RUN: {}; 0 changes prepared.");
} else {
  const action = current ? "update" : "create";
  console.log(`DRY RUN: {"script":1}; prepared to ${action} \"${SCRIPT_NAME}\".`);
  if (APPLY) {
    const backupDirectory = path.join(__dirname, "backups");
    fs.mkdirSync(backupDirectory, { recursive: true });
    const backupPath = path.join(backupDirectory, `ga4-events-before-${new Date().toISOString().replace(/[:.]/g, "-")}.json`);
    fs.writeFileSync(backupPath, JSON.stringify({ captured_at: new Date().toISOString(), before: current || null }, null, 2));

    if (current) {
      await api(`/v3/content/scripts/${current.uuid}`, { method: "PUT", body: JSON.stringify(payload) });
    } else {
      await api("/v3/content/scripts", { method: "POST", body: JSON.stringify(payload) });
    }
    console.log(`APPLY: ${action}d \"${SCRIPT_NAME}\". Backup: ${path.relative(ROOT, backupPath)}`);
  }
}
