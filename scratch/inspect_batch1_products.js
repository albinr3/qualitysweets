import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const envPath = path.join(ROOT, ".env");

const env = {};
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const idx = trimmed.indexOf("=");
    env[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim().replace(/^['"]|['"]$/g, "");
  }
}

const storeHash = env.BIGCOMMERCE_STORE_HASH || process.env.BIGCOMMERCE_STORE_HASH;
const token = env.BIGCOMMERCE_ACCESS_TOKEN || process.env.BIGCOMMERCE_ACCESS_TOKEN;

const productIds = [112, 77, 104, 98, 127, 126, 92, 94, 105];

async function inspectProducts() {
  const results = [];
  for (const id of productIds) {
    const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/products/${id}`, {
      headers: { "X-Auth-Token": token, "Accept": "application/json" }
    });
    if (!res.ok) {
      console.error(`Failed to fetch product ${id}:`, res.status);
      continue;
    }
    const p = await res.json();
    
    // Also fetch primary image
    let imageUrl = "";
    if (p.images && p.images.url) {
      const imgRes = await fetch(p.images.url, {
        headers: { "X-Auth-Token": token, "Accept": "application/json" }
      });
      if (imgRes.ok) {
        const imgs = await imgRes.json();
        if (Array.isArray(imgs) && imgs.length > 0) {
          imageUrl = imgs[0].zoom_url || imgs[0].standard_url || "";
        }
      }
    }

    results.push({
      id: p.id,
      name: p.name,
      sku: p.sku,
      price: p.price,
      custom_url: p.custom_url,
      page_title: p.page_title,
      meta_description: p.meta_description,
      search_keywords: p.search_keywords,
      imageUrl: imageUrl,
      currentDescSnippet: (p.description || "").slice(0, 100)
    });
  }

  console.log(JSON.stringify(results, null, 2));
  fs.writeFileSync(path.join(ROOT, "scratch", "batch1_inspect.json"), JSON.stringify(results, null, 2), "utf8");
}

inspectProducts().catch(console.error);
