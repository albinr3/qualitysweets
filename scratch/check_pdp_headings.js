// Native fetch in Node 18+

async function checkHeadings() {
  const res = await fetch("https://qualitysweetsnj.com/carrot-halwa/");
  const html = await res.text();

  const regex = /<(h[1-6])([^>]*)>([\s\S]*?)<\/\1>/gi;
  let match;
  console.log("=== HEADINGS ON CARROT HALWA LIVE ===");
  while ((match = regex.exec(html)) !== null) {
    const tag = match[1].toUpperCase();
    const attrs = match[2];
    const text = match[3].replace(/<[^>]+>/g, "").trim().replace(/\s+/g, " ");
    console.log(`${tag} | attrs: [${attrs.trim()}] | text: "${text}"`);
  }
}

checkHeadings().catch(console.error);
