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
  console.log('Store:', store.body?.name);
  console.log('Domain:', store.body?.domain);
  console.log('Timezone:', JSON.stringify(store.body?.timezone));

  // Current time: 2026-10-08T22:43:47-04:00
  // 20 days ago: 2026-09-18T22:43:47Z (or 2026-09-18T00:00:00Z to cover full days)
  const now = new Date();
  const twentyDaysAgo = new Date(now.getTime() - (20 * 24 * 60 * 60 * 1000));
  const minDateIso = twentyDaysAgo.toISOString();
  console.log(`Current local/system time: ${now.toISOString()}`);
  console.log(`Calculating last 20 days from: ${minDateIso}`);

  // Query order count
  const countRes = await get(`/v2/orders/count?min_date_created=${encodeURIComponent(minDateIso)}`);
  console.log('Count endpoint response:', countRes.body);

  // Query orders with pagination or limit
  // BigCommerce supports min_date_created in RFC 2822 or ISO 8601
  const ordersRes = await get(`/v2/orders?min_date_created=${encodeURIComponent(minDateIso)}&sort=date_created:desc&limit=250`);
  console.log('Orders status code:', ordersRes.status);

  let orders = [];
  if (Array.isArray(ordersRes.body)) {
    orders = ordersRes.body;
  } else {
    console.log('Orders response body:', ordersRes.body);
  }

  console.log(`\n=== RESULTADO: ${orders.length} ORDENES EN LOS ULTIMOS 20 DIAS ===`);
  
  if (orders.length > 0) {
    let totalRevenue = 0;
    for (let idx = 0; idx < orders.length; idx++) {
      const o = orders[idx];
      const amount = parseFloat(o.total_inc_tax || 0);
      totalRevenue += amount;
      console.log(`\n------------------------------------------------------------`);
      console.log(`[${idx + 1}] ORDEN #${o.id} - ${o.status.toUpperCase()}`);
      console.log(`    Fecha: ${o.date_created}`);
      console.log(`    Total: $${o.total_inc_tax} (Subtotal: $${o.subtotal_inc_tax}, Envío: $${o.shipping_cost_inc_tax})`);
      console.log(`    Cliente: ${o.billing_address?.first_name} ${o.billing_address?.last_name}`);
      console.log(`    Email: ${o.billing_address?.email}`);
      console.log(`    Método de Pago: ${o.payment_method || 'N/A'}`);
      console.log(`    Dirección de entrega: ${o.billing_address?.city}, ${o.billing_address?.state} ${o.billing_address?.zip}`);
      
      const productsRes = await get(`/v2/orders/${o.id}/products`);
      if (Array.isArray(productsRes.body)) {
        console.log(`    Productos (${productsRes.body.length}):`);
        productsRes.body.forEach(p => {
          console.log(`      * ${p.quantity}x ${p.name} - $${p.total_inc_tax}`);
        });
      }
    }
    console.log(`\n============================================================`);
    console.log(`Total monetario de órdenes registradas: $${totalRevenue.toFixed(2)}`);
  } else {
    console.log('No se encontraron órdenes registradas en ese período.');
  }

  // Also query the most recent orders overall to see when the last orders were placed
  console.log('\n--- Últimas órdenes registradas en toda la tienda (muestra general) ---');
  const recentOrders = await get('/v2/orders?sort=date_created:desc&limit=5');
  if (Array.isArray(recentOrders.body)) {
    recentOrders.body.forEach(o => {
      console.log(`- ID: ${o.id} | Fecha: ${o.date_created} | Estado: ${o.status} | Total: $${o.total_inc_tax} | Cliente: ${o.billing_address?.first_name} ${o.billing_address?.last_name}`);
    });
  } else {
    console.log('Recent orders response:', recentOrders.body);
  }
}

run().catch(console.error);
