import fs from "fs";
import path from "path";
import os from "os";

const home = os.homedir();
console.log("Home dir:", home);

const checks = [
  path.join(home, ".config", "codex-seo", "google-api.json"),
  path.join(home, ".gemini", "config", "skills", "seo-google", "scripts"),
  path.join(home, "Documents", "QualitySweets", ".env"),
  path.join(home, ".google"),
  path.join(home, ".gcp")
];

for (const c of checks) {
  console.log(`${c}: exists=${fs.existsSync(c)}`);
}

// Check .env keys
const envPath = path.join(home, "Documents", "QualitySweets", ".env");
if (fs.existsSync(envPath)) {
  const keys = fs.readFileSync(envPath, "utf8").split("\n").map(l => l.split("=")[0].trim()).filter(k => k && !k.startsWith("#"));
  console.log(".env keys:", keys);
}
