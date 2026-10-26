import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

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

if (!STORE_HASH || !ACCESS_TOKEN) {
  console.error("Error: Missing BigCommerce credentials in .env");
  process.exit(1);
}

const API_ROOT = `https://api.bigcommerce.com/stores/${STORE_HASH}/v3/catalog/products/93`;
const headers = {
  "X-Auth-Token": ACCESS_TOKEN,
  "Accept": "application/json",
  "Content-Type": "application/json",
};
if (CLIENT_ID) headers["X-Auth-Client"] = CLIENT_ID;

const APPLY = process.argv.includes("--apply");

const NEW_PAGE_TITLE = "Carrot Halwa (Gajar Ka Halwa) | Fresh Mithai | Quality Sweets";
const NEW_META_DESCRIPTION = "Handmade Gajar Ka Halwa made fresh with grated carrots, slow-cooked khoya, and pure ghee. No preservatives. Ships nationwide in insulated cold packs.";
const NEW_SEARCH_KEYWORDS = "gajar ka halwa, carrot halwa, gajrela, buy carrot halwa online, gajar halwa near me, indian carrot pudding, warm halwa";

const SCHEMA_JSON = {
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://qualitysweetsnj.com/carrot-halwa/#product",
  "name": "Carrot Halwa",
  "alternateName": [
    "Gajar Ka Halwa",
    "Gajar Halwa",
    "Gajrela"
  ],
  "url": "https://qualitysweetsnj.com/carrot-halwa/",
  "description": NEW_META_DESCRIPTION,
  "sku": "27",
  "image": [
    "https://cdn10.bigcommerce.com/s-2ygwtj/products/93/images/288/Carrot_halwa__62877.1790725932.1280.1280.jpg?c=2"
  ],
  "brand": {
    "@type": "Brand",
    "name": "Quality Sweets"
  },
  "category": "Traditional Mithai",
  "suitableForDiet": "https://schema.org/VegetarianDiet",
  "offers": {
    "@type": "Offer",
    "url": "https://qualitysweetsnj.com/carrot-halwa/",
    "priceCurrency": "USD",
    "price": 7.00,
    "priceValidUntil": "2027-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "seller": {
      "@type": "Organization",
      "name": "Quality Sweets",
      "url": "https://qualitysweetsnj.com/"
    },
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": {
        "@type": "MonetaryAmount",
        "value": "Calculated at checkout",
        "currency": "USD"
      },
      "shippingDestination": {
        "@type": "DefinedRegion",
        "addressCountry": "US"
      },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {
          "@type": "QuantitativeValue",
          "minValue": 1,
          "maxValue": 2,
          "unitCode": "d"
        },
        "transitTime": {
          "@type": "QuantitativeValue",
          "minValue": 1,
          "maxValue": 4,
          "unitCode": "d"
        }
      }
    },
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "US",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 2,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn"
    }
  }
};

const NEW_DESCRIPTION_HTML = `<div class="qs-product-content-wrapper" style="font-family: inherit; line-height: 1.6; color: #333;">
  <p style="font-size: 15px; margin-bottom: 16px;">
    Gajar Ka Halwa (also called Gajrela or Carrot Halwa) is slowly simmered in small batches at our Iselin shop using grated carrots, whole milk khoya, pure desi ghee, and cardamom. We make it fresh every day without canned carrots, artificial flavorings, or chemical preservatives.
  </p>

  <div style="background: #fdfbf7; border: 1px solid #ebdcc5; border-radius: 8px; padding: 14px 18px; margin: 18px 0;">
    <h3 style="color: #7a1526; font-size: 16px; margin: 0 0 10px 0; font-family: 'Marcellus', Georgia, serif;">Why Quality Sweets Carrot Halwa Stands Apart</h3>
    <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: #4a0e17;">
      <li><strong>Zero Chemical Preservatives:</strong> Prepared fresh from scratch daily in New Jersey.</li>
      <li><strong>Pure Ingredients:</strong> Whole milk solids (khoya), pure desi ghee, and natural cardamom.</li>
      <li><strong>100% Vegetarian:</strong> Strictly eggless, gelatin-free, and crafted following traditional purity standards.</li>
    </ul>
  </div>

  <h3 style="color: #7a1526; font-size: 16px; margin-top: 20px; font-family: 'Marcellus', Georgia, serif;">Serving &amp; Reheating Tips</h3>
  <p style="font-size: 14px;">
    Gajar Halwa is best eaten warm. Heat a portion in the microwave for 20 to 30 seconds to bring out the aroma of the ghee and cardamom. It pairs great with vanilla ice cream or after a savory meal.
  </p>

  <h3 style="color: #7a1526; font-size: 16px; margin-top: 20px; font-family: 'Marcellus', Georgia, serif;">Storage &amp; Freshness</h3>
  <p style="font-size: 14px;">
    Keep refrigerated between 38&deg;F and 42&deg;F. Because we use fresh dairy and zero preservatives, enjoy it within 7 to 10 days of delivery.
  </p>

  <div style="margin-top: 22px; border-top: 1px dashed #d4af37; padding-top: 14px;">
    <h3 style="color: #7a1526; font-size: 15px; margin-bottom: 8px; font-family: 'Marcellus', Georgia, serif;">Frequently Asked Questions</h3>
    <details style="margin-bottom: 8px; font-size: 13.5px; cursor: pointer;">
      <summary style="font-weight: bold; color: #4a0e17;">How does nationwide shipping work for Carrot Halwa?</summary>
      <p style="margin: 6px 0 0 16px; color: #555;">Orders ship Monday through Wednesday with food-grade gel ice packs in insulated boxes via FedEx Ground to ensure it arrives fresh without weekend transit delays.</p>
    </details>
    <details style="font-size: 13.5px; cursor: pointer;">
      <summary style="font-weight: bold; color: #4a0e17;">Can I combine Carrot Halwa with other sweets?</summary>
      <p style="margin: 6px 0 0 16px; color: #555;">Yes! You can order it alongside our fresh <a href="/traditional-mithai/" style="color: #7a1526; font-weight: bold; text-decoration: underline;">traditional Indian mithai</a> or include it in custom <a href="/mithai-box/" style="color: #7a1526; text-decoration: underline;">Mithai Gift Boxes</a>.</p>
    </details>
  </div>
</div>
<script id="qs-schema-product-93-v2" type="application/ld+json">
${JSON.stringify(SCHEMA_JSON, null, 2)}
</script>`;

