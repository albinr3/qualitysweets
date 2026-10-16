const https = require('https');

https.get('https://qualitysweetsnj.com/manpasand/', res => {
  let html = '';
  res.on('data', chunk => html += chunk);
  res.on('end', () => {
    const idx = html.indexOf('productDetailsAddToCartForm');
    if (idx !== -1) {
      console.log('--- Form full content ---');
      console.log(html.slice(idx, idx + 2500));
    }
  });
}).on('error', console.error);
