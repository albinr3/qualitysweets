const fs = require('fs');

const rawHtml = fs.readFileSync('content/menu/samosas.html', 'utf8');

// Extract prose text from HTML (ignoring script, style, tags)
let clean = rawHtml.replace(/<script[\s\S]*?<\/script>/gi, '');
clean = clean.replace(/<style[\s\S]*?<\/style>/gi, '');
clean = clean.replace(/<[^>]+>/g, ' ');
clean = clean.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&raquo;/g, '»').replace(/&bull;/g, '•').replace(/&ndash;/g, '–');
clean = clean.replace(/\s+/g, ' ').trim();

const tokens = clean.toLowerCase().match(/[a-z0-9'-]+/g) || [];
const totalTokens = tokens.length;
const uniqueTokens = new Set(tokens).size;
const ttr = (uniqueTokens / totalTokens).toFixed(4);

const sentences = clean.split(/(?<=[.?!])\s+/).filter(s => s.trim().length > 3 && /[a-z]/i.test(s));
const sentLens = sentences.map(s => (s.match(/[a-z0-9'-]+/gi) || []).length);
const msl = (sentLens.reduce((a,b)=>a+b,0) / sentLens.length).toFixed(2);
const variance = sentLens.reduce((a,b)=>a + Math.pow(b - msl, 2), 0) / sentLens.length;
const burstiness = Math.sqrt(variance).toFixed(2);
const cov = (burstiness / msl).toFixed(4);

const freqs = {};
tokens.forEach(t => freqs[t] = (freqs[t]||0)+1);
let entropy = 0;
for (const t in freqs) {
  const p = freqs[t] / totalTokens;
  entropy -= p * Math.log2(p);
}

const lyWords = tokens.filter(t => t.endsWith('ly'));
const contractions = (clean.match(/\b([a-z]+'[a-z]+)\b/gi) || []).length;
const passives = (clean.match(/\b(is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en|fried|made|packed|served|crushed|layered|whisked|held|dropped|kneaded|mixed)\b/gi) || []).length;

// AI vocabulary checks
const tier1 = ['delve', 'tapestry', 'landscape', 'testament', 'serves as a reminder', 'worth noting', 'bears mentioning', 'navigate', 'spearhead', 'multifaceted', 'pivotal', 'paramount', 'underscores', 'underpin', 'in the realm of', 'important to note', 'shed light on'];
const tier2 = ['crucial', 'vital', 'comprehensive', 'robust', 'leverage', 'foster', 'facilitate', 'embark', 'harnessing', 'utilize', 'endeavor', 'moreover', 'furthermore', 'additionally', 'subsequently', 'nonetheless', 'notwithstanding', 'overarching', 'intricate', 'nuanced', 'holistic', 'synergy', 'paradigm', 'catalyst', 'orchestrate', 'seamless', 'ecosystem', 'journey', 'unlock'];
const tier3 = ['significant', 'enhance', 'innovative', 'dynamic', 'diverse', 'inclusive', 'sustainable', 'transformative', 'empower', 'streamline', 'optimize', 'cutting-edge', 'state-of-the-art', 'game-changer', 'disruptive', 'scalable', 'impactful', 'actionable', 'meaningful', 'compelling'];

const t1Found = tier1.filter(w => clean.toLowerCase().includes(w));
const t2Found = tier2.filter(w => clean.toLowerCase().includes(w));
const t3Found = tier3.filter(w => clean.toLowerCase().includes(w));

console.log(JSON.stringify({
  totalTokens,
  uniqueTokens,
  ttr,
  sentenceCount: sentences.length,
  msl,
  burstiness,
  cov,
  entropy: entropy.toFixed(4),
  lyCount: lyWords.length,
  lyPer100: ((lyWords.length / totalTokens) * 100).toFixed(2),
  contractions,
  passives,
  t1Found,
  t2Found,
  t3Found
}, null, 2));
