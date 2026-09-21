import fs from "fs";
import path from "path";
import { createRequire } from "module";
import { fileURLToPath } from "url";

const require = createRequire(import.meta.url);
const detector = require("C:/Users/Albin Rodríguez/.codex/skills/avoid-ai-writing/skills/avoid-ai-writing/detector/patterns.js");
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.resolve(__dirname, "../.env");

for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
  const [key, ...value] = trimmed.split("=");
  process.env[key.trim()] ??= value.join("=").trim().replace(/^['\"]|['\"]$/g, "");
}

const storeHash = process.env.BIGCOMMERCE_STORE_HASH;
const accessToken = process.env.BIGCOMMERCE_ACCESS_TOKEN;
const clientId = process.env.BIGCOMMERCE_CLIENT_ID;
if (!storeHash || !accessToken) throw new Error("BigCommerce credentials are required.");

const headers = {
  "X-Auth-Token": accessToken,
  Accept: "application/json",
  ...(clientId ? { "X-Auth-Client": clientId } : {}),
};

function decodeHtml(text) {
  return text
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&mdash;/gi, "—")
    .replace(/&ndash;/gi, "–")
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([\da-f]+);/gi, (_, code) => String.fromCodePoint(parseInt(code, 16)));
}

function proseFromHtml(html) {
  return decodeHtml(
    html
      .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
      .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim(),
  );
}

const targets = [
  { id: 3, url: "/indian-sweets/", heading: "Authentic Indian Sweets Handcrafted Daily" },
  { id: 8, url: "/bengali-sweets/", heading: "Authentic Bengali Sweets (No Preservatives)" },
  { id: 22, url: "/barfi/", heading: "Premium Indian Barfi & Pure Kaju Katli" },
  { id: 2, url: "/traditional-mithai/", heading: "Traditional Indian Mithai & Fresh Ladoos" },
];

const baseUrl = `https://api.bigcommerce.com/stores/${storeHash}/v3/catalog/categories`;
const reports = [];

for (const target of targets) {
  const response = await fetch(`${baseUrl}/${target.id}`, { headers });
  const result = await response.json();
  if (!response.ok) throw new Error(`BigCommerce HTTP ${response.status}: ${JSON.stringify(result)}`);

  const category = result.data;
  const prose = `${target.heading}. ${proseFromHtml(category.description)}`;
  const analysis = detector.analyzeText(prose, { contextMode: "marketing" });
  reports.push({
    id: target.id,
    url: target.url,
    words: analysis.stats.wordCount,
    score: analysis.score,
    label: analysis.label,
    classification: analysis.document_classification,
    confidence: analysis.confidence_category,
    issues: analysis.issues.map(({ type, severity, text, replace }) => ({ type, severity, text, replace })),
  });
}

console.log(JSON.stringify(reports, null, 2));
