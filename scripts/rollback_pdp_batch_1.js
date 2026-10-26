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

async function rollback() {
  const backupDir = path.join(ROOT, "scripts", "backups");
  const files = fs.readdirSync(backupDir).filter(f => f.startsWith("pdp_batch1_remaining9_backup_")).sort().reverse();
  if (files.length === 0) {
    console.error("No backup file found in scripts/backups!");
    process.exit(1);
  }

  const latestBackup = path.join(backupDir, files[0]);
  console.log(`Using latest backup: ${latestBackup}`);
  const items = JSON.parse(fs.readFileSync(latestBackup, "utf8"));

  for (const item of items) {
    console.log(`Restoring product ${item.id} (${item.name})...`);
    const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/products/${item.id}`, {
      method: "PUT",
      headers: {
        "X-Auth-Token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        page_title: item.page_title,
        meta_description: item.meta_description,
        search_keywords: item.search_keywords,
        description: item.description
      })
    });
    if (res.ok) {
      console.log(`Restored product ${item.id} successfully.`);
    } else {
      console.error(`Failed to restore product ${item.id}:`, res.status, await res.text());
    }
  }
}

rollback().catch(console.error);
