const https = require('https');

https.get('https://qualitysweetsnj.com/manpasand/', res => {
  let html = '';
  res.on('data', chunk => html += chunk);
  res.on('end', () => {
    const idx = html.indexOf('id="productDetailsAddToCartForm"');
    console.log('id="productDetailsAddToCartForm" index:', idx);
    if (idx !== -1) {
      console.log('--- Form HTML ---');
      console.log(html.slice(idx - 100, idx + 1200));
    }
    const pdIdx = html.indexOf('ProductMain');
    if (pdIdx !== -1) {
      console.log('--- ProductMain ---');
      console.log(html.slice(pdIdx, pdIdx + 400));
    }
  });
}).on('error', console.error);
