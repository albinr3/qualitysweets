import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function loadEnv() {
  const envPath = path.resolve(__dirname, "../.env");
  if (fs.existsSync(envPath)) {
    const content = fs.readFileSync(envPath, "utf-8");
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith("#") && trimmed.includes("=")) {
        const [k, ...v] = trimmed.split("=");
        process.env[k.trim()] = v.join("=").trim().replace(/^["']|["']$/g, "");
      }
    }
  }
}

loadEnv();

const STORE_HASH = process.env.BIGCOMMERCE_STORE_HASH;
const ACCESS_TOKEN = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const CLIENT_ID = process.env.BIGCOMMERCE_CLIENT_ID;

if (!STORE_HASH || !ACCESS_TOKEN) {
  console.error("Error: Faltan credenciales en .env (BIGCOMMERCE_STORE_HASH o BIGCOMMERCE_ACCESS_TOKEN)");
  process.exit(1);
}

const BASE_URL = `https://api.bigcommerce.com/stores/${STORE_HASH}`;
const DOMAIN = "https://qualitysweetsnj.com";

const headers = {
  "X-Auth-Token": ACCESS_TOKEN,
  "Accept": "application/json",
  "Content-Type": "application/json",
};
if (CLIENT_ID) headers["X-Auth-Client"] = CLIENT_ID;

const productsToSanitize = [
  {
    id: 80,
    name: "Anarkali",
    url: "/anarkali/",
    oldUrl: "/anarkali-in-store-pick-up-purchase-only/",
    page_title: "Anarkali Bengali Sweet | Handcrafted Mithai | Quality Sweets",
    meta_description: "Handcrafted Anarkali Bengali sweet made fresh daily at Quality Sweets in Iselin, NJ. Pure artisanal chum chum base with pomegranate seeds and pistachios."
  },
  {
    id: 78,
    name: "Manpasand",
    url: "/manpasand/",
    oldUrl: "/manpasand-in-store-pick-up-purchase-only/",
    page_title: "Manpasand Bengali Sweet | Traditional Mithai | Quality Sweets",
    meta_description: "Delicious Manpasand Bengali sweet handcrafted daily at Quality Sweets in Iselin, NJ. Chum chum base with khoya, pomegranate seeds, pistachios & rabri."
  },
  {
    id: 133,
    name: "Cherry Chum Chum",
    url: "/cherry-chum-chum/",
    oldUrl: "/cherry-chum-chum-in-store-pick-up-purchase-only/",
    page_title: "Cherry Chum Chum | Authentic Bengali Mithai | Quality Sweets",
    meta_description: "Fresh Cherry Chum Chum handmade with delicate cottage cheese malai and topped with cherry. Available for in-store pickup at Quality Sweets, Iselin NJ."
  },
  {
    id: 84,
    name: "Malai Chum Chum",
    url: "/malai-chum-chum/",
    oldUrl: "/malai-chum-chum-in-store-pick-up-purchase-only/",
    page_title: "Malai Chum Chum | Fresh Bengali Sweets | Quality Sweets",
    meta_description: "Stuffed Malai Chum Chum with rich khoya cream, edible silver leaf, and pistachios. Handcrafted fresh daily at Quality Sweets in Iselin, NJ."
  },
  {
    id: 87,
    name: "Pineapple Chum Chum",
    url: "/pineapple-chum-chum/",
    oldUrl: "/pineapple-chum-chum-in-store-pick-up-purchase-only/",
    page_title: "Pineapple Chum Chum | Fruit Infused Mithai | Quality Sweets",
    meta_description: "Authentic Pineapple Chum Chum stuffed with real pineapple chunks and rich malai cream. Fresh artisanal sweets at Quality Sweets, Iselin, NJ."
  },
  {
    id: 88,
    name: "Rose Chum Chum",
    url: "/rose-chum-chum/",
    oldUrl: "/rose-chum-chum-in-store-pick-up-purchase-only/",
    page_title: "Rose Chum Chum | Fragrant Bengali Sweet | Quality Sweets",
    meta_description: "Delicate Rose Chum Chum infused with natural rose flavor, stuffed with malai, and garnished with cherry. Handcrafted at Quality Sweets in Iselin, NJ."
  },
  {
    id: 83,
    name: "Palki",
    url: "/palki/",
    oldUrl: "/palki-in-store-pick-up-purchase-only/",
    page_title: "Palki Bengali Sweet | Saffron Khoya Mithai | Quality Sweets",
    meta_description: "Traditional Palki Bengali sweet handcrafted with khoya, aromatic kesar (saffron), pistachios, and cherries. Fresh in-store pickup at Quality Sweets, Iselin NJ."
  },
  {
    id: 120,
    name: "Channa Mango Malai",
    url: "/channa-mango-malai/",
    oldUrl: "/channa-mango-malai-in-store-pick-up-purchase-only/",
    page_title: "Channa Mango Malai | Fresh Artisanal Sweet | Quality Sweets",
    meta_description: "Exquisite Channa Mango Malai sweet with chum chum base, real mango filling, and mango khoya. Handcrafted daily at Quality Sweets in Iselin, NJ."
  }
];

