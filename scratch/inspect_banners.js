const fs = require('fs');

const env = {};
if (fs.existsSync('.env')) {
  fs.readFileSync('.env', 'utf8').split('\n').forEach(line => {
    const parts = line.trim().split('=');
    if (parts.length >= 2 && !parts[0].startsWith('#')) {
      env[parts[0].trim()] = parts.slice(1).join('=').trim().replace(/^['"]|['"]$/g, '');
    }
  });
}

const storeHash = env.BIGCOMMERCE_STORE_HASH || process.env.BIGCOMMERCE_STORE_HASH;
const token = env.BIGCOMMERCE_ACCESS_TOKEN || process.env.BIGCOMMERCE_ACCESS_TOKEN;

async function checkBanners() {
  const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v2/banners`, {
    headers: { 'X-Auth-Token': token, 'Accept': 'application/json' }
  });
  const banners = await res.json();
  console.log(`Found ${banners.length} banners:`);
  banners.forEach(b => {
    console.log(`ID: ${b.id} | Name: "${b.name}" | Page: ${b.page} | Loc: ${b.location} | Visible: ${b.visible}`);
  });
}

checkBanners().catch(console.error);
