import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function loadEnv() {
  const possiblePaths = [
    path.resolve(__dirname, "../../.env"),
    path.resolve(process.cwd(), ".env"),
    path.resolve(__dirname, ".env"),
  ];

  for (const envPath of possiblePaths) {
    if (fs.existsSync(envPath)) {
      const content = fs.readFileSync(envPath, "utf-8");
      for (const line of content.split("\n")) {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith("#") && trimmed.includes("=")) {
          const [k, ...v] = trimmed.split("=");
          const key = k.trim();
          const val = v.join("=").trim().replace(/^["']|["']$/g, "");
          if (!process.env[key]) {
            process.env[key] = val;
          }
        }
      }
      break;
    }
  }
}

loadEnv();

const STORE_HASH = process.env.BIGCOMMERCE_STORE_HASH;
const ACCESS_TOKEN = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const CLIENT_ID = process.env.BIGCOMMERCE_CLIENT_ID;

if (!STORE_HASH || !ACCESS_TOKEN) {
  console.error("Faltan variables en .env");
  process.exit(1);
}

const BASE_URL = `https://api.bigcommerce.com/stores/${STORE_HASH}`;

async function bcFetch(endpoint, options = {}) {
  const url = endpoint.startsWith("http") ? endpoint : `${BASE_URL}${endpoint}`;
  const headers = {
    "X-Auth-Token": ACCESS_TOKEN,
    Accept: "application/json",
    "Content-Type": "application/json",
    ...options.headers,
  };
  if (CLIENT_ID) headers["X-Auth-Client"] = CLIENT_ID;

  const res = await fetch(url, { ...options, headers });
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

const [action, ...args] = process.argv.slice(2);

async function run() {
  switch (action) {
    case "store": {
      const res = await bcFetch("/v2/store");
      console.log(JSON.stringify(res, null, 2));
      break;
    }
    case "seo:get": {
      const res = await bcFetch("/v3/settings/storefront/seo");
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }
    case "seo:set": {
      const [title, desc] = args;
      const payload = {};
      if (title) payload.page_title = title;
      if (desc) payload.meta_description = desc;
      const res = await bcFetch("/v3/settings/storefront/seo", {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }
    case "pages:list": {
      const res = await bcFetch("/v3/content/pages");
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }
    case "pages:get": {
      const [id] = args;
      const res = await bcFetch(`/v3/content/pages/${id}`);
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }
    case "pages:create": {
      const [name, url, bodyFile, metaTitle, metaDesc] = args;
      let body = "<p>Contenido</p>";
      if (bodyFile && fs.existsSync(bodyFile)) {
        body = fs.readFileSync(bodyFile, "utf-8");
      }
      const payload = {
        name,
        url,
        body,
        // BigCommerce only accepts page-level SEO fields on CMS pages.
        type: "page",
        is_visible: true,
        meta_title: metaTitle,
        meta_description: metaDesc,
      };
      const res = await bcFetch("/v3/content/pages", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }
    case "pages:update": {
      const [id, bodyFile, metaDescription, metaTitle] = args;
      if (!id || !bodyFile || !fs.existsSync(bodyFile)) {
        throw new Error("Uso: pages:update <page_id> <body_file_path>");
      }
      const res = await bcFetch(`/v3/content/pages/${id}`, {
        method: "PUT",
        body: JSON.stringify({
          body: fs.readFileSync(bodyFile, "utf-8"),
          ...(metaDescription ? { meta_description: metaDescription } : {}),
          ...(metaTitle ? { meta_title: metaTitle } : {}),
        }),
      });
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }
    case "categories:list": {
      const res = await bcFetch("/v3/catalog/categories?limit=50");
      console.log(JSON.stringify(res.data, null, 2));
      break;
    }
    default:
      console.log(`
Uso de la CLI BigCommerce:
  node cli.js store
  node cli.js seo:get
  node cli.js seo:set "<title>" "<description>"
  node cli.js pages:list
  node cli.js pages:get <page_id>
  node cli.js pages:create <name> <url> <body_file_path> "<meta_title>" "<meta_description>"
  node cli.js pages:update <page_id> <body_file_path> ["meta_description"] ["meta_title"]
  node cli.js categories:list
`);
  }
}

run().catch(console.error);