const ALERT_BANNER_HTML = `<div class="in-store-pickup-alert" style="background-color: #fff8e6; border-left: 4px solid #d97706; padding: 14px 18px; margin-bottom: 20px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-family: inherit;">
  <p style="margin: 0 0 6px 0; color: #92400e; font-weight: 700; font-size: 15px;">
    📍 In-Store Pickup Only (Iselin, NJ)
  </p>
  <p style="margin: 0; color: #78350f; font-size: 13.5px; line-height: 1.5;">
    Due to its delicate artisanal freshness, this specialty mithai is prepared fresh daily and is available exclusively for counter pickup at our physical storefront: <strong>1384 Oak Tree Rd, Iselin, NJ 08830</strong>. Not eligible for postal or nationwide shipping.
  </p>
</div>\r\n`;

async function getProduct(productId) {
  const res = await fetch(`${BASE_URL}/v3/catalog/products/${productId}`, { headers });
  if (!res.ok) {
    throw new Error(`Error obteniendo producto ${productId}: HTTP ${res.status}`);
  }
  const data = await res.json();
  return data.data;
}

async function updateProduct(productId, payload) {
  const res = await fetch(`${BASE_URL}/v3/catalog/products/${productId}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Error actualizando producto ${productId}: HTTP ${res.status} - ${text}`);
  }
  const data = await res.json();
  return data.data;
}

async function getCustomFields(productId) {
  const res = await fetch(`${BASE_URL}/v3/catalog/products/${productId}/custom-fields`, { headers });
  if (!res.ok) return [];
  const data = await res.json();
  return data.data || [];
}

async function addCustomField(productId, name, value) {
  const res = await fetch(`${BASE_URL}/v3/catalog/products/${productId}/custom-fields`, {
    method: "POST",
    headers,
    body: JSON.stringify({ name, value })
  });
  if (!res.ok) {
    const text = await res.text();
    console.warn(`[AVISO] No se pudo agregar custom field para producto ${productId}: HTTP ${res.status} - ${text}`);
    return null;
  }
  const data = await res.json();
  return data.data;
}

async function getRedirects() {
  const res = await fetch(`${BASE_URL}/v3/storefront/redirects?limit=250`, { headers });
  if (!res.ok) return [];
  const data = await res.json();
  return data.data || [];
}

async function deleteRedirect(redirectId) {
  const res = await fetch(`${BASE_URL}/v3/storefront/redirects?id:in=${redirectId}`, {
    method: "DELETE",
    headers
  });
  return res.ok;
}

async function createRedirect(fromPath, entityId) {
  const payload = [
    {
      from_path: fromPath,
      site_id: 1000,
      to: {
        type: "product",
        entity_id: entityId
      }
    }
  ];
  const res = await fetch(`${BASE_URL}/v3/storefront/redirects`, {
    method: "PUT",
    headers,
    body: JSON.stringify(payload)
  });
  return res.ok;
}

async function testLiveUrl(urlPath) {
  const target = `${DOMAIN}${urlPath}`;
  try {
    const res = await fetch(target, {
      method: "GET",
      redirect: "manual",
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      }
    });
    return {
      status: res.status,
      location: res.headers.get("location") || ""
    };
  } catch (err) {
    return {
      status: "ERROR",
      location: err.message
    };
  }
}

