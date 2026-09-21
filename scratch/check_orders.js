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
const token = env.BIGCOMMERCE_ACCESS_TOKEN || '5sply9j97mi812e8sjqw3x029vtkivm';

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
        if (res.statusCode === 204) {
          return resolve({ status: 204, body: [] });
        }
        try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch (e) { resolve({ status: res.statusCode, body: data }); }
      });
    }).on('error', reject);
  });
}

async function run() {
  const store = await get('/v2/store');
  console.log('Store Name:', store.body?.name);
  console.log('Store Timezone:', store.body?.timezone);

  // Check orders today in UTC or store timezone
  const todayOrders = await get('/v2/orders?min_date_created=2026-09-20T00:00:00Z');
  console.log('Orders created >= 2026-09-20T00:00:00Z (HTTP Status):', todayOrders.status);
  console.log('Orders count:', Array.isArray(todayOrders.body) ? todayOrders.body.length : todayOrders.body);

  // Check orders yesterday
  const yesterdayOrders = await get('/v2/orders?min_date_created=2026-09-19T00:00:00Z');
  console.log('Orders created >= 2026-09-19T00:00:00Z (HTTP Status):', yesterdayOrders.status);
  if (Array.isArray(yesterdayOrders.body)) {
    console.log(`Orders since yesterday (${yesterdayOrders.body.length}):`);
    yesterdayOrders.body.forEach(o => {
      console.log(`- ID: ${o.id}, Status: "${o.status}", Date Created: ${o.date_created}, Date Modified: ${o.date_modified}, Total: $${o.total_inc_tax}, Customer: ${o.billing_address?.first_name} ${o.billing_address?.last_name}`);
    });
  }

  // Check order 1299
  const order1299 = await get('/v2/orders/1299');
  console.log('\nOrder 1299 details:', {
    id: order1299.body?.id,
    date_created: order1299.body?.date_created,
    date_modified: order1299.body?.date_modified,
    date_shipped: order1299.body?.date_shipped,
    status: order1299.body?.status,
    status_id: order1299.body?.status_id,
    total_inc_tax: order1299.body?.total_inc_tax,
    payment_method: order1299.body?.payment_method,
    items_total: order1299.body?.items_total
  });

  // Check abandoned carts / checkouts if available
  const abandonedCarts = await get('/v3/abandoned-carts/settings');
  console.log('\nAbandoned cart settings status:', abandonedCarts.status);
}

run();
