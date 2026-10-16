const https = require('https');

const testUrls = [
  'https://qualitysweetsnj.com/manpasand/',
  'https://qualitysweetsnj.com/kesar-peda/',
  'https://qualitysweetsnj.com/motichur-ladoo/'
];

testUrls.forEach(url => {
  https.get(url, res => {
    let html = '';
    res.on('data', chunk => html += chunk);
    res.on('end', () => {
      const hasForm = html.includes('id="productDetailsAddToCartForm"');
      const hasAddto = html.includes('class="addto"');
      const hasProductDetails = html.includes('id="ProductDetails"');
      console.log(url, '-> hasForm:', hasForm, '| hasAddto:', hasAddto, '| hasProductDetails:', hasProductDetails);
    });
  });
});
