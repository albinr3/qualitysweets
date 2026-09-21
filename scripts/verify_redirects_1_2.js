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

const BASE_URL = `https://api.bigcommerce.com/stores/${STORE_HASH}`;
const DOMAIN = "https://qualitysweetsnj.com";

const urlsToTest = [
  // 1. Redirecciones de categorías principales
  { path: "/Traditional", expected: "/traditional-mithai/" },
  { path: "/sweets", expected: "/indian-sweets/" },
  { path: "/sweets/", expected: "/indian-sweets/" },
  { path: "/sweets/bengali/", expected: "/bengali-sweets/" },
  { path: "/sweets/burfi/", expected: "/barfi/" },
  { path: "/Snacks/nuts/", expected: "/nuts/" },
  { path: "/Nuts/savories/", expected: "/savories/" },
  { path: "/gift-boxes/custom/", expected: "/custom/" },
  { path: "/gift-boxes/ready-made/", expected: "/ready-made/" },
  { path: "/bulk-corporate-orders/", expected: "/catering/" },
  { path: "/bulk-orders", expected: "/catering/" },

  // 2. Saneamiento de categorías heredadas de plantilla demo
  { path: "/ladies/", expected: "/indian-sweets/" },
  { path: "/mens/", expected: "/indian-snacks/" },
  { path: "/accessories-3/", expected: "/mithai-box/" },
  { path: "/sale/", expected: "/chaats/" },
  { path: "/accessories-2/", expected: "/bengali-sweets/" },
  { path: "/shoes/", expected: "/traditional-mithai/" },
  { path: "/Designer/", expected: "/traditional-mithai/" },
];

async function checkApiRedirects() {
  console.log(`\n=== 1. Consultando API de Redirecciones de BigCommerce (/v3/storefront/redirects) ===`);
  try {
    const res = await fetch(`${BASE_URL}/v3/storefront/redirects?limit=250`, {
      headers: {
        "X-Auth-Token": ACCESS_TOKEN,
        "Accept": "application/json",
        ...(CLIENT_ID ? { "X-Auth-Client": CLIENT_ID } : {})
      }
    });

    if (!res.ok) {
      console.log(`[AVISO] API v3 storefront/redirects retornó HTTP ${res.status}. Probando /v2/redirects...`);
      const resV2 = await fetch(`${BASE_URL}/v2/redirects?limit=250`, {
        headers: {
          "X-Auth-Token": ACCESS_TOKEN,
          "Accept": "application/json"
        }
      });
      if (!resV2.ok) {
        console.log(`[AVISO] API v2 redirects retornó HTTP ${resV2.status}.`);
        return [];
      }
      const dataV2 = await resV2.json();
      console.log(`[OK] Total de redirecciones registradas en API v2: ${Array.isArray(dataV2) ? dataV2.length : 0}`);
      return dataV2;
    }

    const data = await res.json();
    const redirects = data.data || [];
    console.log(`[OK] Total de redirecciones registradas en API v3: ${redirects.length}`);
    const bulkMatches = redirects.filter(r => (r.from_path && r.from_path.includes("bulk")) || (r.to?.url && r.to.url.includes("bulk")));
    console.log("Redirecciones relacionadas con 'bulk':", JSON.stringify(bulkMatches, null, 2));
    if (redirects.length > 0) {
      console.log("Ejemplo de estructura de redirección:", JSON.stringify(redirects[0], null, 2));
    }
    return redirects;
  } catch (err) {
    console.log(`[ERROR API Redirects] ${err.message}`);
    return [];
  }
}

async function testLiveUrl(item) {
  const targetUrl = `${DOMAIN}${item.path}`;
  try {
    const res = await fetch(targetUrl, {
      method: "GET",
      redirect: "manual", // No seguir redirecciones automáticamente
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      }
    });

    const status = res.status;
    const location = res.headers.get("location") || "";
    const isRedirect = status === 301 || status === 302 || status === 307 || status === 308;

    let match = false;
    if (location.includes(item.expected)) {
      match = true;
    }

    return {
      path: item.path,
      expected: item.expected,
      status,
      location,
      isRedirect,
      match
    };
  } catch (err) {
    return {
      path: item.path,
      expected: item.expected,
      status: "ERROR",
      location: err.message,
      isRedirect: false,
      match: false
    };
  }
}

async function ensureRedirect(fromPath, entityId) {
  try {
    const payload = [
      {
        from_path: fromPath,
        site_id: 1000,
        to: {
          type: "category",
          entity_id: entityId
        }
      }
    ];
    const res = await fetch(`${BASE_URL}/v3/storefront/redirects`, {
      method: "PUT",
      headers: {
        "X-Auth-Token": ACCESS_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });
    const text = await res.text();
    console.log(`[BLINDAJE REDIRECT] ${fromPath} -> Status ${res.status}: ${text}`);
  } catch (err) {
    console.error(`[ERROR creando redirect]: ${err.message}`);
  }
}

async function run() {
  console.log(`Iniciando Auditoría Forense y Verificación de Redirecciones 301 en Vivo (Paso 1.2)...`);
  console.log(`Dominio auditado: ${DOMAIN}`);

  // Asegurar que /bulk-corporate-orders/ y /bulk-corporate-orders estén registrados hacia Category ID 21
  await ensureRedirect("/bulk-corporate-orders/", 21);
  await ensureRedirect("/bulk-corporate-orders", 21);

  const apiRedirects = await checkApiRedirects();
  if (apiRedirects.length > 0) {
    console.log(`Muestra de redirecciones configuradas en el servidor BigCommerce:`);
    for (const r of apiRedirects.slice(0, 10)) {
      const from = r.from_path || r.path;
      const to = r.to?.url || r.forward?.url || (r.to?.type === "category" ? `Category ID ${r.to.entity_id}` : JSON.stringify(r.to || r.forward));
      console.log(`   * ${from} -> ${to}`);
    }
  }

  console.log(`\n=== 2. Comprobación en Vivo de Respuestas HTTP contra el Servidor ===\n`);

  const results = [];
  for (const item of urlsToTest) {
    const result = await testLiveUrl(item);
    results.push(result);

    const icon = result.match ? "[OK 301]" : (result.isRedirect ? "[REDIR A OTRO]" : "[NO REDIR]");
    console.log(`${icon} ${result.path.padEnd(28)} -> HTTP ${result.status} | Destino: ${result.location || "(Sin cabecera Location)"}`);
  }

  console.log(`\n=== 3. Resumen Forense ===`);
  const successCount = results.filter(r => r.match).length;
  console.log(`Redirecciones verificadas correctamente: ${successCount} de ${results.length}`);
}

run();
