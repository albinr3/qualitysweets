const fs = require('fs');
const https = require('https');

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

async function fetchPage(pid) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.bigcommerce.com',
      path: `/stores/${storeHash}/v3/content/pages/${pid}`,
      method: 'GET',
      headers: {
        'X-Auth-Token': token,
        'Accept': 'application/json'
      }
    };
    const req = https.request(options, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body).data);
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function main() {
  for (const pid of [2, 7]) {
    try {
      const page = await fetchPage(pid);
      console.log(`\n=================== PAGE ${pid}: ${page.name} (${page.url}) ===================`);
      console.log(`Meta Title: ${page.meta_title}`);
      console.log(`Is Visible: ${page.is_visible}`);
      console.log(`Body length: ${(page.body || '').length}`);
      console.log(`Body snippet:`);
      console.log((page.body || '').slice(0, 1000));
    } catch (err) {
      console.error(`Error with page ${pid}:`, err);
    }
  }
}

main();
