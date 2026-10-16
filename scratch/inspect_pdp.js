const https = require('https');

https.get('https://qualitysweetsnj.com/manpasand/', res => {
  let html = '';
  res.on('data', chunk => html += chunk);
  res.on('end', () => {
    console.log('Product page length:', html.length);
    // Find Add to Cart or ProductDetails
    const formIdx = html.indexOf('productDetailsAdd');
    console.log('productDetailsAdd index:', formIdx);
    if (formIdx !== -1) {
      console.log('--- Form excerpt ---');
      console.log(html.slice(formIdx, formIdx + 1500));
    } else {
      const cartIdx = html.indexOf('add-to-cart') || html.indexOf('Add to Cart');
      console.log('Cart text index:', cartIdx);
      if (cartIdx !== -1) {
        console.log(html.slice(cartIdx - 200, cartIdx + 500));
      }
    }
  });
}).on('error', console.error);
