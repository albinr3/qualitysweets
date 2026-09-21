const AIDetector = require('C:/Users/Albin Rodriguez/.gemini/config/skills/avoid-ai-writing/detector/patterns.js');

const draft2 = `Quality Sweets opened on Oak Tree Road in Iselin, New Jersey in 2003. When we started, fresh Bengali mithai was hard to find in the Tri-State area, so we built our kitchen around traditional recipes made with fresh milk, chhena, and pure desi ghee.

More than twenty years later, we still make our sweets every morning at the exact same location.

Our sweet makers from Bengal and Punjab prepare specialties from across India. Signature Bengali sweets include Manpasand, Anarkali, Malai Chum Chum, and Palki. The display counter also includes classic North Indian favorites like Kaju Katli, milk barfi, Motichur Ladoos, and Gulab Jamun, with each batch made in small quantities.

We do not cut corners with dairy or premixed powders. Everything is made with whole milk, fresh khoya, pistachios, cashews, and saffron, and our entire kitchen is 100% vegetarian.

Our shop at 1384 Oak Tree Road is open seven days a week for takeout and counter pickup. Stop by for sweets by the pound, hot samosas, and fresh chaat, or order custom gift boxes for weddings and celebrations. For friends and family outside New Jersey, we ship nationwide through our website.`;

const res = AIDetector.analyzeText(draft2);
console.log('Score:', res.score, 'Label:', res.label, 'Classification:', res.document_classification);
console.log('Issues:', JSON.stringify(res.issues, null, 2));
