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

async function checkProduct92() {
  const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/products/92`, {
    headers: { "X-Auth-Token": token, "Accept": "application/json" }
  });
  const p = await res.json();
  console.log("Product 92 details:");
  console.log({
    id: p.id,
    name: p.name,
    is_visible: p.is_visible,
    availability: p.availability,
    custom_url: p.custom_url,
    categories: p.categories,
    inventory_level: p.inventory_level,
    inventory_tracking: p.inventory_tracking
  });
}

checkProduct92().catch(console.error);
