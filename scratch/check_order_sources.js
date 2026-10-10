const https = require('https');
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '..', '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
const env = {};
envContent.split('\n').forEach(line => {
  const match = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
  if (match) env[match[1]] = (match[2] || '').trim();
});

const storeHash = env.BIGCOMMERCE_STORE_HASH || '2ygwtj';
const token = env.BIGCOMMERCE_ACCESS_TOKEN;

function get(apiPath) {
  return new Promise((resolve, reject) => {
    https.get({
      hostname: 'api.bigcommerce.com',
      path: `/stores/${storeHash}${apiPath}`,
      headers: { 'X-Auth-Token': token, 'Accept': 'application/json' }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { resolve(data); }
      });
    }).on('error', reject);
  });
}

async function run() {
  const o1301 = await get('/v2/orders/1301');
  const o1300 = await get('/v2/orders/1300');

  console.log('--- Order 1301 ---');
  console.log('order_source:', o1301.order_source);
  console.log('channel_id:', o1301.channel_id);
  console.log('external_source:', o1301.external_source);
  console.log('ip_address_v4:', o1301.ip_address_v4);
  console.log('geoip_country:', o1301.geoip_country);
  console.log('customer_message:', o1301.customer_message);
  console.log('staff_notes:', o1301.staff_notes);

  console.log('\n--- Order 1300 ---');
  console.log('order_source:', o1300.order_source);
  console.log('channel_id:', o1300.channel_id);
  console.log('external_source:', o1300.external_source);
  console.log('ip_address_v4:', o1300.ip_address_v4);
  console.log('geoip_country:', o1300.geoip_country);
  console.log('customer_message:', o1300.customer_message);
  console.log('staff_notes:', o1300.staff_notes);

  fs.writeFileSync(path.join(__dirname, 'order_1301_dump.json'), JSON.stringify(o1301, null, 2));
  fs.writeFileSync(path.join(__dirname, 'order_1300_dump.json'), JSON.stringify(o1300, null, 2));

  // Check form fields or custom order fields
  const f1301 = await get('/v2/orders/1301/formfields');
  console.log('\n1301 formfields:', f1301);
  const f1300 = await get('/v2/orders/1300/formfields');
  console.log('1300 formfields:', f1300);

  // Check order messages
  const m1301 = await get('/v2/orders/1301/messages');
  console.log('1301 messages:', m1301);
}

run().catch(console.error);
