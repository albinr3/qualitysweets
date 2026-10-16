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

async function inspectProvider6() {
  const res = await fetch(`https://api.bigcommerce.com/stores/${storeHash}/v3/settings/analytics/6`, {
    headers: { 'X-Auth-Token': token, 'Accept': 'application/json' }
  });
  const json = await res.json();
  const code = (json.data && json.data.code) || '';
  console.log('Provider 6 status:', res.status);
  console.log('Provider 6 code length:', code.length);
  console.log('Provider 6 preview (first 400 chars):');
  console.log(code.slice(0, 400));
  console.log('Provider 6 preview (last 400 chars):');
  console.log(code.slice(-400));
}

inspectProvider6().catch(console.error);
