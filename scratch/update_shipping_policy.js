const https = require('https');
const fs = require('fs');
const path = require('path');

const env = {};
fs.readFileSync(path.join(__dirname, '..', '.env'), 'utf8').split('\n').forEach(line => {
  const m = line.match(/^\s*([\w.-]+)\s*=\s*(.*)?\s*$/);
  if (m) env[m[1]] = (m[2] || '').trim();
});

const storeHash = env.BIGCOMMERCE_STORE_HASH || '2ygwtj';
const token = env.BIGCOMMERCE_ACCESS_TOKEN;

function apiRequest(method, apiPath, payload) {
  return new Promise((resolve, reject) => {
    const data = payload ? JSON.stringify(payload) : null;
    const req = https.request({
      hostname: 'api.bigcommerce.com',
      path: `/stores/${storeHash}${apiPath}`,
      method: method,
      headers: {
        'X-Auth-Token': token,
        'Accept': 'application/json',
        ...(data ? { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) } : {})
      }
    }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(body) });
        } catch (e) {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function main() {
  const getRes = await apiRequest('GET', '/v2/pages/2');
  if (getRes.status !== 200) {
    console.error('Error fetching page 2:', getRes);
    return;
  }

  const currentBody = getRes.data.body;
  console.log('Current body snippet around Returns Policy:');
  const returnsIdx = currentBody.indexOf('Returns Policy');
  console.log(currentBody.substring(returnsIdx, returnsIdx + 700));

  let newBody = currentBody;

  // Replace "If items never arrive due to carrier issues or product is spoiled, please contact us."
  newBody = newBody.replace(
    'If items never arrive due to carrier issues or product is spoiled, please contact us.',
    'If items never arrive due to carrier issues, please contact us.'
  );

  // Replace "In such cases we will need proof that item never arrived or images of spoiled goods to be qualified for a refund."
  newBody = newBody.replace(
    'In such cases we will need proof that item never arrived or images of spoiled goods to be qualified for a refund.',
    'In such cases we will need proof that item never arrived to be qualified for a refund.'
  );

  // Also fix typo "within four weeks of clain" -> "within four weeks of claim"
  newBody = newBody.replace('within four weeks of clain', 'within four weeks of claim');

  // Also fix typo "FRIDAY-STURDAY-SUNDAY" -> "FRIDAY-SATURDAY-SUNDAY"
  newBody = newBody.replace('FRIDAY-STURDAY-SUNDAY', 'FRIDAY-SATURDAY-SUNDAY');

  if (newBody === currentBody) {
    console.log('No changes were made; check string matching.');
    return;
  }

  console.log('\nModified snippet:');
  const newReturnsIdx = newBody.indexOf('Returns Policy');
  console.log(newBody.substring(newReturnsIdx, newReturnsIdx + 700));

  console.log('\nUpdating page in BigCommerce via PUT /v2/pages/2...');
  const putRes = await apiRequest('PUT', '/v2/pages/2', { body: newBody });
  console.log('PUT Response status:', putRes.status);
  console.log('Updated successfully!');
}

main().catch(console.error);
