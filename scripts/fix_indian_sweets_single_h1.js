import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, "../.env");
if (!fs.existsSync(envPath)) throw new Error("Missing .env with BigCommerce credentials.");

for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
  const [key, ...value] = trimmed.split("=");
  process.env[key.trim()] ??= value.join("=").trim().replace(/^['\"]|['\"]$/g, "");
}

const storeHash = process.env.BIGCOMMERCE_STORE_HASH;
const accessToken = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const clientId = process.env.BIGCOMMERCE_CLIENT_ID;
if (!storeHash || !accessToken) throw new Error("BIGCOMMERCE_STORE_HASH and BIGCOMMERCE_ACCESS_TOKEN are required.");

const baseUrl = `https://api.bigcommerce.com/stores/${storeHash}/v3`;
const headers = {
  "X-Auth-Token": accessToken,
  Accept: "application/json",
  "Content-Type": "application/json",
  ...(clientId ? { "X-Auth-Client": clientId } : {}),
};

async function bcFetch(endpoint, options = {}) {
  const response = await fetch(`${baseUrl}${endpoint}`, { ...options, headers });
  const body = await response.json();
  if (!response.ok) throw new Error(`BigCommerce HTTP ${response.status}: ${JSON.stringify(body)}`);
  return body;
}

const nativeHeadingCss = `#CategoryHeading > .TitleHeading { color: #6d1427 !important; display: block !important; font-family: Georgia, 'Times New Roman', serif !important; font-size: clamp(2rem, 4vw, 3.05rem) !important; line-height: 1.15 !important; margin: 0 0 10px !important; text-align: center; }`;

const targets = [
  { id: 3, heading: "Authentic Indian Sweets Handcrafted Daily" },
  { id: 8, heading: "Authentic Bengali Sweets (No Preservatives)" },
  { id: 22, heading: "Premium Indian Barfi & Pure Kaju Katli" },
  { id: 2, heading: "Traditional Indian Mithai & Fresh Ladoos" },
];

function updateDescription(description, heading) {
  let updated = description
    .replace(/#CategoryHeading\s*>\s*\.TitleHeading\s*\{\s*display:\s*none\s*!important;?\s*\}/g, nativeHeadingCss)
    .replace(/#CategoryHeading\s*>\s*\.TitleHeading\s*\{\s*display:\s*none;?\s*\}/g, nativeHeadingCss)
    .replace(/<h1\b[^>]*\bid="qs-[^"]+-title"[^>]*>[\s\S]*?<\/h1>\s*/g, "")
    .replace(/(<section\s+class="qs-[^"]+-intro)\s+aria-labelledby="qs-[^"]+-title"/g, "$1");

  updated = updated.replace(/<script>\s*\(function \(\) \{\s*var heading = document\.querySelector\("#CategoryHeading > \\.TitleHeading"\);[\s\S]*?<\/script>\s*$/g, "");

  const headingScript = `\n<script>\n(function () {\n  var heading = document.querySelector('#CategoryHeading > .TitleHeading');\n  if (!heading) return;\n  heading.textContent = ${JSON.stringify(heading)};\n  heading.setAttribute('data-qs-seo-heading', 'true');\n}());\n</script>`;
  return `${updated.trim()}${headingScript}`;
}

function h1Count(html) {
  return (html.match(/<h1\b/gi) || []).length;
}

const apply = process.argv.includes("--apply");
for (const target of targets) {
  const category = (await bcFetch(`/catalog/categories/${target.id}`)).data;
  const description = updateDescription(category.description, target.heading);
  const count = h1Count(description);
  if (count !== 0) throw new Error(`Category ${target.id} still has ${count} content H1 tag(s) after the update.`);
  console.log(`Category ${target.id}: ${category.name} — content H1 tags before/after: ${h1Count(category.description)}/${count}`);

  if (!apply) continue;
  const result = (await bcFetch(`/catalog/categories/${target.id}`, {
    method: "PUT",
    body: JSON.stringify({ description }),
  })).data;
  if (result.description !== description || h1Count(result.description) !== 0) {
    throw new Error(`BigCommerce did not persist the single-H1 update for Category ID ${target.id}.`);
  }
  console.log(`Updated Category ${target.id} successfully.`);
}

if (!apply) console.log("Dry run complete. Use --apply to update the four Indian sweets category pages.");
