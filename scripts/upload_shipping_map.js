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

async function upload() {
  const fileBuf = fs.readFileSync('assets/fedex_ground_transit_map_nj.png');
  const blob = new Blob([fileBuf], { type: 'image/png' });
  const form = new FormData();
  form.append('image_file', blob, 'fedex_ground_transit_map_nj.png');
  form.append('description', 'FedEx Ground Delivery Transit Schedule Map Quality Sweets');
  form.append('is_thumbnail', 'false');

  const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/catalog/products/176/images`, {
    method: 'POST',
    headers: {
      'X-Auth-Token': token
    },
    body: form
  });

  const json = await res.json();
  console.log('Status:', res.status);
  console.log('Result:', JSON.stringify(json, null, 2));
}

upload().catch(console.error);
