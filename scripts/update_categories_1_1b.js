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

const BASE_URL = `https://api.bigcommerce.com/stores/${STORE_HASH}/v3/catalog/categories`;

const headers = {
  "X-Auth-Token": ACCESS_TOKEN,
  "Accept": "application/json",
  "Content-Type": "application/json",
};
if (CLIENT_ID) headers["X-Auth-Client"] = CLIENT_ID;

// Tabla de equivalencias oficial de Sub-paso 1.1B
const categoriesToUpdate = [
  {
    id: 3,
    name: "All Indian Sweets",
    url: "/indian-sweets/",
    parent_id: 0,
    page_title: "Authentic Indian Sweets Handcrafted Daily | Quality Sweets",
    meta_description: "Buy authentic Indian sweets online handcrafted daily with pure ingredients and zero preservatives. Fast nationwide shipping with thermal insulated packaging.",
    notes: "Madre E-commerce"
  },
  {
    id: 8,
    name: "Bengali Sweets",
    url: "/bengali-sweets/",
    parent_id: 3,
    page_title: "Authentic Bengali Sweets (No Preservatives) | Quality Sweets",
    meta_description: "Fresh Bengali sweets made daily in New Jersey. Shop Chum Chum, Rasgulla, Sandesh and Kalakand with refrigerated nationwide delivery.",
    notes: "Subcategoría de All Indian Sweets"
  },
  {
    id: 22,
    name: "Barfi & Kaju Katli",
    url: "/barfi/",
    parent_id: 3,
    page_title: "Premium Indian Barfi & Pure Kaju Katli | Quality Sweets",
    meta_description: "Order authentic Indian Barfi and pure Kaju Katli online made with 100% premium cashews. Zero artificial additives. Fresh USA delivery.",
    notes: "Subcategoría de All Indian Sweets"
  },
  {
    id: 2,
    name: "Traditional Mithai",
    url: "/traditional-mithai/",
    parent_id: 3,
    page_title: "Traditional Indian Mithai & Fresh Ladoos | Quality Sweets",
    meta_description: "Handcrafted traditional Indian mithai, Motichur Ladoo, Besan Laddu, Kesar Peda, and Gulab Jamun. Authentic family recipes since 2003.",
    notes: "Subcategoría de All Indian Sweets"
  },
  {
    id: 1,
    name: "Indian Snacks & Namkeen",
    url: "/indian-snacks/",
    parent_id: 0,
    page_title: "Traditional Indian Snacks & Namkeen Online | Quality Sweets",
    meta_description: "Crispy traditional Indian snacks and namkeen: Mathi, Namak Para, Gud Para, Sev, and spiced cashews. Perfect tea-time snacks delivered fresh across the USA.",
    notes: "Colección Raíz Hermana"
  },
  {
    id: 14,
    name: "Mithai Boxes & Gift Baskets",
    url: "/mithai-box/",
    parent_id: 0,
    page_title: "Luxury Mithai Boxes & Sweet Gift Baskets | Quality Sweets",
    meta_description: "Elegant luxury mithai gift boxes and sweet baskets for Diwali, weddings, and corporate gifting. Custom assortments with nationwide shipping.",
    notes: "Colección Raíz Hermana"
  },
  {
    id: 21,
    name: "Catering & Bulk Orders",
    url: "/catering/",
    parent_id: 0,
    page_title: "Indian Sweets & Snack Catering Tri-State | Quality Sweets",
    meta_description: "Bulk sweet catering, wedding return gifts, and temple prasad across New Jersey, New York, and Connecticut. Fresh samosas, chaat, and mithai.",
    notes: "Hub B2B Tri-State"
  },
  {
    id: 15,
    name: "Chaat Counter (Iselin Takeout)",
    url: "/chaats/",
    parent_id: 0,
    page_title: "Fresh Chaat Counter & Street Food Iselin NJ | Quality Sweets",
    meta_description: "Authentic Indian Chaat and street food in Iselin, NJ. Samosa Chaat, Pani Puri, Papri Chaat, and Dahi Vada prepared fresh daily. Takeout & pickup only.",
    notes: "Comida Caliente (No Shippable)"
  }
];

async function updateCategory(cat) {
  console.log(`\n----------------------------------------------------`);
  console.log(`[ACTUALIZANDO] Category ID ${cat.id}: ${cat.name} (${cat.notes})`);
  console.log(`   -> Nuevo Slug: ${cat.url}`);
  console.log(`   -> Parent ID: ${cat.parent_id}`);

  const payload = {
    name: cat.name,
    parent_id: cat.parent_id,
    custom_url: {
      url: cat.url,
      is_customized: true
    },
    page_title: cat.page_title,
    meta_description: cat.meta_description
  };

  try {
    const res = await fetch(`${BASE_URL}/${cat.id}`, {
      method: "PUT",
      headers,
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      console.error(`   [FALLO HTTP ${res.status}]`, JSON.stringify(data, null, 2));
      return false;
    }

    console.log(`   [OK] Categoría ${cat.id} actualizada exitosamente:`);
    console.log(`        Nombre: "${data.data?.name}"`);
    console.log(`        URL: "${data.data?.custom_url?.url}"`);
    console.log(`        Parent ID: ${data.data?.parent_id}`);
    console.log(`        Title: "${data.data?.page_title}"`);
    return true;
  } catch (err) {
    console.error(`   [ERROR DE CONEXION] ${err.message}`);
    return false;
  }
}

async function run() {
  console.log(`Iniciando Sub-paso 1.1B: Actualización de Categorías en BigCommerce...`);
  console.log(`Tienda: https://api.bigcommerce.com/stores/${STORE_HASH}/v3/`);

  let successCount = 0;
  for (const cat of categoriesToUpdate) {
    const ok = await updateCategory(cat);
    if (ok) successCount++;
  }

  console.log(`\n====================================================`);
  console.log(`Resultado: ${successCount} de ${categoriesToUpdate.length} categorías actualizadas con éxito.`);
  console.log(`====================================================\n`);
}

run();
