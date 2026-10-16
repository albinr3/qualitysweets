const https = require('https');

https.get('https://qualitysweetsnj.com/', res => {
  let html = '';
  res.on('data', chunk => html += chunk);
  res.on('end', () => {
    const featIdx = html.indexOf('Featured Products');
    if (featIdx !== -1) {
      console.log('Found "Featured Products" at index', featIdx);
      console.log('--- Context before Featured Products (200 chars) ---');
      console.log(html.slice(Math.max(0, featIdx - 400), featIdx));
      console.log('--- Context after Featured Products (200 chars) ---');
      console.log(html.slice(featIdx, featIdx + 300));
    } else {
      console.log('"Featured Products" text not found, searching for FeaturedProducts ID/class:');
      const idx2 = html.indexOf('FeaturedProducts');
      if (idx2 !== -1) {
        console.log(html.slice(idx2 - 200, idx2 + 300));
      }
    }
  });
}).on('error', console.error);
