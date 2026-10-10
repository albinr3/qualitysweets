const fs = require('fs');

const postText = `Quick heads-up: our hot samosas and street chaats are walk-in takeout and pickup only—we don't ship fried food by mail, and there's no dine-in seating here. If you're in a rush, give us a quick call at (732) 283-3799 before you pull in, and we'll have your box boxed hot and ready at the counter.
We start rolling dough and heating the oil at 6:00 AM every morning. Expect a crisp, blistered crust stuffed with cumin-spiced potatoes and sweet peas—never frozen, always vegetarian, and packed with our homemade tamarind and mint chutneys.
Rolled & Fried From Scratch Daily. 100% Pure Vegetarian Kitchen. Fresh Oil & Zero Preservatives. Fryers Hot from 6:00 AM.
Golden Vegetable Samosas ($1.75): Hand-crimped pastry triangles fried in clean vegetable oil until shatteringly crisp.
Street-Style Samosa Chaat ($8.00): Two steaming samosas crushed under slow-cooked Punjabi chole, whisked spiced yogurt, and sweet-tart tamarind.
Nothing sits under heat lamps here. Our halwais knead the dough with toasted ajwain seeds each morning, crimp each pocket by hand, and drop small batches into the fryers all day long so your crust is actually crisp when you bite into it.
Flaky pastry pockets packed with spiced potatoes, green peas, cracked coriander seed, and warm Punjabi garam masala. We pack every single samosa with generous sides of our sweet tamarind and spicy mint chutneys.
Two fresh samosas crushed right into a bowl of thick, slow-simmered Punjabi chole, then ladled with whipped seasoned yogurt, sharp mint chutney, dark date-tamarind sauce, crispy sev, and cilantro. We pack it in deep, leak-resistant containers so it stays hot and doesn't spill on your ride home.
Hosting a puja, Diwali get-together, office lunch, or family party around Edison or Iselin? Don't settle for lukewarm supermarket trays. We time our fryer batches directly to your pickup schedule so your platters arrive hot and crunchy.
Great for 15 to 25 people. Comes packed in heavy-duty steam-vented catering boxes alongside two full 32 oz tubs of chutney (tamarind and mint). Call 2–3 hours ahead and we'll drop them fresh.
Our most popular order for mandir pujas, milestone birthdays, and company events. Includes two giant 64 oz containers of homemade chutneys so nobody runs out.
Planning a wedding weekend, temple festival, or convention across NJ, NY, or CT? We handle custom high-volume orders with direct catering delivery.
We run Quality Sweets as a focused takeout counter—no sit-down tables or long restaurant waits. Everything is designed to get hot food into your hands in minutes.
Grabbing a couple for the car? Just walk up to the counter. Ordering 10+ or a party box? Give us a call at (732) 283-3799 so we can get a fryer basket ready.
We hate soggy pastries as much as you do. We drop fresh samosas into clean vegetable oil so the crust is piping hot right when you arrive.
Park right in our storefront lot off Oak Tree Road, grab your bagged order and cold chutneys at the register, and you're good to go.
Folks stop here on their way through Middlesex County because they can taste the difference between a defrosted frozen snack and real halwai craftsmanship.
We knead the flour with pure vegetable ghee and whole ajwain (carom) seeds every morning. That's what gives our crust its signature aroma and delicate, biscuit-like flake.
Our kitchen is strictly vegetarian—no animal fats, gelatin, or shortcuts. We change our fryer oil constantly so every bite tastes clean and golden, never greasy or burnt.
Chutneys make or break a samosa. Ours are blended in-house: dark simmered tamarind for sweet tang, and raw mint with cilantro and green chilies for a clean kick.
Hot samosas don't travel well by mail, but our handmade mithai certainly does. We pack our fresh Kaju Katli, Bengali sweets, and festive gift boxes in insulated cold-pack cartons and ship them to all 50 states.
We don't have dining tables—Quality Sweets is strictly a walk-in counter and takeout shop. Everything is boxed in sturdy containers so it stays hot on your drive home or to the office.
Fried food doesn't survive shipping, so samosas and chaats are local counter pickup only. That said, our full sweets collection (mithai, barfi, and gift boxes) ships nationwide with cold packs.
Give us a call 2 to 3 hours ahead for trays of 50 or 100 so we can drop a dedicated fryer batch before you arrive. For weddings, temple events, or orders over 250 pieces, please give us 24 to 48 hours' notice.
Yes, 100% vegetarian. Just potatoes, peas, spices, flour, and vegetable oil—no meat, animal fats, or gelatin. If anyone in your group has a severe peanut or nut allergy, please let us know when ordering.
Never. Every samosa comes with our homemade tamarind and mint chutneys. Our 50-pack trays include two 32 oz tubs, and 100-pack platters come with two 64 oz tubs at no extra charge.`;

const tokens = postText.toLowerCase().match(/[a-z0-9'-]+/g) || [];
const totalTokens = tokens.length;
const uniqueTokens = new Set(tokens).size;
const ttr = (uniqueTokens / totalTokens).toFixed(4);

const sentences = postText.split(/(?<=[.?!])\s+/).filter(s => s.trim().length > 3 && /[a-z]/i.test(s));
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
const contractions = (postText.match(/\b([a-z]+'[a-z]+)\b/gi) || []).length;
const passives = (postText.match(/\b(is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en|fried|made|packed|served|crushed|layered|whisked|held|dropped|kneaded|mixed)\b/gi) || []).length;

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
  passives
}, null, 2));
