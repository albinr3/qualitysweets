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

async function inspect() {
  const res = await fetch(`https://api.bigcommerce.com/stores/${env.BIGCOMMERCE_STORE_HASH}/v3/settings/analytics/6`, {
    headers: { "X-Auth-Token": env.BIGCOMMERCE_ACCESS_TOKEN, "Accept": "application/json" }
  });
  const json = await res.json();
  const code = json.data?.code || "";
  console.log("Provider 6 code length:", code.length);
  const ids = [...code.matchAll(/<script\s+id=["']([^"']+)["']/g)].map(m => m[1]);
  console.log("Script IDs in Provider 6:", ids);
  fs.writeFileSync(path.join(ROOT, "scratch", "live_provider_6.html"), code, "utf8");
  console.log("Saved live provider 6 to scratch/live_provider_6.html");
}

inspect().catch(console.error);
