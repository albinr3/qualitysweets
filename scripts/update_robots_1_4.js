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
  console.error("Error: Faltan credenciales en .env");
  process.exit(1);
}

const BASE_URL = `https://api.bigcommerce.com/stores/${STORE_HASH}`;
const DOMAIN = "https://qualitysweetsnj.com";
const SITEMAP_URL = `${DOMAIN}/xmlsitemap.php`;

const headers = {
  "X-Auth-Token": ACCESS_TOKEN,
  "Accept": "application/json",
  "Content-Type": "application/json",
};
if (CLIENT_ID) headers["X-Auth-Client"] = CLIENT_ID;

async function run() {
  console.log("================================================================================");
  console.log("EJECUCIÓN PASO 1.4: Ajuste de Robots.txt y Directiva Sitemap XML");
  console.log("================================================================================");

  // 1. Verificar disponibilidad del Sitemap XML
  console.log(`\n[1/3] Verificando sitemap XML en vivo: ${SITEMAP_URL}...`);
  const sitemapRes = await fetch(SITEMAP_URL);
  if (!sitemapRes.ok) {
    console.error(`[ERROR] El sitemap no respondió 200 OK. Status: ${sitemapRes.status}`);
    process.exit(1);
  }
  console.log(`[OK] Sitemap XML activo con HTTP ${sitemapRes.status} (Content-Type: ${sitemapRes.headers.get("content-type")}).`);

  // 2. Obtener y actualizar robots.txt vía API de BigCommerce
  console.log(`\n[2/3] Consultando y configurando robots.txt en BigCommerce Settings API...`);
  const getRes = await fetch(`${BASE_URL}/v3/settings/storefront/robotstxt`, { headers });
  if (!getRes.ok) {
    console.error(`[ERROR] Falló la consulta de robotstxt. Status: ${getRes.status}`);
    process.exit(1);
  }
  const current = await getRes.json();
  let content = current.data?.robots_txt_ssl || "";

  if (!content.includes("xmlsitemap.php")) {
    content = content.trimEnd() + `\r\n\r\nSitemap: ${SITEMAP_URL}\r\n`;
    const putRes = await fetch(`${BASE_URL}/v3/settings/storefront/robotstxt`, {
      method: "PUT",
      headers,
      body: JSON.stringify({ robots_txt_ssl: content })
    });
    if (!putRes.ok) {
      console.error(`[ERROR] No se pudo guardar robots.txt. Status: ${putRes.status}`);
      process.exit(1);
    }
    console.log(`[OK] Directiva Sitemap inyectada exitosamente en BigCommerce API.`);
  } else {
    console.log(`[OK] La directiva Sitemap ya se encuentra presente en la configuración de BigCommerce.`);
  }

  // 3. Verificación en vivo contra el servidor público
  console.log(`\n[3/3] Verificando https://qualitysweetsnj.com/robots.txt en vivo...`);
  const pubRes = await fetch(`${DOMAIN}/robots.txt`, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
  });
  const pubText = await pubRes.text();
  if (pubText.includes(SITEMAP_URL)) {
    console.log(`\n🎉 [ÉXITO TOTAL] robots.txt público incluye la directiva Sitemap oficial:`);
    console.log(`   Sitemap: ${SITEMAP_URL}`);
  } else {
    console.warn(`[AVISO] BigCommerce puede tardar unos instantes en purgar la caché CDN de robots.txt.`);
  }
}

run().catch(err => {
  console.error("Error fatal:", err);
  process.exit(1);
});