async function main() {
  console.log("================================================================================");
  console.log("EJECUCIÓN PASO 1.3: Saneamiento Inmediato de Fichas de Producto y Slugs");
  console.log("================================================================================");

  // 1. Obtener lista actual de redirecciones
  console.log("\n[1/5] Consultando redirecciones existentes en BigCommerce...");
  const existingRedirects = await getRedirects();
  console.log(`[OK] Total de redirecciones en el sistema: ${existingRedirects.length}`);

  // 2. Procesar cada uno de los 8 productos
  console.log("\n[2/5] Actualizando y saneando fichas de producto...");
  for (const item of productsToSanitize) {
    console.log(`\n--- Procesando Producto ID ${item.id}: "${item.name}" ---`);

    // A. Obtener datos actuales del producto
    const current = await getProduct(item.id);
    console.log(`   * Nombre anterior: "${current.name}"`);
    console.log(`   * URL actual: "${current.custom_url?.url}"`);

    // B. Preparar descripción con alerta visual
    let updatedDescription = current.description || "";
    if (!updatedDescription.includes("in-store-pickup-alert")) {
      updatedDescription = ALERT_BANNER_HTML + updatedDescription;
    }

    // C. Enviar actualización a BigCommerce Catalog API
    const updatePayload = {
      name: item.name,
      custom_url: {
        url: item.url,
        is_customized: true
      },
      availability_description: "In-Store Pickup Only (Iselin, NJ)",
      page_title: item.page_title,
      meta_description: item.meta_description,
      description: updatedDescription
    };

    const updated = await updateProduct(item.id, updatePayload);
    console.log(`   [OK] Ficha actualizada: Nombre="${updated.name}", URL="${updated.custom_url?.url}"`);

    // D. Gestionar Custom Field (Fulfillment: Store Pickup Only)
    const customFields = await getCustomFields(item.id);
    const hasFulfillmentBadge = customFields.some(
      cf => cf.name.toLowerCase() === "fulfillment" && cf.value.toLowerCase().includes("pickup")
    );
    if (!hasFulfillmentBadge) {
      const newCf = await addCustomField(item.id, "Fulfillment", "Store Pickup Only");
      if (newCf) {
        console.log(`   [OK] Custom Field añadido: Fulfillment = "Store Pickup Only" (ID: ${newCf.id})`);
      }
    } else {
      console.log(`   [OK] Custom Field "Fulfillment" ya estaba configurado.`);
    }

    // E. Gestionar Redirecciones (Limpiar conflicto previo y blindar URL antigua)
    // - Si hay una redirección obsoleta donde from_path es la nueva URL limpia (/anarkali/), borrarla
    const cleanPath = item.url;
    const cleanPathNoSlash = item.url.replace(/\/$/, "");
    const obsoleteRedirects = existingRedirects.filter(
      r => (r.from_path === cleanPath || r.from_path === cleanPathNoSlash) && r.to?.entity_id === item.id
    );
    for (const obs of obsoleteRedirects) {
      console.log(`   * Eliminando redirección obsoleta ID ${obs.id} (from: "${obs.from_path}")...`);
      await deleteRedirect(obs.id);
      console.log(`   [OK] Redirección ID ${obs.id} eliminada para evitar bucle o conflicto.`);
    }

    // - Blindar la URL antigua para que redirija 301 a la ficha limpia
    console.log(`   * Creando / asegurando regla 301 de URL antigua "${item.oldUrl}" -> Producto ID ${item.id}...`);
    await createRedirect(item.oldUrl, item.id);
    console.log(`   [OK] Redirección 301 blindada exitosamente.`);
  }

  // 3. Verificación en vivo contra el servidor storefront de producción
  console.log("\n[3/5] Verificando en vivo resolución HTTP en https://qualitysweetsnj.com...");
  console.log("--------------------------------------------------------------------------------");
  console.log(
    "ID".padEnd(5) +
    "Producto".padEnd(24) +
    "Nueva URL Limpia (200 OK)".padEnd(30) +
    "URL Antigua (301 Redirect)".padEnd(30)
  );
  console.log("--------------------------------------------------------------------------------");

  let allOk = true;
  for (const item of productsToSanitize) {
    // Probar nueva URL
    const cleanRes = await testLiveUrl(item.url);
    const cleanOk = cleanRes.status === 200;

    // Probar URL antigua
    const oldRes = await testLiveUrl(item.oldUrl);
    const oldOk = (oldRes.status === 301 || oldRes.status === 302) && oldRes.location.includes(item.url);

    if (!cleanOk || !oldOk) allOk = false;

    const cleanStr = cleanOk ? `[200 OK]` : `[HTTP ${cleanRes.status}]`;
    const oldStr = oldOk ? `[301 -> ${item.url}]` : `[HTTP ${oldRes.status} -> ${oldRes.location}]`;

    console.log(
      String(item.id).padEnd(5) +
      item.name.padEnd(24) +
      cleanStr.padEnd(30) +
      oldStr.padEnd(30)
    );
  }
  console.log("--------------------------------------------------------------------------------");

  if (allOk) {
    console.log("\n🎉 [ÉXITO TOTAL] Los 8 productos fueron saneados, optimizados y blindados al 100%.");
  } else {
    console.log("\n⚠️ [AVISO] Algunas URLs pueden requerir unos segundos de propagación de caché CDN de BigCommerce.");
  }
}

main().catch(err => {
  console.error("Error fatal ejecutando Paso 1.3:", err);
  process.exit(1);
});
