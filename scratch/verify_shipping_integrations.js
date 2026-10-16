const https = require('https');

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data }));
    }).on('error', reject);
  });
}

async function verifyAll() {
  console.log('=== VERIFYING INTEGRATIONS ACROSS 3 LOCATIONS ===\n');

  // 1. Shipping Page (/shipping-refunds/)
  const pageRes = await fetchUrl('https://qualitysweetsnj.com/shipping-refunds/');
  console.log('1. /shipping-refunds/ -> Status:', pageRes.status);
  console.log('   Contains FedEx map image:', pageRes.data.includes('fedex_ground_transit_map_nj'));
  console.log('   Contains Transit Time by Region:', pageRes.data.includes('Transit Time by Region'));
  console.log('   Contains Freshness Guarantee:', pageRes.data.includes('Freshness Guarantee'));

  // 2. Homepage (above Featured Products)
  const homeRes = await fetchUrl('https://qualitysweetsnj.com/');
  console.log('\n2. Homepage (/) -> Status:', homeRes.status);
  console.log('   Contains qs-home-shipping-section:', homeRes.data.includes('qs-home-shipping-section'));
  console.log('   Contains FedEx map image:', homeRes.data.includes('fedex_ground_transit_map_nj'));
  const featPos = homeRes.data.indexOf('Featured Products');
  const shipPos = homeRes.data.indexOf('qs-home-shipping-section');
  console.log('   Shipping section index:', shipPos, '| Featured Products index:', featPos);
  console.log('   Shipping section is ABOVE Featured Products:', shipPos !== -1 && featPos !== -1 && shipPos < featPos);

  // 3. Product Detail Page (/kesar-peda/)
  const pdpRes = await fetchUrl('https://qualitysweetsnj.com/kesar-peda/');
  console.log('\n3. Product Page (/kesar-peda/) -> Status:', pdpRes.status);
  console.log('   Contains qs-pdp-shipping-transit-widget script:', pdpRes.data.includes('qs-pdp-shipping-transit-widget'));
  console.log('   Contains FedEx map image in script:', pdpRes.data.includes('fedex_ground_transit_map_nj'));
}

verifyAll().catch(console.error);
