const fs = require('fs');
const AIDetector = require('C:/Users/Albin Rodriguez/.gemini/config/skills/avoid-ai-writing/detector/patterns.js');

const html = fs.readFileSync('scratch/about_page_new.html', 'utf8');
const text = html
  .replace(/<style[\s\S]*?<\/style>/gi, '')
  .replace(/<script[\s\S]*?<\/script>/gi, '')
  .replace(/<[^>]+>/g, ' ')
  .replace(/&bull;/g, ' ')
  .replace(/&rarr;/g, ' ')
  .replace(/&amp;/g, '&')
  .replace(/&ndash;/g, '-')
  .replace(/\s+/g, ' ')
  .trim();

console.log('Text preview:\n', text.slice(0, 300));
const res = AIDetector.analyzeText(text);
console.log('\n--- AIDetector Results ---');
console.log('Score:', res.score, 'Label:', res.label, 'Classification:', res.document_classification);
console.log('Issues:', JSON.stringify(res.issues, null, 2));
