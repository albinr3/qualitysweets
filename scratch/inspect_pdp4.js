const https = require('https');

https.get('https://qualitysweetsnj.com/kesar-peda/', res => {
  let html = '';
  res.on('data', chunk => html += chunk);
  res.on('end', () => {
    const idx = html.indexOf('class="addto"');
    if (idx !== -1) {
      console.log('--- .addto excerpt ---');
      console.log(html.slice(idx, idx + 800));
    }
  });
}).on('error', console.error);