async function run() {
  console.log("=== DESPLIEGUE SEO PILOTO: PRODUCTO 93 (CARROT HALWA) ===");
  console.log(`Modo: ${APPLY ? "APLICACIÓN EN PRODUCCIÓN (--apply)" : "DRY-RUN (Simulación)"}`);

  // 1. Obtener producto actual
  const getRes = await fetch(API_ROOT, { headers });
  if (!getRes.ok) {
    throw new Error(`Error al consultar producto 93: HTTP ${getRes.status} ${await getRes.text()}`);
  }
  const currentProduct = (await getRes.json()).data;

  // 2. Crear backup local
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  const backupDir = path.join(ROOT, "scripts", "backups");
  if (!fs.existsSync(backupDir)) fs.mkdirSync(backupDir, { recursive: true });
  const backupPath = path.join(backupDir, `product-93-before-pdp-seo-${timestamp}.json`);
  fs.writeFileSync(backupPath, JSON.stringify(currentProduct, null, 2), "utf8");
  console.log(`[BACKUP] Copia de seguridad guardada en: ${backupPath}`);

  // 3. Preparar payload
  const payload = {
    page_title: NEW_PAGE_TITLE,
    meta_description: NEW_META_DESCRIPTION,
    search_keywords: NEW_SEARCH_KEYWORDS,
    description: NEW_DESCRIPTION_HTML
  };

  console.log("\n--- PROPUESTA DE CAMBIOS ---");
  console.log(`page_title actual:      "${currentProduct.page_title}"`);
  console.log(`page_title nuevo:       "${payload.page_title}" (${payload.page_title.length} chars)`);
  console.log(`meta_description actual: "${currentProduct.meta_description}"`);
  console.log(`meta_description nuevo:  "${payload.meta_description}" (${payload.meta_description.length} chars)`);
  console.log(`search_keywords actual:  "${currentProduct.search_keywords}"`);
  console.log(`search_keywords nuevo:   "${payload.search_keywords}"`);
  console.log(`description actual:      ${currentProduct.description.length} caracteres`);
  console.log(`description nuevo:       ${payload.description.length} caracteres`);

  if (!APPLY) {
    console.log("\n[AVISO] Ejecución en modo DRY-RUN completada. No se modificó la tienda.");
    console.log("Para aplicar los cambios a producción, ejecuta con flag --apply.");
    return;
  }

  // 4. Aplicar cambios a BigCommerce
  console.log("\n[APLICANDO] Enviando actualización a la API de BigCommerce...");
  const putRes = await fetch(API_ROOT, {
    method: "PUT",
    headers,
    body: JSON.stringify(payload)
  });

  if (!putRes.ok) {
    const errorText = await putRes.text();
    throw new Error(`Error actualizando producto 93: HTTP ${putRes.status} - ${errorText}`);
  }

  const updatedProduct = (await putRes.json()).data;
  console.log("[ÉXITO] Producto 93 actualizado exitosamente en BigCommerce.");
  console.log(`ID: ${updatedProduct.id} | Nombre: ${updatedProduct.name}`);
  console.log(`Page Title confirmado: "${updatedProduct.page_title}"`);
  console.log(`Meta Description confirmada: "${updatedProduct.meta_description}"`);
  console.log(`Fecha de modificación: ${updatedProduct.date_modified}`);
}

run().catch((err) => {
  console.error("\n[ERROR FATAL]", err);
  process.exit(1);
});
